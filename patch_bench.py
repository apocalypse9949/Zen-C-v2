import re

with open('.github/workflows/bench.yml', 'r') as f:
    content = f.read()

content = content.replace(
    'skip-fetch-gh-pages: true',
    'skip-fetch-gh-pages: true\n        gh-pages-branch: gh-pages'
)

with open('.github/workflows/bench.yml', 'w') as f:
    f.write(content)
