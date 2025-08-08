from google.genai import types

from functions.get_files_info import get_file_content, get_files_info, run_python_file, write_file
from functions.schemas import schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

def call_function(function_call_part, verbose=False):
    
    working_directory = './calculator'
    
    functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if not verbose:
        print(f" - Calling function: {function_call_part.name}")

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    
    func_to_call = functions[function_call_part.name]
    function_result = func_to_call(working_directory, **function_call_part.args)
    
    if not function_call_part.name:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )


    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result}
            )
        ],
    )
