import random

# Function for generating food in a cell
def foodGen():
    return random.randint(0, 15) # Returns a random integer between 0 and 15

# Function for generating the world as a grid with food in each cell
def worldGenerator():
    size = 10 # Size of the grid
    world = []
    for x in range(-size // 2, size // 2 + 1):
        for y in range(-size // 2, size // 2 + 1):
            world.append([x, y, foodGen()]) # Each cell has x and y coordinates and a food value
    return world

# Base class for an organism
class BaseOrganism:
    id_counter = 1
    
    def __init__(self, health, name):
        self.health = health
        self.name = f"{name}_{BaseOrganism.id_counter}"
        BaseOrganism.id_counter += 1
    
    def get_health(self):
        return self.health
    
    def set_health(self, value):
        self.health = value
    
    def reproduce(self, organisms):
        hp = self.get_health()
        self.set_health(hp // 2)
        # The type(self) ensures that the offspring is the same type as the parent (Truth or Fitness seeing)
        new_org = type(self)(hp // 2, "child_of_" + self.name)
        organisms.append(new_org)

# Class for truth-seeing organism
class TruthOrganism(BaseOrganism):
    
    def decide(self, world):
        hp = self.get_health()
        gains = []
        for each in world:
            gain = each[2] + hp
            if gain > 10:
                surplus = gain - 10
                gain = 10 - surplus
            rep = [each[0], each[1], gain]
            gains.append(rep)
        gains.sort(key=lambda x: x[2])
        return gains[-1]
    
    def cycle(self, world, organisms):
        decision = self.decide(world)
        hp = self.get_health()
        moveCost = (abs(decision[0]) + abs(decision[1])) // 3
        hp = decision[2] - moveCost - 1 # Cost of seeing the full truth
        
        if hp <= 0:
            organisms.remove(self)
            return
        
        self.set_health(hp)
        
        if hp >= 9:
            self.reproduce(organisms)
        
        for cell in world:
            if cell[0] == decision[0] and cell[1] == decision[1]:
                cell[2] = 0 # consume the food

# Class for fitness-seeing organism
class FitnessOrganism(BaseOrganism):
    
    def decide(self, world):
        hp = self.get_health()
        gains = []
        for each in world:
            raw_gain = each[2] + hp
            if raw_gain > 10:
                surplus = raw_gain - 10
                raw_gain = 10 - surplus
            if raw_gain < 5:
                gain = 1
            elif raw_gain < 8:
                gain = 2
            else:
                gain = 3
            rep = [each[0], each[1], gain, each[2]] # Simplified perception
            gains.append(rep)
        gains.sort(key=lambda x: x[2])
        return gains[-1]
    
    def cycle(self, world, organisms):
        decision = self.decide(world)
        hp = self.get_health()
        moveCost = (abs(decision[0]) + abs(decision[1])) // 3
        hp = decision[3] + hp - moveCost # Using actual food resource value for health
        
        if hp <= 0:
            organisms.remove(self)
            return
        
        self.set_health(hp)
        
        if hp >= 9:
            self.reproduce(organisms)
        
        for cell in world:
            if cell[0] == decision[0] and cell[1] == decision[1]:
                cell[2] = 0 # consume the food

# Running the simulation
def run_simulation(num_cycles):
    total_truth_organisms = 0
    total_fitness_organisms = 0
    num_simulations = 100
    for sim in range(num_simulations):
        BaseOrganism.id_counter = 1 # Reset ID counter for each simulation
        truth_organisms = [TruthOrganism(2, "TruthOrganism")]
        fitness_organisms = [FitnessOrganism(2, "FitnessOrganism")]
        for i in range(num_cycles):
            world = worldGenerator()
            for org in list(truth_organisms):
                org.cycle(world, truth_organisms)
            for org in list(fitness_organisms):
                org.cycle(world, fitness_organisms)
        total_truth_organisms += len(truth_organisms)
        total_fitness_organisms += len(fitness_organisms)
    
    average_truth_organisms = total_truth_organisms / num_simulations
    average_fitness_organisms = total_fitness_organisms / num_simulations
    print(f"Average number of surviving truth-seeing organisms over {num_simulations} simulations: {average_truth_organisms}")
    print(f"Average number of surviving fitness-seeing organisms over {num_simulations} simulations: {average_fitness_organisms}")

run_simulation(100)
