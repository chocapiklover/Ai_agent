import os
from config import MAX_CHARS
import subprocess

def get_files_info(working_directory, directory="."):
    absolute_working_path = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, directory))
    
    if not full_path.startswith(absolute_working_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'

    try: 
        dir_contents = os.listdir(full_path)
    except Exception as e:
        return f'Error: {str(e)}'
        
    joined_dir_contents = []

    for item in dir_contents:
        item_path = os.path.join(full_path, item)
        
        try:
            file_size = os.path.getsize(item_path)

            is_dir = os.path.isdir(item_path)
        except Exception as e:
            return f'Error: {str(e)}'
        
        joined_dir_contents.append(f'- {item}: file_size={file_size} bytes, is_dir={is_dir}')
    return '\n'.join(joined_dir_contents)


def get_file_content(working_directory, file_path):
    absolute_working_path = os.path.abspath(working_directory)
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not absolute_file_path.startswith(absolute_working_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(absolute_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(absolute_file_path, 'r') as f:
            file_contents = f.read(MAX_CHARS + 1)
            
            if len(file_contents) > MAX_CHARS:
                shorten_contents = file_contents[:MAX_CHARS]
                shorten_contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return shorten_contents
            
            return file_contents
    
    except Exception as e:
        return f'Error: {str(e)} '

    
def write_file(working_directory, file_path, content):
    absolute_working_path = os.path.abspath(working_directory)
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not absolute_file_path.startswith(absolute_working_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        directory = os.path.dirname(absolute_file_path)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
    except Exception as e:
        return f'Error: {str(e)}'
    with open(absolute_file_path, 'w') as f:
        f.write(content)
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

def run_python_file(working_directory, file_path, args=[]):

    absolute_working_path = os.path.abspath(working_directory)
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not absolute_file_path.startswith(absolute_working_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    if not os.path.exists(file_path):
        return f'Error: File "{file_path}" not found.'

    try:
    
        result = subprocess.run(
                        ['python', file_path] + args,
                        cwd=absolute_working_path,       
                        capture_output=True,
                        timeout=30,
                        text=True
        )

        stdout = result.stdout
        stderr = result.stderr

        output = ''

        if stdout:
            output += f'STDOUT: {stdout}\n'

        if stderr:
            output += f'STDERR: {stderr}\n'

        if result.returncode != 0:
            output += f'Process exited with code {result.returncode}'

        if not stderr and not stdout:
            output = 'No output produced.'
        
        return output
        
    except Exception as e:
        return f'Error {str(e)}'
