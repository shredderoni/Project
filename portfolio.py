import sqlite3 as sql
from user import User

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
    def __init__(self, title, category, name, username):
        self.title = title
        self.category = category
        self.name = name
        self.username = username
    
    @staticmethod
    def title():
        check = False
        while not check:
            portfolio_title = input("Selectati un nume pentru portofoliul dumneavoastra: ")
            if not portfolio_title.isalpha():
                print('Numele portofoliului trebuie sa contina doar litere.')
                check = False
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
                    check = False
                else:
                    check = True
                    return category_list[portfolio_category]
            except ValueError:
                print(User.valoare_invalida)
    
    def insert_portfolio(self):
        cursor.execute("""
        INSERT INTO portfolios (portfolio_title, portfolio_category, portfolio_photographer_name) VALUES (?, ?, ?)
        """, (self.title, self.category, self.name))
        connect.commit()
        print('Portofoliul a fost creat cu succes.')

    @classmethod
    def menu_portfolio(cls, name, username):
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
            2: Portfolio.display_portfolio, #display portfolios
            3: '', #enter portfolio
            4: '', #edit portfolio
            5: '' #delete portfolio
        }
        while True:
            try:
                option = int(input('Optiunea dumneavoastra: '))
                if option == 1:
                    menu_portfolio[option](name, username)
                elif option == 2 or option == 3:
                    menu_portfolio[option]()
                elif option == 4 or option == 5:
                    menu_portfolio[option](username)
                elif option == 6:
                    print('Iesire submeniu...')
                    return
                else:
                    print('Optiunea selectata nu este valida.')
            except ValueError:
                print(User.valoare_invalida)

    @classmethod
    def initiate_create(cls, name, username):
        create = Portfolio(Portfolio.title(), Portfolio.category(), name, username)
        create.insert_portfolio()
        connect.close()

    @staticmethod
    def display_portfolio():
        id = [id[0] for id in cursor.execute("SELECT portfolio_id FROM portfolios")]
        title = [title[0] for title in cursor.execute("SELECT portfolio_title FROM portfolios")]
        category = [category[0] for category in cursor.execute("SELECT portfolio_category FROM portfolios")]
        pname = [pname[0] for pname in cursor.execute("SELECT portfolio_photographer_name FROM portfolios")]
        for id, title, category, pname in zip(id, title, category, pname):
            print(f'Id: {id}, Title: {title}, Category: {category}, Photographer Name: {pname}')

    # def select_portfolio(self):
    #     cursor.execute("""
    #     SELECT i.Image FROM users u JOIN images i ON u.
    #     """.format(self.photographer_id))

if __name__ == "__main__":
    Portfolio.initiate_create('NumeTest', 'soptr')
    # Portfolio.menu_portfolio('Alexandra', 'soptr')
    # Portfolio.category()
    # Portfolio.display_portfolio()