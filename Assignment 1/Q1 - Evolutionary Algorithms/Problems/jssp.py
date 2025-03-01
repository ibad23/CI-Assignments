from Problems.problem import problem
from EA.evolutionary_algorithm import *
import numpy as np # for random

class jssp(problem):
    """
    This class represents the Job Shop Scheduling Problem (JSSP) 
    and inherits from the problem class.
    """
    def __init__(self, file):
        self.data = []
        self.population = []
        self.makespan = []

        self.operations = []
        self.machines = []
        self.processing_time = []
        
        self.load_data(file)

        # generate a population and calculate the fitness values
        self.population = self.generate_population()
        self.fitness_values = self.fitness_function()

    def load_data(self, file_path):
        """
        Load the data from the .txt file
        and store it in the data list,
        where the key is the job number and
        the value is a list of tuples containing the machine number and the processing time.
        """
        with open(file_path, "r") as file:
            parameters = file.readline().strip().split()
            self.num_jobs = int(parameters[0])
            self.num_machines = int(parameters[1])
            for line in file:
                job_operations = []
                val = line.strip().split()
                for i in range(0, len(val), 2):
                    job_operations.append((int(val[i]), int(val[i+1])))
                self.data.append(job_operations)
        
        for i in range(self.num_jobs):
            job = []
            job_time = []
            for j in range(self.num_machines):
                job.append(self.data[i][j][0])
                job_time.append(self.data[i][j][1])
            self.machines.append(job)
            self.processing_time.append(job_time)

    def chromosome(self):
        """
        Generate and return a random chromosome
        """
        return list(np.random.permutation(self.num_machines * self.num_jobs) % self.num_jobs)
    
    def generate_population(self):
        """
        Generate and return a random population of chromosomes
        """
        local_population  = []
        for i in range(population_size):
            local_population.append(self.chromosome())
        return local_population
    
    def fitness_function(self):
        """
        Calculate the fitness values for the entire population
        """
        makespans = []
        for chromosome in self.population:
            job_completion_time = [0] * self.num_jobs
            machine_available_time = [0] * self.num_machines

            job_operation_index = [0] * self.num_jobs

            for gene in chromosome:
                job_id = gene
                operation_index = job_operation_index[job_id]
                machine_id, processing_time = self.data[job_id][operation_index]

                earliest_start_time = max(job_completion_time[job_id], machine_available_time[machine_id])
                completion_time = earliest_start_time + processing_time

                job_completion_time[job_id] = completion_time
                machine_available_time[machine_id] = completion_time
                job_operation_index[job_id] += 1
            
            makespan = max(job_completion_time)
            makespans.append(makespan * -1) # we want to minimize the makespan
    
        return makespans

    def crossover (self, parent1, parent2):
        """
        Perform the crossover operation on two parents
        by selecting a random segment from one parent and
        filling the missing genes with the genes from the other parent.
        """
        child = parent1[:]

        cutpoint = list(np.random.choice(len(parent1), 2, replace=False))
        cutpoint.sort()

        segment_p2 = parent2[cutpoint[0]:cutpoint[1]]

        child[cutpoint[0]:cutpoint[1]] = segment_p2

        for job_id in range(self.num_jobs):

            total_count_in_child = child.count(job_id)
            over_count = total_count_in_child - self.num_machines

            if over_count > 0:
                for i in range(over_count):
                    for idx in range(len(child)):
                        if child[idx] == job_id and not (cutpoint[0] <= idx < cutpoint[1]):
                            child[idx] = None
                            break
        
        for job_id in range(self.num_jobs):
            count_in_child = child.count(job_id)
            missing_count = self.num_machines - count_in_child
            none_positions = [idx for idx, val in enumerate(child) if val is None]

            for i in range(missing_count):
                child[none_positions[i]] = job_id

        return child
    
    def mutation(self, rate, chromosome):
        """
        Perform the mutation operation on a chromosome
        by swapping two random genes with a probability of rate (mutation rate).
        """
        mutation_prob = np.random.rand()
        if mutation_prob <= rate:

            index = list(np.random.choice(self.num_jobs, 2, replace=False))
            chromosome[index[0]], chromosome[index[1]] = chromosome[index[1]], chromosome[index[0]]
        
        return chromosome