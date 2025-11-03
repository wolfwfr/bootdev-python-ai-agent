import os
import subprocess
from functions.common import validate_path
from google import genai

types = genai.types


def run_python_file(working_directory, file_path, args=[]):
    abs_path, err = validate_path(working_directory, file_path, "execute")
    if err != "":
        return err
    if not os.path.exists(abs_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    args_new = ["uv", "run", abs_path]
    for arg in args:
        args_new.append(arg)
    try:
        compl = subprocess.run(
            args_new,
            timeout=30,
            capture_output=True,
            cwd=os.path.abspath(working_directory),
        )
    except Exception as e:
        return f"Error: executing Python file: {e}"
    res = []
    res.append(f"STDOUT: {compl.stdout}")
    res.append(f"STDERR: {compl.stderr}")
    if compl.returncode != 0:
        res.append(f"Process exited with code {compl.returncode}")
    if len(compl.stdout) == 0:
        res.append("No output produced")
    return "\n".join(res)


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="executes a .py file in specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to the file to execute, relative to the working directory. If not provided or if it does not point to a python file, an error string is returned.",
            ),
        },
    ),
)
