import os
from subprocess import run


class CompilationError(Exception):
    pass


def compile_lib(project_filename):
    path = "/Users/guadaluperomero/ProjectsTSB/amarex/abimo/"
    os.chdir(path)
    command = f"qmake {project_filename}.pro && make"
    result = run(command, shell=True, check=True)

    if result.returncode == 0:
        return

    raise CompilationError(result.stdout.decode())
