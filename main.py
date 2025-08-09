import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.tools import available_functions, call_function
from config import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():

    if len(sys.argv) < 2:
        print("enter a prompt")
        sys.exit(1)
    
    user_prompt = sys.argv[1]
    messages = [
        types.Content(
            role='user',
            parts=[types.Part(text=user_prompt)],
        )
    ]

    verbose = False
    if len(sys.argv) >= 3 and sys.argv[2] == '--verbose':
        verbose = True

    for tries in range(20):
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt),
            )

            if verbose:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)

            function_call = response.function_calls
            response_content = None
            if function_call:
                for function_call_part in function_call:
                    result = call_function(function_call_part, verbose=verbose)
                    messages.append(result)

                    response_content = result.parts[0].function_response.response

                if not response_content:
                    raise Exception("fatal error")

                if verbose:
                    print(f"-> {response_content}")

            if not function_call and response.text:
                print(response.text)
                break

        except Exception as e:
            print(f'Error: {str(e)}')
            
                
if __name__ == "__main__":
    main()
