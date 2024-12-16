import re
import sys
import toml

def read_input():
    return sys.stdin.read()

def remove_comments(input_data):
    return re.sub(r'#.*$', '', input_data, flags=re.MULTILINE).strip()

def parse_defs(input_data):
    defs_dict = {}
    matches = re.findall(r'def\s+([_a-zA-Z]+)\s*:=\s*([0-9]+|".*?"|\[.*?\])', input_data)
    for name, value in matches:
        if value.isdigit():
            defs_dict[name] = int(value)
        else:
            defs_dict[name] = value.strip('"').strip()
    return defs_dict

def parse_array(input_data, defs_dict):
    output = []
    arrays = re.findall(r'([_a-zA-Z]+)\s*=\s*\[(.*?)\]', input_data)

    for key, content in arrays:
        items = []
        for item in re.split(r',\s*', content):
            item = item.strip()
            if item.startswith('$') and item.endswith('$'):
                var_name = item[1:-1]
                resolved_value = defs_dict.get(var_name, None)
                if resolved_value is None:
                    raise ValueError(f"Undefined variable: {var_name}")
                items.append(resolved_value)
            elif item.isdigit():
                items.append(int(item))
            elif item.startswith('"') and item.endswith('"'):
                items.append(item.strip('"'))
            else:
                raise ValueError(f"Invalid value in array: {item}")
        output.append(f'{key} = [{", ".join(map(str, items))}]')

    return '\n'.join(output)

def main():
    try:
        input_data = read_input()
        input_data = remove_comments(input_data)

        defs_dict = parse_defs(input_data)
        transformed_output = parse_array(input_data, defs_dict)

        print(transformed_output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()

