from create_random_spawning_maps import create_map
import argparse
import glob
from pathlib import Path
from cbs import CBSSolver
from prioritized import PrioritizedPlanningSolver
from distributed import DistributedPlanningSolver # Placeholder for Distributed Planning
from single_agent_planner import get_path_time, get_path_distance, get_distance_ratio, get_time_ratio
"""" The plan:
Create X maps for each environment/number of agents combination.
Run each of the algorithms on each of the maps saving data to a file.
This data includes:
    - Mean travel time of all agents
    - Mean length of paths of all agents (distance)
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
  remains fairly constant with increasing X, we can be confident that our results are representative.
"""
SOLVER = "CBS"


def print_mapf_instance(my_map, starts, goals):
    """
    Prints start location and goal location of all agents, using @ for an obstacle, . for a open cell, and
    a number for the start location of each agent.

    Example:
        @ @ @ @ @ @ @
        @ 0 1 . . . @
        @ @ @ . @ @ @
        @ @ @ @ @ @ @
    """
    print('Start locations')
    print_locations(my_map, starts)
    print('Goal locations')
    print_locations(my_map, goals)


def print_locations(my_map, locations):
    """
    See docstring print_mapf_instance function above.
    """
    starts_map = [[-1 for _ in range(len(my_map[0]))] for _ in range(len(my_map))]
    for i in range(len(locations)):
        starts_map[locations[i][0]][locations[i][1]] = i
    to_print = ''
    for x in range(len(my_map)):
        for y in range(len(my_map[0])):
            if starts_map[x][y] >= 0:
                to_print += str(starts_map[x][y]) + ' '
            elif my_map[x][y]:
                to_print += '@ '
            else:
                to_print += '. '
        to_print += '\n'
    print(to_print)


def import_mapf_instance(filename):
    """
    Imports mapf instance from instances folder. Expects input as a .txt file in the following format:
        Line1: #rows #columns (number of rows and columns)
        Line2-X: Grid of @ and . symbols with format #rows * #columns. The @ indicates an obstacle, whereas . indicates free cell.
        Line X: #agents (number of agents)
        Line X+1: xCoordStart yCoordStart xCoordGoal yCoordGoal (xy coordinate start and goal for Agent 1)
        Line X+2: xCoordStart yCoordStart xCoordGoal yCoordGoal (xy coordinate start and goal for Agent 2)
        Line X+n: xCoordStart yCoordStart xCoordGoal yCoordGoal (xy coordinate start and goal for Agent n)

    Example:
        4 7             # grid with 4 rows and 7 columns
        @ @ @ @ @ @ @   # example row with obstacle in every column
        @ . . . . . @   # example row with 5 free cells in the middle
        @ @ @ . @ @ @
        @ @ @ @ @ @ @
        2               # 2 agents in this experiment
        1 1 1 5         # agent 1 starts at (1,1) and has (1,5) as goal
        1 2 1 4         # agent 2 starts at (1,2) and has (1,4) as goal
    """
    f = Path(filename)
    if not f.is_file():
        raise BaseException(filename + " does not exist.")
    f = open(filename, 'r')
    # first line: #rows #columns
    line = f.readline()
    rows, columns = [int(x) for x in line.split(' ')]
    rows = int(rows)
    columns = int(columns)
    # #rows lines with the map
    my_map = []
    for r in range(rows):
        line = f.readline()
        my_map.append([])
        for cell in line:
            if cell == '@':
                my_map[-1].append(True)
            elif cell == '.':
                my_map[-1].append(False)
    # #agents
    line = f.readline()
    num_agents = int(line)
    # #agents lines with the start/goal positions
    starts = []
    goals = []
    for a in range(num_agents):
        line = f.readline()
        sx, sy, gx, gy = [int(x) for x in line.split(' ')]
        starts.append((sx, sy))
        goals.append((gx, gy))
    f.close()
    return my_map, starts, goals


