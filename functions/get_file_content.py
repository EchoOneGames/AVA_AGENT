import os
from google.genai import types
from config import MAX_CHARS

schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="gets the file content in a specified directory relative to the working directory, returning a maximum of 10,000 characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file intended to be read from",
            ),
        },
    ),
)

def get_file_content(working_directory: str, file_path: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    file_content_string = ""

    if not valid_target_dir:
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    
    elif not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    with open(target_file, "r") as f:
        file_content_string = f.read(MAX_CHARS)
        if f.read(1):
            file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

    return file_content_string