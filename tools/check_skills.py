"""Validate project skill descriptors without installing or executing upstream code."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    'qa-academy-development',
    'frontend-design',
    'webapp-testing',
    'web-design-guidelines',
    'systematic-debugging',
    'verification-before-completion',
}

def main() -> int:
    problems = []
    rows = []
    for name in sorted(EXPECTED):
        file = ROOT / '.agents' / 'skills' / name / 'SKILL.md'
        if not file.is_file():
            problems.append(f'{name}: SKILL.md missing')
            continue
        text = file.read_text(encoding='utf-8')
        parts = text.split('---', 2)
        if len(parts) != 3 or parts[0].strip():
            problems.append(f'{name}: frontmatter missing')
            continue
        header = parts[1]
        actual = re.search(r'^name:\s*(\S+)\s*$', header, re.M)
        description = re.search(r'^description:\s*(.+)$', header, re.M)
        if not actual or actual.group(1) != name:
            problems.append(f'{name}: name does not match directory')
        if not description or len(description.group(1).strip()) < 20:
            problems.append(f'{name}: meaningful description missing')
        if len(parts[2].strip()) < 200:
            problems.append(f'{name}: instructions missing')
        if name != 'qa-academy-development' and not file.with_name('LICENSE.txt').is_file():
            problems.append(f'{name}: license missing')
        rows.append({'name': name, 'path': str(file.relative_to(ROOT))})
    print(json.dumps({'descriptors_found': len(rows), 'errors': problems, 'skills': rows}, ensure_ascii=False, indent=2))
    return 1 if problems else 0

if __name__ == '__main__':
    sys.exit(main())
