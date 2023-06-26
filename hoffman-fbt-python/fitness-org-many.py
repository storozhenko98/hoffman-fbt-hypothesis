import random

def foodGen():
    return random.randint(0, 15)

def worldGenerator():
    size = 10
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
            raw_gain = each[2] + hp
            
            # Simplifying the perception of gains
            if raw_gain < 5:
                gain = 1
            elif raw_gain < 8:
                gain = 2
            else:
                gain = 3
            
            rep = [each[0], each[1], gain, each[2]] # Adding actual food resource value
            gains.append(rep)
        gains.sort(key=lambda x: x[2])
        return gains[-1]
    
    def cycle(self, world, organisms):
        decision = self.decide(world)
        hp = self.get_health()
        moveCost = (abs(decision[0]) + abs(decision[1])) // 3
        
        # Using actual food resource value for health
        actual_food_resource = decision[3]
        hp = actual_food_resource + hp - moveCost
        
        if hp <= 0:
            organisms.remove(self)
            return
        
        self.set_health(hp)
        
        if hp >= 9:
            self.reproduce(organisms)
        
        for cell in world:
            if cell[0] == decision[0] and cell[1] == decision[1]:
                cell[2] = 0
    
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
