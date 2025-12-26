from handlers.json_handler import reader
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(BASE_DIR, "../", "data", "cfg.json")



def get_primary_screen():
    data = reader(PATH)
    if 'primary_display' in data.keys():
        return data['primary_display']
    else:
        return -1

print(get_primary_screen())





