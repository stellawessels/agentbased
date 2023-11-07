import heapq


def move(loc, dir):
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0), (0, 0)]
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


def build_constraint_table(constraints, agent):
    ##############################
    # Task 1.2/1.3: Return a table that constraints the list of constraints of
    #               the given agent for each time step. The table can be used
    #               for a more efficient constraint violation check in the
    #               is_constrained function.
    constraint_table = {}
    for constraint in constraints:
        if constraint['agent'] == agent:
            # check if there is a constraint at this timestep already
            if constraint['timestep'] in constraint_table:
                # if True, append a new constraint
                constraint_table[constraint['timestep']].append(
                    constraint['loc'])
            else:
                # if False, create a new key for the timestep and add the constraint
                constraint_table[constraint['timestep']] = [
                    constraint['loc']]
    return constraint_table


def build_goal_constraint_table(constraints, agent, goals):
    goal_constraint_table = {}
    for constraint in constraints:
        if constraint['agent'] == agent:
            if constraint['loc'] == [goals[agent]]:
                if constraint['timestep'] in goal_constraint_table:
                    goal_constraint_table[constraint['timestep']].append(constraint['loc'])
                else:
                    goal_constraint_table[constraint['timestep']] = [constraint['loc']]
    return goal_constraint_table


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
    pathlength_previousagent = len(path)
    goal_previousagent = path[-1]
    return path


def is_constrained(curr_loc, next_loc, next_time, constraint_table):
    ##############################
    # Task 1.2/1.3: Check if a move from curr_loc to next_loc at time step next_time violates
    #               any given constraint. For efficiency the constraints are indexed in a constraint_table
    #               by time step, see build_constraint_table.

    # Execute if the key next_time is in the constraint table
    if next_time in constraint_table:
        # Make a list of constrained locations
        list_constrained_locations = constraint_table[next_time]
        # Separate edge constraints from vertex constraints
        # This is done by separating the constraints with 1 element (next_loc, vertex constraint)
        # from the constraints with 2 (or !=1) elements ((curr_loc, next_loc), edge constraint)
        list_vertex_constraints = []
        list_edge_constraints = []
        for i in range(len(list_constrained_locations)):
            if len(list_constrained_locations[i]) == 1:
                list_vertex_constraints.append(list_constrained_locations[i][0])
            else:
                list_edge_constraints.append(list_constrained_locations[i])
        # Check if there is a constraint
        for edge_constraint in list_edge_constraints:
            if [curr_loc, next_loc] == edge_constraint:
                return True

        for constrained_location in list_vertex_constraints:
            if next_loc == constrained_location:
                return True
    return False


def push_node(open_list, node):
    heapq.heappush(open_list, (node['g_val'] + node['h_val'], node['h_val'], node['loc'], node))


def pop_node(open_list):
    _, _, _, curr = heapq.heappop(open_list)
    return curr


def compare_nodes(n1, n2):
    """Return true is n1 is better than n2."""
    return n1['g_val'] + n1['h_val'] < n2['g_val'] + n2['h_val']


def a_star(my_map, start_loc, goal_loc, h_values, agent, constraints, goals, path_lengths):
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
    timestep = 0
    current_timestep = 0
    constraint_table = build_constraint_table(constraints, agent)  # builds constraint table
    # print(f"constraint_table {constraint_table}")
    goal_constraint_table = build_goal_constraint_table(constraints, agent, goals)  # builds goal constraint table
    if len(goal_constraint_table) == 0:
        earliest_goal_constraint_timestep = 0
    else:
        earliest_goal_constraint_timestep = max(goal_constraint_table.keys())
    h_value = h_values[start_loc]
    root = {'loc': start_loc, 'g_val': 0, 'h_val': h_value, 'parent': None, 'timestep': timestep}
    push_node(open_list, root)
    closed_list[(root['loc'], root['timestep'])] = root
    #print("timestep", timestep)
    #print(agent)


    while len(open_list) > 0:
        curr = pop_node(open_list)
        # Ensure that if there is no solution due to priority, the algorithm stops after a certain amount of time
        if curr['timestep'] > 3 * len(my_map) * len(my_map[0]):
            return None
        if len(path_lengths) > 0 and curr['timestep'] > 3 * path_lengths[-1]:
            return None
        #############################
        # Task 1.4: Adjust the goal test condition to handle goal constraints
        current_timestep = curr['timestep']


        if curr['loc'] == goal_loc and current_timestep > earliest_goal_constraint_timestep:
            return get_path(curr)
        if agent > 0:
            if len(path_lengths) > 0 and current_timestep + 1 > path_lengths[-1] - 1:
                if current_timestep + 1 in constraint_table:
                    constraint_table[current_timestep + 1].append([goals[agent - 1]])
                else:
                    constraint_table[current_timestep + 1] = [[goals[agent - 1]]]
        for dir in range(5):
            child_loc = move(curr['loc'], dir)
            if child_loc[0] < 0 or child_loc[0] >= len(my_map) \
                    or child_loc[1] < 0 or child_loc[1] >= len(my_map[0]):
                continue
            if my_map[child_loc[0]][child_loc[1]]:
                continue
            child = {'loc': child_loc,
                     'g_val': curr['g_val'] + 1,
                     'h_val': h_values[child_loc],
                     'parent': curr,
                     'timestep': curr['timestep'] + 1}
            # check if there is a constraint present, continue if True
            if is_constrained(curr['loc'], child_loc, child['timestep'], constraint_table):
                continue
            if (child['loc'], child['timestep']) in closed_list:
                existing_node = closed_list[(child['loc'], child['timestep'])]
                if compare_nodes(child, existing_node):
                    closed_list[(child['loc'], child['timestep'])] = child
                    push_node(open_list, child)
            else:
                closed_list[(child['loc'], child['timestep'])] = child
                push_node(open_list, child)
                # Use the push_node function to push child to open_list

    return None # Failed to find solutions