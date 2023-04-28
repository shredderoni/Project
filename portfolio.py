import sqlite3 as sql

connect = sql.connect("data.db")
cursor = connect.cursor()
cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolios (
            portfolio_id INTEGER PRIMARY KEY AUTOINCREMENT,
            portfolio_title NVARCHAR(60),
            portfolio_category NVARCHAR(60),
            portfolio_photographer_name NVARCHAR(160)
        )
        """)
# FOREIGN KEY (portfolio_photographer_id) REFERENCES users (user_id)

class Portfolio:
    def __init__(self, title, category, name):
        self.title = title
        self.category = category
        self.name = name
    
    @classmethod
    def title(cls):
        check = False

        while not check:
            portfolio_title = input("Selectati un nume pentru portofoliul dumneavoastra: ")
            if not portfolio_title.isalpha():
                print('Numele portofoliului trebuie sa contina doar litere.')
                check = False
            else:
                check = True
                return portfolio_title
            
    @classmethod
    def category(cls):
        check = False

        while not check:
            portfolio_category = input("Selectati o categorie pentru portofoliul dumneavoastra: ")
            if not portfolio_category.isalpha():
                print('Numele categoriei trebuie sa contina doar litere.')
                check = False
            elif portfolio_category not in []:
                print('Categoria selectata nu este valabila.')
                check = False
            else:
                check = True
                return portfolio_category
    
    def insert_portfolio(self):
        cursor.execute("""
        INSERT INTO portfolios (portfolio_title, portfolio_category, portfolio_photographer_name) VALUES (?, ?, ?)
        """, (self.title, self.category, self.name))
        connect.commit()
        print('Portofoliul a fost creat cu succes.')

    @classmethod
    def menu_portfolio(cls, name):
        print("""
Pentru a crea un portofoliu, selectati 1.
Pentru afisarea portofoliilor, selectati 2.
Pentru a vizualiza un portofoliu, selectati 3.
Pentru a edita un portofoliu, selectati 4.
Pentru a sterge un portofoliu, selectati 5.
Pentru revenirea la meniul anterior, selectati 6.
""")
        menu_portfolio = {
            1: Portfolio.initiate_create, #create portfolio
            2: '', #display portfolios
            3: '', #enter portfolio
            4: '', #edit portfolio
            5: '' #delete portfolio
        }

        option = int(input('Optiunea dumneavoastra: '))
        if option == 6:
            print('Iesire submeniu...')
            return
        menu_portfolio[option](name)

    @classmethod
    def initiate_create(cls, name):
        create = Portfolio(Portfolio.title(), Portfolio.category(), name)
        create.insert_portfolio()
        connect.close()

    # def select_portfolio(self):
    #     cursor.execute("""
    #     SELECT i.Image FROM users u JOIN images i ON u.
    #     """.format(self.photographer_id))

if __name__ == "__main__":
    Portfolio.initiate_create('NumeTest')