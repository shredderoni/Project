import sqlite3 as sql
from portfolio import Portfolio
from string import ascii_letters

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
    characters = ascii_letters + ' '
    valoare_invalida = """
* *  ********************************  * *
 *   Ati introdus o valoare invalida!   *
* *  ********************************  * *
"""

    def __init__(self, username, password, first_name, last_name, tag):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.tag = tag

    # Date pentru crearea utilizatorului
    @staticmethod
    def username():
        print('ATENTIE! Username-ul trebuie sa contina doar litere!')
        check = False
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
        print('''ATENTIE! Parola trebuie sa contina:
        - minim 8 caractere.
        - minim o majuscula.
        - minim o minuscula.
        - minim o cifra
        - minim unul dintre caracterele !, %, &, $, #''')

        check = False
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
            if set(create_first_name).difference(__class__.characters):
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
            if set(create_last_name).difference(__class__.characters): 
                print('Numele trebuie sa contina doar litere.')
                check = False
            else:
                check = True
                return create_last_name
            
    @staticmethod
    def tag(state):
        options = {
            1: 'Utilizator',
            2: 'Fotograf',
            3: 'Admin'
        }
        print('Tipuri de cont:')
        if state == 'New' or state == 'Utilizator':
            options_filtered = {key: options[key] for key in options.keys() & {1, 2}}
            for i,j in options_filtered.items():
                print(f'    {i} -> {j}') 
        elif state == 'Admin':
            for i,j in options.items():
                print(f'    {i} -> {j}')
        check = False
        while not check:
            try:
                creare_tag = int(input('\nIn ce scop creati acest cont? (numarul tipului, de ex. 1): '))
                if creare_tag not in range(1,4): 
                    print('Va rugam selectati una din optiunile valabile.')
                    check = False
                else:
                    check = True
                    return options[creare_tag]
            except ValueError:
                print(__class__.valoare_invalida)

    # Trecerea utilizatorului in baza de date
    def insert_user(self):
        cursor.execute("""
        INSERT INTO users (user_login, user_password, user_first_name, user_last_name, user_tag) VALUES (?, ?, ?, ?, ?)
        """, (self.username, self.password, self.first_name, self.last_name, self.tag))
        connect.commit()
        print('Contul a fost creat cu succes.')

    # Creare utilizator
    @staticmethod
    def initiate_create(state):
        create = User(User.username(), User.password(), User.first_name(), User.last_name(), User.tag(state))
        create.insert_user()

    # Login utilizator
    @classmethod
    def initiate_login(cls):
        print("""
    *********
    * LOGIN *
    *********
""")

        check_username = False
        while not check_username:
            username = input('Username: ')
            check_if_exist = [user[0] for user in cursor.execute("SELECT user_login FROM users")]
            if username not in check_if_exist: 
                print("Acest utilizator nu exista.")
                check_username = False
            else:
                check_username = True
        cursor.execute("SELECT user_password FROM users WHERE user_login = '{}'".format(username))
        db_password = cursor.fetchone()[0]
        check_password = 0
        while check_password < 3:
            password = input('Password: ')
            if password != db_password:
                check_password += 1
                print(f'Parola este gresita! Mai aveti {3-check_password} incercari.')
            else:
                check_password += 3
                cls.menu_user(username)
        print('V-ati logat cu succes!')

    # Meniu principal dupa login
    @classmethod
    def menu_user(cls, username):
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
            try:
                option = int(input('Optiunea dumneavoastra: '))
                if option == 1 or option == 2:
                    main_menu[option](username)
                elif option == 3:
                    print('Iesire submeniu...')
                    return
                else:
                    print('Optiunea selectata nu este valida.')
            except ValueError:
                print(cls.valoare_invalida)

    # Submeniu utilizator
    @classmethod
    def submenu_user(cls, username):
        cursor.execute("SELECT user_tag FROM users WHERE user_login = '{}'".format(username))
        db_tag = cursor.fetchone()[0]

        while True:
            if db_tag == 'Fotograf' or db_tag == 'Utilizator':
                print("""
    Pentru a vizualiza detaliile contului dumneavoastra, selectati 1.
    Pentru a schimba parola, selectati 2.
    Pentru a schimba numele, selectati 3.
    Pentru a schimba tipul de utilizator, selectati 4.        
    Pentru a reveni la meniul anterior, selectati 5.
    """)
                sub_menu = {
                    1: User.details_user,
                    2: User.change_password,
                    3: User.change_name,
                    4: User.change_tag
                }
                try:
                    option = int(input('Optiunea dumneavoastra: '))
                    if option in range(1,4):
                        sub_menu[option](username)
                    elif option == 4:
                        sub_menu[option]('Utilizator')
                    elif option == 5:
                        print('Iesire submeniu...')
                        return
                    else:
                        print('Optiunea selectata nu este valida.')    
                except ValueError:
                    print(cls.valoare_invalida)

            elif db_tag == 'Admin':
                print("""
    Pentru a vizualiza detaliile contului dumneavoastra, selectati 1.
    Pentru a schimba parola, selectati 2.
    Pentru a schimba numele, selectati 3.
    Pentru a vizualiza toti utilizatorii, selectati 4.
    Pentru a sterge un utilizator, selectati 5. 
    Pentru a crea un utilizator, selectati 6.
    Pentru a reveni la meniul anterior, selectati 7.
    """)
                sub_menu = {
                    1: User.details_user,
                    2: User.change_password,
                    3: User.change_name,
                    4: User.display_users,
                    5: User.delete_user,
                    6: User.initiate_create
                }
                try:
                    option = int(input('Optiunea dumneavoastra: '))
                    if option in range(1, 4):
                        sub_menu[option](username)
                    elif option in range(4, 6):
                        sub_menu[option]()
                    elif option == 6:
                        sub_menu[option]('Admin')
                    elif option == 7:
                        print('Iesire submeniu...')
                        return
                    else:
                        print('Optiunea selectata nu este valida.')
                except ValueError:
                    print(cls.valoare_invalida)

    # Detaliile contului
    @staticmethod
    def details_user(username):
        cursor.execute("SELECT user_first_name, user_last_name, user_tag FROM users WHERE user_login = '{}'".format(username))
        detail = cursor.fetchone()
        print(f"""
    Nume de utilizator: {username}
    Prenume: {detail[0]}
    Nume: {detail[1]}
    Tip de utilizator: {detail[2]}
""")
    
    # Account settings
    @classmethod
    def change_password(cls, username):
        print("""
    *******************
    * RESETARE PAROLA *
    *******************
""")
        cursor.execute("UPDATE users SET user_password = ? WHERE user_login = ?", (User.password(), username))
        connect.commit()
        print('Parola a fost actualizata.')

    @classmethod
    def change_name(cls, username):
        while True:
            try:
                option = int(input("""
            Pentru schimbare "nume", selectati 1.
            Pentru schimbare "prenume", selectati 2.
            Pentru anulare, selectati 3.
        Optiune: """))
                if option == 1:
                    cursor.execute("UPDATE users SET user_last_name = ? WHERE user_login = ?", (User.last_name(), username))
                elif option == 2:
                    cursor.execute("UPDATE users SET user_first_name = ? WHERE user_login = ?", (User.first_name(), username))
                elif option == 3:
                    print('Anulare...')
                    return
                else:
                    print('Optiunea selectata nu este valida.')
            except ValueError:
                print(cls.valoare_invalida)
            connect.commit()
            print('Numele a fost actualizat.')

    @classmethod
    def change_tag(cls, username):
        print("""
    *****************
    * SCHIMBARE TAG *
    *****************
""")
        cursor.execute("UPDATE users SET user_tag = ? WHERE user_login = ?", (User.tag('Utilizator'), username))
        connect.commit()
        print('Tipul contului a fost actualizat.')

    # Functii admin
    # Afisare utilizatori
    @staticmethod
    def display_users():
        ids = [user[0] for user in cursor.execute("SELECT user_id FROM users")]
        users = [user[0] for user in cursor.execute("SELECT user_login FROM users")]
        for id, user in zip(ids, users):
            print(f'Id: {id} -> Username: {user}')
                
    # Stergere utilizator
    @staticmethod
    def delete_user():
        User.display_users()

        check = False
        while not check:
            try:
                option = int(input('Ce utilizator doriti sa stergeti? (Id, de ex "2"): '))
                check_if_exist = [user[0] for user in cursor.execute("SELECT user_id FROM users")]
                if option not in check_if_exist:
                    print("Acest utilizator nu exista.")
                    check = False
                else:
                    check = True
                    cursor.execute("DELETE FROM users WHERE user_id = {}".format(option))
                    connect.commit()
                    return
            except ValueError:
                print(__class__.valoare_invalida)


if __name__ == '__main__':
    User.menu_user('ssilviu')