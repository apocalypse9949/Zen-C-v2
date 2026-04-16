## 2024-05-20 - O(N^2) string construction in ast_to_string_recursive
**Learning:** `ast_to_string_recursive` used `strcat()` and `strlen()` inside a loop for `NODE_EXPR_CALL` and `NODE_EXPR_STRUCT_INIT`. This leads to O(N^2) complexity for large structs or calls.
**Action:** When building strings in C inside loops, prefer manual length tracking (`curr_len`) and `memcpy()` to keep complexity at O(N). Ensure null termination is explicitly added (`buf[curr_len] = '\0'`).
