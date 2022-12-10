from psycopg2 import connect
from am_project.settings import PSYORG_CONFIG
from collections import OrderedDict


def get_ordered_dict(data_fetch, data_description):
    data_description = tuple(map(lambda x: x.name, data_description))
    return [OrderedDict(zip(data_description, item)) for item in data_fetch]


def execute_sql(get_query):
    def wrapper(*args):
        params = ()
        try:
            sql, params = get_query(*args)
        except ValueError:
            sql = get_query()
        connection = cursor = None
        try:
            connection = connect(PSYORG_CONFIG)
            cursor = connection.cursor()
            cursor.execute(sql, params)
            result = get_ordered_dict(cursor.fetchall(), cursor.description)
        except Exception as e:
            connection.close()
            raise e
        else:
            connection.commit()
        finally:
            connection.close()
        return result
    return wrapper
