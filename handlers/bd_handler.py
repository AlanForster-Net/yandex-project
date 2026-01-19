import sqlite3


STATS_TABLE = 'stats'
DB = 'data/data.db'


def add_stats(searching, modifier=1, mod='add',type_of_search='short_name'):
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()
    if mod == 'add':
        value = cursor.execute(f"""
            SELECT value 
            FROM {STATS_TABLE}
            WHERE {type_of_search} == '{searching}';
        """).fetchall()[0][0]
        cursor.execute(f"""
            UPDATE {STATS_TABLE}
            SET value = {value + modifier}
            WHERE {type_of_search} == '{searching}'
        """)
    elif mod == 'new_val':
        cursor.execute(f"""
            UPDATE {STATS_TABLE}
            SET value = {modifier}
            WHERE {type_of_search} == '{searching}'
        """)
    connection.commit()
    connection.close()


def get_stats(searching, type_of_search='short_name'):
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()
    value = cursor.execute(f"""
        SELECT value 
        FROM {STATS_TABLE}
        WHERE {type_of_search} == '{searching}';
    """).fetchall()[0][0]
    connection.commit()
    connection.close()
    return value