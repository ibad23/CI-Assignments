import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.ticker import FuncFormatter

# Read the matrices from files
def read_matrix(file_name):
    with open(file_name, "r") as f:
        return np.array([[int(x) for x in line.split()] for line in f])

facilities = []
locations = []

# Initial parameters - as described in PDF
alpha = 1
beta = 1
gamma = 0.8
no_of_ants = 20
no_of_iterations = 500
Q = 1

# alpha = 1.5
# beta = 0.2
# gamma = 0.2
# no_of_ants = 500
# no_of_iterations = 1000
# Q = 1

# For record keeping
records = {}

def main():
    # Read the matrices from files
    distance_matrix = read_matrix("src/distance_matrix.txt")
    flow_matrix = read_matrix("src/flow_matrix.txt")

    # Initialize the pheromone and heuristic matrix
    pheromone_matrix = np.ones_like(distance_matrix)
    heuristic_matrix = 1 / (
        distance_matrix
    )
    heuristic_matrix = np.nan_to_num(heuristic_matrix, nan=0.0, posinf=0.0, neginf=0.0)

    # Initialize best solution and cost
    best_sol = None
    best_cost = float("inf")

    # Break if no convergence - need a few vars
    no_improvement_count = 0
    conv_thresh = 100
    min_improvement = 0
    # If the best cost does not improve at all for 50 iterations, stop the algorithm

    for iteration in range(no_of_iterations):
        all_sols = []
        all_costs = []

        # Create solutions for each ant
        for ant in range(no_of_ants):
            if iteration == 0:
                sol = random_sol(len(pheromone_matrix))
            else:
                sol = create_sol(pheromone_matrix, heuristic_matrix)
            cost = total_cost(sol, distance_matrix, flow_matrix)
            all_sols.append(sol)
            all_costs.append(cost)

        # Update best solution
        best_sol_idx = np.argmin(all_costs)
        best_sol_itr = all_sols[best_sol_idx]
        best_cost_itr = all_costs[best_sol_idx]

        # Check for improvement
        if best_cost_itr < best_cost * (1 - min_improvement):
            best_cost = best_cost_itr
            best_sol = best_sol_itr
            no_improvement_count = 0  # Reset the counter
        else:
            no_improvement_count += 1  # Increment the counter

        if best_cost_itr < best_cost:
            best_cost = best_cost_itr
            best_sol = best_sol_itr

        # Update pheromones
        pheromone_matrix = update_pheromones(
            pheromone_matrix, all_sols, all_costs, gamma, Q
        )

        # Record best and average cost
        records[iteration] = (best_cost, np.mean(all_costs))

        if no_improvement_count >= conv_thresh:
            print("Convergence detected. Stopping early")
            print()
            print(records)
            plot_results(records)
            break


def random_sol(n):
    sol = list([i for i in range(n)])
    random.shuffle(sol)
    return sol

def create_sol(pheromone_matrix, heuristic_matrix):
    n = len(pheromone_matrix)
    unassigned_facilities = list(range(n))
    unassigned_locations = list(range(n))
    sol = [0] * n

    while unassigned_facilities:
        fac = unassigned_facilities.pop(0)

        # Calculate probabilities
        prob = np.zeros(len(unassigned_locations))
        for loc in range(len(unassigned_locations)):
            l = unassigned_locations[loc]
            prob[loc] = (
                pheromone_matrix[fac][l] ** alpha * heuristic_matrix[fac][l] ** beta
            )

        # Add a small constant to avoid division by zero
        prob = prob + 1e-10
        prob = prob / np.sum(prob)

        # Choose a location based on probabilities
        pick = np.random.choice(unassigned_locations, p=prob)
        sol[fac] = pick
        unassigned_locations.remove(pick)

    return sol

# Calculate the total cost of a solution
def total_cost(sol, distance_matrix, flow_matrix):
    cost = 0
    n = len(sol)
    for i in range(n):
        for j in range(n):
            cost += flow_matrix[i][j] * distance_matrix[sol[i]][sol[j]]
    return cost

def update_pheromones(pheromone_matrix, all_sols, all_costs, gamma, Q):
    # Evaporation
    pheromone_matrix = (1 - gamma) * pheromone_matrix

    # Deposit pheromones for top 50% solutions
    top_solutions = np.argsort(all_costs)[: int(1 * len(all_costs))]

    # Weighted pheromone update
    for rank, sol_idx in enumerate(top_solutions):
        sol = all_sols[sol_idx]
        cost = all_costs[sol_idx]
        weight = (len(top_solutions) - rank) / len(top_solutions)  # Higher rank gets more weight
        for i in range(len(sol)):
            pheromone_matrix[i][sol[i]] += weight * (Q / cost)

    return pheromone_matrix

# Compress the solution matrix into a list of facilities
def compress_sol(sol_matrix):
    s = []
    for i in range(len(sol_matrix)):
        for j in range(len(sol_matrix)):
            if sol_matrix[i][j] == 1:
                s.append(j+1)
    return s


def plot_results(records):
    # Plot two graphs, one for best cost and one for average cost
    x = list(records.keys())
    y1 = [records[k][0] for k in records]
    y2 = [records[k][1] for k in records]

    plt.plot(x, y1, label="Best cost", color="red")
    plt.plot(x, y2, label="Average cost", color="blue")

    # Format the y-axis to show values in millions
    def millions_formatter(x, pos):
        return f"{x / 1e6:.1f}"  # Divide by 1e6 and add 'M' for millions

    plt.gca().yaxis.set_major_formatter(FuncFormatter(millions_formatter))

    plt.legend()
    plt.xlabel("Iteration")
    plt.ylabel("Cost (Million)")
    # plt.grid(True)

    plt.title("Best and average cost over iterations")

    # plt.show()
    plt.savefig("src/plot_2.png")


if __name__ == "__main__":
    main()
