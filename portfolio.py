import sqlite3 as sql

connect = sql.connect("data.db")
cursor = connect.cursor()
cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolios (
            portfolio_id INTEGER PRIMARY KEY AUTOINCREMENT,
            portfolio_title NVARCHAR(60),
            portfolio_photographer_id INTEGER,
            FOREIGN KEY (portfolio_photographer_id) REFERENCES users (user_id)
        )
        """)

class Portfolio:
    def __init__(self, title):
        self.title = title
    
    @classmethod
    def create_portfolio(cls):
        check = False

        while not check:
            portfolio_title = input("Selectati un nume pentru portofolio dumneavoastra: ")
            if not portfolio_title.isalpha():
                print('Numele portofoliului trebuie sa contina doar litere.')
                check = False
            else:
                check = True
                return portfolio_title
    
    def insert_portfolio(self):
        cursor.execute("""
        INSERT INTO portfolios (portfolio_title) VALUES ('{}')
        """.format(self.title))
        connect.commit()
        print('Portofoliul a fost creat cu succes.')

    @classmethod
    def initiate(cls):
        create = Portfolio(Portfolio.create_portfolio())
        create.insert_portfolio()

    # def select_portfolio(self):
    #     cursor.execute("""
    #     SELECT i.Image FROM users u JOIN images i ON u.
    #     """.format(self.photographer_id))

if __name__ == "__main__":
    create = Portfolio(Portfolio.create_portfolio())
    create.insert_portfolio()