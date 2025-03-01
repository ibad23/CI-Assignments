import random

class selection_schemes:
    """
    This class contains the five selection schemes for parent and survival selection
    """
    @staticmethod
    def fitness_proportional(population, fitness_values, num_parents):
        """
        Select chorosomes based on fitness proportional selection, 
        where the probability of selecting a chorosomes is proportional to its fitness value
        """
        total_fitness = sum(fitness_values)
        probabilities = [fitness/total_fitness for fitness in fitness_values]
        parents = random.choices(population, probabilities, k=num_parents)
        return parents
    
    @staticmethod
    def binary_tournament(population, fitness_values, num_parents):
        """
        Select chorosomes based on binary tournament selection, 
        where two chorosomes are selected and the one with the higher fitness value is selected
        """
        parents = []
        for i in range(num_parents):
            parent1_index = random.randint(0, len(population) - 1)
            parent2_index = random.randint(0, len(population) - 1)
            
            parent1 = population[parent1_index]
            parent2 = population[parent2_index]

            # fight
            if fitness_values[parent1_index] > fitness_values[parent2_index]:
                parents.append(parent1)
            else:
                parents.append(parent2)

        return parents
    
    @staticmethod
    def rank_based(population, fitness_values, num_parents):
        """
        Select chorosomes based on rank based selection,
        where the probability of selecting a chorosomes is proportional to its rank in the population
        """
        sorted_population = sorted(population, key=lambda x: fitness_values[population.index(x)])
        probabilties = list(map(lambda x: x / len(population), range(1, len(population) + 1)))
        parents = random.choices(sorted_population, probabilties, k=num_parents)
        return parents
    
    @staticmethod
    def truncation(population, fitness_values, num_parents):
        """
        Select chorosomes based on truncation selection,
        where always the best chorosomes are picked based on their fitness values 
        """
        sorted_population = sorted(population, key=lambda x: fitness_values[population.index(x)], reverse=True)
        return sorted_population[:num_parents]
    
    @staticmethod
    def random_selection(population, fitness_values, num_parents):
        """
        Select chorosomes based on random selection,
        where chorosomes are selected randomly from the population
        """
        return random.choices(population, k=num_parents)