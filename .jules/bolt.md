## 2026-05-09 - Caching Type Sanitization in O(N) Mangling

**Learning:** When applying the O(N) string building pattern (`memcpy` instead of `strcat`) to complex AST mangling loops (like `resolve_struct_name_from_type` in Zen-C's parser), it's highly inefficient to calculate lengths in Pass 1 and then recalculate the exact same sanitized strings in Pass 2. Redundant calls to recursive functions like `type_to_string` and `sanitize_mangled_name` can cause significant parsing overhead on deeply nested generics.

**Action:** Always allocate a temporary parallel array (e.g., `char **cached_cleans`) during Pass 1 to store the processed sub-strings. Use these cached pointers in Pass 2 to build the final `memcpy` buffer, and then free them. This completely eliminates the need to traverse the AST or re-sanitize the names a second time, resulting in a pure mathematically optimal string construction.
