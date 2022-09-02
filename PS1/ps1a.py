###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cowDictionary = {}
    
    cowFile = open(filename, 'r')
    
    for line in cowFile:
        currentCow = line.rstrip('\n').split(',')
        cowDictionary[currentCow[0]] = int(currentCow[1])

    return cowDictionary


# Problem 2
def greedy_cow_transport(cows,limit=10):
    #test code
    # dictionary = load_cows("ps1_cow_data.txt")
    # greedy_cow_transport(dictionary)
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    answer = []
    cowList = list(cows.items())
    cowList = sorted(cowList, key = lambda x: x[1])
    
    taken = [False] * 10
    countTaken = 0
    
    while(countTaken < len(cowList)):
        currentWeight = 0
        index = len(cowList) - 1
        currentTransport = []
        
        for index in range(len(cowList) - 1, -1, -1):
            # print(index, cowList[index], ":", taken[index], currentWeight + cowList[index][1])
            
            if(taken[index] == False and currentWeight + cowList[index][1] <= limit):
                taken[index] = True
                countTaken += 1
                currentWeight += cowList[index][1]
                currentTransport.append(cowList[index][0])
                
                # print("    Taken:", currentWeight)
            
        
        answer.append(currentTransport)
        # print("------------")
    
    return answer

def withinWeight(currentPossibility, limit=10):
    for i in currentPossibility:
        weight = 0
        
        for j in i:
            weight += j[1]
        
        if(weight > limit):
            return False
    
    return True

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    
    cowList = list(cows.items())
    possibleLists = get_partitions(cowList)
    
    answer = []
    
    for currentPossibility in possibleLists:
        if(withinWeight(currentPossibility)):
            if(answer == [] or len(answer) > len(currentPossibility)):
                answer = currentPossibility
    
    return answer
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    pass

dictionary = load_cows("ps1_cow_data.txt")
answer = brute_force_cow_transport(dictionary)

for i in answer:
    for j in i:
        print(j[0] + " ", end = '')
    
    print()
    
    
    
    
    
    
    
    