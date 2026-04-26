## 2024-04-26 - O(N²) strcat bottlenecks in string building loops
**Learning:** `strcat` and `strlen` inside a loop can severely degrade performance by causing O(N²) behavior when building large strings (e.g., dynamically mangled types in compiler AST passes).
**Action:** Always maintain an external length tracker (`curr_len`) and append chunks via O(N) `memcpy` over `strcat`. Furthermore, correctly use a `while (curr + len >= cap) cap *= 2;` multiplier block over repetitive additions for exponential backoff dynamically growing buffers.
