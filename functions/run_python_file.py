import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="run the specified python file. ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
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
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The array of armuments that may be required based on the python function called.",               
                items= types.Schema(
                    type=types.Type.STRING,
                    description="The arguments provided via the args array parameter",
                ),
            ),
        },
    ),
)

def run_python_file( working_directory: str, file_path: str, args: list[str] | None = None) -> str:

    worling_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(worling_dir_abs, file_path))
    valid_target_dir = os.path.commonpath([worling_dir_abs, target_file]) == worling_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    elif not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", os.path.abspath(target_file)]
    if args != None:
        command.extend(args)
    
    output = subprocess.run(command, stdout=True, stderr=True, capture_output=False, timeout=30, text=True)

    result = ""

    if output.returncode != 0:
        result = f'Process exited with code "{output.returncode}"'
    
    if output.stdout != None or output.stderr != None:
        result + "No output produced"
    
    result = result + f'STDOUT: "{output.stdout}", STDERR: "{output.stderr}"'
    
    return result