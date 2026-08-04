import re

with open('src/parser/utils/utils_registry.c', 'r') as f:
    content = f.read()

content = content.replace(
    'if (!ctx->struct_hash[slot].name[0] || ctx->struct_hash[slot].name[0] == name[0] && strcmp(ctx->struct_hash[slot].name, name) == 0)',
    'if (!ctx->struct_hash[slot].name[0] || (ctx->struct_hash[slot].name[0] == name[0] && strcmp(ctx->struct_hash[slot].name, name) == 0))'
)

with open('src/parser/utils/utils_registry.c', 'w') as f:
    f.write(content)
