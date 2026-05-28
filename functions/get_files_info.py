import os
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory: str, directory: str = ".") -> str:

    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    elif not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    

    raw_contents = os.listdir(target_dir)
    reply = []
    for entry in raw_contents:
        reply.append(f" - {entry}: file_size={os.path.getsize(os.path.join(target_dir, entry))}, is_dir={os.path.isdir(os.path.join(target_dir, entry))}")
    result = "\n".join(reply)
    return result
        