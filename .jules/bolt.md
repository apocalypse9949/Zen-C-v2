## 2026-05-13 - O(N^2) strcat loops
**Learning:** The codebase relies on xmalloc, which interacts with an arena allocator that causes iterative string allocation to persist. Additionally, concatenating strings using strcat and strlen in a loop causes severe O(N^2) bottlenecks.
**Action:** Replace loops containing strlen and strcat with a two-pass approach: pre-calculate max needed buffer length, allocate once, and use memcpy with a manual length pointer to populate the buffer in O(N).
