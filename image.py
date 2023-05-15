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
    def __init__(self, name, image, settings, portfolio_title, portfolio_id, username):
        self.name = name
        self.image = image
        self.settings = settings
        self.title = portfolio_title
        self.id = portfolio_id
        self.username = username

    # Selectare imagine si inserare in baza de date
    @staticmethod
    def name():
        check = False
        while not check:
            name = input('Selectati un nume pentru imagine: ')
            if set(name).difference(__class__.characters):
                print('Numele imaginii trebuie sa contina doar litere.')
            else:
                check = True
                return name

    @staticmethod
    def image():
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
    def settings():
        settings = input('Introduceti setarile camerei pentru aceasta imagine: ')
        return settings


    def image_insert(self):
        cursor.execute("""
        INSERT INTO images (image_name, image_data, image_settings, image_portfolio_title, image_portfolio_id, image_username) VALUES (?, ?, ?, ?, ?, ?)
        """, (self.name, self.image, self.settings, self.title, self.id, self.username))
        connect.commit()
        print('Imaginea a fost adaugata cu succes.')

    @staticmethod
    def image_create(portfolio_id, username):
        cursor.execute(f"SELECT portfolio_title FROM portfolios WHERE portfolio_id = '{portfolio_id}'") 
        title = cursor.fetchone()[0]
        add = Image(Image.name(), Image.image(), Image.settings(), title, portfolio_id, username)
        add.image_insert()

    @classmethod
    def image_menu(cls, portfolio_id, username):
        cursor.execute(f"SELECT user_tag FROM users WHERE user_login = '{username}'")
        tag = cursor.fetchone()[0]
        menu = {
            1: cls.image_catalog,
            2: cls.image_submenu
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
                        menu[option](portfolio_id)
                    elif option == 2:
                        print('Iesire submeniu...')
                        return
                except ValueError:
                    print(__class__.valoare_invalida)
            elif tag in ['Fotograf', 'Admin']:
                print("""
    Pentru a afisa imaginile, selectati 1.        
    Pentru mai multe optiuni, selectati 2.
    Pentru a reveni la meniul anterior, selectati 3.
""")
                try:
                    option = int(input('Optiunea dumneavoastra: '))
                    if option == 1:
                        menu[option](portfolio_id)
                    elif option == 2:
                        menu[option](portfolio_id, username)
                    elif option == 3:
                        print('\nIesire submeniu...')
                        return
                    else:
                        print('\nOptiunea selectata nu este valida')
                except ValueError:
                    print(__class__.valoare_invalida)

    @classmethod
    def image_submenu(cls, portfolio_id, username):
        menu = {
            1: cls.image_create,
            2: cls.image_name_edit,
            3: cls.image_settings_edit,
            4: cls.image_delete,
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
                if option == 1:
                    menu[option](portfolio_id, username)
                elif option in range(2,5):
                    menu[option](username)
                elif option == 5:
                    print('\nIesire submeniu...')
                    return
                else:
                    print('\nOptiunea selectata nu este valida.')
            except ValueError:
                print(cls.valoare_invalida)
    
    # Vizualizare imagine
    @staticmethod
    def image_catalog(portfolio_id):
        cursor.execute(f"SELECT image_id, image_name, image_settings, image_portfolio_title FROM images WHERE image_portfolio_id = '{portfolio_id}'")
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
                print(__class__.valoare_invalida)
            except KeyboardInterrupt:
                return

    @staticmethod
    def image_data(username):
        cursor.execute(f"SELECT image_id, image_name, image_settings, image_portfolio_title \
                                                 FROM images WHERE image_username = '{username}'")
        for value in cursor.fetchall():
            print(f'\nId: {value[0]}\nName: {value[1]}\nSettings: {value[2]}\nPortfolio: {value[3]}')

    @staticmethod
    def image_name_edit(username):
        Image.image_data(username)
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
                            if select not in [id[0] for id in cursor.execute(f"SELECT image_id FROM images WHERE image_username = '{username}'")]:
                                print('\nImaginea selectata nu exista.')
                            else:
                                break
                        except ValueError:
                            print(__class__.valoare_invalida)
                        except KeyboardInterrupt:
                            return
                    cursor.execute("UPDATE images SET image_name = ? WHERE image_id = ?", (Image.name(), select))
                    connect.commit()
                    print('\nNumele a fost actualizat cu succes.')
                elif option == 2:
                    print('\nAnulare...')
                    return
                else:
                    print('\nOptiunea selectata nu este valida.')
            except ValueError:
                print(__class__.valoare_invalida)

    @staticmethod
    def image_settings_edit(username):
        Image.image_data(username)
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
                            if select not in [id[0] for id in cursor.execute(f"SELECT image_id FROM images WHERE image_username = '{username}'")]:
                                print('\nImaginea selectata nu exista.')
                            else:
                                break
                        except ValueError:
                            print(__class__.valoare_invalida)
                        except KeyboardInterrupt:
                            return
                    cursor.execute("UPDATE images SET image_settings = ? WHERE image_id = ?", (Image.settings(), select))
                    connect.commit()
                    print('\nSetarile imaginii au fost actualizate cu succes.')
                elif option == 2:
                    print('\nAnulare...')
                    return
                else:
                    print('\nOptiunea selectata nu este valida.')
            except ValueError:
                print(__class__.valoare_invalida)


    @staticmethod
    def image_delete(username):
        Image.image_data(username)
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
                            if select not in [id[0] for id in cursor.execute(f"SELECT image_id FROM images WHERE image_username = '{username}'")]:
                                print('\nImaginea selectata nu exista.')
                            else:
                                break
                        except ValueError:
                            print(__class__.valoare_invalida)
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
                print(__class__.valoare_invalida)

if __name__ == '__main__':
    pass