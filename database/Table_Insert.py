__author__ = 'Ben Phillips'

import sqlite3
from database import DataValidation
from common.globalconfig import GlobalConfig
from common.logger import Logger

def insert_data(name, data_list, session_value):
    config = GlobalConfig()
    connection = sqlite3.connect(config['Database']['path'])
    cursor = connection.cursor()
    Logger().get('database.Table_Insert').debug(data_list)
    delimiter = ','
    param_placeholder = delimiter.join('?' * len(data_list))
    insert_string = 'insert into ' + name + ' values(null,' + param_placeholder + ')'
    cursor.execute(insert_string, data_list)

    if session_value is not None:
        session_recorded = cursor.execute('select count(session) from sessions where session = "' + session_value + '" and table_name = "' + name + '"').fetchall()
        if session_recorded[0][0] > 0:
            pass
        else:
            cursor.execute('insert into sessions values("' + session_value + '","' + name + '")')

    connection.commit()
    connection.close()

# we should already know the data is good but now we should break the
# dictionary into a table name and a list of data to insert into the
# table. We must also sort the list according to the table structure
# then call the insert_data method

def prepare_data_for_insertion(schema, data):
    #get the correct table schema we want to sort to
    table_schema = schema[
        DataValidation.DataValidation.get_first_key_value_of_dictionary(data)]
    #print(table_schema)
    #break the table/data dictionary into a table name and a dictionary of data
    table_name = DataValidation.DataValidation.get_first_key_value_of_dictionary(data)
    #print(table_name)
    data_dict = data[table_name]

    #session extraction
    session_value = None
    if 'session' in data_dict:
        session_value = data_dict.get('session')

    #build a list of data in the correct order
    Logger().get('database.Table_Insert').debug('Inserting Data: ' + str(data_dict))
    insert_list = []
    for col in table_schema:
        if col[1] == 'ID':
            pass
        elif col[1] not in data_dict:
            insert_list.append(None)
        else:
            insert_list.append(data_dict[col[1]])
    insert_data(table_name,insert_list,session_value)
