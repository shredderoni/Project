import sqlite3 as sql

connect = sql.connect("data.db")
cursor = connect.cursor()
cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_login NVARCHAR(60) NOT NULL,
            user_password NVARCHAR(60) NOT NULL,
            user_first_name NVARCHAR(60),
            user_last_name NVARCHAR(60),
            user_tag NVARCHAR(60)
        )
        """)

class User:
    def __init__(self, username, password, first_name, last_name, tag):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.tag = tag

    @classmethod
    def username(cls):
        cursor.execute("SELECT user_login FROM users")
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
    def first_name(cls):
        check = False

        while not check:
            creare_first_name = input('Prenume: ')
            if not creare_first_name.isalpha():
                print('Numele trebuie sa contina doar litere.')
                check = False
            else:
                check = True
                return creare_first_name
            
    @classmethod
    def last_name(cls):
        check = False

        while not check:
            creare_last_name = input('Nume: ')
            if not creare_last_name.isalpha():
                print('Numele trebuie sa contina doar litere.')
                check = False
            else:
                check = True
                return creare_last_name
            
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
        cursor.execute("""
        INSERT INTO users (user_login, user_password, user_first_name, user_last_name, user_tag) VALUES (?, ?, ?, ?, ?)
        """, (self.username, self.password, self.first_name, self.last_name, self.tag))

        connect.commit()

    def load_user(self):
        cursor.execute("""
        SELECT * FROM users
        """)

        results = cursor.fetchall()
        print(results)

    @classmethod
    def initiate(cls):
        create = User(User.username(), User.password(), User.first_name(), User.last_name(), User.tag())
        create.create_user()

# stergere_utilizator = input("Ce utilizator doriti sa stergeti?: ")

# cursor.execute("DELETE FROM users WHERE user_login=?", (stergere_utilizator))
# connection.commit()

if __name__ == '__main__':
    # User('', '', '', '', '')
    create = User(User.username(), User.password(), User.first_name(), User.last_name(), User.tag())
    create.create_user()
    create.load_user()