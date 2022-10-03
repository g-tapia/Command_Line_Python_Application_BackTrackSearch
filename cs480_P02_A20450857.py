

import sys
import argparse
import pandas as pd
import csv
import heapq

driving_data_sheet = pd.read_csv('driving2.csv')
zones_data_sheet = pd.read_csv('zones.csv')
parks_data_sheet = pd.read_csv('parks.csv')


class Node:
    def __init__(self, state):
        self.name = state
        self.neighbors = self.findNeighbors()
        self.zone = self.findZone()
        self.parks = self.findParks()
        
    def findZone(self):
        state = self.name
        zone = zones_data_sheet[state][0]
        # self.zone = zone
        return zone
        

    def findNeighbors(self):
        state = self.name
        for num in range(0, len(driving_data_sheet.columns)-1):
            if driving_data_sheet.loc[num][0] == state: 

                neighbors = dict(driving_data_sheet.loc[num])
                del neighbors['STATE'] 
                neighbors = {key:value for (key,value) in neighbors.items() if value > 0} 

                groupNeighbors=[]
                for key,values in neighbors.items():
                    groupNeighbors.append([key,values]) 
                
                return groupNeighbors 

    def findParks(self):
        state = self.name
        parks = parks_data_sheet[state][0]
        return parks


    

def findVariables(state):
    variables= {}
    variables[state.zone] = [state.name,state.parks]
    for zone in range(state.zone+1, 13):
        variables.setdefault(zone, [None,None])
    return variables

def selectUnassignedVariable(csp,assignment): 
    for variable in assignment:
        if assignment[variable][0] == None:
            return variable
    
def orderDomainValues(csp,var,assignment):
    state = assignment[var-1][0] 
    state = Node(state)
    successors = state.neighbors
    successors.sort(key=lambda x:x[0])
    for successor in successors: 
        current = Node(successor[0])
        successor.insert(1,current.parks)
    csp['domains'] = successors
    return csp['domains']


        
def assignmentIsComplete(csp,assignment):
    visitedParks = 0
    start = list(assignment.keys())[0]
    end = None
    pathCost = 0
    statesOnPath=[]
    
    for value in assignment: 
        if assignment[value][1] != None:
            visitedParks = visitedParks + assignment[value][1]
            statesOnPath.append(assignment[value][0])
            end = assignment[value][0]
            
    if (visitedParks >= csp['constraint'][0]) and (end in csp['constraint'][1]):
        for num in range(start+1, len(assignment)+start): 
            pathCost = pathCost + assignment[num][2]
            
        print("\nThe Assignment was completed...\n")
        print("(BackTrackSearch Algorithm)\n====================================\nName: George Tapia (A20450857)")
        print("Initial State:",initialState.name,'\nMinimum number of parks:',parksTovisit,"\nSolutionPath:", statesOnPath,"\nNumber of states on path:", len(statesOnPath))
        print("Path cost:",pathCost,'\nNumber of national parks visited:',visitedParks)
        print('Zone assignments:',assignment)
        return assignment
    else:
        return False


def noSolution():
    print("\nThe assignment was not complete...\n")
    print("(BackTrackSearch Algorithm)\n====================================\nName: George Tapia (A20450857)")
    print("Solution path: FAILURE: NO PATH FOUND")
    print("Number of states on path:", 0)
    print("Path cost:",0,'\nNumber of national parks visited:',0)
    
 


    
    
def backTrackingSearch(csp): 
    result = backTrack(csp,assignment)
    if result == False:
        return noSolution()
    else:
        return

def backTrack(csp,assignment):
    if assignment[12][0]!=None: 
        return assignmentIsComplete(csp, assignment)
    var = selectUnassignedVariable(csp,assignment) 
    
    for value in orderDomainValues(csp,var,assignment): 
        assignment[var] = value 
        result = backTrack(csp, assignment) 
        if result != False:
            return
    assignment[var] = [None,None] 
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
                initialState = Node(arg1)
                parksTovisit = arg2
                assignment = findVariables(initialState)
                csp ={'variables':findVariables(initialState),'domains':initialState.neighbors,'constraint':[ parksTovisit, ['CA','NV','OR','WA'] ]}
                backTrackingSearch(csp)
            else:
                raise ValueError('ERROR: Not enough or too many input arguments. Inputs might be incorrect.\nInput(1) should be in list of states and Input(2) should be an int type.')
        except ValueError as flag:
            print(flag)
            print("\nHere's the list of states:")
            print(*states,'\n')
            exit(1)




