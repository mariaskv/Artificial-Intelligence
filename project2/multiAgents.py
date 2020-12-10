# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()

        "*** YOUR CODE HERE ***"
        value = successorGameState.getScore()
        # keep the distance from every food in a priority queue
        food_distance = util.PriorityQueue()

        for food in newFood.asList():
            distance = manhattanDistance(newPos, food)
            food_distance.push((newPos, food, distance), distance)

        if (not food_distance.isEmpty()):
            #if there is at least one food
            pos, food, distance = food_distance.pop()
            #and its distance is equal to zero return infinity(maximum score) because we are already on the food position
            if(distance == 0):
                return float("inf")
            else:
            #else we divide the points earned by the food with the distance to that point and add it to the score
                value += (10/distance)

        #if there is no food return the current score
        return value




def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    #initialize index, depth
    pacmanIndex = 0
    starting_depth = 0

    #function to check weather a state is terminal
    def terminal_state(self, gameState, cur_index, cur_depth):
        actions = gameState.getLegalActions(cur_index)
        #if there is any action to be done or depth is equal to self ddepth
        terminate = (len(actions) == 0) or (cur_depth == self.depth)
        return terminate

    def result(self, gameState, action, cur_index):
        # return the result of an action
        successor = gameState.generateSuccessor(cur_index, action)
        return successor

    def minimax(self, gameState, cur_index):
        # the minimax algorithm
        #initialize arg_max to the smallest value exist and assign no action
        arg_max = float("-inf")
        arg_max_action = None
        # start from the starting depth
        cur_depth = self.starting_depth

        actions = gameState.getLegalActions(cur_index)

        for action in actions:
            # for every action take the result of that action
            successorState = self.result(gameState, action, cur_index)
            # increase the index
            next_index = cur_index + 1
            # take the value of that result at the current index and depth
            value = self.min_value(successorState, next_index, cur_depth)

            # if the value is greater than argmax set argmax as value and assign at it the current action
            if(arg_max < value):
                arg_max = value
                arg_max_action = action

        # when all the actions are checked return argmax's action
        return arg_max_action

    def find_max(self, max_v, value):
        if(value > max_v):
            max_v = value
        return max_v

    # max value algorithm as it is in the lesons's notes
    def max_value(self, gameState, cur_index, cur_depth):
        cur_depth += 1
        if(self.terminal_state(gameState, cur_index, cur_depth)):
            return  self.evaluationFunction(gameState)

        max_v = float("-inf")
        actions = gameState.getLegalActions(cur_index)

        for action in actions:
            successorsState = self.result(gameState, action, cur_index)
            next_index = cur_index + 1
            value = self.min_value(successorsState, next_index, cur_depth)
            max_v = self.find_max(max_v, value)

        return max_v

    def find_min(self, min_v, value):
        if (value < min_v):
            min_v = value
        return min_v

    # min value algorithm as it is in the lesons's notes
    def min_value(self, gameState, cur_index, cur_depth):
        if (self.terminal_state(gameState, cur_index, cur_depth)):
            return self.evaluationFunction(gameState)

        min_v = float("inf")
        actions = gameState.getLegalActions(cur_index)

        no_ghosts = gameState.getNumAgents()-1
        all_ghosts_checked = (cur_index == no_ghosts)

        for action in actions:
            successorsState = self.result(gameState, action, cur_index)
            if(not all_ghosts_checked):
                # if not all ghosts are checked call min for the next ghost
                next_index = cur_index + 1
                value = self.min_value(successorsState, next_index, cur_depth)
                min_v = self.find_min(min_v, value)
            else:
                # else call max for pacman
                new_index = self.pacmanIndex
                value = self.max_value(successorsState, new_index, cur_depth)
                min_v = self.find_min(min_v, value)

        return min_v



    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return  self.minimax(gameState, self.index)
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    pacmanIndex = 0
    starting_depth = 0

    def terminal_state(self, gameState, cur_index, cur_depth):
        actions = gameState.getLegalActions(cur_index)
        terminate = (len(actions) == 0) or (cur_depth == self.depth)
        return terminate

    def result(self, gameState, action, cur_index):
        successor = gameState.generateSuccessor(cur_index, action)
        return successor

    def alphabeta(self, gameState, cur_index):
        arg_max = float("-inf")
        arg_max_action = None
        cur_depth = self.starting_depth
        # initialize a, b values
        a = float("-inf")
        b = float("inf")

        actions = gameState.getLegalActions(cur_index)

        for action in actions:
            successorState = self.result(gameState, action, cur_index)
            next_index = cur_index + 1
            # take the min value
            value = self.min_value(successorState, next_index, cur_depth, a, b)

            # if argmax < value set argmax to value and assign its action to the current action
            if(arg_max < value):
                arg_max = value
                arg_max_action = action

            # if value > b return
            if(value > b):
                return arg_max_action

            # else assign to a the max value and return
            a = self.find_max(a, value)

        return arg_max_action

    def find_max(self, max_v, value):
        if(value > max_v):
            max_v = value
        return max_v

    # max value algorithm as it is in the lesons's notes
    def max_value(self, gameState, cur_index, cur_depth, a, b):
        cur_depth += 1
        if(self.terminal_state(gameState, cur_index, cur_depth)):
            return  self.evaluationFunction(gameState)

        max_v = float("-inf")
        actions = gameState.getLegalActions(cur_index)

        for action in actions:
            successorsState = self.result(gameState, action, cur_index)
            next_index = cur_index + 1
            value = self.min_value(successorsState, next_index, cur_depth, a, b)
            max_v = self.find_max(max_v, value)
            if(value > b):
                return value

            a = self.find_max(a, value)

        return max_v

    def find_min(self, min_v, value):
        if (value < min_v):
            min_v = value
        return min_v

    # min value algorithm as it is in the lesons's notes
    def min_value(self, gameState, cur_index, cur_depth, a, b):
        if (self.terminal_state(gameState, cur_index, cur_depth)):
            return self.evaluationFunction(gameState)

        min_v = float("inf")
        actions = gameState.getLegalActions(cur_index)

        no_ghosts = gameState.getNumAgents()-1
        all_ghosts_checked = (cur_index == no_ghosts)

        for action in actions:
            successorsState = self.result(gameState, action, cur_index)
            # if not all ghosts cheched call min value for next ghost
            if(not all_ghosts_checked):
                next_index = cur_index + 1
                value = self.min_value(successorsState, next_index, cur_depth, a, b)
                min_v = self.find_min(min_v, value)
            # else call max value for pacman
            else:
                new_index = self.pacmanIndex
                value = self.max_value(successorsState, new_index, cur_depth, a, b)
                min_v = self.find_min(min_v, value)

            if(value < a):
                return value

            b = self.find_min(b, value)

        return min_v

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        return  self.alphabeta(gameState, self.index)

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    pacmanIndex = 0
    starting_depth = 0

    def terminal_state(self, gameState, cur_index, cur_depth):
        actions = gameState.getLegalActions(cur_index)
        terminate = (len(actions) == 0) or (cur_depth == self.depth)
        return terminate

    def result(self, gameState, action, cur_index):
        successor = gameState.generateSuccessor(cur_index, action)
        return successor

    # same as minimax agent
    def expectiimax(self, gameState, cur_index):
        arg_max = float("-inf")
        arg_max_action = None
        cur_depth = self.starting_depth

        actions = gameState.getLegalActions(cur_index)

        for action in actions:
            successorState = self.result(gameState, action, cur_index)
            next_index = cur_index + 1
            value = self.min_value(successorState, next_index, cur_depth)

            if(arg_max < value):
                arg_max = value
                arg_max_action = action

        return arg_max_action

    def find_max(self, max_v, value):
        if(value > max_v):
            max_v = value
        return max_v

    def max_value(self, gameState, cur_index, cur_depth):
        cur_depth += 1
        if(self.terminal_state(gameState, cur_index, cur_depth)):
            return  self.evaluationFunction(gameState)

        max_v = float("-inf")
        actions = gameState.getLegalActions(cur_index)

        for action in actions:
            successorsState = self.result(gameState, action, cur_index)
            next_index = cur_index + 1
            value = self.min_value(successorsState, next_index, cur_depth)
            max_v = self.find_max(max_v, value)

        return max_v

    def find_min(self, min_v, value):
        if (value < min_v):
            min_v = value
        return min_v

    def min_value(self, gameState, cur_index, cur_depth):
        if (self.terminal_state(gameState, cur_index, cur_depth)):
            return self.evaluationFunction(gameState)

        actions = gameState.getLegalActions(cur_index)

        no_ghosts = gameState.getNumAgents()-1
        all_ghosts_checked = (cur_index == no_ghosts)

        # take the amount of actions
        div = len((actions))
        return_value = 0.0

        for action in actions:
            successorsState = self.result(gameState, action, cur_index)
            if(not all_ghosts_checked):
                next_index = cur_index + 1
                value = self.min_value(successorsState, next_index, cur_depth)
            else:
                new_index = self.pacmanIndex
                value = self.max_value(successorsState, new_index, cur_depth)

            # each time increase the return_value by the current value
            return_value = return_value + value

        # return the average of all values
        return return_value * (1.0/div)

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return  self.expectiimax(gameState, self.index)
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()

    "*** YOUR CODE HERE ***"
    # keep the distance from every food in a priority queue
    food_distance = util.PriorityQueue()

    # value is the current score
    value = currentGameState.getScore()

    for food in newFood.asList():
        # keep the manchatan distance from every food
        distance = manhattanDistance(newPos, food)
        food_distance.push(distance, distance)

    if (not food_distance.isEmpty()):
        # if there is at least one food
        distance = food_distance.pop()
        # and its distance is equal to zero return infinity(maximum score) because we are already on the food position
        if (distance == 0):
            return float("inf")
        else:
            # else we divide the points earned by the food with the distance to that point and add it to the score
            value += (10 / distance)

    # if there is no food return the current score
    return value

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
