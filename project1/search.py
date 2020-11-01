# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    #create an empty list to save the solution path
    solution = []

    #initialize the frontier with an empty stack
    frontier = util.Stack()

    #take the start state

    node = problem.getStartState()
    #push the start state with an empty solution at the frontier
    frontier.push((node, solution))

    #initialize the explored set
    ExploredSet = set([])

    while(not frontier.isEmpty()):

        #if the frontier is not empty pop out a node
        node, solution = frontier.pop()

        #and check if that node is a goal state
        if(problem.isGoalState(node)):
            return solution

        #add that node to the set if there is not exist
        if node not in ExploredSet:
            ExploredSet.add(node)

        #for every possible successor state if exists in the set set flag true
        for succ in problem.getSuccessors(node):
            if(succ[0] in ExploredSet):
                flag_set = True
            else:
                flag_set = False

            flag_frontier = False
            #for every succ state check if exists at the frontier too
            for entry in frontier.list:
                if(entry[0] == succ[0]):
                    flag_frontier = True
                    break

            #if the succ state does not exist at the set, insert it at the frontier
            #insert the succ and insert at the solution list the action needed to reach that state
            #flag_set == False
            if(not flag_set):
                frontier.push((succ[0], solution + [succ[1]]))

    return []


    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #initialize an empty list for the solution
    solution = []

    #get a start state
    node = problem.getStartState()

    #initialize frontier as an queue and insert the start node with an empty solution list
    frontier = util.Queue()
    frontier.push((node, solution))

    #initialize an empty explored set
    ExploredSet = set([])

    while(not frontier.isEmpty()):

        #if the frontier is not empty pop out a node
        node, solution = frontier.pop()

        #if a goal state is found return the solution
        if problem.isGoalState(node):
            return solution

        #add the node to the set if there is not exist
        if node not in ExploredSet:
            ExploredSet.add(node)

        #for every successor state check if exists at the frontier and at the set
        for succ in problem.getSuccessors(node):
            if(succ[0] in ExploredSet):
                flag_set = True
            else:
                flag_set = False

            flag_frontier = False
            for entry in frontier.list:
                if(entry[0] == succ[0]):
                    flag_frontier = True
                    break

            #if the successor does not exist neither at the set or frontier push it at the frontier
            if(not(flag_frontier or flag_set)):
                #push the succcessor with a list increased by the action to reach the successor
                frontier.push((succ[0], solution + [succ[1]]))



    return []
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #the UCS algorithm is based on the bfs algorithm

    #initialize an empty list for the solution
    solution = []

    #get a start node
    node = problem.getStartState()

    #initialize its cost to zero
    node_cost = 0

    #initialize frontier as an empty pq
    frontier = util.PriorityQueue()

    #insert at the pq the start node,with an empty solution list and a zero cost variable
    frontier.push((node, solution, node_cost), node_cost)

    #initialize the explored set
    ExploredSet = set([])

    while(not frontier.isEmpty()):

        #if the frontier is not empty pop out a node
        node, solution, node_cost = frontier.pop()

        #if the node is a goal state return its solution list
        if problem.isGoalState(node):
            return solution

        #if the node is not at the explored set insert it
        if node not in ExploredSet:
            ExploredSet.add(node)

            #for every successor state check if there is at the explored set and at the frontier
            for succ in problem.getSuccessors(node):
                if(succ[0] in ExploredSet):
                    flag_set = True
                else:
                    flag_set = False

                flag_frontier = False
                for entry in frontier.heap:
                    if(entry[0] == succ[0]):
                        flag_frontier = True
                        break

                #get cost of actions for the solution already have and the action needeed to reach the successor state
                path_cost = problem.getCostOfActions(solution + [succ[1]])


                #if the successor state does not exist neither at the set,frontier insert it
                if (not (flag_set or flag_frontier)):
                    frontier.push((succ[0], solution + [succ[1]], path_cost), path_cost)

                #else if already exists and a cheapest path is found update it
                elif (flag_frontier) and (path_cost < node_cost):
                    frontier.update((succ[0], solution + [succ[1]], path_cost), path_cost)


    return []
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    #initialize an empty solution list
    solution = []

    #get a start node
    node = problem.getStartState()

    #initialize frontier as an empty pq
    frontier = util.PriorityQueue()

    #initialize the cost as the sum of getCostofActions and heuristic functions together
    fn = problem.getCostOfActions(solution) + heuristic(node, problem)

    #push at the frontier the node with the solution using the fn as priority
    frontier.push((node, solution), fn)

    #initialize the explored set
    ExploredSet = set([])

    while (not frontier.isEmpty()):

        #if the frontier is not empty pop out a node
        node, solution = frontier.pop()

        #if the node is a goal state return its solution
        if problem.isGoalState(node):
            return solution

        #if the node does not exist at the explored set insert it
        if(node not in ExploredSet):
            ExploredSet.add(node)

            #for every successor state check if exists at the set or frontier
            for succ in problem.getSuccessors(node):

                if(succ[0] in ExploredSet):
                    flag_found_explored = True
                else:
                    flag_found_explored = False

                flag_found_frontier = False
                for entry in frontier.heap:
                    if(entry[0] == succ[0]):
                        flag_found_frontier = True
                        break

                #if the succ does not exist at the frontier or set push it with the new fn
                if(not (flag_found_frontier or flag_found_explored) ):
                    fn = problem.getCostOfActions(solution + [succ[1]]) + heuristic(succ[0], problem)
                    frontier.push((succ[0], solution+[succ[1]]), fn)

    return []
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
