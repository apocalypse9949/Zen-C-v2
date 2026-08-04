import re

with open('src/parser/utils/utils_registry.c', 'r') as f:
    content = f.read()

# Replace strcmp(a, b) == 0 with a[0] == b[0] && strcmp(a, b) == 0 in loops in utils_registry.c
content = re.sub(r'strcmp\(ctx->struct_hash\[slot\]\.name, name\) == 0', r'ctx->struct_hash[slot].name[0] == name[0] && strcmp(ctx->struct_hash[slot].name, name) == 0', content)
content = re.sub(r'strcmp\(ta->alias, alias\) == 0', r'ta->alias[0] == alias[0] && strcmp(ta->alias, alias) == 0', content)
content = re.sub(r'strcmp\(c->name, type\) == 0', r'c->name[0] == type[0] && strcmp(c->name, type) == 0', content)
content = re.sub(r'strcmp\(c->sig, sig\) == 0', r'c->sig[0] == sig[0] && strcmp(c->sig, sig) == 0', content)
content = re.sub(r'strcmp\(curr->name, name\) == 0', r'curr->name[0] == name[0] && strcmp(curr->name, name) == 0', content)
content = re.sub(r'strcmp\(s->strct\.name, name\) == 0', r's->strct.name[0] == name[0] && strcmp(s->strct.name, name) == 0', content)
content = re.sub(r'strcmp\(i->name, name\) == 0', r'i->name[0] == name[0] && strcmp(i->name, name) == 0', content)
content = re.sub(r'strcmp\(r->node->strct\.name, name\) == 0', r'r->node->strct.name[0] == name[0] && strcmp(r->node->strct.name, name) == 0', content)
content = re.sub(r'strcmp\(r->node->enm\.name, name\) == 0', r'r->node->enm.name[0] == name[0] && strcmp(r->node->enm.name, name) == 0', content)
content = re.sub(r'strcmp\(all->name, name\) == 0', r'all->name[0] == name[0] && strcmp(all->name, name) == 0', content)
content = re.sub(r'strcmp\(d->name, name\) == 0', r'd->name[0] == name[0] && strcmp(d->name, name) == 0', content)
content = re.sub(r'strcmp\(e->node->enm\.name, name\) == 0', r'e->node->enm.name[0] == name[0] && strcmp(e->node->enm.name, name) == 0', content)
content = re.sub(r'strcmp\(r->node->trait\.name, name\) == 0', r'r->node->trait.name[0] == name[0] && strcmp(r->node->trait.name, name) == 0', content)
content = re.sub(r'strcmp\(c->name, name\) == 0', r'c->name[0] == name[0] && strcmp(c->name, name) == 0', content)
content = re.sub(r'strcmp\(n->func\.name, name\) == 0', r'n->func.name[0] == name[0] && strcmp(n->func.name, name) == 0', content)

with open('src/parser/utils/utils_registry.c', 'w') as f:
    f.write(content)
