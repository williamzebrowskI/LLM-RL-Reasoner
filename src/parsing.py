import re

def parse_options(options_list):
    options_dict = {}
    for opt in options_list:
        parts = opt.split(')', 1)
        if len(parts) == 2:
            key = parts[0].strip().upper()
            value = parts[1].strip()
            value = re.sub(r'^[A-E]\)', '', value).strip()
            if key in options_dict:
                print(f"Warning: Duplicate option key '{key}' found. Overwriting previous value.")
            options_dict[key] = value
        else:
            print(f"Warning: Option '{opt}' is not in the expected format 'Letter)Text'. Skipping.")
    return options_dict