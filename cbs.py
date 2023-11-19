import time as timer
import heapq
from single_agent_planner import compute_heuristics, a_star, get_location, get_sum_of_cost


##############################
# Task 3.1: Return the first collision that occurs between two robot paths (or None if there is no collision)
#           There are two types of collisions: vertex collision and edge collision.
#           A vertex collision occurs if both robots occupy the same location at the same timestep
#           An edge collision occurs if the robots swap their location at the same timestep.
#           You should use "get_location(path, t)" to get the location of a robot at time t.
def detect_collision(path1, path2):
    # Iterate over time steps to detect collision at certain timestep
    for t in range(max(len(path1), len(path2))):
        location_agent1 = get_location(path1, t)
        location_agent2 = get_location(path2, t)
        # Vertex
        if location_agent1 == location_agent2:
            return {'loc_vertex_collision': [location_agent1], 'timestep': t}
        # Edge
        if t < min(len(path1), len(path2)) - 1:  # one because before end of path
            next_location_agent1 = get_location(path1, t + 1)
            next_location_agent2 = get_location(path2, t + 1)
            if location_agent1 == next_location_agent2 and location_agent2 == next_location_agent1:
                return {'loc_edge_collision': [location_agent1, location_agent2], 'timestep': t}
    # No collisions
    return None


##############################
# Task 3.1: Return a list of first collisions between all robot pairs.
#           A collision can be represented as dictionary that contains the id of the two robots, the vertex or edge
#           causing the collision, and the timestep at which the collision occurred.
#           You should use your detect_collision function to find a collision between two robots.
def detect_collisions(paths):
    collisions = []
    for i in range(len(paths)):  # each agent
        for j in range(i + 1, len(paths)):  # all following agents
            collision = detect_collision(paths[i], paths[j])
            if collision:
                if 'loc_vertex_collision' in collision:
                    collisions.append({'a1': i, 'a2': j, 'loc_vertex': collision['loc_vertex_collision'],
                                       'timestep': collision['timestep']})
                elif 'loc_edge_collision' in collision:
                    collisions.append({'a1': i, 'a2': j, 'loc_edge': collision['loc_edge_collision'],
                                       'timestep': collision['timestep']})
    return collisions


##############################
# Task 3.2: Return a list of (two) constraints to resolve the given collision
#           Vertex collision: the first constraint prevents the first agent to be at the specified location at the
#                            specified timestep, and the second constraint prevents the second agent to be at the
#                            specified location at the specified timestep.
#           Edge collision: the first constraint prevents the first agent to traverse the specified edge at the
#                          specified timestep, and the second constraint prevents the second agent to traverse the
#                          specified edge at the specified timestep
def standard_splitting(collision):  # Note to self: collision is not the same as collision in detect_collisions
    constraints = []
    agent1 = collision['a1']
    agent2 = collision['a2']
    timestep_collision = collision['timestep']

    if 'loc_vertex' in collision:
        location_vertex_collision = collision['loc_vertex'][0]

        # First vertex constraint: Prohibits the first agent from occupying the same location at the same timestep
        vertex_constraint1 = {'agent': agent1, 'loc': [location_vertex_collision], 'timestep': timestep_collision}
        constraints.append(vertex_constraint1)

        # Second vertex constraint: Prohibits the second agent from occupying the same location at the same timestep
        vertex_constraint2 = {'agent': agent2, 'loc': [location_vertex_collision], 'timestep': timestep_collision}
        constraints.append(vertex_constraint2)

    if 'loc_edge' in collision:
        location_edge_collision = collision['loc_edge'][0]  # The location of the second agent at the collision timestep
        swap_location = collision['loc_edge'][1]  # The location of the first agent at the timestep of the collision

        # First edge constraint: Prohibits the first agent from executing the edge action
        edge_constraint1 = {'agent': agent1, 'loc': [location_edge_collision, swap_location],
                            'timestep': timestep_collision + 1}
        constraints.append(edge_constraint1)

        # Second edge constraint: Prohibits the second agent from executing the edge action
        edge_constraint2 = {'agent': agent2, 'loc': [swap_location, location_edge_collision],
                            'timestep': timestep_collision + 1}
        constraints.append(edge_constraint2)

    return constraints


