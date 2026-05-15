## 2026-05-15 - Optimize string concatenation in code generation
**Learning:** O(N^2) string building using sequential `xmalloc` and `strcat`/`strlen` loops in C causes performance degradation and excessive memory retention when using the project's global arena allocator.
**Action:** Replace `strcat` with manual length tracking, pre-calculate lengths for a single contiguous memory allocation, and use `memcpy` for O(N) execution.
