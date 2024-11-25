import os, sys, random, time, math

def solve(n, get_neighbors):
    start = time.time()

    N = n
    neighbors = [get_neighbors(i) for i in range(N)]
    best_order = list(range(N))
    best_cost = float('inf')

    def square_wire_length_objective(V):
        position = {node: idx for idx, node in enumerate(V)}  
        total = 0
        for node in range(len(V)):
            node_pos = position[node]
            for neighbor in neighbors[node]:
                total += (node_pos - position[neighbor]) ** 2
        return total / 2

    def greedy_grouping():
      
        visited = [False] * N
        grouped_order = []

        def bfs(node):
            queue = [node]
            visited[node] = True
            cluster = []

            while queue:
                current = queue.pop(0)
                cluster.append(current)
                for neighbor in neighbors[current]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        queue.append(neighbor)
            return cluster

        degree_sorted_nodes = sorted(range(N), key=lambda x: len(neighbors[x]), reverse=True)

        for node in degree_sorted_nodes:
            if not visited[node]:
                cluster = bfs(node)
                grouped_order.extend(cluster)

        return grouped_order

    def simulated_annealing(max_time):
        nonlocal best_order, best_cost
        current_order = greedy_grouping()
        current_cost = square_wire_length_objective(current_order)

        temperature = max(1.0, N / 5.0)  
        cooling_rate = 0.995
        min_temperature = 1e-3
        batch_size = max(1, N // 50)

        while temperature > min_temperature and time.time() - start < max_time:
            for _ in range(batch_size):
                i, j = random.sample(range(N), 2)
                current_order[i], current_order[j] = current_order[j], current_order[i]
                new_cost = square_wire_length_objective(current_order)

                delta = new_cost - current_cost
                if delta < 0 or random.random() < math.exp(-delta / temperature):
                    current_cost = new_cost
                    if current_cost < best_cost:
                        best_order = current_order.copy()
                        best_cost = current_cost
                else:
                    current_order[i], current_order[j] = current_order[j], current_order[i]

            temperature *= cooling_rate

    def local_search(max_time):
        nonlocal best_order, best_cost

        current_order = best_order.copy()
        current_cost = square_wire_length_objective(current_order)
        window_size = min(20, N // 10)

        while time.time() - start < max_time:
            improved = False

            for i in range(N - window_size):
                for j in range(i + 1, i + window_size):
                    candidate = current_order.copy()
                    candidate[i], candidate[j] = candidate[j], candidate[i]
                    candidate_cost = square_wire_length_objective(candidate)

                    if candidate_cost < current_cost:
                        current_order = candidate
                        current_cost = candidate_cost
                        improved = True

                        if current_cost < best_cost:
                            best_order = current_order.copy()
                            best_cost = current_cost

            if not improved:
                break

    remaining_time = max(0, 28.0 - (time.time() - start))
    if remaining_time > 1:
        if N < 50:
            local_search(max_time=remaining_time)
        elif N <= 200:
            simulated_annealing(max_time=remaining_time * 0.65)
            local_search(max_time=remaining_time * 0.35)
        else:
            simulated_annealing(max_time=remaining_time * 0.8)
            local_search(max_time=remaining_time * 0.2)

    return best_order

def main():
    global N
    try:
        N = int(os.environ["N"])
    except:
        N = 20

    try:
        from compile_with_soln import grader_stub
        grader = grader_stub()
        neighbor_func = grader.get_neighbors
    except:
        neighbor_func = get_neighbors_local

    best_order = solve(N, neighbor_func)
    print(" ".join(map(str, best_order)))

if __name__ == "__main__":
    main()
