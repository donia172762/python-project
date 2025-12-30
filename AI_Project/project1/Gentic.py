def genetic_algorithm(packages, vehicles, population_size=50, mutation_rate=0.05, generations=500):
    import copy
    from utils import total_cost
    import random

    def create_individual(max_attempts=100):
        for _ in range(max_attempts):
            indiv = copy.deepcopy(vehicles)
            for v in indiv:
                v.packages.clear()
            unassigned = packages[:]
            random.shuffle(unassigned)
            used_ids = set()
            for pkg in unassigned:
                random.shuffle(indiv)
                for v in indiv:
                    if v.can_add(pkg) and pkg.id not in used_ids:
                        v.packages.append(pkg)
                        used_ids.add(pkg.id)
                        break
            if len(used_ids) == len(packages):
                return indiv
        return None  

    def get_used_package_ids(indiv):
        return set(pkg.id for v in indiv for pkg in v.packages)

    def crossover(parent1, parent2):
        child = copy.deepcopy(parent1)
        for v in child:
            v.packages.clear()
        used_ids = set()
        for i in range(len(child)):
            source = parent1[i] if random.random() < 0.5 else parent2[i]
            for pkg in source.packages:
                if pkg.id not in used_ids and child[i].total_weight() + pkg.weight <= child[i].capacity:
                    child[i].packages.append(pkg)
                    used_ids.add(pkg.id)
        return child if len(used_ids) == len(packages) else None

    def mutate(indiv):
        all_packages = [pkg for v in indiv for pkg in v.packages]
        random.shuffle(all_packages)
        for v in indiv:
            v.packages.clear()
        used_ids = set()
        for pkg in all_packages:
            for v in sorted(indiv, key=lambda v: v.total_weight()):
                if pkg.id not in used_ids and v.can_add(pkg):
                    v.packages.append(pkg)
                    used_ids.add(pkg.id)
                    break

  
    population = []
    attempts = 0
    while len(population) < population_size and attempts < 200:
        indiv = create_individual()
        if indiv:
            population.append(indiv)
        attempts += 1

    if not population:
        raise Exception("Failed to initialize a valid population. Check vehicle capacities or input size.")

    for _ in range(generations):
        population.sort(key=total_cost)
        next_generation = population[:10]
        while len(next_generation) < population_size:
            p1, p2 = random.sample(population[:25], 2)
            child = crossover(p1, p2)
            if child:
                mutate(child)
                if len(get_used_package_ids(child)) == len(packages):
                    next_generation.append(child)
        population = next_generation

    best = min(population, key=total_cost)
    return best
