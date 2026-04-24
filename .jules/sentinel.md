
## $(date +%Y-%m-%d) - Fix buffer overflow in process_fstring
**Vulnerability:** A static 8192-byte buffer was used to generate code for formatted strings (`f-strings`) using `strcat` and `strcpy` in a loop inside `src/parser/parser_utils.c`. An attacker could cause a buffer overflow by supplying an excessively large or nested f-string literal.
**Learning:** Fixed-size buffers combined with unbounded loop concatenation are dangerous in compiler C code. The compiler must securely handle arbitrary length strings, typically using dynamically resized buffers.
**Prevention:** Avoid `strcat` into fixed buffers. Use an O(N) append macro with dynamic capacity scaling via `xrealloc` and memory copying (`memcpy`).
