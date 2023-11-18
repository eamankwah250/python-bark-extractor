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
        try:
            self.connection = psycopg2.connect(
                database=self.db,
                user=self.user,
                password=self.password,
                port=self.port,
                host=self.host
            )
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("UNABLE TO CONNECT TO THE DATABASE.")
            print("MAKE SURE YOUR IP ADDRESS IS WHITELISTED BY BLUEHOST!")
            quit()

    def executeQuery(self, query, values=None):
        print('query:', query)
        print('values:', values)
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        self.connection.commit()
        cursor.close()

    def selectQuery(self, relation):
        cursor = self.connection.cursor()
        query = 'SELECT * FROM {};'.format(relation)
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def countQuery(self, name, state, job_type):
        try:
            cursor = self.connection.cursor()
            query= """SELECT COUNT(*) FROM "public"."Bark_Client" WHERE "Name"= %s AND "State"= %s AND "Job_Type"= %s; """
            values= name, state, job_type
            cursor.execute(query, vars=values)
            result= cursor.fetchone()[0]

           # print(cursor.mogrify(query, values))
            #print(result)

            cursor.close()
        except(Exception, psycopg2.Error) as error:
            print(error)
            quit()
        return (result)

    def updateQuery(self, name, date, job_type,
                    state, phone, email, responses, urgent, credits, details, budget, attachment, mapImage, remote):
        try:
            cursor= self.connection.cursor()
            query= """UPDATE "public"."Bark_Client" SET "Date_Received"= %s, "Phone"= %s, "Email"= %s, "Responded_Professional_Number"= %s, 
            "Urgent"= %s,"Credits"= %s, "Details"= %s, "Budget"= %s, "Attachments"= %s, "Map"= %s, "Remote"= %s WHERE "Name"= %s AND "State"= %s
            AND "Job_Type"= %s;"""
            values= date, phone, email, responses, urgent, credits, details, budget, attachment, mapImage, remote, name, state,job_type
            cursor.execute(query, vars= values)
            self.connection.commit()
            cursor.close()
        except(Exception, psycopg2.Error) as error:
            print(error)
            quit()

    def insertQuery(self, name, date, job_type,
                    state, phone, email, responses, urgent, credits, details, budget, attachment, mapImage, remote):
        try:
            cursor = self.connection.cursor()
            # query = """INSERT INTO "public"."Bark_Client" ("Name", "Date_Received", "Job_Type", "State", 
            # "Phone", "Email", "Responded_Professional_Number", "Urgent", "Credits", "Details", "Budget", "Attachments", "Map", "Remote") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT ("Name","Job_Type","State") DO UPDATE SET "Responded_Professional_Number"=EXCLUDED."Responded_Professional_Number";"""
            query = """INSERT INTO "public"."Bark_Client" ("Name", "Date_Received", "Job_Type", "State", "Phone", "Email", "Responded_Professional_Number", "Urgent", "Credits", "Details", "Budget", "Attachments", "Map", "Remote") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
            vars = name, date, job_type, state, phone, email, responses, urgent, credits, details, budget, attachment, mapImage, remote
            cursor.execute(query, vars=vars)
            self.connection.commit()
            cursor.close()
        except (Exception, psycopg2.Error) as error:
            print(error)
            quit()

    def close(self):
        self.connection.close()
