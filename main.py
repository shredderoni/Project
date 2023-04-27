from user import User
from portfolio import Portfolio
from image import Image
import sys

menu = {
    1: '',
    2: User.create_user,
    3: sys.exit
}

print("""
Pentru a adauga un portfolio, selectati 1.
Pentru a adauga o poza, selectati 2.
""")
menu_portfolio = {
    1: Portfolio.initiate,
    2: Image.initiate
}

while True:
    option = int(input('Optiunea dumneavoastra: '))
    menu_portfolio[option]()