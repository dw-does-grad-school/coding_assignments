#If this works I'm going to have a stroke
import os, sys, random, time, math

#This works for smaller datasets but not larger.
#The breaking point seems to be around 250 test cases. 

def solve(n, get_neighbors):
    global N

    N = n
    start = time.time()
    best_order = list(range(N))
    best_cost = float('inf')

    def square_wire_length_objective(V):
        """
        Compute the squared wire length objective for a given ordering.
        """
        # where[i] is the index in V at which the data point i resides
        where = [None] * N
        for i in range(N):
            where[V[i]] = i
        
        total = 0
        for i in range(N):
            for j in get_neighbors(i):
                d = where[i] - where[j]
                total += d * d
        return total / 2  # Divide by 2 as each pair is counted twice

    def simulated_annealing(max_time=25):
        nonlocal best_order, best_cost

        current_order = list(range(N))
        random.shuffle(current_order)

        current_cost = square_wire_length_objective(current_order)

        # Annealing parameters
        temperature = 1.0
        cooling_rate = 0.995
        min_temperature = 0.01

        while temperature > min_temperature and time.time() - start < max_time:
            new_order = current_order.copy()
            i, j = random.sample(range(N), 2)
            new_order[i], new_order[j] = new_order[j], new_order[i]
            new_cost = square_wire_length_objective(new_order)

            # Decide if the new solution is acceptable
            delta = new_cost - current_cost
            if delta < 0 or random.random() < math.exp(-delta / temperature):
                current_order = new_order
                current_cost = new_cost

            # Update the best solution
            if current_cost < best_cost:
                best_order = current_order.copy()
                best_cost = current_cost

            # Cool it down
            temperature *= cooling_rate

        return best_order

    def local_search(max_time=25):
        nonlocal best_order, best_cost

        current_order = list(range(N))
        random.shuffle(current_order)

        current_cost = square_wire_length_objective(current_order)

        while time.time() - start < max_time:
            improved = False

            for i in range(N):
                for j in range(i + 1, N):
                    # Create a potential solution by swapping
                    candidate = current_order.copy()
                    candidate[i], candidate[j] = candidate[j], candidate[i]

                    candidate_cost = square_wire_length_objective(candidate)

                    if candidate_cost < current_cost:  # Correct comparison
                        current_order = candidate
                        current_cost = candidate_cost
                        improved = True

                        if current_cost < best_cost:
                            best_order = current_order.copy()
                            best_cost = current_cost

                if not improved:
                    break

        return best_order

    # Apply the problem-solving strategies
    strategies = [simulated_annealing, local_search]
    for strategy in strategies:
        remaining_time = max(0, 28.0 - (time.time() - start))
        if remaining_time > 1:
            strategy(max_time=remaining_time)

    return best_order

def main():
    global N
    # The value for N is set in the grading system through an environment variable, if present.
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
