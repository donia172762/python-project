def euclidean_distance(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

def route_cost(route):
    # route = [pkg1, pkg2, ...]
    x0, y0 = 0, 0  # موقع المحل
    cost = 0
    for pkg in route:
        cost += euclidean_distance(x0, y0, pkg.x, pkg.y)
        x0, y0 = pkg.x, pkg.y
    cost += euclidean_distance(x0, y0, 0, 0)  # الرجوع للمحل
    return cost

def total_cost(vehicles, penalty_per_empty_vehicle=20): 
    total_distance = 0
    empty_count = 0

    for v in vehicles:
        if not v.packages:
            empty_count += 1
            continue
        x_prev, y_prev = 0, 0
        for pkg in v.packages:
            total_distance += euclidean_distance(x_prev, y_prev, pkg.x, pkg.y)
            x_prev, y_prev = pkg.x, pkg.y
        total_distance += euclidean_distance(x_prev, y_prev, 0, 0)

    penalty = empty_count * penalty_per_empty_vehicle
    return total_distance + penalty