import time as timer
from single_agent_planner import compute_heuristics, a_star, get_sum_of_cost


class PrioritizedPlanningSolver(object):
    """A planner that plans for each robot sequentially."""

    def __init__(self, my_map, starts, goals):
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """

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
        """ Finds paths for all agents from their start locations to their goal locations."""

        start_time = timer.time()
        result = []
        constraints = [{'agent': 0, 'loc': [(1, 5)], 'timestep': 10}
                       #{'agent': 1, 'loc': [(1, 3), (1, 4)], 'timestep': 2},
                       #{'agent': 1, 'loc': [(1, 3), (1, 2)], 'timestep': 2}
                       ]
        # {'agent': 1, 'loc': [(1, 1)], 'timestep': 1}
        # constraints.append({'agent': 0, 'loc': [(1, 2)], 'timestep': 5}) # Test constraint to see whether the constrained_table is formatted correctly.
        for i in range(self.num_of_agents):  # Find path for each agent

            path = a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i],
                          i, constraints, self.goals)  # , atgoal
            # print("path here", path)
            if path is None:
                raise BaseException('No solutions')
            result.append(path)
            ##############################
            # Task 2: Add constraints here

            for j,k in enumerate(path):
                #print(f"path{path}, j {j}, k {k}")
                if i + 1 < self.num_of_agents:
                    #print("i+1",i+1)
                    #print(self.num_of_agents)
                    for q in range(i+1,self.num_of_agents):
                        #print(self.num_of_agents)
                        #print(q)
                        constraints.append({'agent': q, 'loc': [k], 'timestep': j})
                        if j+1 < len(path):
                            constraints.append({'agent': q, 'loc': [path[j+1],k], 'timestep': j+1})
            #         Useful variables:
            #            * path contains the solution path of the current (i'th) agent, e.g., [(1,1),(1,2),(1,3)]
            #            * self.num_of_agents has the number of total agents
            #            * constraints: array of constraints to consider for future A* searches

            # print("constraints", constraints)
            ##############################

        self.CPU_time = timer.time() - start_time

        print("\n Found a solution! \n")
        print("CPU time (s):    {:.2f}".format(self.CPU_time))
        print("Sum of costs:    {}".format(get_sum_of_cost(result)))
        # print(result)
        return result
