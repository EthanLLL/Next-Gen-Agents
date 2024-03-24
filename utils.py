import json

def parse_json_str(json_str):
    # response from LLM may contains \n
    result = {}
    try:
        result = json.loads(json_str.replace('\n', '').replace('\r', ''))
        print('LLM response can be parsed as a valid JSON object.')
    except Exception as e:
        print('Cannot parsed to a valid python dict object')
        print(e)
    print(json.dumps(result, indent=4))
    return result