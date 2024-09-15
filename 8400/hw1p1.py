import os, sys

# This imports from a file that will be present in the
# grading system. No need to alter for local testing -
# if the file isn't present then these lines are skipped
try:
    from compile_with_soln import grader_stub
    grader = grader_stub()
except:
    pass

# ----------------------------------------
# This function, grader.call_grader() (which will be
# present with our code when it is submitted to the
# grading system), takes an integer index i and returns
# A[i].

# If you pass an invalid index or call this function
# more than 32 times, you'll get back -1
    
# grader.call_grader(int i) 
# ----------------------------------------

# For testing on your own system, you can call 
# this function instead.  It uses an array of length 10 
# with values 1000, 2000, 3000, ..., 10,000. 
# Don't forget to switch your code back to calling 
# grader.call_grader() before submitting. 
def call_grader_local(i):
    A = [1000, 2000, 3000, 4000, 5000,
         6000, 7000, 8000, 9000, 10000]
    return A[i]

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''
    I've been attempting to solve this like I'm just writing a function, which does not seem to be working. 
    So how about taking a class based approach? 
'''
class Binary_Search: 
    
    def __init__(self, data): 
        self.data = data
        self.left_side = None
        self.right_side = None

    def add_child(self, data): 
        if data == self.data: # this demonstrates that the node already exists
            return
        if data < self.data: 
            if self.left_side: 
                self.left_side.add_child(data)
            else: 
                self.left_side = Binary_Search(data)
        else: 
            if self.right_side: 
                self.right_side.add_child(data)
            else: 
                self.right_side = Binary_Search(data)
    
    def search(self, val):
        if self.data == val:
            return True
        
        if val < self.data: 
            if self.left_side: 
                return self.left_side.search(val)
            else: 
                return False
            
        if val > self.data: 
            if self.right_side: 
                return self.right_side.search(val)
            else: 
                return False
            
    def order_of_traversal(self): 
        elements = []
        if self.left_side: 
            elements += self.left_side.order_of_traversal()
        
        elements.append(self.data)

        if self.right_side: 
            elements += self.right_side.order_of_traversal()

        return elements
        
def build_the_tree(elements): 

    root = Binary_Search(elements[0])

    for i in range(1, len(elements)): 
        root.add_child(elements[i])

    return root

def find_closest_value(root, target): 

    closest = float('inf')
    current = root

    while current: 
        if abs(current.data - target) < abs(closest - target): 
            closest = current.data

        if target < current.data: 
            current = current.left_side
        elif target > current.data: 
            current = current.right_side
        else: 
            break

        return closest

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def main():
    try:
        # Fetch values from environment variables or use defaults
        N = int(os.environ.get("N"))
        T = int(os.environ.get("T"))
    except NameError:
        N = 10
        T = 8400
        # Implementation of it is where I am struggling. 

        # Perform binary search
        
        
        values = []
        for i in range(N):
            value = grader.call_grader(i)
            if value == -1:
                break
            values.append(value)
    
        # Build the f-----g tree
        root = build_the_tree(values)

        closest_value = find_closest_value(root, T)
        closest_index = values.index(closest_value) if closest_value in values else -1

        print(f"Closest index: {my_answer}")

if __name__ == "__main__":
    main()