# Set the environment number and number of agents.
# env = 1  # 1, 2, or 3
# numb_agents = 2  # max 18
# numb_maps = 100
# for index in range(numb_maps):
#     create_map(env, numb_agents, index)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs various MAPF algorithms')
    parser.add_argument('--instance', type=str, default=None,
                        help='The name of the instance file(s)')

    args = parser.parse_args()
    n_agents = args.instance.split("n-agents")[1].split("_")[0]
    env = args.instance.split("env")[1].split("_")[0]
    # solvers = ["CBS","Prioritized", "Distributed"]
    solvers = ["Prioritized"]

    for solver_name in solvers:
        result_file = open(f"statistics_files/env{env}-n_agents{n_agents}-{solver_name}.csv", "w")
        result_file.write("File index,Travel time,Path distance,Travel time ratio,Path length ratio,"
                          "Travel time standard deviation,Computation time\n")
        env_mean_travel_times = []
        env_mean_path_distances = []
        env_mean_time_ratios = []
        env_mean_distance_ratios = []
        env_mean_computation_times = []
        env_sd_travel_time = []
        n_failed_instances = 0
        for file in sorted(glob.glob(args.instance)):

            my_map, starts, goals = import_mapf_instance(file)

            if solver_name == "CBS":
                solver = CBSSolver(my_map, starts, goals)
            elif solver_name == "Prioritized":
                solver = PrioritizedPlanningSolver(my_map, starts, goals)
            elif solver_name == "Distributed":  # Wrapper of distributed planning solver class
                solver = DistributedPlanningSolver(my_map, starts, goals,...) # Placeholder for Distributed Planning
            else:
                raise RuntimeError("Unknown solver!")
            paths = solver.find_solution()
            if paths is None:
                n_failed_instances += 1
                continue
            file_index = file.split("index")[1].split(".")[0]
            travel_times = []
            path_distances = []
            time_ratios = []
            distance_ratios = []
            computation_times = []
            for i in range(len(paths)):
                travel_times.append(get_path_time(paths[i]))
                path_distances.append(get_path_distance(paths[i]))
                time_ratios.append(get_time_ratio(paths[i], my_map, starts[i], goals[i], solver.heuristics[i], i,
                                                  [], goals, []))
                distance_ratios.append(get_distance_ratio(paths[i], my_map, starts[i], goals[i], solver.heuristics[i],
                                                          i, [], goals, []))
                computation_times.append(solver.CPU_time)

            map_mean_travel_time = sum(travel_times) / len(travel_times)
            env_mean_travel_times.append(map_mean_travel_time)
            map_mean_path_distance = sum(path_distances) / len(path_distances)
            env_mean_path_distances.append(map_mean_path_distance)
            map_mean_time_ratio = sum(time_ratios) / len(time_ratios)
            env_mean_time_ratios.append(map_mean_time_ratio)
            map_mean_distance_ratio = sum(distance_ratios) / len(distance_ratios)
            env_mean_distance_ratios.append(map_mean_distance_ratio)
            variance_travel_time = sum([((x - map_mean_travel_time) ** 2) for x in travel_times]) / len(travel_times)
            map_sd_travel_time = variance_travel_time ** 0.5
            env_sd_travel_time.append(map_sd_travel_time)
            map_mean_computation_time = solver.CPU_time / len(computation_times)
            env_mean_computation_times.append(map_mean_computation_time)

            result_file.write(f"{file_index}, {map_mean_travel_time}, {map_mean_path_distance}, {map_mean_time_ratio}, "
                              f"{map_mean_distance_ratio},{map_sd_travel_time} {map_mean_computation_time}\n")
        result_file.close()

        plot_data = open(f"statistics_files/plot_data/plot_data-env{env}-n_agents{n_agents}-{solver_name}.csv", "w")
        plot_data.write("Travel time,Path distance,Travel time ratio,Path length ratio,"
                        "Travel time standard deviation,Ratio failed instances,Computation time\n")
        env_travel_time = sum(env_mean_travel_times) / len(env_mean_travel_times)
        env_path_distance = sum(env_mean_path_distances) / len(env_mean_path_distances)
        env_time_ratio = sum(env_mean_time_ratios) / len(env_mean_time_ratios)
        env_distance_ratio = sum(env_mean_distance_ratios) / len(env_mean_distance_ratios)
        env_sd_travel_time = sum(env_sd_travel_time) / len(env_sd_travel_time)
        env_failed_instances = n_failed_instances / len(glob.glob(args.instance))
        env_computation_time = sum(env_mean_computation_times) / len(env_mean_computation_times)
        plot_data.write(f"{env_travel_time},{env_path_distance},{env_time_ratio},{env_distance_ratio},"
                        f"{env_sd_travel_time},{env_failed_instances},{env_computation_time}\n")
        plot_data.close()
