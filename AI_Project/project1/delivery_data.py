import random

class Package:
    def __init__(self, id, x, y, weight, priority):
        self.id = id
        self.x = x
        self.y = y
        self.weight = weight
        self.priority = priority

class Vehicle:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.packages = [] 

    def total_weight(self):
        return sum(pkg.weight for pkg in self.packages)

    def can_add(self, package):
        return self.total_weight() + package.weight <= self.capacity



def generate_random_packages(num):
    packages = []
    for i in range(num):
        x, y = random.randint(0, 100), random.randint(0, 100)
        weight = random.randint(1, 30)
        priority = random.randint(1, 5)
        packages.append(Package(i, x, y, weight, priority))
    return packages

def generate_vehicles(num, capacity):
    return [Vehicle(i, capacity) for i in range(num)]