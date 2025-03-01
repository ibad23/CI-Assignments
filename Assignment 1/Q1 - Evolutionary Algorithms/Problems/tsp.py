from Problems.problem import problem
import random
from EA.evolutionary_algorithm import *

class tsp(problem):
    """
    This class represents the Travelling Salesman Problem (TSP) 
    and inherits from the problem class.
    """
    def __init__(self, file):
        self.cities = {} # immutable dictionary
        self.load_data(file)

        # generate a population and calculate the fitness values
        self.population = self.generate_population()
        self.fitness_values = self.fitness_function()
    
    def load_data(self, file):
        """
        Load the data from the .tsp file
        and store it in the cities dictionary,
        where the key is the city number and 
        the value is a tuple containing the x and y coordinates.
        """
        with open(file) as f:
            for city in f.readlines()[7:-1]:
                city = city.split()
                self.cities[int(city[0])] = (float(city[1]), float(city[2]))
        f.close()
    
    def chromosome(self):
        """
        Generate and return a random chromosome
        """
        return random.sample(sorted(self.cities.keys()), len(self.cities))

    def generate_population(self):
        """
        Generate and return a random population of chromosomes
        """
        local_population = []
        for i in range(population_size):
            local_population.append(self.chromosome())
        return local_population

    def distance_formula(self, city1, city2):
        """
        Calculate the distance between two cities
        using the Euclidean distance formula
        """
        x1, y1 = self.cities[city1]
        x2, y2 = self.cities[city2]
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    
    def total_distance(self, chromosome):
        """
        Calculate the total distance of a chromosome
        by summing the distances between the cities,
        basically the fitness function for a single candidate solution.
        """
        total_distance = 0
        for i in range(len(chromosome) - 1):
            total_distance += self.distance_formula(chromosome[i], chromosome[i + 1])
        total_distance += self.distance_formula(chromosome[0], chromosome[-1]) # cycle back to the first city
        return total_distance*-1 # fitness function is negative of total distance, so that we can maximize it
    
    def fitness_function(self):
        """
        Calculate the fitness values for the entire population
        """
        return list(map(self.total_distance, self.population))

    def crossover(self, parent1, parent2):
        """
        Perform the crossover operation between two parents
        and return the child chromosome.

        We are performing the Crossover by selecting a sequence of genes from parent1,
        and then filling the remaining genes from parent2 in the order they appear.
        """
        gene1 = random.randint(0, len(parent1) - 1)
        gene2 = random.randint(0, len(parent2) - 1)

        start_gene = min(gene1, gene2)
        end_gene = max(gene1, gene2)

        child1 = parent1[start_gene:end_gene]
        child2 = [city for city in parent2 if city not in child1]
        child = child1 + child2

        return child
    
    def mutation(self, rate, chromosome):
        """
        Perform the mutation operation on a chromosome
        by swapping two random genes with a probability of rate (mutation rate).
        """
        if random.random() < rate:
            gene1 = random.randint(0, len(chromosome) - 1)
            gene2 = random.randint(0, len(chromosome) - 1)
            
            chromosome[gene1], chromosome[gene2] = chromosome[gene2], chromosome[gene1]

        return chromosome