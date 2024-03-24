import random
from aws.image_file.file import traverse_dict_by_filter


def region_id():
    return random.randint(1, 16383)


def find_items_in_dict(value, want_keys):
    if not isinstance(want_keys, list):
        return traverse_dict_by_filter(value, [want_keys])
    else:
        return traverse_dict_by_filter(value, want_keys)