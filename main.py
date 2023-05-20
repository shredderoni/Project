from user import User
import sys

print("""
    *******************
    *    WELCOME !    *
    *******************
""")
while True:
    print("""
    Pentru login, selectati 1.
    Pentru a crea un cont nou, selectati 2.
    Pentru a iesi din program, selectati 3.
""")
    try:
        option = int(input('Optiunea dumneavoastra: '))
        if option == 1:
            login = User()
            login.user_login()
        elif option == 2:
            create = User()
            create.user_create()
        elif option == 3:
            print('\nIesire program...')
            sys.exit()
        else:
            print('\nOptiunea selectata nu este valida.')
    except ValueError:
        print(User.valoare_invalida)