## 2026-05-03 - Optimize `extract_call_args` string building

**Learning:** When building strings inside a loop, especially extracting variables or types, repeatedly using `strcat` with `strlen` (e.g., in `extract_call_args`) causes $O(N^2)$ performance degradation. A single string with many arguments (such as 50,000) causes significant compilation lag.

**Action:** Replace `strcat` loops with manual length tracking and `memcpy`. Explicitly allocate sufficient buffer size (e.g., `strlen(args) * 2 + 1` when adding extra comma/space formatting) and maintain a length counter (`out_len += appended_len`) to safely bounds-check and append characters in $O(N)$ time.
