#Alejandro Mariacca Santin A01654102
#Tarea M2
import mesa

# def compute_gini(model):
#     agent_wealths = [agent.wealth for agent in model.schedule.agents]
#     x = sorted(agent_wealths)
#     N = model.num_agents
#     B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
#     return 1 + (1 / N) - 2 * Basdasd

class VaccumAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        
        
    def removeAgent(self):
        #Recolectar los elementos de la casilla
        cellmates = self.model.grid.get_cell_list_contents([self.pos])

        #Encontrar al otro agente
        #print("Cellmates: " , cellmates)    # DEBUG
        if "DirtAgent" in str(cellmates):
            print("Encontré un agente tierra")
            #print("Cellmates[0]: " , cellmates[0], " CON TIPO: ", type(cellmates[0]))
            #print("Cellmates[1]: " , cellmates[1])
            self.model.grid.remove_agent(cellmates[0])
            self.model.schedule.remove(cellmates[0])
            

    def step(self):
        self.move()
        self.removeAgent()

class VaccumModel(mesa.Model):
    """A model with some number of agents."""


    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True

        # Create agents
        for i in range(6,10):
            a = VaccumAgent(i, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
        
        # Create trash
        for i in range(0,2):
            a = DirtAgent(i, self)
            print("Creé agente A, con tipo: ", type(a), " y valor: ", a)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        self.schedule.step()


class DirtAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}

    if agent.unique_id > 5:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    return portrayal



grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)
chart = mesa.visualization.ChartModule([{"Label": "Gini", "Color": "Black"}], data_collector_name='datacollector')
server = mesa.visualization.ModularServer(
    VaccumModel, [grid], "Aspiradoras de tierra", {"N": 1, "width": 10, "height": 10},
)
server.port = 8521  # The default
server.launch()
