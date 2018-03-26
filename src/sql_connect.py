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
            query = "SELECT * FROM " + table + " WHERE city_name = ?"
            self.cur.execute(query, (city,))
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


"""Example create table query"""
# dbmgr.query("CREATE TABLE IF NOT EXISTS social_class ( city_name text PRIMARY KEY, country text NOT NULL, "
#            "lower_class number, middle_class number, upper_class number);")

"""Example INSERT queries"""
# dbmgr.query("INSERT INTO social_class VALUES ('London', 'UK', 20, 60, 20);")
# dbmgr.query("INSERT INTO race VALUES ('London', 'UK', 59.79, 13.32, 8.4, 18.49)")


"""Example usage if you want to use this as a standalone script"""
# dbmgr = DatabaseManager("testdb.db")
# returned_data = dbmgr.demo_data("default", "race")
# print(returned_data)




