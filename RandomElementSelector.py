#Version 1.0

import random

def choose_random_element(elements):
    available_elements = [e for e in elements if e.active]

    priority_list = []

    for e in available_elements:
        for _ in range(e.priority):
            priority_list.append(e.name)

    return random.choice(priority_list)