import sqlite3 as sql
import os
from string import ascii_letters
from image import Image

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
    def __init__(self):
        self.title = ''
        self.category = ''
        self.name = ''
        self.username = ''
    
    # Date pentru portofoliu si inserare in baza de date
    @staticmethod
    def create_title():
        check = False
        while not check:
            portfolio_title = input("Selectati un nume pentru portofoliul dumneavoastra: ")
            if set(portfolio_title).difference(__class__.characters):
                print('Numele portofoliului trebuie sa contina doar litere.')
            else:
                check = True
                return portfolio_title
            
    @staticmethod
    def create_category():
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
                portfolio_category = int(input("\nSelectati o categorie pentru portofoliul dumneavoastra: "))
                if portfolio_category not in category_list.keys():
                    print('\nCategoria selectata nu este disponibila.')
                else:
                    check = True
                    return category_list[portfolio_category]
            except ValueError:
                print(__class__.valoare_invalida)
        

    @staticmethod
    def create_name(username):
        cursor.execute(f"SELECT user_first_name, user_last_name FROM users WHERE user_login = '{username}'")
        db_name_t = cursor.fetchone()
        return db_name_t[0] + ' ' + db_name_t[1]

    def portfolio_create(self):
        self.title = self.create_title()
        self.category = self.create_category()
        self.name = self.create_name(self.username)
        self.portfolio_insert()

    def portfolio_insert(self):
        cursor.execute("""
        INSERT INTO portfolios (portfolio_title, portfolio_category, portfolio_photographer_name, portfolio_username) VALUES (?, ?, ?, ?)
        """, (self.title, self.category, self.name, self.username))
        connect.commit()
        print('Portofoliul a fost creat cu succes.')

    # Meniu principal
    def portfolio_menu(self, username):
        self.username = username
        print(self.username)
        cursor.execute(f"SELECT user_tag FROM users WHERE user_login = '{self.username}'")
        tag = cursor.fetchone()[0]
        while True:
            if tag == 'Utilizator':
                print("""
    Pentru afisarea portofoliilor, selectati 1.
    Pentru a vizualiza pozele dintr-un portofoliu, selectati 2.
    Pentru a reveni la meniul anterior, selectati 3.
""")
                try:
                    option = int(input('Optiunea dumneavoastra: '))
                    if option == 1:
                        self.portfolio_display()
                    elif option == 2:
                        image = Image()
                        image.image_menu(self.portfolio_select(), self.username)
                    elif option == 3:
                        print('Iesire submeniu...')
                        return
                    else:
                        print('\nOptiunea selectata nu este valida.')
                except ValueError:
                    print(self.valoare_invalida)
            elif tag in ['Fotograf', 'Admin']:
                print("""
    Pentru afisarea portofoliilor, selectati 1.
    Pentru a vizualiza pozele dintr-un portofoliu, selectati 2.
    Pentru mai multe optiuni, selectati 3.
    Pentru revenirea la meniul anterior, selectati 4.
""")
                try:
                    option = int(input('Optiunea dumneavoastra: '))
                    if option == 1:
                        self.portfolio_display()
                    elif option == 2:
                        image = Image()
                        image.image_menu(self.portfolio_select(), self.username)
                    elif option == 3:
                        self.portfolio_submenu()
                    elif option == 4:
                        print('Iesire submeniu...')
                        return
                    else:
                        print('\nOptiunea selectata nu este valida.')
                except ValueError:
                    print(self.valoare_invalida)

    # Meniu secundar (dupa selectarea unui portofoliu)
    def portfolio_submenu(self):
        menu = {
            1: self.portfolio_create,
            2: self.portfolio_edit,
            3: self.portfolio_delete
        }
        while True: 
            print("""
    Pentru a crea un portofoliu, selectati 1.
    Pentru a edita un portofoliu, selectati 2.
    Pentru a sterge un portofoliu, selectati 3.
    Pentru a reveni la meniul anterior, selectati 4.
""")
            try:
                option = int(input('Optiunea dumneavoastra: '))
                if option in range(1,4):
                    menu[option]()
                elif option == 4:
                    print('Iesire submeniu...')
                    return
                else:
                    print('\nOptiunea selectata nu este valida.')
            except ValueError:
                print(self.valoare_invalida)

    @staticmethod
    def portfolio_display():
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
            while True: 
                try:
                    filtrare = int(input('\nSelectati o categorie pe care doriti sa o vizualizati: '))
                    if filtrare in range(1,8):
                        cursor.execute("SELECT portfolio_id, portfolio_title, portfolio_category, portfolio_photographer_name FROM portfolios \
                                                        WHERE portfolio_category = '{}'".format(category_list[filtrare]))
                        for value in cursor.fetchall():
                            print(f'\nId: {value[0]}\nTitlu: {value[1]}\nCategorie: {value[2]}\nFotograf: {value[3]}')
                        return
                    elif filtrare == 8:
                        cursor.execute("SELECT portfolio_id, portfolio_title, portfolio_category, portfolio_photographer_name FROM portfolios")
                        for value in cursor.fetchall():
                            print(f'\nId: {value[0]}\nTitle: {value[1]}\nCategory: {value[2]}\nPhotographer: {value[3]}')
                        return
                    elif filtrare == 9:
                        print('Iesire submeniu...')
                        return
                    else:
                        print('\nOptiunea selectata nu este valida.')
                except ValueError:
                    print(__class__.valoare_invalida)
    
    @staticmethod
    def portfolio_select():
        Portfolio.portfolio_display()
        while True:
            try:
                portfolio_id = int(input('\nSelectati portofoliul pe care doriti sa il vizualizati: '))
                if portfolio_id not in [id[0] for id in cursor.execute("SELECT portfolio_id FROM portfolios")]: 
                    print('\nAcest portofoliu nu contine poze.')
                else:
                    return portfolio_id
            except ValueError:
                print(__class__.valoare_invalida)
            except KeyboardInterrupt:
                return
    
    def portfolio_select_edit(self):
        cursor.execute(f"SELECT portfolio_id, portfolio_title, portfolio_category FROM portfolios WHERE portfolio_username = '{self.username}'")
        while True:
            data = cursor.fetchall()
            if len(data) == 0:
                print('\nNu aveti niciun portofoliu creat.')
                return
            else:
                for value in data:
                    print(f'\nId: {value[0]}\nTitle: {value[1]}\nCategory: {value[2]}')
            try:
                select = int(input('\nSelectati un portofoliu: '))
                if select not in [id[0] for id in cursor.execute(f"SELECT portfolio_id FROM portfolios WHERE portfolio_username = '{self.username}'")]:
                    print('\nPortofoliul selectat nu exista.')
                else:
                    return select
            except ValueError:
                print(self.valoare_invalida)
            except KeyboardInterrupt:
                return
                
    def portfolio_edit(self):
        while True:
            print("""
    Pentru a modifica titlul, selectati 1.
    Pentru a modfica categoria, selectati 2.
    Pentru a reveni la meniul anterior, selectati 3.    
""")
            try:
                option = int(input('Optiunea dumneavoastra: '))
                if option == 1:
                    id = self.portfolio_select_edit()
                    if id == None:
                        return
                    title = self.create_title()
                    cursor.execute("UPDATE portfolios SET portfolio_title = ? WHERE portfolio_id = ?", (title, id))
                    cursor.execute(f"SELECT image_portfolio_id FROM images WHERE image_portfolio_id = '{id}'")
                    images = [id[0] for id in cursor.fetchall()]
                    if len(images) != 0:
                        cursor.execute("UPDATE images SET image_portfolio_title = ? WHERE image_portfolio_id = ?", (title, id))
                    connect.commit()
                    print('\nTitlul a fost actualizat.')
                elif option == 2:
                    id = self.portfolio_select_edit()
                    if id == None:
                        return
                    cursor.execute("UPDATE portfolios SET portfolio_category = ? WHERE portfolio_id = ?", (self.create_category(), id))
                    connect.commit()
                    print('\nCategoria a fost actualizata.')
                elif option == 3:
                    print('\nIesire submeniu...')
                    return
                else:
                    print('\nOptiunea selectata nu este valida.')
            except ValueError:
                print(self.valoare_invalida)

    def portfolio_delete(self):
        id = self.portfolio_select_edit()
        if id == None:
            return
        while True:
            print("""
    Pentru confirmare, selectati 1. ATENTIE!: Se vor sterge si toate imaginile asociate cu acesta!
    Pentru anulare, selectati 2.
""")
            try:
                option = int(input('Optiunea dumneavoastra: '))
                if option == 1:
                    cursor.execute(f"SELECT image_data FROM images WHERE image_portfolio_id = '{id}'")
                    if cursor.fetchone() != None:
                        path_to_image = cursor.fetchone()[0]
                        try:
                            os.remove(f'{path_to_image}')
                        except OSError:
                            pass
                        cursor.execute(f"DELETE FROM images WHERE image_portfolio_id = '{id}'")
                    cursor.execute(f"DELETE FROM portfolios WHERE portfolio_id = '{id}'")
                    connect.commit()
                    print('Portofoliul si imaginile asociate au fost sterse.')
                    return
                elif option == 2:
                    print('Anulare...')
                    return
                else:
                    print('Optiunea selectata nu este valida.')
            except ValueError:
                print(self.valoare_invalida)

            
if __name__ == "__main__":
    # Portfolio.portfolio_menu('soptr')
    Portfolio.portfolio_select()