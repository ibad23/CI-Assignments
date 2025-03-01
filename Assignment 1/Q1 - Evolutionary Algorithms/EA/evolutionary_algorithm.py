from EA.selection_schemes import selection_schemes

# Parameters
population_size = 500
num_generations = 1000
mutation_rate = 1.0
num_offspring = 70
num_iterations = 1

class evolutionary_algorithm:
    """
    This class implements the evolutionary algorithm for a generic problem.
    """
    def __init__(self, problem):
        """
        initialize the evolutionary algorithm with the problem instance and its population.
        """
        self.problem = problem
        self.population = self.problem.population
        self.fitness_values = self.problem.fitness_values
        self.generations_count = 1
    
    def best_fitness_score(self):
        """
        return the best fitness score in the population.
        """
        return max(self.fitness_values)
    
    def best_chromosome(self):
        """
        return the best chromosome in the population.
        """
        return self.population[self.fitness_values.index(self.best_fitness_score())]
    
    def worst_fitness_score(self):
        """
        return the worst fitness score in the population.
        """
        return min(self.fitness_values)
    
    def worst_chromosome(self):
        """
        return the worst chromosome in the population.
        """
        return self.population[self.fitness_values.index(self.worst_fitness_score())]
    
    def avg_fitness_score(self):
        """
        return the average fitness score in the population.
        """
        return sum(self.fitness_values) / len(self.fitness_values)

    def parent_selection(self, selection):
        """
        selects parents from the population using the selection scheme,
        and generates two offspring using crossover and mutation,
        and adds them to the population.
        """
        selection_method = getattr(selection_schemes, selection)
        parents = selection_method(self.population, self.fitness_values, num_offspring)

        # mutation and crossover happens here
        for i in range(0, num_offspring, 2):
            child1 = self.problem.crossover(parents[i], parents[i + 1])
            child1 = self.problem.mutation(mutation_rate, child1)

            child2 = self.problem.crossover(parents[i], parents[i + 1])
            child2 = self.problem.mutation(mutation_rate, child2)

            self.population.append(child1)
            self.population.append(child2)
        
    def survival_selection(self, selection):
        """
        selects the best chromosomes from the population using the selection scheme,
        and replaces the population with the new generation.

        Note: Elitism is used here, the best chromosome is kept in the population,
        to ensure that the best solution is not lost.
        """
        self.problem.population = self.population
        self.problem.fitness_values = self.fitness_values = self.problem.fitness_function()

        selection_method = getattr(selection_schemes, selection)
        new_generation = selection_method(self.population, self.problem.fitness_values, population_size - 1)

        # Elitism - keep the best choromosome
        new_generation.append(self.best_chromosome())

        self.population = new_generation
        self.problem.population = self.population
        self.problem.fitness_values = self.fitness_values = self.problem.fitness_function()
        self.generations_count += 1