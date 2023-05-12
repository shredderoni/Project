from user import User
import sys

menu = {
    1: User.user_login,
    2: User.user_create,
    3: sys.exit
}

while True:
    print("""
    Pentru login, selectati 1.
    Pentru a crea un cont nou, selectati 2.
    Pentru a iesi din program, selectati 3.
""")
    try:
        option = int(input('Optiunea dumneavoastra: '))
        if option == 1:
            menu[option]()
        elif option == 2:
            menu[option]('New')
        elif option == 3:
            print('\nIesire program...')
            menu[option]()
        else:
            print('\nOptiunea selectata nu este valida.')
    except ValueError:
        print(User.valoare_invalida)