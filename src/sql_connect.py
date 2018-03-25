import mysql.connector


class DbCon(object):

    def __init__(self, db):
        # Create connection to our server
        self.ns = mysql.connector.connect(host='178.62.1.222', database=db, user='ns',
                                          password='Nsim1234!')

        self.cur = self.ns.cursor()

    def query(self, query):
        try:
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

    def __del__(self):
        self.ns.close()

    def city_demographics(self, city):

        # Form the query
        query = ("SELECT city, population, crime_rate, birth_rate, divorce_rate FROM NeighborhoodSimulator.Demo_demo "
                 "WHERE city = %s")

        # Execute the query, including the 'city' variable which gets passed into the function.
        self.cur.execute(query, (city,))

        # Iterate through the results and print
        for (city, population, crime_rate, birth_rate, divorce_rate) in self.cur:
            print("{}, {}, {}, {}, {}".format(city, population, crime_rate, birth_rate, divorce_rate))
