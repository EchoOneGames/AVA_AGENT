import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="write contents to a file in a specified directory relative to the working directory, ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text to be written to the declared file",
            ),    
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file intended to be read from",
            ),
        },
    ),
)



def write_file(working_directory: str, file_path: str, content: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs


    if not valid_target_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    elif os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    if not os.path.exists(target_file):
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

    with open(target_file, "w") as f:
        f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'