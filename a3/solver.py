import rubik
from collections import deque

# Class to store the state of the node
class node_info:
    def __init__(self, st, parent, order):
        self.st = st
        self.parent = parent
        self.order = order

# Gets the next frontier
def next_frontier(frontier, p_nodes):
    starting_order = frontier[0].order

    """
    Invariant: At each iteration, we are looking at the nodes in the frontier of the same order as starting_order
    Initialization: The order of the frontier node is the same as starting_order
    Maintenance: Given that the starting_order and frontier node order is the same, the loop will continue 
    Termination: The order of the frontier no longer equals the order we want to look at 
    """
    while starting_order == frontier[0].order:
        elm = frontier.popleft()

        """
        Invariant: At each iteration, the position of move in quarter_twists is less than the len(quarter_twists)
        Initialization: There are moves in quarter_twists
        Maintenance: Given that there are still moves in quarter_twists to go through, the loop will continue 
                     and apply the permutation to the node and add the permutation to the frontier if it
                     doesn't already exist
        Termination: We have gone through the entire tuple of twists 
        """
        # Changes the rubik state
        for move in rubik.quarter_twists:
            move_st = rubik.perm_apply(move, elm.st)
            # Checks to see if the new move_st is not in the nodes list
            if move_st not in p_nodes:
                # new node_info with the new move_st, the move command it took
                # frontier that was popped, and the new depth of node
                new_st = node_info(move_st, (move, elm), elm.order + 1)
                frontier.append(new_st)
                p_nodes.append(move_st)


def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves.

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_apply
    """

    # Start side of BFS
    start_init = node_info(start, (None, None), 0)
    s_frontier = deque([start_init])
    s_parents = []

    # End side of BFS
    end_init = node_info(end, (None, None), 0)
    e_frontier = deque([end_init])
    e_parents = []
    
    # Flag determines which side we need to advance the frontier
    # When flag is 1 it means that we might advance the left frontier
    # When flag is -1 it means we might advance the right frontier
    flag = 1

    # Test to see if the two given states (start, end) are the same
    # We know to return an empty list

    """
    Invariant: At each iteration, the position of l_elm in s_frontier is less than the len(s_frontier)
    Initialization: There is a list called s_frontier that has elements in it
    Maintenance: Given that there are still elements in s_frontier to go through, the loop will continue 
    Termination: We have reached the end of s_frontier or the two given states are the same, thus returning an 
                 empty list because no path needs to be found
    """
    for l_elm in s_frontier:
        """
        Invariant: At each iteration, the position of r_elm in e_frontier is less than the len(e_frontier)
        Initialization: There is a list called e_frontier that has elements in it
        Maintenance: Given that there are still elements in e_frontier to go through, the loop will continue and 
                     check to see if the the states are the same
        Termination: We have reached the end of e_frontier or the two given states are the same, thus returning an 
                     empty list because no path needs to be found
        """
        for r_elm in e_frontier:
            if l_elm.st == r_elm.st:
                return []

    found = False

    """
    Invariant: At each iteration, the solution has not been found
    Initialization: found = False 
    Maintenance: Given that we have not found a solution, the function will alternate between the start and end 
                 sides (bidirectional) to create a new frontier and check its values for a solution
    Termination: The cube is unsolvable (order exceeds 7) or we have found a solution
    """
    # Run while False
    while not found:
        # Checks the depth of the nodes in both frontiers
        # If their order exceeds 7, then there is no shortest path
        if s_frontier[0].order > 6 and e_frontier[0].order > 6:
            return None

        # Flag alternates the sides
        if flag == 1:
            # Gets the next frontier
            next_frontier(s_frontier, s_parents)
            flag = flag * (-1)
        else:
            # Gets the next frontier
            next_frontier(e_frontier, e_parents)
            flag = flag * (-1)

        # Checking to see if there is the same block state in each list
        
        """
        Invariant: At each iteration, the position of l_elm in s_frontier is less than the len(s_frontier)
        Initialization: There is a list called s_frontier that has elements in it
        Maintenance: Given that there are still elements in s_frontier to go through, the loop will continue 
        Termination: We have reached the end of s_frontier or the intersection of the two ends has been found
        """
        # Grabs a left element from the starting frontier
        for l_elm in s_frontier:
         
            """
            Invariant: At each iteration, the position of r_elm in e_frontier is less than the len(e_frontier)
            Initialization: There is a list called e_frontier that has elements in it
            Maintenance: Given that there are still elements in e_frontier to go through, the loop will continue and 
                         check to see if s_frontier and e_frontier has an intersection
            Termination: We have reached the end of e_frontier or the intersection of the two ends has been found
            """
            # Compares it to each of the right elements from the end frontier
            for r_elm in e_frontier:
                # If we find an element that matches
                if l_elm.st == r_elm.st:
                    # Find the intersect of the two lists
                    intersect = (l_elm, r_elm)
                    # We set found to true
                    found = True
                    # Then break out of the loop
                    break
            # If the element was found we can break out of this loop as well
            if found == True:
                break
    # Creates a lsit for return
    final_list = []
    # Temp variable to hold l_elm
    l_temp = intersect[0]

    """
    Invariant: At each iteration, there are still nodes to be added to the final solution list
    Initialization: The current node does not equal the first parent node of start
    Maintenance: Given that we have not reached the first parent node of start, the parent of the current node is 
                 added to the beginning of the final solution list. The new node to look at is then updated.
    Termination: We have reached the first parent node of start and now have a list of its path
    """
    
    # Gets the parent of l_temp (l_elm) until the start state
    while (l_temp.st != start):
        final_list.insert(0, l_temp.parent[0])
        l_temp = l_temp.parent[1]

    r_temp = intersect[1]

    """
    Invariant: At each iteration, there are still nodes to be added to the final solution list
    Initialization: The current node does not equal the first parent node of end
    Maintenance: Given that we have not reached the first parent node of end, the parent of the current node is 
                 added to the end of the final solution list. The new node to look at is then updated.
    Termination: We have reached the first parent node of end and now have a list of its path connecting start to end
    """
    # Gets the parent of r_temp (r_elm) until the end state
    # Perm inverse is because we have to do the inverse of each move to get the parent.
    while (r_temp.st != end):
        final_list.append(rubik.perm_inverse(r_temp.parent[0]))
        r_temp = r_temp.parent[1]

    return final_list
