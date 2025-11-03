import os

from functions import common

from google import genai

types = genai.types


def get_files_info(working_directory, directory="."):
    abs_path, err = common.validate_path(working_directory, directory, "list")
    if err != "":
        return err
    # full_path = os.path.join(working_directory, directory)
    # abs_path = os.path.abspath(full_path)
    # if not abs_path.startswith(os.path.abspath(working_directory)):
    #     return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_path):
        return f'Error: "{directory}" is not a directory'

    res = []
    for dir_item in os.listdir(abs_path):
        path = os.path.join(abs_path, dir_item)
        try:
            string = f"{dir_item}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)}"
        except Exception as e:
            return f"Error: {e}"
        res.append(string)
    return "\n".join(res)


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
