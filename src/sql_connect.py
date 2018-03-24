import mysql.connector


def city_demographics(city):
    # Create connection to our server
    ns = mysql.connector.connect(host='178.62.1.222', database='NeighborhoodSimulator', user='ns', password='Nsim1234!')

    # Create a cursor to query the database and navigate through results
    cur = ns.cursor()

    # Form the query
    query = ("SELECT city, population, crime_rate, birth_rate, divorce_rate FROM Demo_demo WHERE city = %s")

    # Execute the query, including the 'city' variable which gets passed into the function.
    cur.execute(query, (city,))

    # Iterate through the results and print
    for (city, population, crime_rate, birth_rate, divorce_rate) in cur:
        print("{}, {}, {}, {}, {}".format(city, population, crime_rate, birth_rate, divorce_rate))

    # Clean up and close connection
    cur.close()
    ns.close()


city_demographics("Madrid")


