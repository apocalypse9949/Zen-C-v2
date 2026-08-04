import re

with open('src/lexer/token.c', 'r') as f:
    content = f.read()

new_content = re.sub(
    r'static __attribute__\(\(unused\)\) int is_ident_start\(char c\)\n{\n    return isalpha\(c\) \|\| c == \'_.*\';\n}',
    '''static const unsigned char ident_start_map[256] = {
    ['A' ... 'Z'] = 1, ['a' ... 'z'] = 1, ['_'] = 1
};

static __attribute__((unused)) inline int is_ident_start(unsigned char c)
{
    return ident_start_map[c];
}''',
    content
)

new_content = re.sub(
    r'static __attribute__\(\(unused\)\) int is_ident_char\(char c\)\n{\n    return isalnum\(c\) \|\| c == \'_.*\';\n}',
    '''static const unsigned char ident_char_map[256] = {
    ['A' ... 'Z'] = 1, ['a' ... 'z'] = 1, ['0' ... '9'] = 1, ['_'] = 1
};

static __attribute__((unused)) inline int is_ident_char(unsigned char c)
{
    return ident_char_map[c];
}''',
    new_content
)

with open('src/lexer/token.c', 'w') as f:
    f.write(new_content)
