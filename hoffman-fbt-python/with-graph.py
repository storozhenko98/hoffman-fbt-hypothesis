# Importing required libraries
import numpy as np
import matplotlib.pyplot as plt

# Define the Organism class
class Organism:
    # Constructor for the Organism class, takes the type ('truth_seer' or 'fitness_seer') as input
    def __init__(self, type):
        self.type = type  # Sets the type of the organism
        self.energy = 10  # Sets the initial energy level of the organism

    # Define how the organism perceives the environment based on its type
    def perceive_environment(self, true_resources):
        if self.type == 'truth_seer':  # If the organism is a truth_seer
            return true_resources  # It perceives the true resource levels
        elif self.type == 'fitness_seer':  # If the organism is a fitness_seer
            return np.sqrt(true_resources) + 0.1  # It perceives a slightly biased version of the resource levels

    # Define the actions the organism takes based on the perceived resources
    def take_action(self, perceived_resources):
        if perceived_resources > 0.5:  # If perceived resources are above a threshold
            self.energy += 3  # Increase energy
        else:
            self.energy -= 1  # Decrease energy

    # Define the reproduction behavior of the organism
    def reproduce(self):
        if self.energy > 15:  # If energy is above a certain threshold
            self.energy -= 7  # Energy cost for reproduction
            return Organism(self.type)  # Create a new organism of the same type
        else:
            return None

# Set simulation parameters
num_time_steps = 200  # Number of time steps in the simulation
num_organisms = 200  # Initial number of organisms
max_population = 1000  # Maximum population size
environment_size = 100  # Size of the environment (used for generating resource levels)

# Initialize the list of organisms
organisms = [Organism('truth_seer') if i < num_organisms / 2 else Organism('fitness_seer') for i in range(num_organisms)]

# Initialize lists to store population counts of each type of organism
truth_seer_count = [num_organisms / 2]
fitness_seer_count = [num_organisms / 2]

# Run the simulation over the defined number of time steps
for t in range(num_time_steps):
    # Generate a variable resource distribution for the environment
    true_resources = np.random.random(environment_size) + (np.sin(t / 10) + 1) / 2

    # Temporary list to store new organisms from reproduction
    new_organisms = []

    # Loop through each organism
    for organism in organisms:
        # Organism perceives the environment
        perceived_resources = organism.perceive_environment(true_resources[0])
        # Organism takes action based on perceived resources
        organism.take_action(perceived_resources)
        
        # Organism tries to reproduce
        offspring = organism.reproduce()
        # If reproduction is successful, add offspring to the new_organisms list
        if offspring:
            new_organisms.append(offspring)

    # Add new organisms to the main list
    organisms.extend(new_organisms)

    # Remove dead organisms (energy <= 0)
    organisms = [organism for organism in organisms if organism.energy > 0]

    # Limit the population size to prevent runaway growth
    if len(organisms) > max_population:
        organisms = np.random.choice(organisms, max_population, replace=False).tolist()

    # Count the number of organisms of each type and store them in the lists
    truth_seer_count.append(sum(1 for organism in organisms if organism.type == 'truth_seer'))
    fitness_seer_count.append(sum(1 for organism in organisms if organism.type == 'fitness_seer'))

# Plot the results
plt.plot(truth_seer_count, label="Truth Seers")  # Plot the population of truth_seers over time
plt.plot(fitness_seer_count, label="Fitness Seers")  # Plot the population of fitness_seers over time
plt.xlabel("Time Steps")  # Label for the x-axis
plt.ylabel("Population Size")  # Label for the y-axis
plt.legend()  # Show the legend
plt.title("Truth-seers vs. Fitness-seers")  # Title of the plot
plt.show()  # Display the plot
