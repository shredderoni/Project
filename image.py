import sqlite3 as sql
from os.path import exists

connect = sql.connect("data.db")
cursor = connect.cursor()
cursor.execute("""
        CREATE TABLE IF NOT EXISTS images (
            image_id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_name NVARCHAR(60),
            image_data BLOB,
            image_portfolio_title NVARCHAR(60),
        )
        """)
# FOREIGN KEY (image_portfolio_id) REFERENCES portfolios (portfolio_id)

class Image:
    def __init__(self, image, name):
        self.image = image
        self.name = name

    @classmethod
    def select_image(cls):
        check = False

        while not check:
            image = input("Select image: ")
            if not exists(f'C:\\Users\\soptr\\Desktop\\Project\\{image}'):
                print('Imaginea selectata nu exista.')
                check = False
            else:
                with open(f'{image}', 'rb') as w:
                    data = w.read()
                check = True
                return data

    @classmethod
    def image_name(cls):
        check = False

        while not check:
            name = input('Selectati un nume pentru imagine: ')
            if not name.isalpha():
                print('Numele imaginii trebuie sa contina doar litere.')
                check = False
            else:
                check = True
                return name

    def insert_image(self):
        cursor.execute("""
        INSERT INTO images (image_name, image_data) VALUES (?, ?)
        """, (self.name, self.image))
        connect.commit()
        print('Imaginea a fost adaugata cu succes.')

    @classmethod
    def initiate(cls):
        add = Image(Image.select_image(), Image.image_name())
        add.insert_image()
        connect.close()

if __name__ == '__main__':
    add = Image(Image.select_image(), Image.image_name())
    add.insert_image()