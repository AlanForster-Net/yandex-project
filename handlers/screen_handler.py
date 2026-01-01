import arcade


def read_scre

def get_primary_screen():
    data = reader(PATH)
    if 'primary_display' in data.keys():
        return data['primary_display']
    else:
        return -1

print(get_primary_screen())





