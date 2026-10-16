# SPDX-License-Identifier: MIT
"""Cross-platform tests for the bundle inventory's path/symlink logic."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import subprocess
import shutil
from unittest.mock import patch
from subprocess import CompletedProcess

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/audit_bundle.py'
spec = importlib.util.spec_from_file_location('audit_bundle', SCRIPT)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class PathClassificationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.app = (self.root / 'Ardour7.app')
        self.bin = self.app / 'Contents/MacOS'
        self.lib = self.app / 'Contents/lib'
        self.bin.mkdir(parents=True)
        self.lib.mkdir(parents=True)
        self.exe = self.bin / 'Ardour7'
        self.exe.write_bytes(b'fake')
        (self.lib / 'liba.dylib').write_bytes(b'fake')
        self.external = self.root / 'private.dylib'
        self.external.write_bytes(b'fake')

    def test_executable_relative(self):
        self.assertEqual('inside-app', audit.dependency_status(
            '@executable_path/../lib/liba.dylib', self.app, self.exe))

    def test_missing_relative(self):
        self.assertEqual('UNRESOLVED', audit.dependency_status(
            '@executable_path/../lib/missing.dylib', self.app, self.exe))

    def test_external_absolute(self):
        self.assertEqual('EXTERNAL-REFERENCE', audit.dependency_status(
            str(self.external), self.app, self.exe))

    def test_symlink_aliased_library(self):
        link = self.lib / 'libalias.dylib'
        link.symlink_to('liba.dylib')
        self.assertEqual('inside-app', audit.link_status(link, self.app)[0])
        self.assertEqual('inside-app', audit.dependency_status(
            '@executable_path/../lib/libalias.dylib', self.app, self.exe))

    def test_executable_relative_through_aliased_parent(self):
        """A symlinked temp parent models macOS /var -> /private/var."""
        aliased_root = self.root / 'parent-alias'
        aliased_root.symlink_to(self.root, target_is_directory=True)
        app_alias = aliased_root / 'Ardour7.app'
        exe_alias = app_alias / 'Contents/MacOS/Ardour7'
        self.assertEqual('inside-app', audit.dependency_status(
            '@executable_path/../lib/liba.dylib', app_alias, exe_alias))

    def test_inside_symlink_through_aliased_parent(self):
        """An inside-app symlink must not be classed as an escape."""
        alias = self.lib / 'libalias.dylib'
        alias.symlink_to('liba.dylib')
        aliased_root = self.root / 'parent-alias'
        aliased_root.symlink_to(self.root, target_is_directory=True)
        app_alias = aliased_root / 'Ardour7.app'
        link_alias = app_alias / 'Contents/lib/libalias.dylib'
        self.assertEqual('inside-app', audit.link_status(link_alias, app_alias)[0])
        self.assertEqual('inside-app', audit.dependency_status(
            '@executable_path/../lib/libalias.dylib', app_alias,
            app_alias / 'Contents/MacOS/Ardour7'))

    def test_external_symlink_is_not_inside(self):
        link = self.lib / 'libbad.dylib'
        link.symlink_to(self.external)
        self.assertEqual('ESCAPES-APP', audit.link_status(link, self.app)[0])
        self.assertEqual('EXTERNAL-REFERENCE', audit.dependency_status(
            '@executable_path/../lib/libbad.dylib', self.app, self.exe))

    def test_broken_link_is_detected(self):
        link = self.lib / 'libbroken.dylib'
        link.symlink_to('missing.dylib')
        self.assertEqual('BROKEN', audit.link_status(link, self.app)[0])

    def test_unresolved_rpath_and_bare_names(self):
        self.assertEqual('REVIEW-RPATH', audit.dependency_status(
            '@rpath/libFLAC.12.dylib', self.app, self.exe))
        self.assertEqual('REVIEW-BARE-NAME', audit.dependency_status(
            'libvamp-sdk.so', self.app, self.exe))

    def test_parse_otool(self):
        output = ("/tmp/demo.dylib:\n"
                  "\t@rpath/libFLAC.12.dylib (compatibility version 12.0.0)\n"
                  "\t/usr/lib/libSystem.B.dylib (compatibility version 1.0.0)\n")
        with patch.object(audit, 'command', return_value=CompletedProcess(
            ['otool'], 0, output, '')):
            self.assertEqual(['@rpath/libFLAC.12.dylib', '/usr/lib/libSystem.B.dylib'],
                             audit.parse_otool(self.exe))

    def test_system_library(self):
        self.assertEqual('macOS-system', audit.dependency_status(
            '/usr/lib/libSystem.B.dylib', self.app, self.exe))


@unittest.skipUnless(shutil.which('git') and shutil.which('bash') and
                     shutil.which('shasum'), 'requires git, bash and shasum')
class SourceIdentityExitStatusTests(unittest.TestCase):
    """Exercise the real source-identity helper in a disposable Git checkout."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / 'ardour-source'
        self.repo.mkdir()
        self.rel = 'libs/gtkmm2ext/nsglview.mm'
        self.file = self.repo / self.rel
        self.file.parent.mkdir(parents=True)
        # The patch hunk begins at line 45, matching the actual upstream context.
        self.original = ('// test line\n' * 44 +
                         '#ifndef ARDOUR_CANVAS_NSVIEW_TAG\n'
                         '#error NO TAG\n'
                         '#define ARDOUR_CANVAS_NSVIEW_TAG 0x0\n'
                         '#endif\n')
        self.file.write_text(self.original, encoding='utf-8')
        self.run_git('init', '-q')
        self.run_git('add', self.rel)
        self.run_git('-c', 'user.name=Test Fixture',
                     '-c', 'user.email=fixture@example.invalid',
                     'commit', '-qm', 'Test source baseline')
        self.patch_file = (Path(__file__).resolve().parents[1] /
                           'patches/0001-catalina-gtk-quartz-canvas-fallback.patch')
        self.helper = (Path(__file__).resolve().parents[1] /
                       'scripts/record_source_identity.sh')

    def run_git(self, *args):
        subprocess.run(['git', '-C', str(self.repo), *args], check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       timeout=15)

    def verify(self):
        return subprocess.run(['bash', str(self.helper), str(self.repo)],
                              capture_output=True, text=True, timeout=15)

    def test_pristine_is_not_yet_applied(self):
        result = self.verify()
        self.assertEqual(3, result.returncode, result.stdout + result.stderr)
        self.assertIn('NOT YET APPLIED', result.stdout)
        self.assertEqual(self.original, self.file.read_text())

    def test_exact_patch_is_pass(self):
        self.run_git('apply', str(self.patch_file))
        result = self.verify()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn('Result: PASS', result.stdout)

    def test_unexpected_edit_is_failure(self):
        self.run_git('apply', str(self.patch_file))
        with self.file.open('a', encoding='utf-8') as f:
            f.write('// unexpected local edit\n')
        result = self.verify()
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn('FAIL (local file contains unexpected differences)', result.stdout)

    def test_wrong_source_revision_is_failure(self):
        self.file.write_text(self.original.replace('#error NO TAG',
                                                   '#error DIFFERENT TAG'))
        self.run_git('add', self.rel)
        self.run_git('-c', 'user.name=Test Fixture',
                     '-c', 'user.email=fixture@example.invalid',
                     'commit', '-qm', 'Mismatched baseline')
        result = self.verify()
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn('patch context mismatch', result.stdout)



if __name__ == '__main__':
    unittest.main()
