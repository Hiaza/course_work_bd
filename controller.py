from consolemenu import SelectionMenu
import db_utils
import random_Users
import random_Checks
import analisys
import os


def show_start_menu():
    opts = "0)Backup\n1)Restore\n2)Generate 10000 users\n3)Generate 20000 checks\n" \
           "4)Show sum per day in millions\n5)Show sum per check\n6)Show num of purchases per check\n" \
           "7)Show sum per distance\n8)Show num of purchases per distance\n9)Exit"

    print("Select a task to do:\n" + opts)
    index = input()

    if index == '0':
        db_utils.dump_db()
    elif index == '1':
        db_utils.restore_db()
    elif index == '2':
        random_Users.Generator_of_users(10000)
    elif index == '3':
        random_Checks.Generator_of_checks(20000)
    elif index == '4':
        analisys.sum_per_day()
    elif index == '5':
        analisys.sum_per_check()
    elif index == '6':
        analisys.num_of_purchases_per_check()
    elif index == '7':
        analisys.sum_per_distance()
    elif index == '8':
        analisys.num_of_purchases_per_distance()
    elif index == '9':
        return

    input('\nPress ENTER...')
    cls()
    show_start_menu()


def cls():
    os.system('cls' if os.name=='nt' else 'clear')


if __name__ == '__main__':
    cls()
    show_start_menu()

