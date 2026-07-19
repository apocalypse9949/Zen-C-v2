import re

def modify_file(filepath, pattern, replacement):
    with open(filepath, 'r') as f:
        content = f.read()
    content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    with open(filepath, 'w') as f:
        f.write(content)

pattern = r'''(    if \(old_struct && new_struct && param\)
    \{
        char tpl_w\[1024\];
        snprintf\(tpl_w, sizeof\(tpl_w\), "%s<%s>", old_struct, param\);
        if \(strstr\(res, tpl_w\)\)
        \{
            char \*tmp = replace_in_string\(res, tpl_w, new_struct\);
            zfree\(res\);
            res = tmp;
        \}
    \}

    if \(old_struct && new_struct && strstr\(res, old_struct\)\)
    \{
        char \*tmp = replace_in_string\(res, old_struct, new_struct\);
        zfree\(res\);
        res = tmp;
    \})'''
replacement = r'''    if (old_struct && new_struct && param && res)
    {
        char tpl_w[1024];
        snprintf(tpl_w, sizeof(tpl_w), "%s<%s>", old_struct, param);
        if (strstr(res, tpl_w))
        {
            char *tmp = replace_in_string(res, tpl_w, new_struct);
            if (tmp) {
                zfree(res);
                res = tmp;
            }
        }
    }

    if (old_struct && new_struct && res && strstr(res, old_struct))
    {
        char *tmp = replace_in_string(res, old_struct, new_struct);
        if (tmp) {
            zfree(res);
            res = tmp;
        }
    }'''
modify_file('src/parser/utils/utils_template_replace.c', pattern, replacement)
