import os
from functions.common import validate_path

from google import genai

types = genai.types


def write_file(working_directory, file_path, content):
    abs_path, err = validate_path(working_directory, file_path, "list")
    if err != "":
        return err
    try:
        dirs = os.path.dirname(abs_path)
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        with open(abs_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes the specified text content to the specified file in specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to the file to execute, relative to the working directory. If not provided or if it does not point to a python file, an error string is returned.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="text content to write to the file. If not provided, no content will be written to the file.",
            ),
        },
    ),
)
