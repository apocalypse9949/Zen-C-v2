## 2024-05-19 - Removed O(N^2) strlen in parser loop
**Learning:** Found a classic C performance pitfall in `src/parser/parser_type.c` where `strlen(name)` was evaluated as the condition of a `for` loop `for (size_t k = 1; k < strlen(name); k++)`. This results in O(N^2) complexity because `strlen` loops through the string on every iteration.
**Action:** When validating string suffixes or parsing characters in C, check against the null terminator `name[k] != '\0'` directly rather than repeatedly measuring the string length.
