import os, sys

# This imports from a file that will be present in the
# grading system. No need to alter for local testing -
# if the file isn't present then these lines are skipped
try:
    from compile_with_soln import grader_stub
    grader = grader_stub()
except:
    pass

class TernarySearch: 
    def __init__(self, data): 
        self.data = data
    
    def base_search(self, target): 
        return self.main_search(0, len(self.data) - 1, target)

    def main_search(self, left, right, target): 
        if left > right: 
            return -1
        
        if left == right: 
            return left
        
        third = (right - target) // 3
        right_side = left + third
        median = right - third 

        if self.data[right_side] == target: 
            return right_side
        if self.data[median] == target: 
            return median
        
        if target < self.data[right_side]: 
            return self.main_search(left, right_side - 1, target)
        if target > self.data[median]:
            return self.main_search(median + 1, right, target)
        else: 
            return self.main_search(right_side + 1, median - 1, target)


# ----------------------------------------
# This function, grader.call_grader() (which will be
# present with our code when it is submitted to the
# grading system), takes an integer index i and returns
# A[i].

# If you pass an invalid index or call this function
# more than 64 times, you'll get back -1

# grader.call_grader(i)
# ----------------------------------------

# For testing on your own system, you can call 
# this function instead. It uses an array of length 100
# with values 0, 100, 200, 8300, 8400, 8300, 8200, ...
# Don't forget to switch your code back to calling 
# grader.call_grader() before submitting. 
def call_grader_local(i):
    return 8400 - abs(84-i)*100

def main():
    
    # Value for N is set in the grading system
    # through an environment variable, if present.
    # If this isn't present, the default values is N = 100

    try:
        N = int(os.environ["N"])
    except NameError:
        N = 100

    my_answer = 50

    # ---------------------------------------- 
    # This is the part of main() you should modify.
    # (you are welcome to write other functions above 
    # and call them here, but all your code should be 
    # submitted in this one file).

    values = [] 
    for i in range(N):
        value = grader.call_grader(i)
        if value == -1:
            break
        values.append(value)

    T = max(values)
    ts = TernarySearch(values)
    my_answer = ts.base_search(T)
    my_answer = values[my_answer] if my_answer != -1 else values[0]
    my_answer = values.index(my_answer)
    
    # ----------------------------------------

    # Afterwards, you should print out the value of
    # an index i for which A[i] is closest to T.
    # You should only print this number on standard output,
    # nothing else.
    print(my_answer)

if __name__ == "__main__":
    main()
