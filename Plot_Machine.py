import math
import numpy as np
from random import choices,choice
from time import time
from collections import OrderedDict

def loop_finder(INPUT_LINES):

    """
Given a list of lines represented as pairs of points, this function finds all loops in the lines.
A loop is defined as a series of lines where the endpoint of one line is the startpoint of the next line, and the endpoint of the last line is the startpoint of the first line.
The function returns a list of loops, with each loop represented as a list of points in the order they are encountered in the loop.
:param INPUT_LINES: list of lines represented as pairs of points
:return: list of loops, each represented as a list of points
"""
    current_Endpoint=[]
    Loops=[]
    
    for current_line in INPUT_LINES: 
        startpoint= current_line[0]
        next_line=current_line[1]
        Loop=[]
        Loop.append(current_line)
        while current_Endpoint != next_line[1] and current_line[0] != next_line[1] and current_line[0] != next_line[1]: 
            current_Endpoint= current_line[1]
            # line is  a connecting line, but not itself
            connecting_lines = [sublist for sublist in INPUT_LINES if sublist[0] == current_Endpoint and sublist != current_line or sublist[1] == current_Endpoint and sublist != current_line]
            connecting_angles = []
            for neighbour_line in connecting_lines:
                if neighbour_line[1]==current_Endpoint:
                    neighbour_line.pop(1)
                    neighbour_line.insert(0,current_Endpoint)# if the endpoint is the connecting point flip line.
                if neighbour_line[1]==current_line[1]:
                    neighbour_line.pop(0)
                    neighbour_line.insert(0,current_line[1])# if the endpoint is the connecting point flip line.
      
                angle = calculate_angle(current_line, neighbour_line)           
                connecting_angles.append(math.degrees(angle))
   
            next_line_index= sharpest_right_turn(connecting_angles)
            
            next_line = connecting_lines[next_line_index]
            
            if next_line[1]==current_Endpoint:
                next_line.pop(1)
                next_line.insert(0,current_Endpoint)# if the endpoint is the connecting point flip line.
            if next_line[1]==current_line[1]:
                    next_line.pop(1)
                    next_line.insert(0,current_line[1])# if the endpoint is the connecting point flip line.
            
            current_line =next_line
            Loop.append(next_line)
            
            
            
            if next_line[1]== startpoint or next_line[1]== current_Endpoint:
                
                Loop_bereinigt=[]
                for lines in Loop:
                    for point in lines:
                        if point in lines:
                            Loop_bereinigt.append(point)
                          
                PRE_OUTPUT_LIST = [i for n, i in enumerate(Loop_bereinigt) if i not in Loop_bereinigt[:n]]
                
                
                
                direction=determine_loop_direction(Loop_bereinigt)
                FlippedStart=[]
                
                if direction == "Counterclockwise":
                    FlippedStart.append(Loop_bereinigt[1])
                    FlippedStart.append(Loop_bereinigt[0])
                    current_line=FlippedStart
                    Loop_bereinigt=[]
                    PRE_OUTPUT_LIST=[]
                     

                else:
                    Loops.append(PRE_OUTPUT_LIST) 
                    PRE_OUTPUT_LIST = [i for n, i in enumerate(Loop_bereinigt) if i not in Loop_bereinigt[:n]]
                    Loops.append(PRE_OUTPUT_LIST)
                    Loop=[]
                    break
            
       
   
    OUTPUT = []
    for sublist in Loops:
        if sorted(sublist) not in [sorted(i) for i in OUTPUT]:
            OUTPUT.append(sublist)
    return OUTPUT
##########################################################################################
def determine_loop_direction(points):
    n = len(points)
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    a = sum(x[i]*y[(i+1)%n] - x[(i+1)%n]*y[i] for i in range(n))
    return "Counterclockwise" if a > 0 else "Clockwise"
##########################################################################################
def calculate_angle(line1, line2):
    x1, y1 = line1[1][0] - line1[0][0], line1[1][1] - line1[0][1]
    x2, y2 = line2[1][0] - line2[0][0], line2[1][1] - line2[0][1]
    return math.atan2(x1*y2 - y1*x2, x1*x2 + y1*y2)
##########################################################################################
def sharpest_right_turn(angles):
    
    angles_in_radians = [math.radians(angle) for angle in angles]
    right_turn_angles = []
    for i in range(len(angles_in_radians)):
        right_turn_angles.append(angles_in_radians[i])
    max_turn_index = right_turn_angles.index(min(right_turn_angles))
    return max_turn_index
