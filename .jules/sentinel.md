## 2024-05-28 - Secure shell execution
**Vulnerability:** Shell command injection via `system()` in the compiler core and REPL components. User inputs and unvalidated string parameters were being directly formatted and executed using `system()`.
**Learning:** Functions like `system()` process commands through the user's shell (e.g., `sh -c`), leaving string constructions involving variables susceptible to injection attacks where a user can break out of arguments and append arbitrary shell commands.
**Prevention:** Always use argument arrays with safe `exec` family wrappers like `z_run_command_capture()` or `arg_run()` (via the `ArgList` API) to execute processes without shell interpolation.
