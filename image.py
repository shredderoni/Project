import sqlite3 as sql
import os, shutil
from os.path import exists

path = os.getcwd()
connect = sql.connect("data.db")
cursor = connect.cursor()
cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            image_id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_name NVARCHAR(60),
            image_data NVARCHAR(255),
            image_portfolio_title NVARCHAR(60),
            image_portfolio_id INTEGER
        )
        """)
# FOREIGN KEY (image_portfolio_id) REFERENCES portfolios (portfolio_id)

class Image:
    def __init__(self, image, name):
        self.image = image
        self.name = name

    # @staticmethod
    # def select_image():
    #     check = False

    #     while not check:
    #         image = input("Select image: ")
    #         if not exists(f'C:\\Users\\soptr\\Desktop\\Project\\{image}'):
    #             print('Imaginea selectata nu exista.')
    #             check = False
    #         else:
    #             with open(f'{image}', 'rb') as w:
    #                 data = w.read()
    #             check = True
    #             return data

    # Selectare imagine si inserare in baza de date
    @staticmethod
    def image_data():
        check = False
        while not check:
            image = input('Selectati imaginea (path to image): ')
            if not exists(image):
                print('Imaginea sau locatia nu exista.')
                check = False
            else:
                check = True
                shutil.copy(image, f'{os.getcwd()}\\images')
                print(image)
                return image

    @staticmethod
    def image_name():
        check = False

        while not check:
            name = input('Selectati un nume pentru imagine: ')
            if not name.isalpha():
                print('Numele imaginii trebuie sa contina doar litere.')
                check = False
            else:
                check = True
                return name

    def image_insert(self):
        cursor.execute("""
        INSERT INTO images (image_name, image_data) VALUES (?, ?)
        """, (self.name, self.image))
        connect.commit()
        print('Imaginea a fost adaugata cu succes.')

    @staticmethod
    def initiate():
        add = Image(Image.image_data(), Image.image_name())
        add.image_insert()

    @staticmethod
    def image_menu():
        menu = {
            1: '', #display images
            2: '',
            3: ''
        }

    # Vizualizare imagine
    @staticmethod
    def image_view():
        cursor.execute("SELECT image_id")
        select = int(input('Ce imagine doriti sa vizualizati?: '))

if __name__ == '__main__':
    Image.initiate()