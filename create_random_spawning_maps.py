import random


""" The goal of this code is to create random maps with agents spawning on only one side of the map.
Firs the function is made and you can run the program at the bottom to create the maps."""
def create_map(env, numb_agents, file_index):
    # Define starting and goal coordinates for each agent.
    # This is done with a dictionary, where the key is the agent name and the value is a tuple of the coordinates.
    # One dictionary for start locations with location (x,y) and one for goal locations with location (x,y).
    start_locations = {}
    start_locations_old = {}
    goal_locations = {}
    goal_locations_old = {}
    for agent in range(numb_agents):
        start_locations[f"agent_{agent}"] = (random.randint(0, 1),
                                             random.randint(0, 8))
        # Check that the starting location has not already been taken by another agent.
        while start_locations[f"agent_{agent}"] in start_locations_old.values():
            start_locations[f"agent_{agent}"] = (random.randint(0, 1),
                                                 random.randint(0, 8))
        start_locations_old[f"agent_{agent}"] = start_locations[f"agent_{agent}"]
        # Repeat the same process for the goal locations.
        goal_locations[f"agent_{agent}"] = (random.randint(20, 21),
                                            random.randint(0, 8))
        while goal_locations[f"agent_{agent}"] in goal_locations_old.values():
            goal_locations[f"agent_{agent}"] = (random.randint(20, 21),
                                                random.randint(0, 8))
        goal_locations_old[f"agent_{agent}"] = goal_locations[f"agent_{agent}"]
    # Create the environment, depending on the environment number.
    # Include all the agents in the environment, as per the format.
    if env == 1:
        f = open(f"instances/evaluation_maps/env{env}_n-agents{numb_agents}_index{file_index}.txt", 'w')
        f.write("9 22\n "
                ". . @ @ @ @ . . . @ @ @ @ . . . @ @ @ @ . .\n"
                ". . . . . . . . . . . . . . . . . . . . . .\n"
                ". . @ @ @ @ . . . @ @ @ @ . . . @ @ @ @ . .\n"
                ". . . . . . . . . . . . . . . . . . . . . .\n"
                ". . @ @ @ @ . . . @ @ @ @ . . . @ @ @ @ . .\n"
                ". . . . . . . . . . . . . . . . . . . . . .\n"
                ". . @ @ @ @ . . . @ @ @ @ . . . @ @ @ @ . .\n"
                ". . . . . . . . . . . . . . . . . . . . . .\n"
                ". . @ @ @ @ . . . @ @ @ @ . . . @ @ @ @ . .\n"
                f"{numb_agents}\n")
        for agent in range(numb_agents):
            f.write(f"{start_locations[f'agent_{agent}'][1]} {start_locations[f'agent_{agent}'][0]} "
                    f"{goal_locations[f'agent_{agent}'][1]} {goal_locations[f'agent_{agent}'][0]}\n")
        f.close()
        map_with_agents = f
        return map_with_agents
    elif env == 2:
        f = open(f"instances/evaluation_maps/env{env}_n-agents{numb_agents}_index{file_index}.txt", 'w')
        f.write("9 22\n "
                ". . @ @ @ @ . . . @ @ @ @ . . . @ @ @ @ . .\n"
                ". . . . . . . @ . . . . . . @ . . . . . . .\n"
                ". . @ @ @ @ . . . @ @ @ @ . . . @ @ @ @ . .\n"
                ". . . . . . . @ . . . . . . @ . . . . . . .\n"
                ". . @ @ @ @ . . . @ @ @ @ . . . @ @ @ @ . .\n"
                ". . . . . . . @ . . . . . . @ . . . . . . .\n"
                ". . @ @ @ @ . . . @ @ @ @ . . . @ @ @ @ . .\n"
                ". . . . . . . @ . . . . . . @ . . . . . . .\n"
                ". . @ @ @ @ . . . @ @ @ @ . . . @ @ @ @ . .\n"
                f"{numb_agents}\n")
        for agent in range(numb_agents):
            f.write(f"{start_locations[f'agent_{agent}'][1]} {start_locations[f'agent_{agent}'][0]} "
                    f"{goal_locations[f'agent_{agent}'][1]} {goal_locations[f'agent_{agent}'][0]}\n")
        f.close()
        map_with_agents = f
        return map_with_agents
    elif env == 3:
        f = open(f"instances/evaluation_maps/env{env}_n-agents{numb_agents}_index{file_index}.txt", 'w')
        f.write("9 22\n "
                ". . @ @ @ @ . . . @ @ @ @ . . . @ @ @ @ . .\n"
                ". . . . . . . @ . . . . . . @ . . . . . . .\n"
                ". . @ @ @ @ . @ . @ @ @ @ . @ . @ @ @ @ . .\n"
                ". . . . . . . @ . . . . . . @ . . . . . . .\n"
                ". . @ @ @ @ . . . @ @ @ @ . . . @ @ @ @ . .\n"
                ". . . . . . . @ . . . . . . @ . . . . . . .\n"
                ". . @ @ @ @ . @ . @ @ @ @ . @ . @ @ @ @ . .\n"
                ". . . . . . . @ . . . . . . @ . . . . . . .\n"
                ". . @ @ @ @ . . . @ @ @ @ . . . @ @ @ @ . .\n"
                f"{numb_agents}\n")
        for agent in range(numb_agents):
            f.write(f"{start_locations[f'agent_{agent}'][1]} {start_locations[f'agent_{agent}'][0]} "
                    f"{goal_locations[f'agent_{agent}'][1]} {goal_locations[f'agent_{agent}'][0]}\n")
        f.close()
        map_with_agents = f
        return map_with_agents
    else:
        raise BaseException('No such environment')


# Set the environment number and number of agents.
env = 2  # 1, 2, or 3
numb_agents = 12  # max 18
numb_maps = 250
for index in range(numb_maps):
    create_map(env, numb_agents, index)
