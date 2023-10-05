import heapq

def move(loc, dir):
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)] #add [0,0] here
    return loc[0] + directions[dir][0], loc[1] + directions[dir][1]


def get_sum_of_cost(paths):
    rst = 0
    for path in paths:
        rst += len(path) - 1
    return rst


def compute_heuristics(my_map, goal):
    # Use Dijkstra to build a shortest-path tree rooted at the goal location
    open_list = []
    closed_list = dict()
    root = {'loc': goal, 'cost': 0}
    heapq.heappush(open_list, (root['cost'], goal, root))
    closed_list[goal] = root
    while len(open_list) > 0:
        (cost, loc, curr) = heapq.heappop(open_list)
        for dir in range(4):
            child_loc = move(loc, dir)
            child_cost = cost + 1
            if child_loc[0] < 0 or child_loc[0] >= len(my_map) \
               or child_loc[1] < 0 or child_loc[1] >= len(my_map[0]):
               continue
            if my_map[child_loc[0]][child_loc[1]]:
                continue
            child = {'loc': child_loc, 'cost': child_cost}
            if child_loc in closed_list:
                existing_node = closed_list[child_loc]
                if existing_node['cost'] > child_cost:
                    closed_list[child_loc] = child
                    # open_list.delete((existing_node['cost'], existing_node['loc'], existing_node))
                    heapq.heappush(open_list, (child_cost, child_loc, child))
            else:
                closed_list[child_loc] = child
                heapq.heappush(open_list, (child_cost, child_loc, child))

    # build the heuristics table
    h_values = dict()
    for loc, node in closed_list.items():
        h_values[loc] = node['cost']
    return h_values

constraints = [{'agent': 0, 'loc': [(3,4)], 'timestep': 5}]
def build_constraint_table(constraints, agent):
    ##############################
    # Task 1.2/1.3: Return a table that contains the list of constraints of
    #               the given agent for each time step. The table can be used
    #               for a more efficient constraint violation check in the 
    #               is_constrained function.

    # constraints = [{'agent': 0, 'loc': [(3,4)], 'timestep': 5}]
    constraint_table = {}

    for constraint in constraints:
        if constraint['agent'] == agent:
            if constraint['timestep'] in constraint_table:
                constraint_table[constraint['timestep']].append(constraint['loc'][0])
            else:
                constraint_table[constraint['timestep']] = [constraint['loc'][0]]
            # old
            # tobeappended = dict()
            # tobeappended[constraint['timestep']] = constraint['loc']
            # constraint_table.append(tobeappended)
    print(f"Constraint Table: {constraint_table}")
    return constraint_table

def get_location(path, time):
    if time < 0:
        return path[0]
    elif time < len(path):
        return path[time]
    else:
        return path[-1]  # wait at the goal location


def get_path(goal_node):
    path = []
    curr = goal_node
    while curr is not None:
        path.append(curr['loc'])
        curr = curr['parent']
    path.reverse()
    return path
childexample = {'loc': (3,4),
                    'g_val': 2,
                    'h_val': 3,
                    'parent': (0,1),
                     'goal_timestep': 5}

def is_constrained(curr_loc, next_loc, next_time, constraint_table):
    ##############################
    # Task 1.2/1.3: Check if a move from curr_loc to next_loc at time step next_time violates
    #               any given constraint. For efficiency the constraints are indexed in a constraint_table
    #               by time step, see build_constraint_table.
    if next_time in constraint_table:
        list_constrained_locations = constraint_table[next_time]
        # Separate edge constraints from vertex constraints
        list_vertex_constraints = []
        list_edge_constraints = []
        for i in range(len(list_constrained_locations)):
            if len(list_constrained_locations[i]) == 1:
                list_vertex_constraints.append(list_constrained_locations[i])
            else:
                list_edge_constraints.append(list_constrained_locations[i])
        for edge_constraint in list_edge_constraints:
            if [curr_loc,next_loc] == edge_constraint:
                return True
        for constrained_location in list_vertex_constraints:
            if next_loc == constrained_location:
                return True
        # for constrained_location in list_constrained_locations:
        #     if next_loc == constrained_location:
        #         return True
        print(f"List of constrained locations: {list_constrained_locations}")
        print(f"List of edge constraints: {list_edge_constraints}")
        print(f"List of vertex constraints: {list_vertex_constraints}")
    return False

    # old
    # for i in constraint_table:
    #     if childexample['goal_timestep'] == constraint_table[i]['timestep']:
    #         if childexample['loc'] == constraint_table[i]['loc']:
    #             return True
    #         else:
    #             return False
    # else:
    #     return False

def push_node(open_list, node):
    heapq.heappush(open_list, (node['g_val'] + node['h_val'], node['h_val'], node['loc'], node))


def pop_node(open_list):
    _, _, _, curr = heapq.heappop(open_list)
    return curr


def compare_nodes(n1, n2):
    """Return true is n1 is better than n2."""
    return n1['g_val'] + n1['h_val'] < n2['g_val'] + n2['h_val']


def a_star(my_map, start_loc, goal_loc, h_values, agent, constraints):
    print(f"2. Agent number {agent}")
    b = build_constraint_table(constraints, agent)
    agent_is_constrained_at_goal_timestep = is_constrained(childexample['loc'], childexample['loc'], childexample['goal_timestep'], b)
    # print(a)
    """ my_map      - binary obstacle map
        start_loc   - start position
        goal_loc    - goal position
        agent       - the agent that is being re-planned
        constraints - constraints defining where robot should or cannot go at each timestep
    """
    ##############################
    # Task 1.1: Extend the A* search to search in the space-time domain
    #           rather than space domain, only.
    open_list = []
    closed_list = dict()
    earliest_goal_timestep = 0
    h_value = h_values[start_loc]
    root = {'loc': start_loc, 'g_val': 0, 'h_val': h_value, 'parent': None, 'goal_timestep': earliest_goal_timestep}
    print(root)
    push_node(open_list, root)
    closed_list[(root['loc'], root['goal_timestep'])] = root
    while len(open_list) > 0:
        curr = pop_node(open_list)
        #############################
        # Task 1.4: Adjust the goal test condition to handle goal constraints
        if curr['loc'] == goal_loc:
            return get_path(curr)
        for dir in range(4): # somewhere here implement constraint!
            child_loc = move(curr['loc'], dir)
            if my_map[child_loc[0]][child_loc[1]]:
                continue
            child = {'loc': child_loc,
                    'g_val': curr['g_val'] + 1,
                    'h_val': h_values[child_loc],
                    'parent': curr,
                     'goal_timestep': curr['goal_timestep'] + 1}
            if (child['loc']) in closed_list:
                existing_node = closed_list[(child['loc'])]
                if compare_nodes(child, existing_node):
                    closed_list[(child['loc'], child['goal_timestep'])] = child
                    push_node(open_list, child)
            else:
                closed_list[(child['loc'], child['goal_timestep'])] = child
                push_node(open_list, child)

        still = {'loc': curr['loc'],
                    'g_val': curr['g_val'],
                    'h_val': curr['h_val'],
                    'parent': curr,
                     'goal_timestep': curr['goal_timestep'] + 1}
        closed_list[(still['loc'], still['goal_timestep'])] = still
        push_node(open_list, still)



    return None  # Failed to find solutions
