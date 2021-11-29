#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import argparse
import pandas as pd
import csv
import heapq
driving_data_sheet = pd.read_csv('driving2.csv')
zones_data_sheet = pd.read_csv('zones.csv')
parks_data_sheet = pd.read_csv('parks.csv')
#Created a node class so that each state can carry the following attributes. This will make it easier to access their respective values.
#function names are self explanetory.
class Node:
    def __init__(self, state):
        self.state = state
        self.neighbors = 0
        self.zone = 0 
        self.parks = 0
        
    def findZone(self):
        state = self.state
        zone = zones_data_sheet[state][0]
        self.zone = zone
        

    def findNeighbors(self):
        state = self.state
        for num in range(0, len(driving_data_sheet.columns)-1):
            if driving_data_sheet.loc[num][0] == state: #looping until we find the corresponding state

                neighbors = dict(driving_data_sheet.loc[num])
                del neighbors['STATE'] # right here, we are deleting the first state column so that we can keep the values/neighbors that correspond to the state.
                neighbors = {key:value for (key,value) in neighbors.items() if value > 0} #grouping the column/row values into a dictionary

                groupNeighbors=[]
                for key,values in neighbors.items():
                    groupNeighbors.append([key,values]) # Storing the key/value pairs into a list, later they will be modified so we can put the zone value in the list
                
                self.neighbors = groupNeighbors #setting instance variable neighbors to the neighbor/value pairs

    def findParks(self):
        state = self.state
        parks = parks_data_sheet[state][0]
        self.parks = parks
        
def assignmentIsComplete(csp,assignment):
    visitedParks = 0
    start = list(assignment.keys())[0]
    end = None
    pathCost = 0
    statesOnPath=[]
    for value in assignment: #looping to calculate the number of parks visited and the states in the following path.
        if assignment[value][1] != None:
            visitedParks = visitedParks + assignment[value][1]
            statesOnPath.append(assignment[value][0])
            end = assignment[value][0]
    if (visitedParks >= csp['constraint'][0]) and (end in csp['constraint'][1]): # if assignment meets the contraints ( >= NoOfParksToVisit and ends in the four states)
        for num in range(start+1, len(assignment)+start): # after we verified that our assignment is complete then we calculate the path cost
            pathCost = pathCost + assignment[num][2]
            
        print("\nThe Assignment was completed...\n")
        print("(BackTrackSearch Algorithm)\n====================================\nName: George Tapia (A20450857)")
        print("Initial State:",initialState,'\nMinimum number of parks:',parksTovisit,"\nSolutionPath:", statesOnPath,"\nNumber of states on path:", len(statesOnPath))
        print("Path cost:",pathCost,'\nNumber of national parks visited:',visitedParks)
        print('Zone assignments:',assignment)
        return assignment
    else:
        return False
    
def findVariables(state):#this function finds the number of zone variables and returns them in a dictionary with the initial state set
    variables= {}
    variables[state.zone] = [state.state,state.parks]
    for zone in range(state.zone+1, 13):
        variables.setdefault(zone, [None,None])
    return variables

def selectUnassignedVariable(csp,assignment): # this function loops through the assignment dictionary to find the next empty/none zone variable
    for variable in assignment:
        if assignment[variable][0] == None:
            return variable
        
def orderDomainValues(csp,var,assignment):#here, we are finding the domain values of the current zone which are the neighbors of the last assigned zone value.
    # assignment[var-1] finds thenprevious zone assignment domain/state so that the current unassigned zone can use these as its domain values. If there is none, then it will return empty
    #the current unassigned zone depends on the previous zone assignment because each state in the same zone can't visit the same states, some could but not all.
    state = assignment[var-1][0] 
    state = Node(state)
    state.findNeighbors() # finds the neighbors of the last assigned zone domain value
    successors = state.neighbors
    successors.sort(key=lambda x:x[0]) #sorts the list of neighbors paired with their distances to each neighbor, in alphabetical order
    for successor in successors: # here, we find the zone value and insert it into position two. Yes, I know this time complexity is not as good
        #because on inserts, we have to allocate new memory, shift the element down and deallocate the previous.
        current = Node(successor[0])
        current.findParks()
        successor.insert(1,current.parks)
    csp['domains'] = successors
    return csp['domains']

def noSolution():
    print("\nThe assignment was not complete...\n")
    print("(BackTrackSearch Algorithm)\n====================================\nName: George Tapia (A20450857)")
    print("Solution path: FAILURE: NO PATH FOUND")
    print("Number of states on path:", 0)
    print("Path cost:",0,'\nNumber of national parks visited:',0)
    
def backTrackingSearch(csp): #calls the backtrack function till it returns false or True, this could've returned what backtrack search returns but made it this way for printing
    result = backTrack(csp,assignment)
    if result == False:
        return noSolution()
    else:
        return

def backTrack(csp,assignment):
    if assignment[12][0]!=None: #checks to see if the assigmnent is full, then calls the assignment complete function to return if it is complete or not(False)
        return assignmentIsComplete(csp, assignment)
    var = selectUnassignedVariable(csp,assignment) #selects next unassigned zone variable
    for value in orderDomainValues(csp,var,assignment): #loops through each domain values for the current zone.
        assignment[var] = value #setting the domain of the current zone as a trio of [state,zone, distanceFromPreviousState]
#         print('Current Zone',var,'\nDomains',csp['domains'],'\nAssignment to zone',var, value,'\nAssignment',assignment,'\n\n')
        #recursively calls bactrack and passes the assignment, will take one route all the way down the left side of the tree, then walk back up the tree
        #as it walks up, it finds the next state with neighbors, goes down its path and fills up on assignments to see if it is the solution or not
        result = backTrack(csp, assignment) 
        if result != False:
            return
    assignment[var] = [None,None] #as we walk back up the tree, this sets the variable zones to none/unassigned so that we can use them as we go down the next path
    return False


if __name__== "__main__":
        try:
            states = list(driving_data_sheet.columns.values[1:])
            string = argparse.ArgumentParser()
            string.add_argument("state1",type = str,help = "Initial state")
            string.add_argument("parks",type = int,help = "Number of parks Intended to visit")
            argument = string.parse_args()
            arg1 = argument.state1
            arg2 = argument.parks
            arg1 = arg1.upper()
            if arg1 in states:
                initialState = arg1
                parksTovisit = arg2
            else:
                raise ValueError('ERROR: Not enough or too many input arguments. Inputs might be incorrect.\nInput(1) should be in list of states and Input(2) should be an int type.')
        except ValueError as flag:
            print(flag)
            print("\nHere's the list of states:")
            print(*states,'\n')
            exit(1)


state = Node(initialState)
state.findNeighbors()
state.findZone()
state.findParks()
assignment = findVariables(state)
counter = 0
csp ={'variables':findVariables(state),'domains':state.findNeighbors(),'constraint':[parksTovisit,['CA','NV','OR','WA']]}
# print('Initial State:',state.state, '\nParks to visit:', parksTovisit,'\nCurrent Zone:',state.zone,'\nAssignment to zone', state.zone, [state.state,state.parks],'\nAssignment',assignment)
# print()
backTrackingSearch(csp)

