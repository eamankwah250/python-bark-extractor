# postgreSQL
import psycopg2


# Database class
class Database:
    def __init__(self, db, user, password, port, host):
        self.db = db
        self.user = user
        self.password = password
        self.port = port
        self.host = host

    def connect(self):
        self.connection = psycopg2.connect(
            database=self.db,
            user=self.user,
            password=self.password,
            port=self.port,
            host=self.host
        )

#     def executeQuery(self, query, values=None):
#         print('query:', query)
#         print('values:', values)
#         cursor = self.connection.cursor()
#         cursor.execute(query, values)
#         self.connection.commit()
#         cursor.close()

#     def selectQuery(self, relation):
#         cursor = self.connection.cursor()
#         query = 'SELECT * FROM {} ORDER BY day;'.format(relation)
#         cursor.execute(query)
#         rows = cursor.fetchall()
#         cursor.close()
#         return rows

#     def insertQuery(self, day, powerusage, electric_cost, waterusage, water_cost, totalcost):
#         cursor = self.connection.cursor()
#         query = 'INSERT INTO daily_summary_2 (day, electric_usage, electric_cost, water_usage, water_cost, total_cost) VALUES ({},{},{},{},{},{});'.format(
#             day, powerusage, electric_cost, waterusage, water_cost, totalcost)
#         cursor.execute(query)
#         self.connection.commit()
#         cursor.close()

    def close(self):
        self.connection.close()
