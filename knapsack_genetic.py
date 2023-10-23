import random

# create items with random weights and profits
#items struct: [(item_id, weight, profit)]
n = 3
max_weight = 2700
def create_items(n, max_weight):
	items = []
	for i in range(n):
		weight = random.randrange(1,max_weight)
		profit = random.randint(1,100)
		items.append((i,weight,profit))
	return items 
items = [(1,2200,500), (2,160,150), (3, 350, 60), (4, 333, 40), (5, 192,30)]
#create a population of random genomes
#genome: [] -> len of items
#0 -> item not included, 1 -> item included
population_size = 10
def create_population():
	genomes = []
	for i in range(population_size):
		genome = random.choices([0,1], k=len(items))
		if genome not in genomes:
			genomes.append(genome)
	return genomes
#compute the fitness of each genome in the population
#fitness -> total profit of each genome in the population
# if total weight is greater than max_weight -> fitness becomes zero 
def compute_fitness(population):
	fitness = {}
	for i in population: 
		weight = 0 
		profit = 0
		value = 0
		for j,item in enumerate(items):
			if i[j] == 1:
				weight += item[1]
				profit += item[2]
		if weight > max_weight:
			value = 0
		else:
			value = profit
		fitness.update({tuple(i): value})
	return fitness 
#simulate natural selection
#genomes with higher fitness are more likely to be selected
#should return two genomes for reproduction and mutation
def selection(fitness, population):
	fitnesses = []
	for i in fitness.items():
		fitnesses.append(i[1])
	return random.choices(population, weights=fitnesses, k=2)

#reproduce with single-point crossover
#two new genomes created with last 4 bits exchanged
#new generation with same size population
def single_point_crossover(population, fitness):
	new_population = []
	max_profit = 0
	while len(new_population) != population_size:
		parents = selection(fitness, population)
		new_genome1 = parents[0][:(len(parents[0])-4)] + parents[1][-4:]
		new_genome2 = parents[1][:(len(parents[1])-4)] + parents[0][-4:]
		new_population.append(new_genome1)
		new_population.append(new_genome2)
		if len(new_population) == (population_size-2):	
			break
	fitness_cp = fitness 
	index = 0
	for i in fitness_cp.items():
		if i[1] > max_profit:
			max_profit = i[1]
	for i in fitness_cp:
		if fitness_cp[i] == max_profit:
			new_population.append(list(i))
			index = i 
	del fitness_cp[index]
	max_profit = 0
	for i in fitness_cp.items():
		if i[1] > max_profit:
			max_profit = i[1]
	for i in fitness_cp:
		if fitness_cp[i] == max_profit:
			new_population.append(list(i))
	return new_population
#Mutate the new population to generate better answers
#mutate -> flip the bits at three random positions
#compute the fitness

def mutate(new_population):
	for i in new_population:
		index1 = random.randrange(len(i))
		if i[index1] == 0:
			i[index1] = 1
		else:
			i[index1] = 0
		index2 = random.randrange(len(i))
		if i[index2] == 0:
			i[index2] = 1
		else:
			i[index2] = 0
	return new_population

def maximum(fitness):
	max_profit = 0
	index = 0
	for i in fitness.items():
		if i[1] > max_profit:
			max_profit = i[1]
			index = i[0]
	return max_profit,index

def main():
	max_generations = 10
	max_profits = []
	index=0
	for i in range(max_generations):
		population = create_population()
		fitness = compute_fitness(population)
		max_profit,index = maximum(fitness)
		new_population = single_point_crossover(population, fitness)
		new_population = mutate(new_population)
		fitness2 = compute_fitness(new_population)
		max_profit,index = maximum(fitness2)
		max_profits.append((max_profit, index))
		print(f"Generation {i}: {max_profit}")
	print("*******************")
	print(f"Maximum Achieved: {max(max_profits, key=lambda x:x[0])}")
	print("*******************")
main()

