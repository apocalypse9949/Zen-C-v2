import re
from pathlib import Path

for path in Path('src').rglob('*.c'):
    content = path.read_text()
    orig = content

    def repl(m):
        a = m.group(1)
        b = m.group(2)
        op = m.group(3)
        if '"' in a or '"' in b or '(' in a or '(' in b or '+' in a or '+' in b or ' ' in a or ' ' in b:
            return m.group(0)
        return f"({a}[0] == {b}[0] && strcmp({a}, {b}) {op} 0)"

    new_content = re.sub(r'strcmp\(([^,]+?),\s*([^)]+?)\)\s*(==|!=)\s*0', repl, content)

    if new_content != orig:
        path.write_text(new_content)