##########################################################################################
def find_overlapping_plots(plots):
    # Create a dictionary to store the mapping from plot number to overlapping plots
    plot_overlaps = {}
    # Iterate over each plot
    for i, plot in enumerate(plots):
        # Initialize an empty list to store the overlapping plots for this plot
        overlaps = []
        # Iterate over the other plots
        for j, other_plot in enumerate(plots):
            # Skip the current plot
            if i == j:
                continue
            # Check if the current plot has 2 or more coordinates in common with the other plot
            common_coords = set(plot).intersection(set(other_plot))
            if len(common_coords) >= 2:
                overlaps.append(j)
        # Add the mapping from plot number to overlapping plots to the dictionary
        plot_overlaps[i] = overlaps
    # Create a list of tuples (plot number, overlapping plots) from the dictionary
    result = [(plot, overlaps) for plot, overlaps in plot_overlaps.items()]
    return result
##########################################################################################
def convert_data(list_neighbours: list[list[int, list[int]]]) -> dict:
    """
    Converts the data from a list to a dictionary.
    """
    # Initialize the dictionary
    dictionary = {}

    # Loop through the plots
    for plot, neighbours in list_neighbours:

        # Add the plot to the dictionary
        dictionary[plot] = {'value': None, 'neighbours': neighbours}
    return dictionary
