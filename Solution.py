import copy
import numpy as np


class NQueen:

    def get_array(self, n):
        # In case of failure this function returns an array of size n*n
        array = np.zeros((n,n))
        cols = np.zeros((n,1))
        for i in range(n):
            col = np.random.randint(0,n)
            array[col,i] = 1
        return array

    def exists(self, i, j,n):
        # Checks if position of queen exists within boundary
        return (i >= 0 and i < n and j >= 0 and j < n)




    def get_possibilities(self, array, size):
        # Getting the neighboring elements for the one particular state
        shape = size*(size-1)
        possibilty = 0
        arr = np.random.randint(1, 5, (shape,size,size))

        for r in range(len(array)):
            copy = np.copy(array[:, r])
            index = np.where(copy == 1)
            #print("Index: ", index)
            if (len(index[0]) > 1):
                index = index[0][0]
            elif (len(index[0]) == 1):
                index = index[0]

            array[:, r][index] = 0
            for j in range(len(copy)):
                if j==index:
                    pass
                else:
                    array[:,r][j]=1
                    arr[possibilty] = array
                    array[:, r][j] = 0
                    possibilty = possibilty + 1
            array[:,r] = copy
        return arr

    def heuristic_value(self, array,n):
        # calculating the heuristic value for current state, i.e; no of pairs of queens attacking each other
        h = 0
        for i in range(n):
            for j in range(n):

                if array[i][j]:
                    for k in range(n):
                        if array[i][k] == 1 and k != j :
                            h += 1

                    for k in range(n):
                        if array[k][j] == 1 and i != k:
                            h += 1

                    l, m = i-1, j+1
                    while self.exists(l, m, n):
                        if array[l][m] == 1 :
                            h += 1
                        l, m = l-1, m+1

                    l, m = i+1, j-1
                    while self.exists(l, m, n):
                        if array[l][m] == 1:
                            h += 1
                        l, m = l+1, m-1

                    l, m = i-1, j-1
                    while self.exists(l, m, n):
                        if array[l][m] == 1 :
                            h += 1
                        l, m = l-1, m-1

                    l, m = i+1, j+1
                    while self.exists(l, m, n):
                        if array[l][m] == 1 :
                            h += 1
                        l, m = l+1, m+1

        return h


    def hill_climbing_steepest_ascend(self, array, times,size):
        # This function returns a dictinary of success and failure/stuck using steepest ascend hill climbimg algorithm
        # Success element contains a list of number of steps taken to reach the success
        # Stuck element contains a list of number of steps which has resulted in
        # failure or stuck(Algorithm is not ascending to goal state )
        success = []
        stuck = []

        heuristic = self.heuristic_value(array,size)
        actual = heuristic
        if heuristic==0:
            array = self.get_array(size)
            print("Solution in first go: ", array)
            success.append(1)
        else:
            count = 0
            step = 0
            while(count<times):
                possibilities = self.get_possibilities(array,size)
                shape = size*(size-1)
                pos = [0]*shape
                pos = np.array(pos)
                for i in range(np.shape(possibilities)[0]):
                    pos[i] = self.heuristic_value(possibilities[i],size)
                min_heuristic = np.min(pos)
                step = step + 1
                array_min = np.where(pos==min_heuristic)
                array_min = array_min[0][0]

                if min_heuristic==0:
                    array = self.get_array(size)
                    print("Solution: ", possibilities[np.where(pos == 0)[0]])
                    success.append(step)
                    count = count + 1
                    step = 0
                    heuristic = actual

                if (min_heuristic>=heuristic):
                    stuck.append(step)
                    array = self.get_array(size)
                    count = count + 1
                    step = 0
                    heuristic = actual

                else:
                    heuristic = min_heuristic
                    array = possibilities[array_min]
        return {"Success": success, "Stuck": stuck}

    def stochastic_hill_climbing(self, array, times, size):
        # This function returns a dictinary of success and failure/stuck using stochastic climbimg algorithm
        # Success element contains a list of number of steps taken to reach the success
        # Stuck element contains a list of number of steps which has resulted in
        # failure or stuck(Algorithm is not ascending to goal state )

        success = []
        stuck = []
        # It will contain elements which had heuristic greater than current heuristic so that we can randomly select the any heuristic from it.
        stochastic_array = []

        heuristic = self.heuristic_value(array, size)
        actual = heuristic
        if heuristic == 0:
            array = self.get_array(size)
            print("Solution in first go: ", array)
            success.append(1)
        else:
            count = 0
            step = 0
            while (count < times):
                possibilities = self.get_possibilities(array, size)
                shape = size * (size - 1)
                pos = [0] * shape
                pos = np.array(pos)
                for i in range(np.shape(possibilities)[0]):
                    pos[i] = self.heuristic_value(possibilities[i], size)
                    if (pos[i] <heuristic):
                        stochastic_array.append(pos[i])
                min_heuristic = np.min(pos)
                step = step + 1
                if min_heuristic == 0:
                    array = self.get_array(size)
                    print("Solution: ", possibilities[np.where(pos==0)[0]])
                    success.append(step)
                    count = count + 1
                    step = 0
                    heuristic = actual
                    stochastic_array = []

                if len(stochastic_array)==0:
                    stuck.append(step)
                    array = self.get_array(size)
                    count = count + 1
                    step = 0
                    heuristic = actual

                else:
                    position_stochastic = np.random.randint(0,len(stochastic_array))
                    stochastic_heuristic = stochastic_array[position_stochastic]
                    array_heuristic = np.where(pos == stochastic_heuristic)

                    if(len(array_heuristic[0])>1):
                        array_heuristic = array_heuristic[0][0]
                    elif(len(array_heuristic[0])==1):
                        array_heuristic = array_heuristic[0]
                    heuristic = stochastic_heuristic
                    array = possibilities[array_heuristic]
                    stochastic_array = []

        return {"Success": success, "Stuck":stuck}

if __name__ == "__main__":
    nqueen =  NQueen()

    array = nqueen.get_array( 8)
    print(array)
    #print("Current position's heuristic value: ", heuristic_value(array))
    result = nqueen.stochastic_hill_climbing(array,1000,8)


    print("result: ", result)

    success = np.array(result["Success"])
    stuck = np.array(result["Stuck"])

    if (len(success) > 0):

        print("Success occurred for: ", len(success), "times")
        print("Minimum steps to reach success:", np.min(success))
        print("Maximum steps to reach success:", np.max(success))
        print("Average steps to reach succes:", np.sum(success)/len(success))

    if (len(stuck) > 0):
        print("Algorithm stuck for: ", len(stuck), "times")
        print("Minimum steps to reach failure:", np.min(stuck))
        print("Maximum steps to reach failure:", np.max(stuck))
        print("Average steps to reach failure:", np.sum(stuck) / len(stuck))
