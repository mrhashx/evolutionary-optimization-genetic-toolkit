from random import randint as rnd
from random import shuffle, random
import matplotlib.pyplot as plt  # Import matplotlib for plotting

N = 7  # Number of items
MAX_WEIGHT = 10  
objects = [(10, 2), (5, 3), (15, 5), (7, 7), (6, 1), (18, 4), (3, 1)]
POPULATION_SIZE = 200
MUTATION_RATE = 0.3
CROSSOVER_RATE = 0.7  
EPOCH = 200

class Item:
    def __init__(self, profit, weight):
        self.profit = profit
        self.weight = weight

def get_input(n, input_items=None, verbose=1):
    items = []
    if input_items is None:
        for i in range(n):
            print(f"Item #{i + 1}")
            item_profit = int(input("What is the profit of this item? "))
            item_weight = int(input("What is the weight of this item? "))
            items.append(Item(item_profit, item_weight))
        print("###########################################################")
    else:
        for item in input_items:
            items.append(Item(item[0], item[1]))
    if verbose:
        for item in items:
            print(f"Item #{items.index(item) + 1}: weight:{item.weight}  profit:{item.profit}")
    return items

def init_population(n, p):
    population_list = []
    for i in range(p):
        new_member = [0 for _ in range(n)] + [1 for _ in range(n)]
        shuffle(new_member)
        new_member = new_member[:n] + [None, None]
        population_list.append(new_member)
    return population_list

def cross_over(population_list, n, p, crossover_rate):
    for i in range(0, p, 2):
        # Check if crossover should happen based on crossover rate
        if random() < crossover_rate:
            child1 = population_list[i][:n // 2] + population_list[i + 1][n // 2:n] + [None, None]
            child2 = population_list[i + 1][:n // 2] + population_list[i][n // 2:n] + [None, None]
            population_list.append(child1)
            population_list.append(child2)
        else:
            # If no crossover, just copy parents to the next generation
            population_list.append(population_list[i].copy())
            population_list.append(population_list[i + 1].copy())
    return population_list

def mutation(population_list, n, p, m):
    chosen_ones = [i for i in range(p, p * 2)]
    shuffle(chosen_ones)
    chosen_ones = chosen_ones[:int(((p * 2) - 1) * m)]
    for i in chosen_ones:
        cell = rnd(0, n - 1)
        population_list[i][cell] = 1 if population_list[i][cell] == 0 else 0
    return population_list

def weight_total(bag, n, max_weight, items_list):
    total_weight = 0
    for i in range(n):
        if bag[i]:
            total_weight += items_list[i].weight
    return abs(max_weight - total_weight) if total_weight > max_weight else 200

def profit(bag, n, items_list):
    total_profit = 0
    for i in range(n):
        if bag[i]:
            total_profit += items_list[i].profit
    return total_profit

def fitness(population_list, n, p, items_list, max_weight):
    for i in range(p * 2):
        if population_list[i][n] is None or population_list[i][n + 1] is None:
            population_list[i][n] = weight_total(population_list[i], n, max_weight, items_list)
            population_list[i][n + 1] = profit(population_list[i], n, items_list)
    return population_list

def sorter(population_list, index1, index2):
    sorted_list = sorted(population_list, key=lambda x: (x[index1], -x[index2]))
    return sorted_list

if __name__ == "__main__":
    print(f"Max Weight is {MAX_WEIGHT}")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    items = get_input(N, input_items=objects, verbose=1)
    print("#######################################################")
    
    current_population = init_population(N, POPULATION_SIZE)
    
    # List to store the best profit values for each generation
    best_profits = []
    while EPOCH:
        current_population = cross_over(current_population, N, POPULATION_SIZE, CROSSOVER_RATE)
        current_population = mutation(current_population, N, POPULATION_SIZE, MUTATION_RATE)
        current_population = fitness(current_population, N, POPULATION_SIZE, items, MAX_WEIGHT)
        current_population = sorter(current_population, N, N + 1)
        current_population = current_population[:POPULATION_SIZE]
        
        # Append the best profit of the current generation to the list
        best_profits.append(current_population[-1][N + 1])  # Last element has the highest profit
        
        EPOCH -= 1
    else:
        # Sort the final population by profit (descending order)
        current_population = sorted(current_population, key=lambda x: x[N + 1], reverse=True)
        
        print("Best Found Solution (Sorted by Profit): ")
        for i in current_population:
            print(i)
    
    # Plotting the best profits over generations
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(best_profits)), best_profits, marker='o', linestyle='-', color='b')
    plt.title('Best Profit Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Best Profit')
    plt.grid(True)
    plt.show()