##########################################################################################
def random_distribution(dictionary: dict) -> dict:
    
    """
    Randomly assign a value to each plot and checks if the rules are
    respected.
    """
    # Declare the possible values
    values = ['L', 'I', 'G', 'O', 'E']
    weights = [20, 20, 20, 20, 20]
    L_Count=0
    I_Count=0
    G_Count=0
    O_Count=0
    E_Count=0
    
    # Get the first plot in the dictionary
    first_plot = list(dictionary.keys())[0]

    # Choose a random value from the list of possible values
    value = choice(['L', 'I', 'G', 'O', 'E'])
    VALID_VALUES=[]
    # Assign the random value to the first plot and change possible Neighbor Values accordingly
    dictionary[first_plot]['value'] = value
    combined_plots = {}
    for neighbor in dictionary[first_plot]['neighbours']:
        if dictionary[first_plot]['value'] == 'L':
                        while "I" in values:
                            index= values.index("I")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
        elif dictionary[first_plot]['value'] == 'I':
            while "L" in values:
                index= values.index("L")
                if index < len(values):
                    values.pop(index)
                    weights.pop(index)
            while "E" in values:
                index= values.index("E")
                if index < len(values):
                    values.pop(index)
                    weights.pop(index)
        #elif dictionary[first_plot]['value'] == 'G':
            # while "G" in values:
            #     index= values.index("G")
            #     if index < len(values):
            #         values.pop(index)
            #         weights.pop(index)
        if L_Count >= 4:
            while "L" in values:
                index= values.index("L")
                if index < len(values):
                    values.pop(index)
                    weights.pop(index)
        if I_Count >= 4:
            while "I" in values:
                index= values.index("I")
                if index < len(values):
                    values.pop(index)
                    weights.pop(index)
        if G_Count >= 4:
            while "G" in values:
                index= values.index("G")
                if index < len(values):
                    values.pop(index)
                    weights.pop(index)
        if O_Count >= 4:
            while "O" in values:
                index= values.index("O")
                if index < len(values):
                    values.pop(index)
                    weights.pop(index)
        if E_Count >= 1:
            while "E" in values:
                index= values.index("E")
                if index < len(values):
                    values.pop(index)
                    weights.pop(index)

        
        
        valid_vals= ([neighbor],values,weights)
        VALID_VALUES.append(valid_vals)
    VALID_VALUES_NO_DOUBLES = []
        
            
    visited=[0]
    #print("visi",visited)
    #print("COMBI",combined_plots)
        


        
    
    # Assign a value to the plot, using weighted probability
    
    #value = choices(values, weights=weights, k=1)[0]
    #Count the Assigned Values
    if value=="L":
        L_Count=L_Count+1                    
        
    elif value=="I":
        I_Count=I_Count+1
        
    elif value=="G":
        G_Count=G_Count+1
        
    elif value=="O":
        O_Count=O_Count+1
        
    elif value=="E":
        E_Count=E_Count+1
    
    
    for i in VALID_VALUES:
                if i not in VALID_VALUES_NO_DOUBLES:
                    VALID_VALUES_NO_DOUBLES.append(i)
    for plot in VALID_VALUES_NO_DOUBLES:
            plot_num, possible_values, weights = plot
            plot_num = plot_num[0]
            indices = range(len(possible_values))
            if plot_num in combined_plots:
                current_values, current_weights= combined_plots[plot_num]
                combined_values = set(current_values) & set(possible_values)
                combined_indices = [i for i in indices if possible_values[i] in combined_values]
                combined_weights = [weights[i] for i in combined_indices]
                combined_plots[plot_num] = (list(combined_values), combined_weights)
            else:
                combined_plots[plot_num] = (possible_values, weights)
    combined_plots = {key: value for key, value in combined_plots.items() if key not in visited}
    sorted_dict = dict(sorted(combined_plots.items(), key=lambda x: len(x[1][0])))
    
    # Assign the value to the plot
    # dictionary[neighbor]['value'] = value

    values = ['L', 'I', 'G', 'O', 'E']
    weights = [20, 20, 20, 20, 20]
        
    

    
    # plots_sorted = []
    # for plot in dictionary.keys():
    #     remaining_values = 5 - len(values)
    #     plots_sorted.append((plot, remaining_values))
    # plots_sorted.sort(key=lambda x: x[1])
    #print("PLOTS_SORTED_WEIRD",sorted_dict)
    

    # Loop through the plots
    while combined_plots != {}:
        for plot in sorted_dict:
            if plot>0:
                visited.append(plot)
                
                # Check the values of the neighbors
                for neighbor in dictionary[plot]['neighbours']:
                    # if dictionary[neighbor]['value'] == 'G':
                    #     while "G" in values:
                    #         index= values.index("G")
                    #         if index < len(values):
                    #             values.pop(index)
                    #             weights.pop(index)
                    # elif dictionary[neighbor]['value'] == 'C':
                    #     while "I" in values:
                    #         index= values.index("I")
                    #         if index < len(values):
                    #             values.pop(index)
                    #             weights.pop(index)
                    if dictionary[neighbor]['value'] == 'L':
                        while "I" in values:
                            index= values.index("I")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
                    elif dictionary[neighbor]['value'] == 'I':
                        while "L" in values:
                            index= values.index("L")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
                        # while "C" in values:
                        #     index= values.index("C")
                        #     if index < len(values):
                        #         values.pop(index)
                        #         weights.pop(index)
                        # while "P" in values:
                        #     index= values.index("P")
                        #     if index < len(values):
                        #         values.pop(index)
                        #         weights.pop(index)
                    elif dictionary[neighbor]['value'] == 'E':
                        while "I" in values:
                            index= values.index("I")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
                    if L_Count >= 4:
                        while "L" in values:
                            index= values.index("L")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
                    if I_Count >= 4:
                        while "C" in values:
                            index= values.index("I")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
                    if G_Count >= 4:
                        while "G" in values:
                            index= values.index("G")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
                    if O_Count >= 4:
                        while "O" in values:
                            index= values.index("O")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
                    if E_Count >= 1:
                        while "E" in values:
                            index= values.index("E")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
                
                    
                    valid_vals= ([neighbor],values,weights)
                    VALID_VALUES.append(valid_vals)

            # Assign a value to the plot, using weighted probability
            if(len(values))>=1:
                value = choices(values, weights=weights, k=1)[0]
                
                # Assign the value to the plot
                dictionary[plot]['value'] = value
                

            else:
                for plot in dictionary.keys():
                    # Set the value to None
                    
                    dictionary[plot]['value'] = None
                return False 
            
            for i in VALID_VALUES: ###################################################### List operations for combining different possibilities when checking from a different neigbor
                    if i not in VALID_VALUES_NO_DOUBLES:
                        VALID_VALUES_NO_DOUBLES.append(i)
            for plot in VALID_VALUES_NO_DOUBLES:
                    plot_num, possible_values, weights = plot
                    plot_num = plot_num[0]
                    indices = range(len(possible_values))
                    if plot_num in combined_plots:
                        current_values, current_weights= combined_plots[plot_num]
                        combined_values = set(current_values) & set(possible_values)
                        combined_indices = [i for i in indices if possible_values[i] in combined_values]
                        combined_weights = [weights[i] for i in combined_indices]
                        combined_plots[plot_num] = (list(combined_values), combined_weights)
                    else:
                        combined_plots[plot_num] = (possible_values, weights)
            values = ['L', 'I', 'G', 'O', 'E']    ##############################reset weights and Values
            weights = [20, 20, 20, 20, 20]
                    
            combined_plots_all = {key: value for key, value in combined_plots.items()}################################# A list with all possible values for all Plots
            sorted_dict_all = dict(sorted(combined_plots_all.items(), key=lambda x: len(x[1][0])))
            #print("Options_if_changes_neccessary:",sorted_dict_all)       
            
            combined_plots = {key: value for key, value in combined_plots.items() if key not in visited}############### A list with all possible values for all Plots that havnt been assigned yet
            sorted_dict = dict(sorted(combined_plots.items(), key=lambda x: len(x[1][0])))
            
            ############### Count the assignment Values
            if value=="L":  
                L_Count=L_Count+1                    
                
            elif value=="I":
                I_Count=I_Count+1
                
            elif value=="G":
                G_Count=G_Count+1
                
            elif value=="O":
                O_Count=O_Count+1
                
            elif value=="E":
                E_Count=E_Count+1
   
    print("LCount",L_Count)
    print("ICount",I_Count)  
    print("GCount",G_Count)  
    print("OCount",O_Count)  
    print("ECount",E_Count)  
    # print(C_Count)     
    # print(R_Count) 
    # print(I_Count) 
    # print(P_Count)
    #print("visited",visited)
    return dictionary, sorted_dict_all
