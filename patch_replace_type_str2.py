import re

with open('src/parser/utils/utils_template_replace.c', 'r') as f:
    c = f.read()

c = c.replace('if (!t->inner) return xstrdup("");\n            char *inner_zens = type_to_string(t->inner);', 'char *inner_zens = type_to_string(t->inner);')
c = c.replace('if (!base) return xstrdup("");\n        char *inner = type_to_c_string(base);', 'char *inner = type_to_c_string(base);')

with open('src/parser/utils/utils_template_replace.c', 'w') as f:
    f.write(c)
