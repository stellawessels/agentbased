
import time as timer
from single_agent_planner import a_star, compute_heuristics
import random

class DistributedPlanningSolver(object):
    def __init__(self, my_map, starts, goals):
        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.num_of_agents = len(goals)
        self.CPU_time = 0
        self.heuristics = [compute_heuristics(my_map, goal) for goal in goals]

    def find_solution(self):
        start_time = timer.time()
        paths = [a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i], i, [], self.goals, []) for i in range(self.num_of_agents)]
        goal_reached_times = [None] * self.num_of_agents
        constraints = []

        def remaining_path_length(path, goal):
            if goal in path:
                return len(path) - path.index(goal)
            return 0

        while not all(goal_reached_times):
            timestep_location_list = []
            for agentnumber, agentpath in enumerate(paths):
                for timestep_agentpath, location_agentpath in enumerate(agentpath):
                    timestep_location_list.append({'agent': agentnumber, 'loc': location_agentpath, 'timestep': timestep_agentpath})

            conflicts_list = []
            for position1 in timestep_location_list:
                for position2 in timestep_location_list:
                    if position1['loc'] == position2['loc'] and position1['timestep'] == position2['timestep'] and position1 != position2:
                        conflicts_list.append({'agent1': position1['agent'], 'agent2': position2['agent'], 'loc': position1['loc'], 'timestep': position1['timestep']})

            if conflicts_list:
                # Resolve conflicts
                for conflict in conflicts_list:
                    agent1 = conflict['agent1']
                    agent2 = conflict['agent2']
                    agent_to_adjust = agent1 if remaining_path_length(paths[agent1], self.goals[agent1]) < remaining_path_length(paths[agent2], self.goals[agent2]) else agent2

                    conflict_timestep = conflict['timestep']
                    new_start = paths[agent_to_adjust][conflict_timestep - 1] if conflict_timestep > 0 else self.starts[agent_to_adjust]
                    constraints.append({'agent': agent_to_adjust, 'loc': [conflict['loc']], 'timestep': conflict_timestep})
                    new_path_segment = a_star(self.my_map, new_start, self.goals[agent_to_adjust], self.heuristics[agent_to_adjust], agent_to_adjust, constraints, self.goals, [])

                    if new_path_segment:
                        paths[agent_to_adjust] = paths[agent_to_adjust][:conflict_timestep] + new_path_segment[1:]

            # Update agents' status
            for i, path in enumerate(paths):
                if goal_reached_times[i] is None and path[-1] == self.goals[i]:
                    goal_reached_times[i] = len(path)

        average_time_to_goal = sum(time for time in goal_reached_times if time is not None) / self.num_of_agents
        print(f"Average Time for Agents to Reach Goals: {average_time_to_goal:.2f} timesteps")

        self.CPU_time = timer.time() - start_time
        return paths