##########################################################################################
def find_solution(dictionary: dict,
                max_time: float = 30) -> dict:
    """
    Generates solutions until a valid one is found or the time limit.
    is reached.
    """
    # Initialize the answer and the time
    answer, start = {}, time()

    # Set the stopping condition
    while answer == {} and (time() - start) < max_time:

        # Get a potential solution
        answer = random_distribution(dictionary)

    if answer == False:
        find_solution(dictionary,5)
    else:
        return answer
##########################################################################################
##########################################################################################
##########################################################################################
INPUT_LINES=[[[0, 0],[ 2, 2]],#Input Lines
[[2, 2], [2, 0]], 
[[2, 0], [0, 0]],
[[6, 0], [2, 0]], 
[[2, 0], [2, 2]],
[[2, 2], [6, 2]], 
[[6, 2], [6, 0]], 
[[6, 0], [6, 2]], 
[[6, 2], [8, 3]], 
[[8, 3], [9, 1]], 
[[9, 1], [8, 0]], 
[[8, 0], [6, 0]], 
[[6, 4], [6, 5]], 
[[6, 5], [8, 5]], 
[[8, 5], [8, 3]], 
[[8, 3], [6, 2]], 
[[6, 2], [6, 4]], 
[[6, 4], [3, 4]], 
[[3, 4], [2, 2]], 
[[2, 2], [6, 2]], 
[[6, 2], [6, 4]], 
[[0, 0], [0, 3]], 
[[0, 3], [2, 2]], 
[[2, 2], [0, 0]], 
[[0, 3], [2, 2]], 
[[2, 2], [3, 4]], 
[[3, 4], [3, 5]], 
[[3, 5], [0, 5]], 
[[0, 5], [0, 3]], 
[[6, 4], [6, 5]], 
[[6, 5], [3, 5]], 
[[3, 5], [3, 4]], 
[[3, 4], [6, 4]], 
[[6, 5], [3, 5]], 
[[3, 5], [3, 7]], 
[[3, 7], [6, 5]], 
[[0, 7], [0, 5]], 
[[0, 5], [3, 5]], 
[[3, 5], [3, 7]], 
[[3, 7], [0, 7]]
]
##########################################################################################
PLOTS= loop_finder(INPUT_LINES)
print("Plots:",PLOTS)
##########################################################################################
toplots = [[tuple(x) for x in sublist] for sublist in PLOTS]#Convert in Tuples
NEIGHBOURS = find_overlapping_plots(toplots)
print("Neighbours:",NEIGHBOURS)
##########################################################################################
DICTIONARY = convert_data(NEIGHBOURS)
DISTRIBUTION=find_solution(DICTIONARY)
#POSSIBLE_CHANGES=random_distribution(DICTIONARY)
print ("Distribution",DISTRIBUTION)
#print ("Possible Changes",POSSIBLE_CHANGES[1])

