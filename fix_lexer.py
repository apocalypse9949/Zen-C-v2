import re

with open('src/lexer/token.c', 'r') as f:
    content = f.read()

# We need to replace the long chain of `if (len == ... && strncmp(...) == 0)` with a switch.

match_block = re.search(r'if \(len == 4 && strncmp\(s, "test", 4\) == 0\)(.*?)if \(len == 1 && s\[0\] == \'f\' && s\[1\] == \'"\'\)', content, re.DOTALL)

if match_block:
    old_code = match_block.group(0)

    # We want to keep everything before and after the matched block.
    # We will generate a switch statement for lengths.

    keywords = re.findall(r'if \(len == (\d+) && strncmp\(s, "([^"]+)", \d+\) == 0\)\n\s+{\n\s+return \(Token\){([^,]+)', old_code)

    switch_code = "switch (len) {\n"
    by_len = {}
    for length, word, tok in keywords:
        by_len.setdefault(int(length), []).append((word, tok))

    for l in sorted(by_len.keys()):
        switch_code += f"        case {l}:\n"
        for word, tok in by_len[l]:
            switch_code += f'            if (s[0] == \'{word[0]}\' && strncmp(s, "{word}", {l}) == 0) return (Token){{{tok}, s, {l}, start_line, start_col, l->filename}};\n'
        switch_code += "            break;\n"

    switch_code += "        default: break;\n        }\n\n        // F-Strings\n        if (len == 1 && s[0] == 'f' && s[1] == '\"')"

    content = content.replace(old_code, switch_code)

with open('src/lexer/token.c', 'w') as f:
    f.write(content)
