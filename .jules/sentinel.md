## 2025-02-28 - Fix command injection and predictable temp files in comptime compilation
**Vulnerability:** Command injection in comptime evaluation due to insecure `system()` usage and predictable temporary filenames generated with `rand()`.
**Learning:** Using `system()` with unescaped variables or paths poses injection risks, and `rand()` for temp files is vulnerable to race conditions and predictability.
**Prevention:** Use `ArgList` with `arg_run()` for compilation and `z_run_command_capture` for execution to bypass shell injection. Use `z_get_temp_dir()` and `z_get_pid()` with a counter for secure temp filenames.
