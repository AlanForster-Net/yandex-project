#import dependencies
import sqlite3


#path constans
STATS_TABLE = 'stats'
DB = 'data/data.db'

#write starts in db func
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


#get starts from db func
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


#get all stats (for stats win) from db
def get_all_stats(rows):
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()
    value = cursor.execute(f"""
            SELECT {rows} 
            FROM {STATS_TABLE}
        """).fetchall()
    connection.commit()
    connection.close()
    return value