##############################
# Task 4.1: Return a list of (two) constraints to resolve the given collision
#           Vertex collision: the first constraint enforces one agent to be at the specified location at the
#                            specified timestep, and the second constraint prevents the same agent to be at the
#                            same location at the timestep.
#           Edge collision: the first constraint enforces one agent to traverse the specified edge at the
#                          specified timestep, and the second constraint prevents the same agent to traverse the
#                          specified edge at the specified timestep
#           Choose the agent randomly
# --- Not implemented --- (Not in tutorial anymore) The code present is a start that was made.
def disjoint_splitting(collision):
    # constraints = []
    # agent1 = collision['a1']
    # agent2 = collision['a2']
    # timestep_collision = collision['timestep']
    # agent = random.choice([agent1, agent2])
    # if 'loc_vertex' in collision:
    #     location_vertex_collision = collision['loc_vertex'][0]
    #
    #     # Enforce agent to be at the specified location at the specified timestep
    #     vertex_constraint1 = {'agent': agent, 'loc': [location_vertex_collision], 'timestep': timestep_collision}
    #     constraints.append(vertex_constraint1)
    #     # Prevent the same agent from being at the same location at the timestep
    #     vertex_constraint2 = {'agent': agent, 'loc': [location_vertex_collision], 'timestep': timestep_collision}
    #     constraints.append(vertex_constraint2)
    pass


class CBSSolver(object):
    """The high-level search of CBS."""

    def __init__(self, my_map, starts, goals):
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """

        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.num_of_agents = len(goals)

        self.num_of_generated = 0
        self.num_of_expanded = 0
        self.CPU_time = 0

        self.open_list = []

        # compute heuristics for the low-level search
        self.heuristics = []
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

    def push_node(self, node):
        heapq.heappush(self.open_list, (node['cost'], len(node['collisions']), self.num_of_generated, node))
        # print("Generate node {}".format(self.num_of_generated))
        self.num_of_generated += 1

    def pop_node(self):
        _, _, id, node = heapq.heappop(self.open_list)
        # print("Expand node {}".format(id))
        self.num_of_expanded += 1
        return node

    def find_solution(self, disjoint=True):
        """ Finds paths for all agents from their start locations to their goal locations

        disjoint    - use disjoint splitting or not
        """

        self.start_time = timer.time()
        path_lengths = []
        # Generate the root node
        # constraints   - list of constraints
        # paths         - list of paths, one for each agent
        #               [[(x11, y11), (x12, y12), ...], [(x21, y21), (x22, y22), ...], ...]
        # collisions     - list of collisions in paths
        root = {'cost': 0,
                'constraints': [],
                'paths': [],
                'collisions': []}
        for i in range(self.num_of_agents):  # Find initial path for each agent
            path = a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i],
                          i, root['constraints'], self.goals, path_lengths)
            # print(path)
            if path is None:
                raise BaseException('No solutions')
            root['paths'].append(path)

        root['cost'] = get_sum_of_cost(root['paths'])
        root['collisions'] = detect_collisions(root['paths'])
        self.push_node(root)

        ##############################
        # Task 3.3: High-Level Search
        #           Repeat the following as long as the open list is not empty:
        #             1. Get the next node from the open list (you can use self.pop_node()
        #             2. If this node has no collision, return solution
        #             3. Otherwise, choose the first collision and convert to a list of constraints (using your
        #                standard_splitting function). Add a new child node to your open list for each constraint
        #           Ensure to create a copy of any objects that your child nodes might inherit
        time_limit = 50
        while self.open_list:
            if timer.time() - self.start_time > time_limit:
                return None
            parent = self.pop_node()
            CPU_time = timer.time() - self.start_time
            if not parent['collisions']:
                # No collisions, return the solution
                self.print_results(parent)
                return parent['paths']
            collision = parent['collisions'][0]  # Choose the first collision
            constraints = standard_splitting(collision)
            for constraint in constraints:
                child = {'cost': 0, 'constraints': parent['constraints'].copy() + [constraint],
                         'paths': parent['paths'].copy(), 'collisions': []}
                a_i = constraint['agent']
                path = a_star(self.my_map, self.starts[a_i], self.goals[a_i], self.heuristics[a_i], a_i,
                              child['constraints'], self.goals, path_lengths)
                if path:
                    child['paths'][a_i] = path.copy()
                    child['collisions'] = detect_collisions(child['paths'])
                    child['cost'] = get_sum_of_cost(child['paths'])
                    self.push_node(child)
        return BaseException('No solutions')


    def print_results(self, parent):
        print("\n Found a solution! \n")
        CPU_time = timer.time() - self.start_time
        print("CPU time (s):    {:.2f}".format(CPU_time))
        print("Sum of costs:    {}".format(get_sum_of_cost(parent['paths'])))
        print("Expanded nodes:  {}".format(self.num_of_expanded))
        print("Generated nodes: {}".format(self.num_of_generated))
