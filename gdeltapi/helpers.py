import json

def load_json(json_message, max_recursion_depth: int = 100, recursion_depth: int = 0):
    try:
        result = json.loads(json_message)
    except Exception as e:
        if recursion_depth >= max_recursion_depth:
            raise ValueError("Max Recursion depth is reached. JSON can not be parsed.")
        idx_to_replace = int(e.pos)
        if isinstance(json_message, bytes):
            json_message.decode("utf-8")
        json_message = list(json_message)
        json_message[idx_to_replace] = ' '
        new_message = ''.join(str(m) for m in json_message)
        return load_json(json_message=new_message, max_recursion_depth=max_recursion_depth,
                         recursion_depth=recursion_depth+1)
    return result