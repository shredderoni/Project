import sqlite3 as sql
import bcrypt
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
    def create_username():
        print('ATENTIE! Username-ul trebuie sa contina doar litere!')
        while True:
            create_username = input("Username: ")
            check_if_exist = [user[0] for user in cursor.execute("SELECT user_login FROM users")]
            if create_username in check_if_exist:
                print("\nAcest username este in folosinta. Va rugam alegeti altul.")
            elif create_username.isalpha() != True:
                print("\nUsername-ul trebuie sa contina doar litere.")
            else:
                return create_username
    
    @staticmethod
    def password():
        SpecialChar = ['!', '%', '&', '$', '#']
        print("""ATENTIE! Parola trebuie sa contina:
        - minim 8 caractere.
        - minim o majuscula.
        - minim o minuscula.
        - minim o cifra
        - minim unul dintre caracterele !, %, &, $, #
""")

        while True:
            create_password = input("Password: ")
            if len(create_password) < 8:
                print("\nParola trebuie sa contina minim 8 caractere.")
            elif not any(char.isdigit() for char in create_password):
                print('\nParola trebuie sa contina minim o cifra.')
            elif not any(char.isupper() for char in create_password):
                print('\nParola trebuie sa contina minim o majuscula.')
            elif not any(char.islower() for char in create_password):
                print('\nParola trebuie sa contina minim o minuscula.')
            elif not any(char in SpecialChar for char in create_password):
                print('\nParola trebuie sa contina minim unul dintre caracterele !, %, &, $, #.')
            else:
                encodedPw = create_password.encode('utf-8')
                saltGen = bcrypt.gensalt()
                hashedPw = bcrypt.hashpw(encodedPw, saltGen)
                return hashedPw
            
    @staticmethod
    def first_name():
        check = False
        while not check:
            create_first_name = input('Prenume: ')
            if set(create_first_name).difference(__class__.characters):
                print('\nNumele trebuie sa contina doar litere.')
            else:
                check = True
                return create_first_name
            
    @staticmethod
    def last_name():
        check = False
        while not check:
            create_last_name = input('Nume: ')
            if set(create_last_name).difference(__class__.characters): 
                print('\nNumele trebuie sa contina doar litere.')
            else:
                check = True
                return create_last_name
            
    @staticmethod
    def create_tag(state):
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
                if state == 'New' or state == 'Utilizator':
                        creare_tag = int(input('\nIn ce scop creati acest cont? (numarul tipului, de ex. 1): '))
                        if creare_tag not in range(1,3):
                            print('\nVa rugam selectati una din optiunile valabile.')
                        else:
                            check = True
                            return options[creare_tag]
                else:
                        creare_tag = int(input('\nIn ce scop creati acest cont? (numarul tipului, de ex. 1): '))
                        if creare_tag not in range(1,4): 
                            print('\nVa rugam selectati una din optiunile valabile.')
                        else:
                            check = True
                            return options[creare_tag]
            except ValueError:
                print(__class__.valoare_invalida)

    # Creare utilizator
    @staticmethod
    def user_create(state):
        create = User(User.create_username(), User.password(), User.first_name(), User.last_name(), User.create_tag(state))
        create.user_insert()

    # Trecerea utilizatorului in baza de date
    def user_insert(self):
        cursor.execute("""
        INSERT INTO users (user_login, user_password, user_first_name, user_last_name, user_tag) VALUES (?, ?, ?, ?, ?)
        """, (self.username, self.password, self.first_name, self.last_name, self.tag))
        connect.commit()
        print('\nContul a fost creat cu succes.')

    # Login utilizator
    @classmethod
    def user_login(cls):
        print("""
    *********
    * LOGIN *
    *********
""")
        while True:
            username = input('\nUsername: ')
            check_if_exist = [user[0] for user in cursor.execute("SELECT user_login FROM users")]
            if username not in check_if_exist: 
                print("\nAcest utilizator nu exista.")
            else:
                break
        cursor.execute("SELECT user_password FROM users WHERE user_login = '{}'".format(username))
        db_password = cursor.fetchone()[0]
        check_password = 0
        while check_password < 3:
            password = input('Password: ')
            password = password.encode('utf-8')
            verify_password = bcrypt.checkpw(password, db_password)
            if not verify_password:
                check_password += 1
                print(f'Parola este gresita! Mai aveti {3-check_password} incercari.')
            else:
                check_password += 3
                print('\nV-ati logat cu succes!')
                cls.username = username
                cls.user_menu()

    # Meniu principal dupa login
    @classmethod
    def user_menu(cls):
        main_menu = {
            1: cls.user_submenu,
            2: Portfolio.portfolio_menu,
        }

        while True:
            print("""
    Pentru setari cont, selectati 1.
    Pentru detalii portofolii, selectati 2.
    Pentru a reveni la meniul anterior, selectati 3.
""")
            try:
                option = int(input('Optiunea dumneavoastra: '))
                if option == 1:
                    main_menu[option]()
                elif option == 2:
                    main_menu[option](cls.username)
                elif option == 3:
                    print('\nIesire submeniu...')
                    return
                else:
                    print('\nOptiunea selectata nu este valida.')
            except ValueError:
                print(cls.valoare_invalida)

    # Submeniu utilizator
    @classmethod
    def user_submenu(cls):
        cursor.execute(f"SELECT user_tag FROM users WHERE user_login = '{cls.username}'")
        cls.tag = cursor.fetchone()[0]

        while True:
            if cls.tag in ['Utilizator', 'Fotograf']: 
                print("""
    Pentru a vizualiza detaliile contului dumneavoastra, selectati 1.
    Pentru a schimba parola, selectati 2.
    Pentru a schimba numele, selectati 3.
    Pentru a schimba tipul de utilizator, selectati 4.        
    Pentru a reveni la meniul anterior, selectati 5.
""")
                sub_menu = {
                    1: cls.user_details,
                    2: cls.change_password,
                    3: cls.change_name,
                    4: cls.change_tag
                }
                try:
                    option = int(input('Optiunea dumneavoastra: '))
                    if option in range(1,4):
                        sub_menu[option]()
                    elif option == 4:
                        sub_menu[option]('Utilizator')
                    elif option == 5:
                        print('\nIesire submeniu...')
                        return
                    else:
                        print('\nOptiunea selectata nu este valida.')    
                except ValueError:
                    print(cls.valoare_invalida)

            elif cls.tag == 'Admin':
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
                    1: cls.user_details,
                    2: cls.change_password,
                    3: cls.change_name,
                    4: cls.display_users,
                    5: cls.user_delete,
                    6: cls.user_create
                }
                try:
                    option = int(input('Optiunea dumneavoastra: '))
                    if option in range(1, 6):
                        sub_menu[option]()
                    elif option == 6:
                        sub_menu[option]('Admin')
                    elif option == 7:
                        print('\nIesire submeniu...')
                        return
                    else:
                        print('\nOptiunea selectata nu este valida.')
                except ValueError:
                    print(cls.valoare_invalida)

    # Detaliile contului
    @classmethod
    def user_details(cls):
        cursor.execute(f"SELECT user_first_name, user_last_name, user_tag FROM users WHERE user_login = '{cls.username}'")
        detail = cursor.fetchone()
        print(f"""
    Nume de utilizator: {cls.username}
    Prenume: {detail[0]}
    Nume: {detail[1]}
    Tip de utilizator: {detail[2]}
""")
    
    # Setari cont
    @classmethod
    def change_password(cls):
        print("""
    *******************
    * RESETARE PAROLA *
    *******************
""")
        cursor.execute("UPDATE users SET user_password = ? WHERE user_login = ?", (User.password(), cls.username))
        connect.commit()
        print('\nParola a fost actualizata.')

    @classmethod
    def change_name(cls):
        while True:
            try:
                option = int(input("""
    Pentru schimbare "nume", selectati 1.
    Pentru schimbare "prenume", selectati 2.
    Pentru anulare, selectati 3.

Optiunea dumneavoastra: """))
                if option == 1:
                    cursor.execute("UPDATE users SET user_last_name = ? WHERE user_login = ?", (User.last_name(), cls.username))
                elif option == 2:
                    cursor.execute("UPDATE users SET user_first_name = ? WHERE user_login = ?", (User.first_name(), cls.username))
                elif option == 3:
                    print('\nAnulare...')
                    return
                else:
                    print('\nOptiunea selectata nu este valida.')
            except ValueError:
                print(cls.valoare_invalida)
            cursor.execute(f"SELECT user_first_name, user_last_name FROM users WHERE user_login = '{cls.username}'")
            db_name_t = cursor.fetchone()
            name = db_name_t[0] + ' ' + db_name_t[1]
            cursor.execute("UPDATE portfolios SET portfolio_photographer_name = ? WHERE portfolio_username = ?", (name, cls.username))
            connect.commit()
            print('\nNumele a fost actualizat.')

    @classmethod
    def change_tag(cls, state):
        print("""
    *****************
    * SCHIMBARE TAG *
    *****************
""")
        cursor.execute("UPDATE users SET user_tag = ? WHERE user_login = ?", (cls.create_tag(state), cls.username))
        connect.commit()
        print('\nTipul contului a fost actualizat.')

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
    def user_delete():
        User.display_users()

        check = False
        while not check:
            try:
                option = int(input('Ce utilizator doriti sa stergeti? (Id, de ex "2"): '))
                check_if_exist = [user[0] for user in cursor.execute("SELECT user_id FROM users")]
                if option not in check_if_exist:
                    print("Acest utilizator nu exista.")
                else:
                    check = True
                    cursor.execute("DELETE FROM users WHERE user_id = {}".format(option))
                    connect.commit()
                    return
            except ValueError:
                print(__class__.valoare_invalida)


if __name__ == '__main__':
    User.user_menu('testclient')
    pass