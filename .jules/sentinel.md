## 2025-02-14 - Replace vulnerable system() with ArgList in comptime execution
**Vulnerability:** Shell command injection risk. `system()` was used for compiler execution and running comptime blocks, which runs via `/bin/sh` or `cmd.exe`.
**Learning:** For executable invocations, especially with arbitrary parameters like paths, using shell execution risks misinterpreting strings as options, redirects, or additional chained commands if spaces or specific tokens exist.
**Prevention:** Construct commands using an `ArgList` combined with `z_run_command_capture` to directly execute processes, strictly separating the executable from arguments. This inherently neutralizes sub-shell expansion bugs.
