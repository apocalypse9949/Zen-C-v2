## 2026-04-30 - Avoid `strlen` in loop conditions
**Learning:** Using `strlen()` inside loop conditions (e.g., `for (size_t k = 1; k < strlen(name); k++)`) evaluates the string length on every iteration, leading to O(N^2) performance degradation.
**Action:** Iterate using a null-terminator check (`name[k] != '\0'`) to ensure O(N) performance.