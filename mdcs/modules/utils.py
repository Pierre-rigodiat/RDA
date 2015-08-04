import json
from django.utils.html import escape


def sanitize(input_value):
    input_type = type(input_value)

    if input_type == list:
        clean_value = []
        for item in input_value:
            clean_value.append(sanitize(item))

        return clean_value
    elif input_type == dict:
        return {sanitize(key): sanitize(val) for key, val in input_value.items()}
    elif input_type == str or input_type == unicode:
        # print 'str'

        try:
            json_value = json.loads(input_value)
            sanitized_value = sanitize(json_value)
            # print sanitized_value

            clean_value = json.dumps(sanitized_value)
            # print clean_value

        except ValueError:
            clean_value = escape(input_value)

        return clean_value
    elif input_type == int or input_type == float:
        # print 'int/float'
        return input_value
    else:
        # Default sanitizing
        # print 'default: '+str(input_type)
        return escape(str(input_value))
