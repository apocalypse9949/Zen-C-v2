## 2024-03-24 - [Remove system() call and rand() usage to prevent shell injection and predictability]
**Vulnerability:** Use of system() for executing runtime/comptime shell commands exposes the application to command injection vulnerabilities, and use of rand() for filename generation allows predictability and race conditions.
**Learning:** Shell redirection in `system()` masks vulnerabilities, while direct process spawning requires capturing output streams safely programmatically.
**Prevention:** Replace all `system()` usages with `z_run_command` or `z_run_command_capture` using `ArgList` from `src/utils/cmd.h` for safe argument passing. Use `z_get_temp_dir()` and `z_get_pid()` along with static counters instead of `rand()` to ensure collision-free, secure temporary file paths.
