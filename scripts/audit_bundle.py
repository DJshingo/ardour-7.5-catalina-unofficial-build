#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only inventory of an Ardour7.app for later manual compliance/security review.

On macOS, requires file, otool and codesign in PATH. Produces CSV data in a
NEW directory; it does not patch, sign, execute or upload app binaries.
This audit does not determine license terms or fully resolve dyld @rpath.
"""
import argparse
from collections import Counter
import csv
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys


def command(args):
    return subprocess.run([str(x) for x in args], capture_output=True, text=True)


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def inside(path, app):
    """Compare canonical paths, including symlinked parent directories.

    On macOS /var may alias /private/var, so resolving only the target
    would misclassify files inside a bundle as external references.
    """
    actual = Path(path).resolve(strict=False)
    bundle = Path(app).resolve(strict=False)
    return actual == bundle or bundle in actual.parents


def link_status(path, app):
    """Do not dereference external or broken symlinks for inventory purposes."""
    try:
        target = path.resolve(strict=True)
    except (OSError, RuntimeError):
        return 'BROKEN', ''
    return ('inside-app' if inside(target, app) else 'ESCAPES-APP', target)


def parse_otool(path):
    p = command(['otool', '-L', path])
    if p.returncode:
        return None
    return [s.strip().split(' (', 1)[0]
            for s in p.stdout.splitlines()[1:] if s.strip()]


def dylib_id(path):
    p = command(['otool', '-D', path])
    if p.returncode:
        return ''
    lines = p.stdout.splitlines()
    return lines[1].strip() if len(lines) > 1 else ''


def resolved_path_status(target, app):
    try:
        actual = target.resolve(strict=True)
    except (OSError, RuntimeError):
        return 'UNRESOLVED'
    if not actual.is_file():
        return 'UNRESOLVED'
    return 'inside-app' if inside(actual, app) else 'EXTERNAL-REFERENCE'


def dependency_status(dep, app, referrer):
    if dep.startswith(('/usr/lib/', '/System/Library/')):
        return 'macOS-system'
    if dep.startswith('@executable_path/'):
        target = app / 'Contents/MacOS' / dep[len('@executable_path/'):]
        return resolved_path_status(target, app)
    if dep.startswith('@loader_path/'):
        target = referrer.parent / dep[len('@loader_path/'):]
        return resolved_path_status(target, app)
    if dep.startswith('@rpath/'):
        # Not all LC_RPATH chains can be resolved by considering one image.
        return 'REVIEW-RPATH'
    if dep.startswith('/'):
        return resolved_path_status(Path(dep), app)
    return 'REVIEW-BARE-NAME'


def sanitize(text, home):
    return str(text).replace(str(home), '$HOME')


def write_csv(dest, fields, rows):
    with dest.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app', type=Path, required=True,
                        help='Existing Ardour7.app directory')
    parser.add_argument('--output', type=Path, required=True,
                        help='New directory for audit files')
    args = parser.parse_args(argv)
    app = args.app.expanduser().resolve()
    output = args.output.expanduser().resolve()
    home = Path.home()

    if not (app / 'Contents/MacOS/Ardour7').is_file():
        parser.error('Missing Contents/MacOS/Ardour7')
    if output.exists():
        parser.error('Output exists; choose a new directory (no overwrite)')
    if inside(output, app) or inside(app, output):
        parser.error('Output must be outside the bundle and outside its ancestors')
    for program in ('file', 'otool', 'codesign'):
        if shutil.which(program) is None:
            parser.error(f'{program} not found (run on macOS with Xcode CLT)')

    # Enumerate first to avoid partially empty reports on early path errors.
    entries = sorted(app.rglob('*'))
    output.mkdir(parents=True)
    machos, deps, assets, links = [], [], [], []
    for path in entries:
        rel = str(path.relative_to(app))
        if path.is_symlink():
            status, resolved = link_status(path, app)
            links.append({
                'bundle_path': rel,
                'link_text': sanitize(os.readlink(path), home),
                'resolved_target': sanitize(resolved, home),
                'status': status,
            })
            continue
        if not path.is_file():
            continue
        fmt = command(['file', '-b', path])
        if fmt.returncode:
            assets.append({'bundle_path': rel, 'size_bytes': path.stat().st_size,
                           'sha256': sha256(path), 'file_type': 'FILE-INSPECTION-FAILED',
                           'license_review': 'PENDING'})
            continue
        kind = fmt.stdout.strip()
        if 'Mach-O' not in kind:
            assets.append({'bundle_path': rel, 'size_bytes': path.stat().st_size,
                           'sha256': sha256(path), 'file_type': kind,
                           'license_review': 'PENDING'})
            continue
        ident = dylib_id(path)
        signature = command(['codesign', '--verify', path])
        machos.append({
            'bundle_path': rel,
            'size_bytes': path.stat().st_size,
            'sha256': sha256(path),
            'architecture_format': kind,
            'install_name': sanitize(ident, home),
            'codesign_verify': 'pass' if signature.returncode == 0 else 'fail',
            'component_and_license': 'PENDING',
        })
        linked = parse_otool(path)
        if linked is None:
            deps.append({'referrer': rel, 'dependency': '<otool failed>',
                         'status': 'UNRESOLVED'})
            continue
        for dep in linked:
            if dep == ident:
                continue
            deps.append({'referrer': rel, 'dependency': sanitize(dep, home),
                         'status': dependency_status(dep, app, path)})

    write_csv(output / 'macho_inventory.csv',
              ['bundle_path', 'size_bytes', 'sha256', 'architecture_format',
               'install_name', 'codesign_verify', 'component_and_license'], machos)
    write_csv(output / 'dependencies.csv',
              ['referrer', 'dependency', 'status'], deps)
    write_csv(output / 'assets.csv',
              ['bundle_path', 'size_bytes', 'sha256', 'file_type', 'license_review'], assets)
    write_csv(output / 'symlinks.csv',
              ['bundle_path', 'link_text', 'resolved_target', 'status'], links)

    issues = [x for x in deps if x['status'] not in ('inside-app', 'macOS-system')]
    link_issues = [x for x in links if x['status'] != 'inside-app']
    failed_codesign = sum(x['codesign_verify'] != 'pass' for x in machos)
    statuses = Counter(x['status'] for x in deps)
    summary = (
        f'Mach-O files (regular): {len(machos)}\n'
        f'Other regular files: {len(assets)}\n'
        f'Symlink aliases: {len(links)}\n'
        f'Dependency references: {len(deps)}\n'
        f'Dependency references needing review: {len(issues)}\n'
        f'Broken or external symlink aliases: {len(link_issues)}\n'
        f'Mach-O signature failures: {failed_codesign}\n'
        + 'Dependency classifications:\n'
        + ''.join(f'  {k}: {v}\n' for k, v in sorted(statuses.items()))
        + 'Licenses and source provenance: NOT VERIFIED\n'
        + 'Note: @rpath and bare-name references require separate dyld analysis.\n'
        + 'Do not publish generated audit files without privacy review.\n'
    )
    (output / 'audit_summary.txt').write_text(summary, encoding='utf-8')
    print(summary)
    print(f'Audit files: {output}')


if __name__ == '__main__':
    main()
