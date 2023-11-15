import time as timer
from single_agent_planner import a_star, compute_heuristics

# probeersel - kijken of de agent naar open locaties wilt verplaatsen uit de weg voor de ander - bijvoorbeeld nodig voor edgecollision.txt
"""
def find_fallback_location(self, current_location, next_location, occupied_locations):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # 4 directions: up, down, right, left
    for dx, dy in directions:
        fallback_location = (current_location[0] + dx, current_location[1] + dy)
        if fallback_location not in occupied_locations and self.is_location_free(
                fallback_location) and fallback_location != next_location:
            return fallback_location
    return None


def is_location_free(self, location):
    rows, cols = len(self.my_map), len(self.my_map[0])
    if 0 <= location[0] < rows and 0 <= location[1] < cols:
        return self.my_map[location[0]][location[1]] == '.'
    return False

"""


class DistributedPlanningSolver:
    def __init__(self, my_map, starts, goals):
        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.num_of_agents = len(goals)
        self.CPU_time = 0
        self.heuristics = [compute_heuristics(my_map, goal) for goal in self.goals]

    def find_solution(self):
        start_time = timer.time()
        paths = []
        path_lengths = []
        constraints = []
        # Find most direct root for each agent
        for i in range(self.num_of_agents):
            path = a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i], i, constraints, self.goals,
                          path_lengths)
            # Append each path and path length to the lists
            paths.append(path)
            path_lengths.append(len(path) if path else 0)

        # Find the maximum path length
        max_timesteps = max(len(path) for path in paths)
        timestep = 0
        # print(paths)

        while timestep < max_timesteps:
            has_conflicts = True

            while has_conflicts:
                # Make a dictionary with each agent and their location at each timestep
                timestep_location_list = []
                for agentnumber, agentpath in enumerate(paths):
                    for timestep_agentpath, location_agentpath in enumerate(agentpath):
                        timestep_location_list.append(
                            {'agent': agentnumber, 'loc': location_agentpath, 'timestep': timestep_agentpath})
                # print(timestep_location_list)
                # Find all conflicts at each timestep
                conflicts = []
                for position1 in timestep_location_list:
                    for position2 in timestep_location_list:
                        # Vertex conflicts (i.e. same location at same timestep)
                        # Note that an agent cannot have a conflict with itself (hence first if-statement)
                        if position1['agent'] < position2['agent'] and position1['timestep'] == position2['timestep']:
                            if position1['loc'] == position2['loc']:
                                conflicts.append((position1, position2, 'vertex'))
                                # Edge conflicts (i.e. agents swap positions)
                            elif position1['timestep'] > 0 and position2['timestep'] > 0:
                                prev_loc1 = paths[position1['agent']][position1['timestep'] - 1]
                                prev_loc2 = paths[position2['agent']][position2['timestep'] - 1]
                                if prev_loc1 == position2['loc'] and prev_loc2 == position1['loc']:
                                    conflicts.append((position1, position2, 'edge'))

                if conflicts:
                    # Find the lowest timestep with a conflict
                    lowest_timestep_conflicts = [c for c in conflicts if
                                                 c[0]['timestep'] == min(c[0]['timestep'] for c in conflicts)]
                    # print(lowest_timestep_conflicts)

                    # Resolve only conflicts at the lowest timestep
                    for conflict in lowest_timestep_conflicts:
                        # print(conflict)
                        agent1, agent2, constrainttype = conflict
                        # Find the agent with the longest remaining path
                        # This is done by finding the first time is at the constraint location and subtracting
                        # the timestep at which that occurs from the total path length
                        l1 = 0
                        for step in paths[agent1['agent']]:
                            # print(step)
                            # print(agent1['loc'])
                            l1 += 1
                            if step == agent1['loc']:
                                # print('gevonden')
                                break
                        # print(path_lengths[agent1['agent']])
                        remaining_length_1 = path_lengths[agent1['agent']] - l1
                        # print('remaining_length',remaining_length_1)
                        l2 = 0
                        for step in paths[agent2['agent']]:
                            l2 += 1
                            if step == agent2['loc']:
                                break
                        remaining_length_2 = path_lengths[agent2['agent']] - l2
                        # print(remaining_length_1)
                        # print(remaining_length_2)

                        # Determine which agent to adjust (one with smallest remaining path)
                        if remaining_length_1 > remaining_length_2:
                            agent_to_adjust = agent2['agent']
                        else:
                            agent_to_adjust = agent1['agent']
                        # print('agent_to_adjust',agent_to_adjust)

                        # update constraints
                        agent1, agent2, constraint_type = conflict
                        constraint = {'agent': agent_to_adjust, 'timestep': agent2['timestep']}
                        if constraint_type == 'vertex':
                            constraint['loc'] = [agent1['loc']]
                        else:  # edge conflict
                            constraint['loc'] = [agent1['loc'], agent2['loc']]

                        constraints.append(constraint)
                        print('constraints_list', constraints)

                        new_start = paths[agent_to_adjust][agent1['timestep'] - 1] if agent1['timestep'] > 0 else \
                            self.starts[agent_to_adjust]
                        new_path = a_star(self.my_map, new_start, self.goals[agent_to_adjust],
                                          self.heuristics[agent_to_adjust], agent_to_adjust, constraints, self.goals,
                                          path_lengths)
                        # print(new_path)
                        if new_path is None:
                            return
                        paths[agent_to_adjust] = paths[agent_to_adjust][:agent1['timestep']] + new_path
                        path_lengths[agent_to_adjust] = len(paths[agent_to_adjust])
                        # print(paths[agent_to_adjust])

                    # Update max_timesteps in case paths have been extended
                max_timesteps = max(len(path) for path in paths)

                for i, path in enumerate(paths):
                    if len(path) == max_timesteps:
                        self.CPU_time = timer.time() - start_time
                        return paths

                timestep += 1
