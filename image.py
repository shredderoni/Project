import sqlite3 as sql
import os, shutil, uuid
from os.path import exists
from PIL import Image as PILImage
from string import ascii_letters

connect = sql.connect("data.db")
cursor = connect.cursor()
cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            image_id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_name NVARCHAR(60),
            image_data NVARCHAR(255),
            image_settings NVARCHAR(255),
            image_portfolio_title NVARCHAR(60),
            image_portfolio_id INTEGER,
            image_username NVARCHAR(60)
        )
        """)
# FOREIGN KEY (image_portfolio_id) REFERENCES portfolios (portfolio_id)

class Image:
    characters = ascii_letters + ' '
    valoare_invalida = """
* *  ********************************  * *
 *   Ati introdus o valoare invalida!   *
* *  ********************************  * *
"""
    def __init__(self):
        self.name = ''
        self.image = ''
        self.settings = ''
        self.title = ''
        self.id = ''
        self.username = ''

    # Selectare imagine si inserare in baza de date
    @staticmethod
    def create_name():
        check = False
        while not check:
            name = input('Selectati un nume pentru imagine: ')
            if set(name).difference(__class__.characters):
                print('Numele imaginii trebuie sa contina doar litere.')
            else:
                check = True
                return name

    @staticmethod
    def create_image():
        check = False
        while not check:
            image = input('Selectati imaginea (path to image): ')
            if not exists(image):
                print('Imaginea sau locatia nu exista.')
            else:
                check = True
                filename = str(uuid.uuid4())
                shutil.copy(image, f'{os.getcwd()}\\images\\{filename}.jpg')
                return f'{os.getcwd()}\\images\\{filename}.jpg'
            
    @staticmethod
    def create_settings():
        settings = input('Introduceti setarile camerei pentru aceasta imagine: ')
        return settings


    def image_insert(self):
        cursor.execute("""
        INSERT INTO images (image_name, image_data, image_settings, image_portfolio_title, image_portfolio_id, image_username) VALUES (?, ?, ?, ?, ?, ?)
        """, (self.name, self.image, self.settings, self.title, self.id, self.username))
        connect.commit()
        print('Imaginea a fost adaugata cu succes.')

    def image_create(self):
        cursor.execute(f"SELECT portfolio_title FROM portfolios WHERE portfolio_id = '{self.id}'") 
        title = cursor.fetchone()[0]
        self.name = self.create_name()
        self.image = self.create_image()
        self.settings = self.create_settings()
        self.title = title
        self.image_insert()

    def image_menu(self, portfolio_id, username):
        self.id = portfolio_id
        self.username = username
        cursor.execute(f"SELECT user_tag FROM users WHERE user_login = '{self.username}'")
        tag = cursor.fetchone()[0]
        menu = {
            1: self.image_catalog,
            2: self.image_submenu
        }
        while True:
            if tag == 'Utilizator':
                print("""
    Pentru a afisa imaginile, selectati 1.        
    Pentru a reveni la meniul anterior, selectati 2.
""")
                try:
                    option = int(input('Optiunea dumneavoastra: '))
                    if option == 1:
                        menu[option]()
                    elif option == 2:
                        print('Iesire submeniu...')
                        return
                except ValueError:
                    print(self.valoare_invalida)
            elif tag in ['Fotograf', 'Admin']:
                print("""
    Pentru a afisa imaginile, selectati 1.        
    Pentru mai multe optiuni, selectati 2.
    Pentru a reveni la meniul anterior, selectati 3.
""")
                try:
                    option = int(input('Optiunea dumneavoastra: '))
                    if option == 1:
                        menu[option]()
                    elif option == 2:
                        cursor.execute(f"SELECT portfolio_username FROM portfolios WHERE portfolio_id = '{self.id}'")
                        data = cursor.fetchone()[0]
                        if data != self.username:
                            print('\nPortofoliul selectat nu va apartine. Iesire submeniu...')
                            return
                        menu[option]()
                    elif option == 3:
                        print('\nIesire submeniu...')
                        return
                    else:
                        print('\nOptiunea selectata nu este valida')
                except ValueError:
                    print(self.valoare_invalida)

    def image_submenu(self):
        menu = {
            1: self.image_create,
            2: self.image_name_edit,
            3: self.image_settings_edit,
            4: self.image_delete,
        }
        while True:
            print("""
    Pentru a incarca o imagine, selectati 1.
    Pentru a modifica numele unei imagini, selectati 2.
    Pentru a modifica setarile unei imagini, selectati 3.
    Pentru a sterge o imagine, selectati 4.
    Pentru a reveni la meniul anterior, selectati 5.
