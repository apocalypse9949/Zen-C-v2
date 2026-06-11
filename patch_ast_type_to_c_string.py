import re

with open('src/ast/ast.c', 'r') as f:
    c = f.read()

c = c.replace('while (base->kind == TYPE_ARRAY && base->array_size > 0)', 'while (base && base->kind == TYPE_ARRAY && base->array_size > 0)')

with open('src/ast/ast.c', 'w') as f:
    f.write(c)
