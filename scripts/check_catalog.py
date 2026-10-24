"""Validate catalogue structure offline; scientific claims need human review."""

from pathlib import Path
import re
import sys
from urllib.parse import urlsplit


def check_catalog(text):
    """Return (entry_count, diagnostics) for Project/What it verifies tables."""
    entries, errors, seen = 0, [], {}
    in_table = False
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped.startswith('|'):
            in_table = False
            continue
        cells = [part.strip() for part in re.split(r'(?<!\\)\|', stripped.strip('|'))]
        if [cell.casefold() for cell in cells] == ['project', 'what it verifies']:
            in_table = True
            continue
        if not in_table:
            continue
        if len(cells) == 2 and all(re.fullmatch(r':?-{3,}:?', cell) for cell in cells):
            continue
        if len(cells) != 2:
            errors.append(f'line {number}: expected two table columns (escape literal pipes as \\|)')
            continue
        entries += 1
        project, description = cells
        if not description or description.casefold() in {'todo', 'tbd'}:
            errors.append(f'line {number}: supply a verification description')
        link = re.fullmatch(r'\[([^\]]+)\]\(([^\s)]+)\)', project)
        if not link or not link.group(1).strip():
            errors.append(f'line {number}: project must be a named Markdown repository link')
            continue
        try:
            url = urlsplit(link.group(2))
        except ValueError:
            errors.append(f'line {number}: invalid repository URL')
            continue
        path = url.path.rstrip('/').split('/')
        if (url.scheme != 'https' or url.netloc.casefold() != 'github.com'
                or url.query or url.fragment or len(path) != 3
                or not re.fullmatch(r'[A-Za-z0-9-]+', path[1])
                or not re.fullmatch(r'[A-Za-z0-9_.-]+', path[2])
                or path[2] in {'.', '..'}):
            errors.append(f'line {number}: use https://github.com/owner/repository')
            continue
        key = (path[1].casefold(), path[2].casefold())
        if key in seen:
            errors.append(f'line {number}: duplicate repository (first listed on line {seen[key]})')
        else:
            seen[key] = number
    if not entries:
        errors.append('no project entries found in Project / What it verifies tables')
    return entries, errors


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) > 1:
        print('usage: python scripts/check_catalog.py [README.md]', file=sys.stderr)
        return 2
    path = Path(args[0]) if args else Path(__file__).resolve().parents[1] / 'README.md'
    try:
        text = path.read_text(encoding='utf-8-sig')
    except (OSError, UnicodeError) as error:
        print(f'{path}: {error}', file=sys.stderr)
        return 2
    count, errors = check_catalog(text)
    for error in errors:
        print(f'{path}: {error}', file=sys.stderr)
    if errors:
        return 1
    print(f'Checked {count} project entries: no structural errors.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
