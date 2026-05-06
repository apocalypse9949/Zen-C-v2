## 2026-05-06 - Optimizing string concatenation in C loops

**Learning:** `strcat` repeatedly traverses the destination string to find the null terminator. When used inside a loop, this turns an $O(n)$ string building process into an $O(n^2)$ operation, causing significant performance degradation for long argument lists or deeply nested structures.
**Action:** Replace `strcat` with manual length tracking (`curr_len`) and `memcpy` inside loops, transforming the operation back to $O(n)$. Always explicitly null-terminate the result buffer.
