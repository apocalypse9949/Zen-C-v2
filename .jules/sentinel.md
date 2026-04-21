## 2024-05-24 - Unsafe Command Execution & Predictable Temporary Files in REPL
**Vulnerability:** The REPL loop generated temporary source files using `rand()` (predictable temp file names) and executed them via `system()` with concatenated command strings (command injection risk). Temporary files were also not cleaned up after execution.
**Learning:** `system()` delegates execution to the shell (`cmd.exe` or `/bin/sh`), which interprets special characters in paths or arguments, leading to command injection vulnerabilities. `rand()` without cryptographically secure seeding creates guessable and highly collision-prone temporary filenames, especially problematic on shared systems.
**Prevention:**
1. Use `z_get_temp_dir()`, `z_get_pid()`, and an incrementing static counter (`eval_counter++`) for conflict-resistant temporary filenames.
2. Replace `system()` with `arg_run(&run_args)` which utilizes `ArgList` and `execvp`/`CreateProcess`, bypassing shell interpretation entirely.
3. Ensure explicit file cleanup `remove(tmp_path)` is performed after operations complete to avoid disk space exhaustion and leave less footprint on the system.
