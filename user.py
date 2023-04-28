import sqlite3 as sql
from portfolio import Portfolio
from string import ascii_letters

characters = ascii_letters + ' '

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
        check = False
        print('ATENTIE! Username-ul trebuie sa contina doar litere!')
        while not check:
            create_username = input("Username: ")
            check_if_exist = [user[0] for user in cursor.execute("SELECT user_login FROM users")]
            if create_username in check_if_exist:
                print("Acest username este in folosinta. Va rugam alegeti altul.")
                check = False
            elif create_username.isalpha() != True:
                print("Username-ul trebuie sa contina doar litere.")
                check = False
            else:
                check = True
                return create_username
    
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
            create_password = input("Password: ")
            if len(create_password) < 8:
                print("Parola trebuie sa contina minim 8 caractere.")
                check = False
            elif not any(char.isdigit() for char in create_password):
                print('Parola trebuie sa contina minim o cifra.')
                check = False
            elif not any(char.isupper() for char in create_password):
                print('Parola trebuie sa contina minim o majuscula.')
                check = False
            elif not any(char.islower() for char in create_password):
                print('Parola trebuie sa contina minim o minuscula.')
                check = False
            elif not any(char in SpecialChar for char in create_password):
                print('Parola trebuie sa contina minim una dintre caracterele !, %, &, $, #.')
                check = False
            else:
                check = True
                return create_password
            
    @classmethod
    def first_name(cls):
        check = False

        while not check:
            create_first_name = input('Prenume: ')
            if set(create_first_name).difference(characters):
                print('Numele trebuie sa contina doar litere.')
                check = False
            else:
                check = True
                return create_first_name
            
    @classmethod
    def last_name(cls):
        check = False

        while not check:
            create_last_name = input('Nume: ')
            if any(char.isdigit() for char in create_last_name):
                print('Numele trebuie sa contina doar litere.')
                check = False
            else:
                check = True
                return create_last_name
            
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

    def insert_user(self):
        cursor.execute("""
        INSERT INTO users (user_login, user_password, user_first_name, user_last_name, user_tag) VALUES (?, ?, ?, ?, ?)
        """, (self.username, self.password, self.first_name, self.last_name, self.tag))

        connect.commit()

    @classmethod
    def display_user(cls):
        users = [user[0] for user in cursor.execute("SELECT user_login FROM users")]
        print(users)

    @classmethod
    def initiate_login(cls):
        cursor.execute("SELECT user_login FROM users")
        results = cursor.fetchall()

        print('''
*      *****  *****  *  *   *
*      *   *  *      *  **  *
*      *   *  *  **  *  * * *
*      *   *  *   *  *  *  **
*****  *****  *****  *  *   *
        ''')
        check_username = False
        while not check_username:
            username = input('Username: ')
            x = [1 for user in results if username in user]
            if len(x) == 0:
                print("Acest username nu exista.")
                check_username = False
            else:
                check_username = True
        
        cursor.execute("SELECT user_login, user_password FROM users WHERE user_login = '{}'".format(username))
        db_password = cursor.fetchall()[0][1]
        check_password = 0
        while check_password < 3:
            password = input('Password: ')
            if password != db_password:
                check_password += 1
                print(f'Parola este gresita! Mai aveti {3-check_password} incercari.')
            else:
                check_password += 3
                cls.menu_user(username)

    @classmethod
    def menu_user(cls, user_login):
        cursor.execute("SELECT user_login, user_first_name FROM users WHERE user_login = '{}'".format(user_login))
        db_first_name = cursor.fetchall()[0][1]
        cursor.execute("SELECT user_login, user_last_name FROM users WHERE user_login = '{}'".format(user_login))
        db_last_name = cursor.fetchall()[0][1]
        db_name = db_first_name + ' ' + db_last_name

        print("""
Pentru setari cont, selectati 1.
Pentru detalii portofolii, selectati 2.
Pentru a reveni la meniul anterior, selectati 3.
""")
        menu_photographer = {
            1: User.submenu_user, #submenu user
            2: Portfolio.menu_portfolio, #submenu portfolio
        }

        option = int(input('Optiunea dumneavoastra: '))
        if option == 1:
            menu_photographer[option](user_login)
        elif option == 2:
            menu_photographer[option](db_name)
        if option == 3:
            print('Iesire submeniu...')
            return

    @classmethod
    def submenu_user(cls, user_login):
        cursor.execute("SELECT user_login, user_tag FROM users WHERE user_login = '{}'".format(user_login))
        db_tag = cursor.fetchall()[0][1]

        if db_tag == 'Fotograf':
            pass
        elif db_tag == 'Utilizator':
            pass
        elif db_tag == 'Admin':
            pass

    @classmethod
    def initiate_create(cls):
        create = User(User.username(), User.password(), User.first_name(), User.last_name(), User.tag())
        create.insert_user()

# stergere_utilizator = input("Ce utilizator doriti sa stergeti?: ")

# cursor.execute("DELETE FROM users WHERE user_login=?", (stergere_utilizator))
# connection.commit()

if __name__ == '__main__':
    # User.display_user()
    User.initiate_create()
    # User.initiate_login()