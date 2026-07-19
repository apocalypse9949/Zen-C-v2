import re

def modify_file(filepath, pattern, replacement):
    with open(filepath, 'r') as f:
        content = f.read()
    content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    with open(filepath, 'w') as f:
        f.write(content)

pattern = r'''(static char \*replace_in_string\(const char \*src, const char \*old_w, const char \*new_w\)
\{
    if \(!src \|\| !old_w \|\| !new_w\)
        return src \? xstrdup\(src\) : NULL;

    if \(strchr\(old_w, ','\)\)
    \{
        char \*running_src = xstrdup\(src\);
        char \*p_ptr = \(char \*\)old_w;
        char \*c_ptr = \(char \*\)new_w;

        while \(\*p_ptr && \*c_ptr\)
        \{
            char \*p_end = strchr\(p_ptr, ','\);
            int p_len = p_end \? \(int\)\(p_end - p_ptr\) : \(int\)strlen\(p_ptr\);

            char \*c_end = strchr\(c_ptr, ','\);
            int c_len = c_end \? \(int\)\(c_end - c_ptr\) : \(int\)strlen\(c_ptr\);

            char curr_p\[256\] = \{0\};
            char curr_c\[256\] = \{0\};

            strncpy\(curr_p, p_ptr, \(size_t\)\(p_len\)\);
            if \(p_len < 256\)
                curr_p\[p_len\] = '\\0';
            else
                curr_p\[255\] = '\\0';

            strncpy\(curr_c, c_ptr, \(size_t\)\(c_len\)\);
            if \(c_len < 256\)
                curr_c\[c_len\] = '\\0';
            else
                curr_c\[255\] = '\\0';

            char \*next_src = replace_in_string\(running_src, curr_p, curr_c\);
            zfree\(running_src\);
            running_src = next_src;

            if \(p_end\)
                p_ptr = p_end \+ 1;
            else
                break;

            if \(c_end\)
                c_ptr = c_end \+ 1;
            else
                break;
        \}
        return running_src;
    \})'''
replacement = r'''static char *replace_in_string(const char *src, const char *old_w, const char *new_w)
{
    if (!src || !old_w || !new_w)
        return src ? xstrdup(src) : NULL;

    if (strchr(old_w, ','))
    {
        char *running_src = xstrdup(src);
        if (!running_src) return NULL;
        char *p_ptr = (char *)old_w;
        char *c_ptr = (char *)new_w;

        while (*p_ptr && *c_ptr)
        {
            char *p_end = strchr(p_ptr, ',');
            int p_len = p_end ? (int)(p_end - p_ptr) : (int)strlen(p_ptr);

            char *c_end = strchr(c_ptr, ',');
            int c_len = c_end ? (int)(c_end - c_ptr) : (int)strlen(c_ptr);

            char curr_p[256] = {0};
            char curr_c[256] = {0};

            strncpy(curr_p, p_ptr, (size_t)(p_len));
            if (p_len < 256)
                curr_p[p_len] = '\0';
            else
                curr_p[255] = '\0';

            strncpy(curr_c, c_ptr, (size_t)(c_len));
            if (c_len < 256)
                curr_c[c_len] = '\0';
            else
                curr_c[255] = '\0';

            char *next_src = replace_in_string(running_src, curr_p, curr_c);
            zfree(running_src);
            if (!next_src) return NULL;
            running_src = next_src;

            if (p_end)
                p_ptr = p_end + 1;
            else
                break;

            if (c_end)
                c_ptr = c_end + 1;
            else
                break;
        }
        return running_src;
    }'''
modify_file('src/parser/utils/utils_template_replace.c', pattern, replacement)

pattern2 = r'''(    if \(slen > 1 && src\[slen - 1\] == '\*'\)
    \{
        char \*base = xmalloc\(\(size_t\)\(intptr_t\)\(slen\)\);
        strncpy\(base, src, slen - 1\);
        base\[slen - 1\] = 0;
        char \*nb = replace_type_str\(base, param, concrete, old_struct, new_struct\);
        char \*res = xmalloc\(strlen\(nb\) \+ 2\);
        sprintf\(res, "%s\*", nb\);
        zfree\(nb\);
        zfree\(base\);
        return res;
    \})'''
replacement2 = r'''    if (slen > 1 && src[slen - 1] == '*')
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
        sprintf(res, "%s*", nb);
        zfree(nb);
        zfree(base);
        return res;
    }'''
modify_file('src/parser/utils/utils_template_replace.c', pattern2, replacement2)

pattern3 = r'''(        char \*base = xmalloc\(\(size_t\)\(slen \- 1\)\);
        strncpy\(base, src, slen - 2\);
        base\[slen - 2\] = 0;
        char \*nb = replace_type_str\(base, param, concrete, old_struct, new_struct\);
        char \*res = xmalloc\(strlen\(nb\) \+ 3\);
        sprintf\(res, "%s\*\*", nb\);
        zfree\(nb\);
        zfree\(base\);
        return res;)'''
replacement3 = r'''        char *base = xmalloc((size_t)(slen - 1));
        strncpy(base, src, slen - 2);
        base[slen - 2] = 0;
        char *nb = replace_type_str(base, param, concrete, old_struct, new_struct);
        if (!nb) {
            zfree(base);
            return NULL;
        }
        char *res = xmalloc(strlen(nb) + 3);
        sprintf(res, "%s**", nb);
        zfree(nb);
        zfree(base);
        return res;'''
modify_file('src/parser/utils/utils_template_replace.c', pattern3, replacement3)

pattern4 = r'''(    if \(old_struct && new_struct && param\)
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
replacement4 = r'''    if (old_struct && new_struct && param && res)
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
modify_file('src/parser/utils/utils_template_replace.c', pattern4, replacement4)
