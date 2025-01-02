from DBOperator import *
from RandomElementSelector import *
from Elements import *

def menu():
    while True:
        command = input('> ')
        match command:
            case 'q':  # Quit
                break

            case 'n':  # Next
                elements = []

                for row in get_all_items():
                    elements.append(Element(row[0], row[1], row[2]))

                print(choose_random_element(elements))

            case 's':
                for row in get_all_items():
                    print(f'{row[0]}, priority: {row[1]}, active: {row[2]}')

            case 'a':  # Add
                e = Element()

                e.name = input('name = ')
                e.priority = input('priority = ')
                e.active = input('active = ')

                add_item(e)