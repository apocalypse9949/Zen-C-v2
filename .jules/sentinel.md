## 2024-04-19 - Insecure Temporary File Creation Fixed
**Vulnerability:** Weak predictability and improper temporary directory bounds in string formatting when creating temp compilation files.
**Learning:** `sprintf(..., "/tmp/...%d", rand())` is insecure and causes predictable side effects and buffer overflow vulnerabilities. Adding entropy with `z_get_pid()` and dynamic platform-safe directory locations like `z_get_temp_dir()` mitigates these. Absolute compilation paths correctly omit the dot-slash run prefix.
**Prevention:** Use `snprintf` along with `z_get_temp_dir()`, `z_get_pid()`, and `rand()` for enhanced unpredictability. Ensure sizes for statically allocated paths correctly anticipate dynamically sized directories (`MAX_PATH_LEN`).
