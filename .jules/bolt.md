## 2024-11-20 - Optimize extract_call_args in codegen_utils.c
**Learning:** `extract_call_args` used an O(N^2) pattern with `strcat` on a progressively growing buffer, causing slow compilation when handling functions with many arguments.
**Action:** Replaced `strcat` with manual length tracking and `memcpy`, ensuring O(N) performance for argument list parsing.
