from subprocess import run


class CompilationError(Exception):
    pass


def compile_lib(library_name):
    command = f"qmake src/{library_name}.pro && make"
    result = run(command, shell=True, check=True)

    if result.returncode == 0:
        return

    raise CompilationError(result.stdout.decode())
