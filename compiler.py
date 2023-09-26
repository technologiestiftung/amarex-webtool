import os
from subprocess import run


class CompilationError(Exception):
    pass


def compile_lib(project_path):
    os.chdir(project_path)
    command = f"qmake src/app/app.pro && make"
    result = run(command, shell=True, check=True)

    if result.returncode == 0:
        return

    raise CompilationError(result.stdout.decode())
