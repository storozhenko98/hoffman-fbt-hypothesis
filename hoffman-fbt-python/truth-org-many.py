import random

def foodGen():
    return random.randint(0, 15)  # Generating a random integer between 0 and 15

def worldGenerator():
    size = 10  # Size of the grid
    world = []
    for x in range(-size // 2, size // 2 + 1):
        for y in range(-size // 2, size // 2 + 1):
            world.append([x, y, foodGen()])
    return world

class Organism:
    id_counter = 1
    
    def __init__(self, health, name):
        self.health = health
        self.name = f"{name}_{Organism.id_counter}"
        Organism.id_counter += 1
    
    def get_health(self):
        return self.health
    
    def set_health(self, value):
        self.health = value
    
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
        moveCost = (abs(decision[0]) + abs(decision[1]))//3
        hp = decision[2]
        hp = hp - moveCost
        hp = hp - 1 # Cost of seeing the full truth, since there are more steps in the representation 
        
        if hp <= 0:
            organisms.remove(self)
            return
        
        self.set_health(hp)
        
        if hp >= 9:
            self.reproduce(organisms)
        
        # Consume resource
        for cell in world:
            if cell[0] == decision[0] and cell[1] == decision[1]:
                cell[2] = 0 # set food to 0 in the cell where organism moved
    
    def reproduce(self, organisms):
        hp = self.get_health()
        self.set_health(hp // 2)
        new_org = Organism(hp // 2, "child_of_" + self.name)
        organisms.append(new_org)

def run_simulation(num_cycles):
    total_organisms = 0
    num_simulations = 100
    for sim in range(num_simulations):
        Organism.id_counter = 1
        organisms = [Organism(2, "Organism")]
        for i in range(num_cycles):
            world = worldGenerator()
            for org in list(organisms):
                org.cycle(world, organisms)
        total_organisms += len(organisms)

    average_organisms = total_organisms / num_simulations
    print(f"Average number of surviving organisms over {num_simulations} simulations: {average_organisms}")

run_simulation(100)
