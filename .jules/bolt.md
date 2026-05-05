## 2026-05-05 - Avoid O(N^2) strcat bottlenecks using memcpy

**Learning:** When generating strings within loops in the C codebase (such as mangling type names or combining generics), repeated `strcat` calls result in O(N^2) performance degradation due to redundant length traversal.

**Action:** Replace `strcat` with manual length tracking and `memcpy`. Always bounds-check with constant buffer limits like `MAX_ERROR_MSG_LEN` or handle dynamic buffer scaling optimally with `while (len > cap) cap *= 2;`.
