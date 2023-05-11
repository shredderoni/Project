import sqlite3 as sql
from PIL import Image
from string import ascii_letters

connect = sql.connect("data.db")
cursor = connect.cursor()
cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolios (
            portfolio_id INTEGER PRIMARY KEY AUTOINCREMENT,
            portfolio_title NVARCHAR(60),
            portfolio_category NVARCHAR(60),
            portfolio_photographer_name NVARCHAR(160),
            portfolio_username NVARCHAR(60)
        )
        """)
# FOREIGN KEY (portfolio_photographer_id) REFERENCES users (user_id)

class Portfolio:
    characters = ascii_letters + ' '
    valoare_invalida = """
* *  ********************************  * *
 *   Ati introdus o valoare invalida!   *
* *  ********************************  * *
"""
    def __init__(self, title, category, name, username):
        self.title = title
        self.category = category
        self.name = name
        self.username = username
    
    # Date pentru portofoliu si inserare in baza de date
    @staticmethod
    def title():
        check = False
        while not check:
            portfolio_title = input("Selectati un nume pentru portofoliul dumneavoastra: ")
            if set(portfolio_title).difference(__class__.characters):
                print('Numele portofoliului trebuie sa contina doar litere.')
            else:
                check = True
                return portfolio_title
            
    @staticmethod
    def category():
        category_list = {
            1: 'Landscape',
            2: 'Portrait',
            3: 'Nature',
            4: 'Animals',
            5: 'Street',
            6: 'B&W',
            7: 'Other'
        }
        for i,j in category_list.items():
            print(f'Nr.{i} -> {j}')
        check = False
        while not check:
            try:
                portfolio_category = int(input("Selectati o categorie pentru portofoliul dumneavoastra: "))
                if portfolio_category not in category_list.keys():
                    print('Categoria selectata nu este disponibila.')
                else:
                    check = True
                    return category_list[portfolio_category]
            except ValueError:
                print(__class__.valoare_invalida)

    @staticmethod
    def name(username):
        cursor.execute(f"SELECT user_first_name, user_last_name FROM users WHERE user_login = '{username}'")
        db_name_t = cursor.fetchone()
        return db_name_t[1] + ' ' + db_name_t[0]

    @staticmethod
    def portfolio_create(username):
        create = Portfolio(Portfolio.title(), Portfolio.category(), Portfolio.name(username), username)
        create.portfolio_insert()

    def portfolio_insert(self):
        cursor.execute("""
        INSERT INTO portfolios (portfolio_title, portfolio_category, portfolio_photographer_name, portfolio_username) VALUES (?, ?, ?, ?)
        """, (self.title, self.category, self.name, self.username))
        connect.commit()
        print('Portofoliul a fost creat cu succes.')

    # Meniu principal
    @classmethod
    def portfolio_menu(cls, username):
        menu_portfolio = {
            1: cls.portfolio_create, #create portfolio
            2: cls.display_portfolio, #display portfolios
        }
        while True:
            print("""
    Pentru a crea un portofoliu, selectati 1.
    Pentru afisarea portofoliilor, selectati 2.
    Pentru revenirea la meniul anterior, selectati 3.
""")
            try:
                option = int(input('Optiunea dumneavoastra: '))
                if option == 1 or option == 2:
                    menu_portfolio[option](username)
                elif option == 3:
                    print('Iesire submeniu...')
                    return
                else:
                    print('Optiunea selectata nu este valida.')
            except ValueError:
                print(cls.valoare_invalida)

    # Meniu secundar (dupa selectarea unui portofoliu)
    @staticmethod
    def portfolio_submenu(username, portfolio_id):
        cursor.execute(f"SELECT user_tag FROM users WHERE user_login = '{username}'")
        tag = cursor.fetchone()[0]
        menu = {
            1: '', #menu to images
            2: '', #edit portfolio
            3: '' #delete portfolio
        }
        if tag == 'Utilizator':
            menu_filtered = {key: menu[key] for key in menu.keys() & {1}}
            for i,j in menu_filtered.items():
                print(f'    {i} -> {j}') 
        else:
            for i,j in menu.items():
                print(f'    {i} -> {j}')
        check = False
        while not check:
            try:
                optiune = int(input('Optiunea dumneavoastra: '))
                if optiune == 1:
                    menu[optiune]()
                elif optiune == 2:
                    pass
            except ValueError:
                pass

    @staticmethod
    def display_portfolio(username):
        category_list = {
            1: 'Landscape',
            2: 'Portrait',
            3: 'Nature',
            4: 'Animals',
            5: 'Street',
            6: 'B&W',
            7: 'Other',
            8: 'All',
            9: 'Revenire la meniul anterior'
        }
        while True:
            print('\nCategorii:')
            for i,j in category_list.items():
                print(f'    Nr.{i} -> {j}')
            check_cat = False
            while not check_cat:
                try:
                    filtrare = int(input('\nSelectati o categorie pe care doriti sa o vizualizati: '))
                    if filtrare not in range(1,10):
                        print('Optiunea selectata nu este valida.')
                    elif filtrare == 8:
                        cursor.execute("SELECT portfolio_id, portfolio_title, portfolio_category, portfolio_photographer_name FROM portfolios")
                        for value in cursor.fetchall():
                            print(f'\n  Id: {value[0]}\nTitle: {value[1]}\nCategory: {value[2]}\nPhotographer: {value[3]}')
                        check_cat = True
                    elif filtrare == 9:
                        print('Iesire submeniu...')
                        check_cat = True
                        return
                    else:
                        cursor.execute("SELECT portfolio_id, portfolio_title, portfolio_category, portfolio_photographer_name FROM portfolios \
                                                        WHERE portfolio_category = '{}'".format(category_list[filtrare]))
                        for value in cursor.fetchall():
                            print(f'\n  Id: {value[0]}\nTitlu: {value[1]}\nCategorie: {value[2]}\nFotograf: {value[3]}')
                        check_cat = True
                except ValueError:
                    print(__class__.valoare_invalida)
            check_portfolio = False
            while not check_portfolio:
                try:
                    select_portfolio = int(input('\nSelectati portofoliul pe care doriti sa il vizualizati: '))
                    if select_portfolio not in [id[0] for id in cursor.execute("SELECT portfolio_id FROM portfolios")]:
                        print('Acest portofoliu nu exista.')
                    else:
                        Portfolio.portfolio_submenu(username, select_portfolio)
                        check_portfolio = True
                except ValueError:
                    print(__class__.valoare_invalida)
            
    @staticmethod
    def images(id):
        cursor.execute(f"SELECT image_id, image_name, image_data, image_portfolio_title FROM images WHERE image_portfolio_id = '{id}'")
        data = cursor.fetchall()
        if len(data) == 0:
            print('Nu exista imagini in acest portofoliu.')
            return
        else:
            for value in data:
                print(f'\nId: {value[0]}\nNume: {value[1]}\nPortofoliu: {value[2]}\n')
        check = False
        while not check:
            try:
                select = int(input('Ce imagine doriti sa vizualizati?: '))
                # if select
            except ValueError:
                print(__class__.valoare_invalida)
        # print(data[0][1])
        # else:
        #     print(data)

if __name__ == "__main__":
    # Portfolio.category()
    # Portfolio.menu_portfolio('soptr')
    Portfolio.display_portfolio('soptr')
    # Portfolio.select_portfolio(1)