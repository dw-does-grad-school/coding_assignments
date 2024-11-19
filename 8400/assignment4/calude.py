import os
import sys
import random
import time

# Global variable to store number of points
N = 0

def solve(n, get_neighbors):
    """
    Main solving function for linear arrangement problem
    
    :param n: Number of points
    :param get_neighbors: Function to get neighbors of a point
    :return: Best ordering found
    """
    global N
    N = n
    start_time = time.time()
    best_order = list(range(N))
    best_cost = float('inf')

    def squared_wire_length_objective(V):
        """
        Compute squared wire length objective
        
        :param V: Current ordering of points
        :return: Objective value
        """
        where = [None] * N
        # where[i] is the index in V at which data point i resides
        for i in range(N):
            where[V[i]] = i
        
        total = 0
        for i in range(N):
            for j in get_neighbors(i):
                d = where[i] - where[j]
                total += d * d
        return total / 2  # divide by 2 since we count each distance twice

    def simulated_annealing(max_time=25):
        """
        Solve using Simulated Annealing
        
        :param max_time: Maximum time allowed for solving
        :return: Best ordering found
        """
        nonlocal best_order, best_cost
        
        current_order = list(range(N))
        random.shuffle(current_order)
        
        current_cost = squared_wire_length_objective(current_order)
        
        # Annealing parameters
        temperature = 1.0
        cooling_rate = 0.995
        min_temperature = 0.01
        
        while temperature > min_temperature and time.time() - start_time < max_time:
            # Generate a neighboring solution by swapping two random points
            new_order = current_order.copy()
            i, j = random.sample(range(N), 2)
            new_order[i], new_order[j] = new_order[j], new_order[i]
            
            # Compute new cost
            new_cost = squared_wire_length_objective(new_order)
            
            # Decide to accept the new solution
            delta = new_cost - current_cost
            if delta < 0 or random.random() < math.exp(-delta / temperature):
                current_order = new_order
                current_cost = new_cost
            
            # Update best solution if needed
            if current_cost < best_cost:
                best_order = current_order.copy()
                best_cost = current_cost
            
            # Cool down
            temperature *= cooling_rate
        
        return best_order

    def local_search(max_time=25):
        """
        Solve using Local Search with iterative improvement
        
        :param max_time: Maximum time allowed for solving
        :return: Best ordering found
        """
        nonlocal best_order, best_cost
        
        current_order = list(range(N))
        random.shuffle(current_order)
        
        current_cost = squared_wire_length_objective(current_order)
        
        while time.time() - start_time < max_time:
            improved = False
            
            # Try swapping every pair of points
            for i in range(N):
                for j in range(i+1, N):
                    # Create a candidate solution by swapping
                    candidate = current_order.copy()
                    candidate[i], candidate[j] = candidate[j], candidate[i]
                    
                    # Compute cost
                    candidate_cost = squared_wire_length_objective(candidate)
                    
                    # If better, update
                    if candidate_cost < current_cost:
                        current_order = candidate
                        current_cost = candidate_cost
                        improved = True
                        
                        # Update best solution
                        if current_cost < best_cost:
                            best_order = current_order.copy()
                            best_cost = current_cost
                
                # Break if no improvement found
                if not improved:
                    break
        
        return best_order

    # Apply solving strategies
    strategies = [simulated_annealing, local_search]
    
    for strategy in strategies:
        remaining_time = max(0, 28.0 - (time.time() - start_time))
        if remaining_time > 1:
            strategy(max_time=remaining_time)

    return best_order

def main():
    global N
    # The value for N is set in the grading system through an
    # environment variable, if present.
    try:
        N = int(os.environ["N"])
    except:
        N = 20

    # Use the local test neighbor function or the grader's function
    try:
        from compile_with_soln import grader_stub
        grader = grader_stub()
        neighbor_func = grader.get_neighbors
    except:
        neighbor_func = get_neighbors_local

    # Solve the linear arrangement problem
    best_order = solve(N, neighbor_func)

    # Print the best order
    print(" ".join(map(str, best_order)))

if __name__ == "__main__":
    main()
