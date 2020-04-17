import numpy as np
import math
import random
from time import time
import signal

start = time()
cities = []
points = []

with open('./mat-test.txt') as f:
    for line in f.readlines():
        city = line.split(' ')
        cities.append(dict(index=int(city[0]), x=float(city[1]), y=float(city[2])))
        points.append((float(city[1]), float(city[2])))

distances = np.empty((len(points), len(points)))
for i in range(len(points)):
    for j in range(len(points)):
        distances[i,j] = round(math.sqrt(
                ((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2)))

def pathCost(path):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += distances[path[i], path[i+1]]
    total_distance += distances[path[len(path) - 1], path[0]]
    return total_distance

def nearest_neighbor():
    length = len(points)
    free_nodes = []
    for i in range(length):
        free_nodes.append(i)
    curr = random.randint(0,length-1)
    free_nodes.remove(curr)
    solution = [curr]
    while free_nodes:
        next = min(free_nodes, key=lambda x: distances[curr, x])
        free_nodes.remove(next)
        solution.append(next)
        curr = next
    return solution

def next_state(path):
    new_path = list(path)
    l = random.randint(1, len(path) - 1)
    i = random.randint(1, len(path) - l)
    new_path[i: (i + l)] = reversed(new_path[i: (i + l)])
    return new_path

def simulated_annealing(temp):
    current_route = nearest_neighbor()
    best_route = current_route
    temperature = temp
    best_temperature = temperature
    explored = []
    explored.append(current_route)
    for iter in range(50000):
        new_route = next_state(current_route)
        if new_route not in explored and temperature >= .00001:
            explored.append(new_route)
            currentCost = pathCost(current_route)
            newCost = pathCost(new_route)
            if newCost < currentCost:
                current_route = new_route
            else:
                delta = newCost - currentCost
                probability = math.exp(-delta / temp)
                if probability >= np.random.rand():
                    current_route = new_route
            if pathCost(current_route) < pathCost(best_route):
                best_route = current_route
                best_temperature = temperature
            temperature *= 0.9995

    return pathCost(best_route), best_route

cost = simulated_annealing(1)

def _handle_timeout(signum, frame):
    print(cost)
    exit()
signal.signal(signal.SIGALRM, _handle_timeout)
signal.alarm(int(start + 180 - time()))
while True:
    new_cost = simulated_annealing(1)
    if new_cost < cost:
        cost = new_cost
