## 2026-05-14 - Secure Temporary File Creation
**Vulnerability:** Predictable temporary file paths created with rand() and fopen() in the compiler (CWE-377 / CWE-362), allowing symlink attacks and race conditions.
**Learning:** In C, rand() and z_get_pid() are insecure for generating unique filenames. Moreover, using fopen() without O_EXCL allows attackers to pre-create files as symlinks.
**Prevention:** Use mkstemp() (or mkstemps() for suffixes) on POSIX or _mktemp_s() + _open(..., _O_CREAT | _O_EXCL, ...) on Windows, combined with fdopen(fd, "w"). Make sure to cleanly close file descriptors if fdopen() fails.
