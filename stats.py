from create_random_spawning_maps import create_map
"""" The plan:
Create X maps for each environment/number of agents combination.
Run each of the algorithms on each of the maps saving data to a file.
This data includes:
    - Mean travel time of all agents
    - Mean length of paths of all agents
    - Mean ratio of travel time of agents compared to most direct path time
    - Mean ratio of path length of agents compared to most direct path length
    - Mean computation time (do we add a max here? What kind of penalty would we give for that?
      If prioritized has no solution does it get the same penalty?)
    - System-wide: how does each algorithm do with more obstacles in the above criteria?




How does an algorithm react to an agent stopping in its tracks?
 - Could be simulated by having an agent have its goal location in the middle of the map.
    -> check how the agents reacts (we don't want it to move out of the way when it is at its goal,
       or in other words when it has stopped.
 - Could also update the map with an obstacle in the middle of the map at a specific timestep?


X is determined by ...?
- Ensure that there is enough 'successful' runs to be sure our conclusion for X is correct
- Option (not my idea) is to use the variation (standard deviation / mean) to determine X. Once this value
  remains fairly constant with inceasing X, we can be confident that our results are representative.
"""

# Set the environment number and number of agents.
env = 3  # 1, 2, or 3
numb_agents = 10  # max 18
numb_maps = 1
for index in range(numb_maps):
    create_map(env, numb_agents, index)
