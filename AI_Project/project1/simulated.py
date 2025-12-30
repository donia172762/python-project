import random
import copy
from solution_generator import initial_random_solution
from utils import total_cost

def simulated_annealing(packages, vehicles, initial_temp=1000, cooling_rate=0.95, stop_temp=1.0):
    def get_neighbor(sol):
        new_sol = copy.deepcopy(sol)

       
        if len(new_sol) < 2:
            return new_sol

          
        v1, v2 = random.sample(new_sol, 2)

        
        if not v1.packages or not v2.packages:
            return new_sol

        
        p1 = random.choice(v1.packages)
        p2 = random.choice(v2.packages)

        
        if v1.total_weight() - p1.weight + p2.weight <= v1.capacity and \
           v2.total_weight() - p2.weight + p1.weight <= v2.capacity:
            v1.packages.remove(p1)
            v2.packages.remove(p2)
            v1.packages.append(p2)
            v2.packages.append(p1)

        return new_sol

    current_sol = initial_random_solution(packages, vehicles)
    best_sol = copy.deepcopy(current_sol)
    current_temp = initial_temp

    while current_temp > stop_temp:
        for _ in range(100):
            neighbor = get_neighbor(current_sol)
            cost_diff = total_cost(neighbor) - total_cost(current_sol)
            if cost_diff < 0 or random.random() < pow(2.718, -cost_diff / current_temp):
                current_sol = neighbor
                if total_cost(current_sol) < total_cost(best_sol):
                    best_sol = copy.deepcopy(current_sol)
        current_temp *= cooling_rate

    return best_sol
