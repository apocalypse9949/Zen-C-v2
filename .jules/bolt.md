## Bolt Journal
## 2024-05-19 - Removed O(N^2) strcat loops from parser
**Learning:** Found several `strcat` loops in parser string manipulation (especially when joining types or arguments, such as in `parser_expr.c` and `parser_utils.c`) that can cause O(N^2) behavior when large generics/templates are involved.
**Action:** Replaced these loops with manual length tracking and `memcpy`, bringing string generation in these hotspots down to O(N).
