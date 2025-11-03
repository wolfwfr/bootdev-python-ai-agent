import os


def validate_path(working_directory, rel_path, op):
    full_path = os.path.join(working_directory, rel_path)
    abs_path = os.path.abspath(full_path)
    if not abs_path.startswith(os.path.abspath(working_directory)):
        return (
            "",
            f'Error: Cannot {op} "{rel_path}" as it is outside the permitted working directory',
        )
    return abs_path, ""
