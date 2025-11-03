import os
from config import MAX_FILE_CHAR_COUNT
from functions.common import validate_path
from google import genai

types = genai.types


def get_file_content(working_directory, file_path):
    abs_path, err = validate_path(working_directory, file_path, "list")
    if err != "":
        return err
    print(abs_path)
    if not os.path.isfile(abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_path, "r") as f:
            contents = f.read(MAX_FILE_CHAR_COUNT + 1)
            if len(contents) == MAX_FILE_CHAR_COUNT + 1:
                contents = contents[: len(contents) - 1]
                contents += f'[...File "{file_path}" truncated at 10000 characters]'
            return contents
    except Exception as e:
        return "Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="get the text content of the specified file, truncated at 10_000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to the file to read, relative to the working directory. If not provided, an error string is returned.",
            ),
        },
    ),
)
