import sqlite3


class DatabaseManager(object):
    """Creates the connection"""
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    """Allows any query to be passed in, and the cursor will be returned"""
    def query(self, arg):
        self.cur.execute(arg)
        self.conn.commit()
        return self.cur

    """Returns the race stats for whichever city is passed as an argument"""
    def demo_data(self, city, table):
        try:
            query = "SELECT * FROM {idf} WHERE city_name = '{city}'".format(idf=table, city=city)
            self.cur.execute(query)
            desc = self.cur.description
            column_names = [col[0] for col in desc]
            data = [dict(zip(column_names, row))
                    for row in self.cur.fetchall()]
        except Exception as error:
            print('error executing query "{}", error: {}'.format(query, error))
            return None
        else:
            return data

    """Closes the connection at the end"""
    def __del__(self):
        self.conn.close()

# dbmgr = DatabaseManager("testdb.db")
"""Example create table query"""
# dbmgr.query("CREATE TABLE IF NOT EXISTS death_cause ( city_name text PRIMARY KEY, country text NOT NULL, "
#             "teen_illness number, teen_suicide number, young_adult_illness number, young_adult_suicide, "
#             "young_adult_accident number, adult_illness number, adult_suicide number, adult_accident number,"
#             "senior_illness number, senior_suicide number, senior_accident number);")

"""Example INSERT queries"""
# dbmgr.query("INSERT INTO death_cause VALUES ('default', 'default', 30, 70, 30, 10, 60, 45, 10, 45, 80, 10, 10);")
# dbmgr.query("INSERT INTO race VALUES ('London', 'UK', 59.79, 13.32, 8.4, 18.49)")

"""Example update query"""
# dbmgr.query("UPDATE race set `white` = 61.7, `black` = 13.8, latino = 18.3, asian = 6.2 where city_name = 'default'")

"""Example usage if you want to use this as a standalone script"""
# dbmgr = DatabaseManager("testdb.db")
# returned_data = dbmgr.demo_data("default", "race")
# print(returned_data)




