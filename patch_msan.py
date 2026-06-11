import re

with open('src/parser/utils/utils_template_replace.c', 'r') as f:
    c = f.read()

c = c.replace('if (nb) sprintf(res, "%s*", nb); else sprintf(res, "*"); /* safe */', 'if (nb) sprintf(res, "%s*", nb); else sprintf(res, "*"); /* safe */\n        if (!res) { return NULL; }')

with open('src/parser/utils/utils_template_replace.c', 'w') as f:
    f.write(c)
