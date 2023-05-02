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

    # Date pentru crearea utilizatorului
    @staticmethod
    def username():
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
    
    @staticmethod
    def password():
        SpecialChar = ['!', '%', '&', '$', '#']

        check = False
        print('''ATENTIE! Parola trebuie sa contina:
        - minim 8 caractere.
        - minim o majuscula.
        - minim o minuscula.
        - minim o cifra
        - minim unul dintre caracterele !, %, &, $, #''')
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
                print('Parola trebuie sa contina minim unul dintre caracterele !, %, &, $, #.')
                check = False
            else:
                check = True
                return create_password
            
    @staticmethod
    def first_name():
        check = False

        while not check:
            create_first_name = input('Prenume: ')
            if set(create_first_name).difference(characters):
                print('Numele trebuie sa contina doar litere.')
                check = False
            else:
                check = True
                return create_first_name
            
    @staticmethod
    def last_name():
        check = False

        while not check:
            create_last_name = input('Nume: ')
            if any(char.isdigit() for char in create_last_name):
                print('Numele trebuie sa contina doar litere.')
                check = False
            else:
                check = True
                return create_last_name
            
    @staticmethod
    def tag():
        check = False

        while not check:
            creare_tag = input('In ce scop creati acest cont? [Fotograf, Utilizator]: ')
            if creare_tag not in ["Fotograf", "Utilizator"]:
                print('Va rugam selectati una din optiunile valabile [Fotograf, Utilizator].')
                check = False
            else:
                check = True
                return creare_tag

    # Trecerea utilizatorului in baza de date
    def insert_user(self):
        cursor.execute("""
        INSERT INTO users (user_login, user_password, user_first_name, user_last_name, user_tag) VALUES (?, ?, ?, ?, ?)
        """, (self.username, self.password, self.first_name, self.last_name, self.tag))

        connect.commit()


    # Login utilizator
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

    # Meniu principal dupa login
    @classmethod
    def menu_user(cls, user_login):
        cursor.execute("SELECT user_login, user_first_name FROM users WHERE user_login = '{}'".format(user_login))
        db_first_name = cursor.fetchall()[0][1]
        cursor.execute("SELECT user_login, user_last_name FROM users WHERE user_login = '{}'".format(user_login))
        db_last_name = cursor.fetchall()[0][1]
        db_name = db_first_name + ' ' + db_last_name

        main_menu = {
            1: User.submenu_user, #submenu user
            2: Portfolio.menu_portfolio, #submenu portfolio
        }

        while True:
            print("""
    Pentru setari cont, selectati 1.
    Pentru detalii portofolii, selectati 2.
    Pentru a reveni la meniul anterior, selectati 3.
""")
            option = int(input('Optiunea dumneavoastra: '))
            if option == 1:
                main_menu[option](user_login)
            elif option == 2:
                main_menu[option](db_name)
            elif option == 3:
                print('Iesire submeniu...')
                return
            else:
                print('Optiunea selectata nu este valida.')

    # Submeniu utilizator
    @classmethod
    def submenu_user(cls, user_login):
        cursor.execute("SELECT user_login, user_tag FROM users WHERE user_login = '{}'".format(user_login))
        db_tag = cursor.fetchall()[0][1]

        while True:
            if db_tag == 'Fotograf' or db_tag == 'Utilizator':
                print("""
    Pentru a schimba parola, selectati 1.
    Pentru a schimba tipul de utilizator, selectati 2.        
    Pentru a schimba numele, selectati 3.
    Pentru a reveni la meniul anterior, selectati 4.
    """)
                sub_menu = {
                    1: User.change_password,
                    2: User.change_tag,
                    3: User.change_name
                }
                option = int(input('Optiunea dumneavoastra: '))
                if option == 4:
                    print('Iesire submeniu...')
                    return
                elif option not in range(1, 5):
                    print('Optiunea selectata nu este valida.')    
                sub_menu[option](user_login)
            elif db_tag == 'Admin':
                print("""
    Pentru a schimba parola, selectati 1.
    Pentru a schimba numele, selectati 2.
    Pentru a vizualiza toti utilizatorii, selectati 3.
    Pentru a sterge un utilizator, selectati 4. 
    Pentru a crea un utilizator, selectati 5.
    Pentru a reveni la meniul anterior, selectati 6.
    """)
                sub_menu = {
                    1: User.change_password,
                    2: User.change_name,
                    3: User.display_user,
                    4: User.delete_user,
                    5: ''
                }
                option = int(input('Optiunea dumneavoastra: '))
                if option in range(1, 3):
                    sub_menu[option](user_login)
                elif option in range(3, 6):
                    sub_menu[option]()
                elif option == 6:
                    print('Iesire submeniu...')
                    return
                else:
                    print('Optiunea selectata nu este valida.')
    
    # Account settings
    @classmethod
    def change_password(cls, user_login):
        print("""
*****  *****  *****  *****  *****    *    *****  *****    *****    *    *****  *****  *        *
*   *  *      *      *        *     * *   *   *  *        *   *   * *   *   *  *   *  *       * *
*****  *****  *****  *****    *    *****  *****  *****    *****  *****  *****  *   *  *      *****
*  *   *          *  *        *    *   *  *  *   *        *      *   *  *  *   *   *  *      *   *
*   *  *****  *****  *****    *    *   *  *   *  *****    *      *   *  *   *  *****  *****  *   *
""")
        cursor.execute("UPDATE users SET user_password = ? WHERE user_login = ?", (User.password(), user_login))
        connect.commit()
        
    @classmethod
    def change_tag(cls, user_login):
        print("""
*****  *****  *****  *****  *****    *    *****  *****    *****    *    *****
*   *  *      *      *        *     * *   *   *  *          *    *   *  *    
*****  *****  *****  *****    *    *****  *****  *****      *    *****  *  **
*  *   *          *  *        *    *   *  *  *   *          *    *   *  *   *
*   *  *****  *****  *****    *    *   *  *   *  *****      *    *   *  *****
""")
        cursor.execute("UPDATE users SET user_tag = ? WHERE user_login = ?", (User.tag(), user_login))
        connect.commit()

    @classmethod
    def change_name(cls, user_login):
        option = int(input("""
    Pentru schimbare "nume", selectati 1.
    Pentru schimbare "prenume", selectati 2.
    Pentru anulare, selectati 3.
Optiune: """))
        if option == 1:
            cursor.execute("UPDATE users SET user_last_name = ? WHERE user_login = ?", (User.last_name(), user_login))
        elif option == 2:
            cursor.execute("UPDATE users SET user_first_name = ? WHERE user_login = ?", (User.first_name(), user_login))
        else:
            print('Anulare...')
            return
        connect.commit()

    # Functii admin
    # Afisare utilizatori
    @staticmethod
    def display_user():
        users = [user for user in cursor.execute("SELECT user_id, user_login FROM users")]
        print(users)

    @staticmethod
    def delete_user():
        User.display_user()

        check = False
        while not check:
            option = int(input('Ce utilizator doriti sa stergeti? (user_id, de ex "2"): '))
            check_if_exist = [user[0] for user in cursor.execute("SELECT user_id FROM users")]
            if option not in check_if_exist:
                print("Acest utilizator nu exista.")
                check = False
            else:
                check = True
                cursor.execute("DELETE FROM users WHERE user_id = {}".format(option))
                connect.commit()

    @staticmethod
    def initiate_create():
        create = User(User.username(), User.password(), User.first_name(), User.last_name(), User.tag())
        create.insert_user()

# stergere_utilizator = input("Ce utilizator doriti sa stergeti?: ")

# cursor.execute("DELETE FROM users WHERE user_login=?", (stergere_utilizator))
# connection.commit()

if __name__ == '__main__':
    # User.display_user()
#    User.initiate_create()
    # User.initiate_login()
#    User.change_password('soptr')
#    User.change_tag('soptr')
#    User.change_name('soptr')
    User.delete_user()