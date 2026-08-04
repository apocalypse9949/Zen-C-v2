import re

with open('src/lexer/token.c', 'r') as f:
    content = f.read()

# Replace the switch in `lexer_next` with proper length bounds check
# Actually, the problem is `while (is_ident_char(s[len]))` in lexer_next
# `is_ident_char` takes a `char` but it should take `unsigned char`
# Also need to check if `len < something` or if `s[len]` is safe.
# In C, `s[len]` is safe if it's null-terminated, but `unsigned char` cast is missing here:
#   `while (is_ident_char(s[len]))` -> `while (is_ident_char((unsigned char)s[len]))`
#   `if (is_ident_start(s[len]))` -> `if (is_ident_start((unsigned char)s[len]))`

content = re.sub(r'is_ident_char\(s\[len\]\)', r'is_ident_char((unsigned char)s[len])', content)
content = re.sub(r'is_ident_start\(s\[len\]\)', r'is_ident_start((unsigned char)s[len])', content)
content = re.sub(r'is_ident_start\(\*s\)', r'is_ident_start((unsigned char)*s)', content)

# But wait, earlier `inline int is_ident_start(char c)` was replaced. Let's make sure it's unsigned char:
content = re.sub(r'inline int is_ident_start\(char c\)', r'inline int is_ident_start(unsigned char c)', content)
content = re.sub(r'inline int is_ident_char\(char c\)', r'inline int is_ident_char(unsigned char c)', content)

with open('src/lexer/token.c', 'w') as f:
    f.write(content)
