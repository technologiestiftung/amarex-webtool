from subprocess import run


class CompilationError(Exception):
    pass


def compile_lib():
    command = "qmake src/clibrary.pro && make"
    result = run(command, shell=True, check=True)

    if result.returncode == 0:
        return

    raise CompilationError(result.stdout.decode())
