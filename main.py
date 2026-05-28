import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_functions import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
]

def main():
    print("AVA")

if api_key == None:
    raise RuntimeError ("No API KEY Provided")

if __name__ == "__main__":
    main()

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
)

if response.usage_metadata == None:
    raise RuntimeError ("API Request Fail")
elif args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens:{response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if response.function_calls != None:
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")
        function_call_result = call_function(function_call)
        if function_call_result.parts == None:
            raise Exception ("Silence")
        elif function_call_result.parts[0].function_response == None:
            raise Exception ("Objection!")
        elif function_call_result.parts[0].function_response.response == None:
            raise Exception ("Mistrial!")
        elif args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
else:
    print(response.text)