""")
            try:
                option = int(input('Optiunea dumneavoastra: '))
                if option in range(1,5):
                    menu[option]()
                elif option == 5:
                    print('\nIesire submeniu...')
                    return
                else:
                    print('\nOptiunea selectata nu este valida.')
            except ValueError:
                print(self.valoare_invalida)
    
    # Vizualizare imagine
    def image_catalog(self):
        cursor.execute(f"SELECT image_id, image_name, image_settings, image_portfolio_title FROM images WHERE image_portfolio_id = '{self.id}'")
        data = cursor.fetchall()
        if len(data) == 0:
            print('\nNu exista imagini in acest portofoliu.')
            return
        else:
            for value in data:
                print(f'\nId: {value[0]}\nNume: {value[1]}\nSetari camera: {value[2]}\nPortofoliu: {value[3]}')
        while True:
            try:
                select = int(input('\nCe imagine doriti sa vizualizati?: '))
                cursor.execute(f"SELECT image_id FROM images WHERE image_id = '{select}'")
                if select != cursor.fetchone()[0]:
                    print('Aceasta imagine nu exista.')
                else:
                    cursor.execute(f"SELECT image_data FROM images WHERE image_id = '{select}'")
                    image = PILImage.open(f"{cursor.fetchone()[0]}")
                    image.show()
                    return
            except ValueError:
                print(self.valoare_invalida)
            except KeyboardInterrupt:
                return

    def image_data(self):
        cursor.execute(f"SELECT image_id, image_name, image_settings, image_portfolio_title \
                                                 FROM images WHERE image_username = '{self.username}'")
        for value in cursor.fetchall():
            print(f'\nId: {value[0]}\nName: {value[1]}\nSettings: {value[2]}\nPortfolio: {value[3]}')

    def image_name_edit(self):
        self.image_data()
        while True:
            print("""
    Pentru a continua, selectati 1.
    Pentru anulare, selectati 2.            
""")
            try:
                option = int(input('Optiunea dumneavoastra: '))
                if option == 1:
                    while True:
                        try:
                            select = int(input('Selectati o imagine: '))
                            if select not in [id[0] for id in cursor.execute(f"SELECT image_id FROM images WHERE image_username = '{self.username}'")]:
                                print('\nImaginea selectata nu exista.')
                            else:
                                break
                        except ValueError:
                            print(self.valoare_invalida)
                        except KeyboardInterrupt:
                            return
                    cursor.execute("UPDATE images SET image_name = ? WHERE image_id = ?", (self.create_name(), select))
                    connect.commit()
                    print('\nNumele a fost actualizat cu succes.')
                elif option == 2:
                    print('\nAnulare...')
                    return
                else:
                    print('\nOptiunea selectata nu este valida.')
            except ValueError:
                print(self.valoare_invalida)

    def image_settings_edit(self):
        self.image_data()
        while True:
            print("""
    Pentru a continua, selectati 1.
    Pentru anulare, selectati 2.
""")
            try:
                option = int(input('Optiunea dumneavoastra: '))
                if option == 1:
                    while True:
                        try:
                            select = int(input('Selectati o imagine: '))
                            if select not in [id[0] for id in cursor.execute(f"SELECT image_id FROM images WHERE image_username = '{self.username}'")]:
                                print('\nImaginea selectata nu exista.')
                            else:
                                break
                        except ValueError:
                            print(self.valoare_invalida)
                        except KeyboardInterrupt:
                            return
                    cursor.execute("UPDATE images SET image_settings = ? WHERE image_id = ?", (self.create_settings(), select))
                    connect.commit()
                    print('\nSetarile imaginii au fost actualizate cu succes.')
                elif option == 2:
                    print('\nAnulare...')
                    return
                else:
                    print('\nOptiunea selectata nu este valida.')
            except ValueError:
                print(self.valoare_invalida)


    def image_delete(self):
        self.image_data()
        while True:
            print("""
    Pentru a continua, selectati 1.
    Pentru anulare, selectati 2.
""")
            try:
                option = int(input('Optiunea dumneavoastra: '))
                if option == 1:
                    while True:
                        try:
                            select = int(input('\nSelectati o imagine: '))
                            if select not in [id[0] for id in cursor.execute(f"SELECT image_id FROM images WHERE image_username = '{self.username}'")]:
                                print('\nImaginea selectata nu exista.')
                            else:
                                break
                        except ValueError:
                            print(self.valoare_invalida)
                        except KeyboardInterrupt:
                            return
                    cursor.execute(f"DELETE FROM images WHERE image_id = '{select}'")
                    connect.commit()
                    print('\nImaginea a fost stearsa.')
                elif option == 2:
                    print('\nAnulare...')
                    return
                else:
                    print('\nOptiunea selectata nu este valida.')
            except ValueError:
                print(self.valoare_invalida)

if __name__ == '__main__':
    pass