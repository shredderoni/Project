from user import User
import sys

menu = {
    1: User.initiate_login,
    2: User.initiate_create,
    3: sys.exit
}

while True:
    print("""
    Pentru login, selectati 1.
    Pentru a crea un cont nou, selectati 2.
""")
    option = int(input('Optiunea dumneavoastra: '))
    menu[option]()