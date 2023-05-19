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

    def __init__(self):
        self.username = ''
        self.password = ''
        self.first_name = ''
        self.last_name = ''
        self.tag = 'New'

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
    def create_password():
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
    def create_first_name():
        check = False
        while not check:
            create_first_name = input('Prenume: ')
            if set(create_first_name).difference(__class__.characters):
                print('\nNumele trebuie sa contina doar litere.')
            else:
                check = True
                return create_first_name
            
    @staticmethod
    def create_last_name():
        check = False
        while not check:
            create_last_name = input('Nume: ')
            if set(create_last_name).difference(__class__.characters): 
                print('\nNumele trebuie sa contina doar litere.')
            else:
                check = True
                return create_last_name
            
    # @staticmethod
    def create_tag(self):
        options = {
            1: 'Utilizator',
            2: 'Fotograf',
            3: 'Admin'
        }
        print('Tipuri de cont:')
        if self.tag == 'New' or self.tag == 'Utilizator':
            options_filtered = {key: options[key] for key in options.keys() & {1, 2}}
            for i,j in options_filtered.items():
                print(f'    {i} -> {j}') 
        elif self.tag == 'Admin':
            for i,j in options.items():
                print(f'    {i} -> {j}')
        check = False
        while not check:
            try:
                if self.tag == 'New' or self.tag == 'Utilizator':
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
    def user_create(self):
        self.username = self.create_username()
        self.password = self.create_password()
        self.first_name = self.create_first_name()
        self.last_name = self.create_last_name()
        self.tag = self.create_tag()
        self.user_insert()

    # Trecerea utilizatorului in baza de date
    def user_insert(self):
        cursor.execute("""
        INSERT INTO users (user_login, user_password, user_first_name, user_last_name, user_tag) VALUES (?, ?, ?, ?, ?)
        """, (self.username, self.password, self.first_name, self.last_name, self.tag))
        connect.commit()
        print('\nContul a fost creat cu succes.')

    # Login utilizator
    def user_login(self):
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
                self.username = username
                self.user_menu()

    # Meniu principal dupa login
    def user_menu(self):
        while True:
            print("""
    Pentru setari cont, selectati 1.
    Pentru detalii portofolii, selectati 2.
    Pentru a reveni la meniul anterior, selectati 3.
""")
            try:
                option = int(input('Optiunea dumneavoastra: '))
                if option == 1:
                    self.user_submenu()
                elif option == 2:
                    portfolio = Portfolio()
                    portfolio.portfolio_menu(self.username)
                elif option == 3:
                    print('\nIesire submeniu...')
                    return
                else:
                    print('\nOptiunea selectata nu este valida.')
            except ValueError:
                print(self.valoare_invalida)

    # Submeniu utilizator
    def user_submenu(self):
        cursor.execute(f"SELECT user_tag FROM users WHERE user_login = '{self.username}'")
        self.tag = cursor.fetchone()[0]

        while True:
            if self.tag in ['Utilizator', 'Fotograf']: 
                print("""
    Pentru a vizualiza detaliile contului dumneavoastra, selectati 1.
    Pentru a schimba parola, selectati 2.
    Pentru a schimba numele, selectati 3.
    Pentru a schimba tipul de utilizator, selectati 4.        
    Pentru a reveni la meniul anterior, selectati 5.
""")
                sub_menu = {
                    1: self.user_details,
                    2: self.change_password,
                    3: self.change_name,
                    4: self.change_tag
                }
                try:
                    option = int(input('Optiunea dumneavoastra: '))
                    if option in range(1,5):
                        sub_menu[option]()
                    elif option == 5:
                        print('\nIesire submeniu...')
                        return
                    else:
                        print('\nOptiunea selectata nu este valida.')    
                except ValueError:
                    print(cls.valoare_invalida)

            elif self.tag == 'Admin':
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
                    1: self.user_details,
                    2: self.change_password,
                    3: self.change_name,
                    4: self.display_users,
                    5: self.user_delete,
                    6: self.user_create
                }
                try:
                    option = int(input('Optiunea dumneavoastra: '))
                    if option in range(1, 7):
                        sub_menu[option]()
                    elif option == 7:
                        print('\nIesire submeniu...')
                        return
                    else:
                        print('\nOptiunea selectata nu este valida.')
                except ValueError:
                    print(cls.valoare_invalida)

    # Detaliile contului
    def user_details(self):
        cursor.execute(f"SELECT user_first_name, user_last_name, user_tag FROM users WHERE user_login = '{self.username}'")
        detail = cursor.fetchone()
        print(f"""
    Nume de utilizator: {self.username}
    Prenume: {detail[0]}
    Nume: {detail[1]}
    Tip de utilizator: {detail[2]}
""")
    
    # Setari cont
    def change_password(self):
        print("""
    *******************
    * RESETARE PAROLA *
    *******************
""")
        cursor.execute("UPDATE users SET user_password = ? WHERE user_login = ?", (self.create_password(), self.username))
        connect.commit()
        print('\nParola a fost actualizata.')

    def change_name(self):
        while True:
            try:
                option = int(input("""
    Pentru schimbare "nume", selectati 1.
    Pentru schimbare "prenume", selectati 2.
    Pentru anulare, selectati 3.

Optiunea dumneavoastra: """))
                if option == 1:
                    cursor.execute("UPDATE users SET user_last_name = ? WHERE user_login = ?", (self.create_last_name(), self.username))
                elif option == 2:
                    cursor.execute("UPDATE users SET user_first_name = ? WHERE user_login = ?", (self.create_first_name(), self.username))
                elif option == 3:
                    print('\nAnulare...')
                    return
                else:
                    print('\nOptiunea selectata nu este valida.')
            except ValueError:
                print(self.valoare_invalida)
            cursor.execute(f"SELECT user_first_name, user_last_name FROM users WHERE user_login = '{self.username}'")
            db_name_t = cursor.fetchone()
            name = db_name_t[0] + ' ' + db_name_t[1]
            cursor.execute("UPDATE portfolios SET portfolio_photographer_name = ? WHERE portfolio_username = ?", (name, self.username))
            connect.commit()
            print('\nNumele a fost actualizat.')

    def change_tag(self):
        print("""
    *****************
    * SCHIMBARE TAG *
    *****************
""")
        cursor.execute("UPDATE users SET user_tag = ? WHERE user_login = ?", (self.create_tag(), self.username))
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
    test = User()
    # test.user_create()
    test.user_login()
    pass