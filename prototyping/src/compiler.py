from pathlib import Path
from subprocess import PIPE, STDOUT, run

SRC = Path(__file__).resolve().parent


class CompilationError(Exception):
    pass


def compile_lib(source: Path, cflags=[], ldadd=[]):
    binary = source.with_suffix(".so")
    print("######" * 5)
    print(SRC)
    result = run(
        ["gcc", "-shared", *cflags, "-o", str(binary), str(source), *ldadd],
        stdout=PIPE,
        stderr=STDOUT,
        cwd=SRC,
    )

    if result.returncode == 0:
        return

    raise CompilationError(result.stdout.decode())
