import random

def initial_random_solution(packages, vehicles):
    import random
    import copy

    vehicles_copy = copy.deepcopy(vehicles)
    unassigned = packages[:]

    random.shuffle(unassigned)        # 🔁 ترتيب عشوائي للطرد
    random.shuffle(vehicles_copy)    # 🔁 ترتيب عشوائي للمركبات

    for pkg in unassigned:
        for v in vehicles_copy:
            if v.can_add(pkg):
                v.packages.append(pkg)
                break

    return vehicles_copy