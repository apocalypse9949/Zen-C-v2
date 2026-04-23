## 2024-04-23 - Array and Tuple literal parsing O(N^2) optimization
**Learning:** In the compiler codebase, repeatedly using `strlen` and `strcat` or `strncat` on dynamic buffers inside `while` loops causes O(N^2) complexity, leading to severe performance bottlenecks for large inputs (like large array or tuple literals).
**Action:** Replace `strlen()` and `strcat/strncat` with manual length tracking (`size_t curr_len`) and `memcpy()` to maintain O(N) performance. Ensure capacity checking uses `while (curr_len + len > cap) { cap *= 2; }` to safely grow buffers.
