import sqlite3

class Utilizator:
    def __init__(self, username, password, tag):
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
        self.username = username
        self.password = password
        self.tag = tag

    @classmethod
    def username(cls):
        connection = sqlite3.connect('mydata.db')
        cursor = connection.cursor()
        cursor.execute("SELECT username FROM utilizatori")
        results = cursor.fetchall()

        check = False
        print('ATENTIE! Username-ul trebuie sa contina doar litere!')
        while not check:
            creare_username = input("Username: ")
            x = [1 for user in results if creare_username in user]
            if len(x) != 0:
                print("Acest username este in folosinta. Va rugam alegeti altul.")
                check = False
            elif creare_username.isalpha() != True:
                print("Username-ul trebuie sa contina doar litere.")
                check = False
            else:
                try:
                    x.pop(0)
                except IndexError:
                    pass
                check = True
                return creare_username
    
    @classmethod
    def password(cls):
        SpecialChar = ['!', '%', '&', '$', '#']

        check = False
        print('''ATENTIE! Parola trebuie sa contina:
        - minim 8 caractere.
        - minim o majuscula.
        - minim o minuscula.
        - minim o cifra
        - minim una dintre caracterele !, %, &, $, #''')
        while not check:
            creare_password = input("Password: ")
            if len(creare_password) < 8:
                print("Parola trebuie sa contina minim 8 caractere.")
                check = False
            elif not any(char.isdigit() for char in creare_password):
                print('Parola trebuie sa contina minim o cifra.')
                check = False
            elif not any(char.isupper() for char in creare_password):
                print('Parola trebuie sa contina minim o majuscula.')
                check = False
            elif not any(char.islower() for char in creare_password):
                print('Parola trebuie sa contina minim o minuscula.')
                check = False
            elif not any(char in SpecialChar for char in creare_password):
                print('Parola trebuie sa contina minim una dintre caracterele !, %, &, $, #.')
                check = False
            else:
                check = True
                return creare_password
    
    @classmethod
    def tag(cls):
        check = False

        while not check:
            creare_tag = input('In ce scop creati acest cont? [Fotograf, Utilizator]: ')
            if creare_tag not in ["Fotograf", "Utilizator"]:
                print('Va rugam selectati una din optiunile valabile [Fotograf, Utilizator].')
                check = False
            else:
                check = True
                return creare_tag

    def create_user(self):
        self.cursor.execute("""
        INSERT INTO utilizatori VALUES
        ('{}', '{}', '{}', '', '')
        """.format(self.username, self.password, self.tag))

        self.connection.commit()

    def load_user(self):
        self.cursor.execute("""
        SELECT * FROM utilizatori
        """)

        results = self.cursor.fetchall()
        print(results)
        
class Fotograf(Utilizator):
    def __init__(self, username, password, tag, first_name, last_name, age, experience):
        super(Utilizator, self).__init__(username, password, tag)
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.experience = experience
        
class Client(Utilizator):
    def __init__(self, username, password, tag, first_name, last_name):
        super(Utilizator, self).__init__(username, password, tag)
        self.first_name = first_name
        self.last_name = last_name
        
class Portfolio(Fotograf):
    def __init__(self, title, category):
        super(Fotograf, self).__init__(title)
        self.category = category

menu = {
    "Start": ['1. Login', '2. Creare cont', '3. Iesire'],
    "Admin": [],
    "Fotograf": [],
    "Utilizator": [],
}

# creare_first_name = input("Prenume: ")
# creare_last_name = input("Nume: ")

# stergere_utilizator = input("Ce utilizator doriti sa stergeti?: ")

# cursor.execute("DELETE FROM utilizatori WHERE username='{}'".format(stergere_utilizator))
# connection.commit()

if __name__ == '__main__':
    create = Utilizator(Utilizator.username(), Utilizator.password(), Utilizator.tag())
    create.create_user()
    create.load_user()