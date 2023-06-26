let idCounter = 1;

function foodGen() {
    return Math.floor(Math.random() * 16);
}

function worldGenerator() {
    const size = 10;
    const world = [];
    for (let x = -Math.floor(size / 2); x <= Math.floor(size / 2); x++) {
        for (let y = -Math.floor(size / 2); y <= Math.floor(size / 2); y++) {
            world.push([x, y, foodGen()]);
        }
    }
    return world;
}

class BaseOrganism {
    constructor(health, name) {
        this.health = health;
        this.name = `${name}_${idCounter}`;
        idCounter++;
    }

    getHealth() {
        return this.health;
    }

    setHealth(value) {
        this.health = value;
    }

    reproduce(organisms) {
        const hp = this.getHealth();
        this.setHealth(Math.floor(hp / 2));
        organisms.push(new this.constructor(Math.floor(hp / 2), `child_of_${this.name}`));
    }
}

class TruthOrganism extends BaseOrganism {
    decide(world) {
        const hp = this.getHealth();
        const gains = world.map(cell => {
            let gain = cell[2] + hp;
            if (gain > 10) {
                const surplus = gain - 10;
                gain = 10 - surplus;
            }
            return [cell[0], cell[1], gain];
        });
        gains.sort((a, b) => a[2] - b[2]);
        return gains[gains.length - 1];
    }

    cycle(world, organisms) {
        const decision = this.decide(world);
        let hp = decision[2] - Math.floor((Math.abs(decision[0]) + Math.abs(decision[1])) / 3) - 1;

        if (hp <= 0) {
            const index = organisms.indexOf(this);
            organisms.splice(index, 1);
            return;
        }

        this.setHealth(hp);

        if (hp >= 9) {
            this.reproduce(organisms);
        }

        world.forEach(cell => {
            if (cell[0] === decision[0] && cell[1] === decision[1]) {
                cell[2] = 0;
            }
        });
    }
}

class FitnessOrganism extends BaseOrganism {
    decide(world) {
        const hp = this.getHealth();
        const gains = world.map(cell => {
            const rawGain = cell[2] + hp;
            let gain;
            if (rawGain < 5) {
                gain = 1;
            } else if (rawGain < 8) {
                gain = 2;
            } else {
                gain = 3;
            }
            return [cell[0], cell[1], gain, cell[2]];
        });
        gains.sort((a, b) => a[2] - b[2]);
        return gains[gains.length - 1];
    }

    cycle(world, organisms) {
        const decision = this.decide(world);
        let hp = decision[3] + this.getHealth() - Math.floor((Math.abs(decision[0]) + Math.abs(decision[1])) / 3);

        if (hp <= 0) {
            const index = organisms.indexOf(this);
            organisms.splice(index, 1);
            return;
        }

        this.setHealth(hp);

        if (hp >= 9) {
            this.reproduce(organisms);
        }

        world.forEach(cell => {
            if (cell[0] === decision[0] && cell[1] === decision[1]) {
                cell[2] = 0;
            }
        });
    }
}

function runSimulation() {
    const numCycles = 100;
    const numSimulations = 100;
    let totalTruthOrganisms = 0;
    let totalFitnessOrganisms = 0;

    for (let sim = 0; sim < numSimulations; sim++) {
        idCounter = 1;
        const truthOrganisms = [new TruthOrganism(2, "TruthOrganism")];
        const fitnessOrganisms = [new FitnessOrganism(2, "FitnessOrganism")];

        for (let i = 0; i < numCycles; i++) {
            const world = worldGenerator();
            truthOrganisms.slice().forEach(org => org.cycle(world, truthOrganisms));
            fitnessOrganisms.slice().forEach(org => org.cycle(world, fitnessOrganisms));
        }

        totalTruthOrganisms += truthOrganisms.length;
        totalFitnessOrganisms += fitnessOrganisms.length;
    }

    const averageTruthOrganisms = totalTruthOrganisms / numSimulations;
    const averageFitnessOrganisms = totalFitnessOrganisms / numSimulations;

    const outputDiv = document.getElementById("output");
    outputDiv.innerHTML = `
        Average number of surviving truth-seeing organisms over ${numSimulations} simulations: ${averageTruthOrganisms}<br>
        Average number of surviving fitness-seeing organisms over ${numSimulations} simulations: ${averageFitnessOrganisms}
    `;
}
