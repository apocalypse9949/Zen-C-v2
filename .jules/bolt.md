## 2026-04-24 - O(N^2) String Append in C
**Learning:** Repeated `strcat` calls inside loops on fixed-size buffers lead to O(N^2) time complexity and buffer overflow risks (Schlemiel the Painter's algorithm). Fixed-size arrays with manual `strcat` are surprisingly common in legacy/C-like string builders.
**Action:** Always refactor `strcat` in loops to use dynamic capacity scaling (`xrealloc`) with a manual length tracker (`curr_len`) and `memcpy` for O(1) appends, ensuring memory safety and massive performance improvements for large strings.
