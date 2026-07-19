import re

def modify_file(filepath, pattern, replacement):
    with open(filepath, 'r') as f:
        content = f.read()
    content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    with open(filepath, 'w') as f:
        f.write(content)

pattern = r'''(    if \(slen > 1 && src\[slen - 1\] == '\*'\)
    \{
        char \*base = xmalloc\(\(size_t\)\(intptr_t\)\(slen\)\);
        strncpy\(base, src, slen - 1\);
        base\[slen - 1\] = 0;
        char \*nb = replace_type_str\(base, param, concrete, old_struct, new_struct\);
        char \*res = xmalloc\(strlen\(nb\) \+ 2\);
        sprintf\(res, "%s\*", nb\); /\* safe \*/
        zfree\(base\);
        zfree\(nb\);
        return res;
    \})'''
replacement = r'''    if (slen > 1 && src[slen - 1] == '*')
    {
        char *base = xmalloc((size_t)(slen));
        strncpy(base, src, slen - 1);
        base[slen - 1] = 0;
        char *nb = replace_type_str(base, param, concrete, old_struct, new_struct);
        if (!nb) {
            zfree(base);
            return NULL;
        }
        char *res = xmalloc(strlen(nb) + 2);
        sprintf(res, "%s*", nb); /* safe */
        zfree(base);
        zfree(nb);
        return res;
    }'''
modify_file('src/parser/utils/utils_template_replace.c', pattern, replacement)

pattern2 = r'''(        char \*base = xmalloc\(\(size_t\)\(intptr_t\)\(slen - 1\)\);
        strncpy\(base, src, slen - 2\);
        base\[slen - 2\] = 0;
        char \*nb = replace_type_str\(base, param, concrete, old_struct, new_struct\);
        char \*res = xmalloc\(strlen\(nb\) \+ 3\);
        sprintf\(res, "%s\*\*", nb\); /\* safe \*/
        zfree\(base\);
        zfree\(nb\);
        return res;)'''
replacement2 = r'''        char *base = xmalloc((size_t)(slen - 1));
        strncpy(base, src, slen - 2);
        base[slen - 2] = 0;
        char *nb = replace_type_str(base, param, concrete, old_struct, new_struct);
        if (!nb) {
            zfree(base);
            return NULL;
        }
        char *res = xmalloc(strlen(nb) + 3);
        sprintf(res, "%s**", nb); /* safe */
        zfree(base);
        zfree(nb);
        return res;'''
modify_file('src/parser/utils/utils_template_replace.c', pattern2, replacement2)
