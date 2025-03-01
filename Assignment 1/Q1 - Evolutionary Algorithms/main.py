from Problems.tsp import *
from Problems.jssp import *
from EA.evolutionary_algorithm import *
from EA.selection_schemes import *
from matplotlib import pyplot as plt

selection_schemes_list = ["fitness_proportional", "binary_tournament", "rank_based", "truncation", "random_selection"]
selection_schemes_dict = {selection_schemes_list[i]: i for i in range(len(selection_schemes_list))}

# all combinations of parent and survivor selection schemes
combination_list = [(i, j) for i in range(len(selection_schemes_list)) for j in range(len(selection_schemes_list))]

def plot(num_generations, avg_of_best_fitness, avg_of_avg_fitness, parent_selection_scheme, survival_selection_scheme, file_path):
    plt.plot(range(num_generations), avg_of_best_fitness, color='blue')
    plt.plot(range(num_generations), avg_of_avg_fitness, color='orange')
    plt.legend(["Average Best Fitness", "Average Average Fitness"])
    plt.title(f"{parent_selection_scheme} Parent Selection : {survival_selection_scheme} Survivor Selection")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    # annotate the best & average fitness value at the end of the run
    plt.annotate(f"{avg_of_best_fitness[-1]:.2f}", (len(avg_of_avg_fitness)-1, avg_of_best_fitness[-1]), textcoords="offset points", xytext=(0,-20), ha='center', arrowprops=dict(arrowstyle="->", color='blue'))
    plt.annotate(f"{avg_of_avg_fitness[-1]:.2f}", (len(avg_of_avg_fitness)-1, avg_of_avg_fitness[-1]), textcoords="offset points", xytext=(0,10), ha='center', arrowprops=dict(arrowstyle="->", color='orange'))
    plt.savefig(f"Plots/{file_path[5:-4]}/{parent_selection_scheme} ; {survival_selection_scheme}.png")
    plt.close()

def run_tsp(parent_selection_string, survival_selection_string, file_path):

    parent_selection_scheme = selection_schemes_list[selection_schemes_dict[parent_selection_string]]
    survival_selection_scheme = selection_schemes_list[selection_schemes_dict[survival_selection_string]]

    average_fitness_values = []
    best_fitness_values = []

    for i in range(num_iterations):

        tsp_instance = tsp(file_path)    
        ea = evolutionary_algorithm(tsp_instance)

        # Hall of Fame
        avg_fitness_per_gen = []
        best_fitness_per_gen = []
        
        for _ in range(num_generations):

            best_fitness_value = abs(ea.best_fitness_score())
            avg_fitness_value = abs(ea.avg_fitness_score())
            
            print(f"Generation {ea.generations_count} completed ; Best Fitness: {best_fitness_value} ; Average Fitness: {avg_fitness_value}")

            ea.parent_selection(parent_selection_scheme)
            ea.survival_selection(survival_selection_scheme)

            best_fitness_per_gen.append(best_fitness_value)
            avg_fitness_per_gen.append(avg_fitness_value)
        
        average_fitness_values.append(avg_fitness_per_gen)
        best_fitness_values.append(best_fitness_per_gen)

        print(f"\nIteration {i+1} completed ; Best Fitness: {best_fitness_per_gen[-1]} ; Average Fitness: {avg_fitness_per_gen[-1]}\n")

    avg_of_best_fitness = [sum(x) / len(x) for x in zip(*best_fitness_values)]
    avg_of_avg_fitness = [sum(x) / len(x) for x in zip(*average_fitness_values)]

    plot(num_generations, avg_of_best_fitness, avg_of_avg_fitness, parent_selection_scheme, survival_selection_scheme, file_path)

def run_tssp(parent_selection_string, survival_selection_string, file_path):

    parent_selection_scheme = selection_schemes_list[selection_schemes_dict[parent_selection_string]]
    survival_selection_scheme = selection_schemes_list[selection_schemes_dict[survival_selection_string]]

    average_fitness_values = []
    best_fitness_values = []

    for i in range(num_iterations):

        jssp_instance = jssp(file_path)
        ea = evolutionary_algorithm(jssp_instance)

        # Hall of Fame
        avg_fitness_per_gen = []
        best_fitness_per_gen = []
        
        for _ in range(num_generations):

            best_fitness_value = abs(ea.best_fitness_score())
            avg_fitness_value = abs(ea.avg_fitness_score())
            
            print(f"Generation {ea.generations_count} completed ; Best Fitness: {best_fitness_value} ; Average Fitness: {avg_fitness_value}")

            ea.parent_selection(parent_selection_scheme)
            ea.survival_selection(survival_selection_scheme)

            best_fitness_per_gen.append(best_fitness_value)
            avg_fitness_per_gen.append(avg_fitness_value)
        
        average_fitness_values.append(avg_fitness_per_gen)
        best_fitness_values.append(best_fitness_per_gen)

        print(f"\nIteration {i+1} completed ; Best Fitness: {best_fitness_per_gen[-1]} ; Average Fitness: {avg_fitness_per_gen[-1]}\n")

    avg_of_best_fitness = [sum(x) / len(x) for x in zip(*best_fitness_values)]
    avg_of_avg_fitness = [sum(x) / len(x) for x in zip(*average_fitness_values)]

    plot(num_generations, avg_of_best_fitness, avg_of_avg_fitness, parent_selection_scheme, survival_selection_scheme, file_path)

def main():
    """
    Run the TSP or JSSP problem for all combinations of parent and survivor selection schemes,
    and plot the average best and average fitness values for each combination
    and save the plot as a .png file
    """
    for combination in combination_list:
        parent_selection_string = selection_schemes_list[combination[0]]
        survival_selection_string = selection_schemes_list[combination[1]]
        
        # run_tsp(parent_selection_string, survival_selection_string, "Data/qa194.tsp")

        # run_tssp(parent_selection_string, survival_selection_string, "Data/ft10.txt") # known optimal solution: 930
        # run_tssp(parent_selection_string, survival_selection_string, "Data/abz7.txt") # known optimal solution: 655
        run_tssp(parent_selection_string, survival_selection_string, "Data/la19.txt") # known optimal solution: 842

if __name__ == "__main__":
    main()