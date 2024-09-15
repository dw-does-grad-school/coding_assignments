import os, sys, random

# This imports from a file that will be present in the
# grading system. No need to alter for local testing -
# if the file isn't present then these lines are skipped
try:
    from compile_with_soln import grader_stub
    grader = grader_stub()
except:
    pass

# ----------------------------------------
# This function (which will be compiled with our code
# when it is submitted to the grading system) takes
# a list of values of x and returns a list of
# values of f(x) for all of them.

# If you pass it a list of length more than K,
# you'll only get back the first K answers.
# If you call it more than R times, you'll start to
# get back empty lists.
# If you pass any values of x outside [0,1], you'll
# get back corresponding values of -1.

# grader.call_grader(x)
# ----------------------------------------
class ParameterFitting: 
    def __init__(self, function, num_tests, num_rounds):
        self.function = function
        self.num_tests = num_tests
        self.num_rounds = num_rounds

    def noisy_function(self, x, round_n): # Taking into consideration how this function changes with background noise
        noise_level = self.get_noise_level(round_n)
        noise = random.gauss(0, noise_level)
        return self.function(x) + noise

    '''
        Retrospectively, the below falls into the "I should've asked about this" category. 
        I was going off of the information given in the powerpoint slides on the range functions, so these probably only work for a
        subset of the "noise" sampling. 

        Lesson learned. DO NOT plan to do coding assignments like this after even a "minor" surgery...
    '''
    def get_noise_level(self, round_n): 
        if 1 <= round_n <= 5: 
            return 0.0
        elif 6 <= round_n <= 10: 
            return 0.1
        elif 11 <= round_n <= 15:
            return 0.5
        elif 16 <= round_n <= 20:
            return 1.0
        else: 
            raise ValueError("Round number must be 1-20")
        
    def evaluate(self, x, round_n): 
        return self.noisy_function(x, round_n)
    
    def find_the_best_x(self, round_n): # Generate the K values
        x_candidates = [i / (self.num_tests - 1) for i in range(self.num_tests)]

        # Evaluate the candidates
        best_x = None
        best_value = -float('inf')
        for x in x_candidates: 
            value = self._evaluate(x, round_n)
            if value > best_value: 
                best_x = x
                best_value = value

        return best_x
    
    def fit_parameters(self): 
        best_ex = None
        best_value = -float('inf')

        for round_n in range(1, self.num_rounds + 1): 
            # It's 8:45PM on a Friday I'm going to get humorous here...
            round_best_ex = self.find_the_best_x(round_n)
            round_best_date = self.function(round_best_ex)

            if round_best_date > best_ex: 
                best_ex = round_best_ex
                best_value = round_best_date

        return best_ex


# For testing on your own system, you can call 
# this function instead. It uses an array of length 100
# with values 0, 100, 200, 8300, 8400, 8300, 8200, ...
# Don't forget to switch your code back to calling 
# grader.call_grader() before submitting. 
def call_grader_local(x):
    result = []
    for i in len(x):
        result.append(1.0 - abs(x[i] - 0.8400))
    return result

def main():
    
    # Values for K and R are set in the grading system
    # through environment variables, if present.
    # If these aren't present, the default values are K = R = 10

    try:
        K = int(os.environ["K"])
        R = int(os.environ["R"])
    except NameError:
        K = 10
        R = 10

    my_answer = 0.5

    # ---------------------------------------- 
    # This is the part of main() you should modify. 
    # For each of R rounds,
    # you can evaluate f(x) at K values of x
    # (you are welcome to write other functions above
    # and call them here, but all your code should be
    # submitted in this one file).

    def target_function(x): 
        result = grader.call_grader([x])
        return result[0]
    
    pf = ParameterFitting(target_function, K, R)

    my_answer = pf.fit_parameters()
    # ----------------------------------------

    # Afterwards, you should print out the value of
    # an index i for which A[i] is closest to T.
    # You should only print this number on standard output,
    # nothing else.
    
    print(my_answer)

if __name__ == "__main__":
    main()
