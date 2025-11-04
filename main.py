import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from config import MAIN_LOOP_LIMIT
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write import schema_write_file, write_file

types = genai.types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

user_prompt = "Hello"
messages = []

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    cwd = "./calculator"

    function_name = function_call_part.name
    function_args = function_call_part.args
    function_result = ""

    match function_name:
        case "get_file_content":
            function_result = get_file_content(cwd, **function_args)
        case "get_files_info":
            function_result = get_files_info(cwd, **function_args)
        case "run_python_file":
            function_result = run_python_file(cwd, **function_args)
        case "write_file":
            function_result = write_file(cwd, **function_args)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )


def main():
    parser = argparse.ArgumentParser(description="python-ai-agent")
    parser.add_argument("string_arg", type=str, help="The user prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    user_prompt = args.string_arg
    messages.append(types.Content(role="user", parts=[types.Part(text=user_prompt)]))

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    try:
        for _ in range(0, MAIN_LOOP_LIMIT):
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )
            for candidate in response.candidates:
                messages.append(candidate.content)

            fc = response.function_calls
            if fc is None:
                fc = []
            for function_call_part in fc:
                function_call_result = call_function(function_call_part, args.verbose)
                if (
                    len(function_call_result.parts) == 0
                    or function_call_result.parts[0].function_response.response[
                        "result"
                    ]
                    == ""
                ):
                    raise Exception("function response missing in action")
                if args.verbose:
                    print(
                        f"-> {function_call_result.parts[0].function_response.response}"
                    )
                messages.append(
                    types.Content(
                        role="user",
                        parts=function_call_result.parts,
                    )
                )

            if args.verbose:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(
                    f"Response tokens: {response.usage_metadata.candidates_token_count}"
                )

            if len(fc) == 0 and len(response.text) > 0:  # done
                print("Final response:")
                print(response.text)
                break
    except KeyboardInterrupt:
        print("exited by user request")
        sys.exit(1)
    except Exception as e:
        print(f"main-loop ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
