import time as timer
from single_agent_planner import a_star, compute_heuristics, get_sum_of_cost

class DistributedPlanningSolver:
    """A distributed planner"""
    def __init__(self, my_map, starts, goals):
        """
        Initializes the solver with the map, start positions, and goal positions.

        my_map - list of lists specifying obstacle positions.
        starts - list of start locations for each agent (e.g., [(x1, y1), (x2, y2), ...]).
        goals  - list of goal locations for each agent.
        """
        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.num_of_agents = len(goals)
        self.CPU_time = 0
        self.heuristics = [compute_heuristics(my_map, goal) for goal in self.goals]

    def _find_conflicts(self, timestep_location_list, paths):
        # Identifies conflicts between agents at different timesteps
        conflicts = []
        for position1 in timestep_location_list:
            for position2 in timestep_location_list:
                # Check for vertex conflicts
                if position1['agent'] < position2['agent'] and position1['timestep'] == position2['timestep']:
                    if position1['loc'] == position2['loc']:
                        conflicts.append((position1, position2, 'vertex'))
                        # Check for edge conflicts
                    elif position1['timestep'] > 0 and position2['timestep'] > 0:
                        prev_loc1 = paths[position1['agent']][position1['timestep'] - 1]
                        prev_loc2 = paths[position2['agent']][position2['timestep'] - 1]
                        if prev_loc1 == position2['loc'] and prev_loc2 == position1['loc']:
                            conflicts.append((position1, position2, 'edge'))
        return conflicts

    def _find_diversions(self, paths, agent1, agent_to_adjust, other_agent):
        # Finds alternative paths to avoid conflicts.
        diverted = False
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        conflict_timestep = agent1['timestep']
        prev_timestep = agent1['timestep'] - 1 if conflict_timestep > 0 else 0
        diversions = {}
        for idx_dir, dir in enumerate(directions):
            prev_loc = paths[agent_to_adjust][prev_timestep]
            new_loc = (prev_loc[0] + dir[0], prev_loc[1] + dir[1])

            # Check if the new location is part of the other agent's future path
            def is_location_in_future_path(new_loc, other_agent, paths,
                                           current_timestep):
                if current_timestep < len(paths[other_agent]):
                    for future_timestep in range(current_timestep, len(paths[other_agent])):
                        if paths[other_agent][future_timestep] == new_loc:
                            return True
                return False

            rows, cols = len(self.my_map), len(self.my_map[0])
            x, y = new_loc
            if 0 <= x < rows and 0 <= y < cols:
                if self.my_map[new_loc[0]][new_loc[1]] is False:
                    # print("here")
                    if new_loc != paths[other_agent][conflict_timestep - 1]:
                        # print("there")
                        print(f'found solution, idx_dir = {idx_dir}, new_loc={new_loc}')
                        if is_location_in_future_path(new_loc, other_agent, paths, agent1['timestep']):
                            diversions[idx_dir] = [True, new_loc]
                        else:
                            diversions[idx_dir] = [False, new_loc]
                        diverted = True
        return diversions, diverted
    def _find_remaining_path_length(self, paths, agent_dict):
        # Calculates the remaining path length for each agent
        l1 = 0
        for step in paths[agent_dict['agent']]:
            l1 += 1
            if step == agent_dict['loc']:
                break
        # Calculate and retrun the remaining path length
        return len(paths[agent_dict['agent']]) - l1

    def _get_best_diversion(self, diversions):
        # Selects the best diversion from the available options
        best_diversion = None
        for idx_dir in diversions.keys():
            # Select the diversion that does not intersect with the future location of another agent
            is_on_future_loc, new_loc = diversions[idx_dir]
            if best_diversion is None:
                best_diversion = new_loc
            else:
                if not is_on_future_loc:
                    best_diversion = new_loc
        return best_diversion

    def _find_paths_for_agent(self, agent_idx, constraints, start):
        # Use the A* algorithm to find a path for the agent
        return a_star(self.my_map, start, self.goals[agent_idx], self.heuristics[agent_idx], agent_idx,
                      constraints, self.goals, self.path_lengths)

    def _find_agent_to_adjust(self, paths, agent1, agent2):
        # Find the remaining path length for both agents
        remaining_length_1 = self._find_remaining_path_length(paths, agent1)
        remaining_length_2 = self._find_remaining_path_length(paths, agent2)
        # Choose the agent with the longer remaining path to adjust
        if remaining_length_1 > remaining_length_2:
            return agent2['agent'], agent1['agent']
        else:
            return agent1['agent'], agent2['agent']

    def _join_paths(self, old_path, conflict_timestep, new_path):
        # Combines the old path up to the conflict timestep with the new path
        adjusted_path = old_path[:conflict_timestep] + new_path
        return adjusted_path

    def find_solution(self):
        """
        Finds paths for all agents from start to goal locations.

        Returns:
                result (list): with a path [(s,t), .....] for each agent.
        """
        # Start measuring the time taken to find a solution
        self.start_time = timer.time()
        paths = []
        constraints = []
        self.path_lengths = []

        # Find most direct root for each agent
        for i in range(self.num_of_agents):
            paths.append(self._find_paths_for_agent(agent_idx=i, constraints=constraints, start=self.starts[i]))
            self.path_lengths.append(len(paths[-1]) if paths[-1] else 0)

        solved_system = False
        # Loop to resolve conflicts and adjust paths
        while solved_system == False:
            # Reset constraints for each iteration
            constraints = []

            timestep_location_list = []
            # Create a lsit of all agents' locations at each timestep 
            for agentnumber, agentpath in enumerate(paths):
                for timestep_agentpath, location_agentpath in enumerate(agentpath):
                    timestep_location_list.append(
                        {'agent': agentnumber, 'loc': location_agentpath, 'timestep': timestep_agentpath})

            # Find all conflicts at each timestep
            conflicts = self._find_conflicts(timestep_location_list, paths)

            # If there are conflicts, try to resolve them
            if conflicts:
                # Find the lowest timestep with a conflict
                lowest_timestep_conflicts = [c for c in conflicts if
                                             c[0]['timestep'] == min(c[0]['timestep'] for c in conflicts)]
                conflict_timestep = lowest_timestep_conflicts[0][0]['timestep']

                # Solve one conflict at a time. Solve the rest in the outer loop.
                selected_conflict = lowest_timestep_conflicts[0]
                conflict = selected_conflict
                
                agent1, agent2, constrainttype = conflict

                # Find which agent to adjust, and which is the other agent
                agent_to_adjust, other_agent = self._find_agent_to_adjust(paths, agent1, agent2)

                print(f"Original paths\nagent adjust = {paths[agent_to_adjust]}\nagent other = {paths[other_agent]}")

                # Resolve if the conflict is an edge constraint
                if constrainttype == 'edge':
                    print(f"Solving edge constraint, t={conflict_timestep}")

                    # Divert the lower-priority agent
                    diversions, diverted = self._find_diversions(paths, agent1, agent_to_adjust, other_agent)
                    if diverted:
                        new_loc = self._get_best_diversion(diversions)
                        paths[agent_to_adjust][conflict_timestep] = new_loc

                        # Replan the path from the new location
                        new_path = self._find_paths_for_agent(agent_to_adjust, constraints, start=new_loc)

                        if new_path is None:
                            # This should be the case if the solver can't find a solution
                            return None

                        print(f"old path = {paths[agent_to_adjust]}")
                        print("new_path = ", new_path)
                        paths[agent_to_adjust] = self._join_paths(
                            paths[agent_to_adjust], conflict_timestep, new_path
                        )
                        print(f"adjusted path = {paths[agent_to_adjust]}")
                        self.path_lengths[agent_to_adjust] = len(paths[agent_to_adjust])

                # Resolve if the conflict is an edge constraint
                if constrainttype == 'vertex':
                    print(f"Solving vertex constraint, t={conflict_timestep}")
                    constraints.append(
                        {'agent': agent_to_adjust, 'timestep': agent2['timestep'], 'loc': [agent1['loc']]}
                    )

                    # Recalculate the path for the adjusted agent
                    if agent1['timestep'] > 0:
                        new_start = paths[agent_to_adjust][conflict_timestep-1]
                    else:
                        print("timestep not above zero")
                        new_start = self.starts[agent_to_adjust]
                    print(f"current constraints = {constraints}")
                    # Replan the path from the new location
                    print("new start", new_start)
                    new_path = self._find_paths_for_agent(agent_to_adjust, constraints, start=new_start)

                    if new_path is None:
                        print('No found')
                        return

                    print(f"old path = {paths[agent_to_adjust]}")
                    print("new_path = ", new_path)
                    paths[agent_to_adjust] = self._join_paths(paths[agent_to_adjust], conflict_timestep, new_path)
                    print(f"adjusted path = {paths[agent_to_adjust]}")

            else:
                # Quit the loop since no future conflicts
                solved_system = True

        # Print the results
        print("\n Found a solution! \n")
        CPU_time = timer.time() - self.start_time
        print("CPU time (s):    {:.2f}".format(CPU_time))
        print("Sum of costs:    {}".format(get_sum_of_cost(paths)))

        return paths
