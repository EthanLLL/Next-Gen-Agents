from openai import OpenAI
import json
import config
from functions import (
    get_current_location,
    get_current_weather,
    get_ip_from_headers,
    function_map
)
from utils import parse_json_str
from execute_tree import execute_tree

client = OpenAI(
    api_key=config.openai_api_key
)

system_prompt = '''
You have access to the following tools:
[
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city or region which is required to fetch weather information.",
                    "get_value_from_tool": "get_current_location"
                },
                "unit": {
                    "type": "string",
                    "enum": [
                        "celsius",
                        "fahrenheit"
                    ]
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "get_current_location",
        "description": "Use this tool to get the current location if user does not provide a location",
        "parameters": {
            "type": "object",
            "properties": {
                "ip": {
                    "type": "string",
                    "description": "The user's request ip to determine the current location",
                    "get_value_from_tool": "get_ip_from_headers"
                }
            }
            "required": ["ip"]
        }
    },
    {
        "name": "get_ip_from_headers",
        "description": "Use this tool to get the user ip from headers",
        "parameters": {
            "type": "object",
            "properties": {
                "headers": {
                    "type": "string",
                    "description": "The user's request headers to determine the ip"
                }
            }
            "required": ["headers"]
        }
    }
]
Select one or more tools if needed, respond with only a recursive tree structure JSON object matching the following schema:
{
    "result": "tool_use",
    "name": "<function name of the root node>",
    "arguments": [
        {
            "name": "<arg name>",
            "source": {
                "name": "<function name of the current node if this arg depends on a result of calling another function>",
                "type": "function",
                "arguments": [<Recursive tree structure to describe multi function arguments dependencies>]
            }
        },
        {
            "name": "<arg name>",
            "value": <Automatically fill in parameters if provided following tools json schema>
        }
    ]
}

If no further tools needed, response with only a JSON object matching the following schema:
{
    "result": "stop",
    "content": "<Your response to the user.>",
    "explanation": "<The explanation why you get the final answer.>"
}
'''

def complete(messages):
    model = 'gpt-3.5-turbo'
    # model = 'gpt-4-turbo-preview'
    completions = client.chat.completions.create(
        model=model,
        temperature=0,
        max_tokens=2000,
        messages=[
            {'role': 'system', 'content': system_prompt},
            *messages
        ]
    )
    # print(completions)
    return parse_json_str(completions.choices[0].message.content)

def agents(messages):
    
    finished = False
    response = ''
    while not finished:
        result = complete(messages)
        if result['result'] == 'tool_use':
            # print(result)
            function_result = execute_tree(result, function_map)
            messages.append({'role': 'assistant', 'content': f'Should execute multi functions which tree defination is {json.dumps(result)}'})
            messages.append({'role': 'user', 'content': f'I have execute the functions and the result is {function_result}'})

        elif result['result'] == 'stop':
            finished = True
            response = result['content']
    return response

def main():
    messages = [
        # {'role': 'user', 'content': 'What is the current weather of Guangzhou, Shanghai and Beijing? Do I have to bring an umbrella?'},
        # {'role': 'user', 'content': '今日の広州と北京の天気はどうですか?外出時に傘が必要ですか?'},
        # {'role': 'user', 'content': '请问今天广州和北京的天气如何？出门需要带伞吗'},
        # Use this messages to test if LLM choose get_current_location before get_weather
        {'role': 'user', 'content': 'What is the current weather? Do I have to bring an umbrella? My request ip is 1.1.1.1'},
        # Use these messages to test if tool is unnecessary.
        # {'role': 'user', 'content': 'What is the current timestamp?'}
        # {'role': 'user', 'content': 'Hi How are you?'}
    ]
    res = agents([*messages])
    print(f'AI: {res}')
    # res = agents([*messages], stream=True)
    # print(f'AI: {res}')

if __name__ == '__main__':
    main()
