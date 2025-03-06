# CS 471
# Project 1
# By Areyan Rastawan and Nikhar Ramlakhan

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

def depthFirstSearch(problem: SearchProblem):
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
     #create a stack 
    stack = util.Stack()
     # push the start state and an empty list to the stack 
     # list will keep track o factions taken to reach each state
    stack.push((problem.getStartState(), []))

    #create a set to keep track of explored states
    explored = set() 

    #while the stack is not empty
    while not stack.isEmpty():
        
        #pop the state and path from the stack
        state, path = stack.pop()

        #check if that state is a goal state , if so return the path to it
        if problem.isGoalState(state):
            return path
        
        # if the state has not been explored
        if state not in explored:
            #mark it as explored 
            explored.add(state)

            #expand the current state by checking each of its succesors
            for successor, action, cost in problem.getSuccessors(state):
                # if successor has not been explored add it to the stack
                if successor not in explored:
                    #update path by adding the action taken to reach this sucessor
                    stack.push((successor, path + [action]))
                    
    #if no paths are found return an empty list
    return []
    
    

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    queue = util.Queue() # create a queue data structure
    
    # push (enquque) the start state onto the queue with an empty path
    queue.push((problem.getStartState(), []))
    
    # use a set to track explored states
    explored = set()
    
    #if the stack is not empty
    while not queue.isEmpty():
        # pop the next node (FIFO order for BFS)
        state, path = queue.pop()
        
        # goal test
        if problem.isGoalState(state):
            return path
        
        # mark the current state as explored
        if state not in explored:
            explored.add(state)
            

          # expands each node by generating its successors, 
          # filters out nodes already explored or in the queue, 
          # and pushes the valid successors onto the queue with an updated path
            for successor, action, cost in problem.getSuccessors(state): # loops though the successors of the current state
                if successor not in explored and not any(successor == s for s, _ in queue.list): # check if successor is already in the quque 
                    queue.push((successor, path + [action])) #push the successor onto the queue with the updated path
                    
    return []


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #use a priotity queue to store the nodes
    priorityQueue = util.PriorityQueue()
    
    # push the start state with an initial cost of 0
    # the path list will store the sequence of actions taken to reach this state
    priorityQueue.push((problem.getStartState(), [], 0), 0)  # (state, path, cost), priority = cost
    
    # use a dictionary to track the lowest cost at which each state has been explored
    explored = {}

    # while there are nodes to explore in the priority queue
    while not priorityQueue.isEmpty():
        # pop the node with the lowest cumulative cost (becuase we put the cheapest one first)
        state, path, cost = priorityQueue.pop()

        # check if the current popped state is the goal state; if so, return the path to it
        if problem.isGoalState(state):
            return path
        
        # If the state hasn't been explored or at a lower cost
        if state not in explored or cost < explored[state]:
            # Mark the state as explored with this cost
            explored[state] = cost
            
            # Expand the current state by checking each of its successors
            for successor, action, step_cost in problem.getSuccessors(state):
                # Calculate the cumulative cost to reach this successor
                new_cost = cost + step_cost
                # If the successor hasn't been explored at a lower cost
                if successor not in explored or new_cost < explored.get(successor, float('inf')):
                    # Push the successor onto the priority queue with the updated cost and path
                    priorityQueue.push((successor, path + [action], new_cost), new_cost) # priority queue takes two args


                     #explored.get(successor, float('inf')):    This line looks up the prev cost to reach this succ in our dictionary

    # If no solution is found, return an empty list
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    #use priotity queue to store the nodes
    priority_queue = util.PriorityQueue()
    
    # Push the start state with an initial cost of 0
    start_state = problem.getStartState()
    priority_queue.push((start_state, [], 0), 0 + heuristic(start_state, problem))  # (state, path, cost), priority = g(n) + h(n)
    
    # Use a dictionary to track the lowest cost at which each state has been explored
    explored = {}

    # While there are nodes to explore in the priority queue
    while not priority_queue.isEmpty():
        # Pop the node with the lowest cumulative cost + heuristic
        state, path, cost = priority_queue.pop()

        # Check if the current state is the goal state; if so, return the path to it
        if problem.isGoalState(state):
            return path
        
        # If the state hasn't been explored at a lower cost
        if state not in explored or cost < explored[state]:
            # Mark the state as explored with this cost
            explored[state] = cost
            
            # Expand the current state by checking each of its successors (search class for parameters)
            for successor, action, step_cost in problem.getSuccessors(state):
                # Calculate the cumulative cost to reach this successor
                newCost = cost + step_cost
                # Calculate f(n) = g(n) + h(n) for the priority
                priority = newCost + heuristic(successor, problem)
                # If the successor hasn't been explored at a lower cost
                if successor not in explored or newCost < explored.get(successor, float('inf')):
                    # Push the successor onto the priority queue with the updated cost + heuristic
                    priority_queue.push((successor, path + [action], newCost), priority)

    # If no solution is found, return an empty list
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

