import re

with open('src/parser/utils/utils_template_replace.c', 'r') as f:
    c = f.read()

c = c.replace('char *inner_zens = type_to_string(t->inner);', 'if (!t->inner) return xstrdup("");\n            char *inner_zens = type_to_string(t->inner);')
c = c.replace('char *inner = type_to_c_string(base);', 'if (!base) return xstrdup("");\n        char *inner = type_to_c_string(base);')

with open('src/parser/utils/utils_template_replace.c', 'w') as f:
    f.write(c)
