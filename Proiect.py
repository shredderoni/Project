import sqlite3

class Utilizator:
    def __init__(self, username, password, tag):
        self.username = username
        self.password = password
        self.tag = tag

        self.connection = sqlite3.connect('mydata.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS utilizatori (
            username TEXT PRIMARY KEY,
            password VARCHAR(15) NOT NULL,
            tag TEXT,
            first_name TEXT,
            last_name TEXT
        )
        """)
        
    def create_user(self):
        self.cursor.execute("""
        INSERT INTO utilizatori VALUES
        ('{}', '{}', '{}', '', '')
        """.format(self.username, self.password, self.tag))

        self.connection.commit()
        self.connection.close()

    def load_user(self):
        self.cursor.execute("""
        SELECT * FROM utilizatori
        """)

        results = self.cursor.fetchone()

        self.tag = results[2]
        self.first = results[3]
        self.last = results[4]
        
class Fotograf(Utilizator):
    def __init__(self, username, password, tag, first_name, last_name, age, experience):
        super(Utilizator, self).__init__(username, password, tag)
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.experience = experience
        
class Client(Utilizator):
    def __init__(self, username, password, tag, first_name, last_name):
        super(Utilizator, self).__init__(username, password, tag, first_name, last_name)
        
class Portfolio(Fotograf):
    def __init__(self, name, category):
        super(Fotograf, self).__init__(name)
        self.category = category

# Check if user can be created
def check_username(cursor):
    global creare_username

    cursor.execute("SELECT username FROM utilizatori")
    results = cursor.fetchall()

    while True:
        x = [1 for user in results if creare_username in user]
        if len(x) != 0:
            print("Acest username este in folosinta. Va rugam alegeti altul.")
            creare_username = input("Username: ")
        elif creare_username.isalpha() != True:
            print("Username-ul trebuie sa contina doar litere.")
            creare_username = input("Username: ")
        else:
            try:
                x.pop(0)
            except IndexError:
                pass
            break

# Check if password is valid
def check_password(password):

    SpecialChar = ['!', '%', '&', '$', '#']

    if len(password) < 8:
        print("Parola trebuie sa contina minim 8 caractere.")
        return False
    elif not any(char.isdigit() for char in password):
        print('Parola trebuie sa contina minim o cifra.')
        return False
    elif not any(char.isupper() for char in password):
        print('Parola trebuie sa contina minim o majuscula.')
        return False
    elif not any(char.islower() for char in password):
        print('Parola trebuie sa contina minim o minuscula.')
        return False
    elif not any(char in SpecialChar for char in password):
        print('Parola trebuie sa contina minim una dintre caracterele !, %, &, $, #.')
        return False
    else:
        return True

# Testing function
def fetch_users(cursor):
    cursor.execute("SELECT * FROM utilizatori")
    results = cursor.fetchall()
    print(results)

menu = {
    "Start": ['1. Login', '2. Creare cont', '3. Iesire'],
    "Admin": [],
    "Fotograf": [],
    "Utilizator": [],
}

connection = sqlite3.connect('mydata.db')
cursor = connection.cursor()

# # Create username and check if it meets requirements
# creare_username = input('''ATENTIE! Username-ul trebuie sa contina doar litere!
# Username: ''')
# check_username(cursor)

# # Create password and check if it meets requirements
# creare_password = input('''ATENTIE! Parola trebuie sa contina:
# - minim 8 caractere.
# - minim o majuscula.
# - minim o minuscula.
# - minim o cifra
# - minim una dintre caracterele !, %, &, $, #
# Password: ''')
# while not check_password(creare_password):
#     creare_password = input("Password: ")

# # What type of user is being created?
# while True:
#     try:
#         creare_tag = input("In ce scop creati acest cont? [Fotograf, Utilizator]: ")
#         assert creare_tag in ["Fotograf", "Utilizator"], "Va rugam selectati una din optiunile valabile [Fotograf, Utilizator]."
#         if creare_tag in ['Fotograf', 'Utilizator']:
#             break
#     except AssertionError as ae:
#         print(ae)

# creare_first_name = input("Prenume: ")
# creare_last_name = input("Nume: ")

# account = Utilizator(creare_username, creare_password, creare_tag)
# account.create_user()

# fetch_users(cursor)

# stergere_utilizator = input("Ce utilizator doriti sa stergeti?: ")

# cursor.execute("DELETE FROM utilizatori WHERE username='{}'".format(stergere_utilizator))
# connection.commit()

# fetch_users(cursor)

connection.close()