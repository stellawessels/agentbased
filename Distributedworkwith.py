class DistributedPlanningSolver(object):
    def __init__(self, my_map, starts, goals):
        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.num_of_agents = len(goals)
        self.CPU_time = 0

        # compute heuristics for the low-level search
        self.heuristics = []
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

    def find_solution(self):
        start_time = timer.time()
        paths = []
        path_lengths = []
        constraints = []
        for i in range(self.num_of_agents):  # Find path for each agent

            path = a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i],
                          i, constraints, self.goals, path_lengths)
            paths.append(path)
            if path is None:
                print("none")
                None
            else:
                path_lengths.append(len(path))
        print("paths are here", paths)
        #iterate on the solution until all agents on goal location
        #set up constraints list based on paths of all agents
        timestep_location_list = []
        for agentnumber, agentpath in enumerate(paths):
            for timestep_agentpath,location_agentpath in enumerate(agentpath):
                timestep_location_list.append({'agent': agentnumber, 'loc': location_agentpath, 'timestep':timestep_agentpath})
        conflicts_list = []
        for position1 in timestep_location_list:
            for position2 in timestep_location_list:
                if position1['loc'] == position2['loc']:
                    if position1['timestep'] == position2['timestep']:
                        if position1 != position2:
                            conflicts_list.append({'agent1':position1['agent'],'agent2':position2['agent'],'loc':position1['loc'], 'timestep':position1['timestep']})
        # Find the minimum timestep
        min_timestep = min(entry['timestep'] for entry in conflicts_list)

        # Filter entries with the minimum timestep
        min_timestep_entries = [entry for entry in conflicts_list if entry['timestep'] == min_timestep]

        # Select a random entry from those with the minimum timestep
        selected_entry = random.choice(min_timestep_entries)
        print("selected entry", selected_entry)

        #selected entry is the conflict
        #give priority to the agent that needs to travel furthest
        full_path_agent1 = paths[selected_entry['agent1']]
        full_path_agent2 = paths[selected_entry['agent2']]
        def sublist_from_element(full_list, target_element):
            try:
                # Find the index of the target element
                start_index = full_list.index(target_element)

                # Slice the list from the found index to the end
                return full_list[start_index:]
            except ValueError:
                # Return an empty list if the target element is not found
                return []
        time_left_agent1 = len(sublist_from_element(full_path_agent1,selected_entry['loc']))
        time_left_agent2 = len(sublist_from_element(full_path_agent2,selected_entry['loc']))
        print('time left agent 1', time_left_agent1)
        print('time left agent 2', time_left_agent2)
        # Decide which agent's path to adjust
        if time_left_agent1 > time_left_agent2 or time_left_agent1 == time_left_agent2:
            agent_to_adjust = selected_entry['agent2']
            print('agent2 adjusted')
        else:
            agent_to_adjust = selected_entry['agent1']
            print('agent1 adjusted')

        # Conflict timestep
        conflict_timestep = selected_entry['timestep']

        # Create the initial segment of the path (up to just before the conflict)
        initial_path_segment = paths[agent_to_adjust][:conflict_timestep]
        print(initial_path_segment)

        # Generate new path from the location at the timestep just before the conflict
        new_start = paths[agent_to_adjust][conflict_timestep - 1] if conflict_timestep > 0 else self.starts[
            agent_to_adjust]
        print(new_start)
        constraints.append({'agent':agent_to_adjust, 'loc': [selected_entry['loc']], 'timestep': conflict_timestep})
        new_path_segment = a_star(self.my_map, new_start, self.goals[agent_to_adjust], self.heuristics[agent_to_adjust],
                                  agent_to_adjust, constraints, self.goals, path_lengths)

        # Combine the initial segment of the path with the new path segment
        full_new_path = initial_path_segment + new_path_segment[1:]
        print(full_new_path)

        # Update the paths list with the new path for the adjusted agent
        if new_path_segment:
            paths[agent_to_adjust] = full_new_path


        self.CPU_time = timer.time() - start_time
        return paths