import os
import sys
from functools import cmp_to_key

try:
    from compile_with_soln import grader_stub
    grader = grader_stub()
except:
    pass

N = 0
D = 0
K = 0

class KDNode:
    def __init__(self, index, left=None, right=None):
        self.index = index
        self.left = left
        self.right = right

def build_kd_tree(points, depth=0):
    if not points:
        return None
    
    axis = depth % D
    points.sort(key=lambda x: grader.get_coord(x, axis))
    median = len(points) // 2

    return KDNode(
        index=points[median],
        left=build_kd_tree(points[:median], depth + 1),
        right=build_kd_tree(points[median + 1:], depth + 1)
    )

def squared_distance(index1, index2):
    return sum((grader.get_coord(index1, i) - grader.get_coord(index2, i)) ** 2 for i in range(D))

def find_k_nearest_neighbors(node, point, k, depth=0, neighbors=None):
    if node is None:
        return
    
    if neighbors is None:
        neighbors = []

    dist = squared_distance(node.index, point)
    neighbors.append((dist, node.index))
    neighbors.sort(key=lambda x: x[0])
    if len(neighbors) > k:
        neighbors.pop()

    axis = depth % D
    point_coord = grader.get_coord(point, axis)
    node_coord = grader.get_coord(node.index, axis)

    if point_coord < node_coord:
        find_k_nearest_neighbors(node.left, point, k, depth + 1, neighbors)
        if len(neighbors) < k or (node_coord - point_coord) ** 2 < neighbors[-1][0]:
            find_k_nearest_neighbors(node.right, point, k, depth + 1, neighbors)
    else:
        find_k_nearest_neighbors(node.right, point, k, depth + 1, neighbors)
        if len(neighbors) < k or (point_coord - node_coord) ** 2 < neighbors[-1][0]:
            find_k_nearest_neighbors(node.left, point, k, depth + 1, neighbors)

def k_nearest_neighbors(tree, point, k):
    neighbors = []
    find_k_nearest_neighbors(tree, point, k, neighbors=neighbors)
    return [neighbor[1] for neighbor in sorted(neighbors, key=lambda x: x[0])]

def majority_vote(neighbors):
    classes = [grader.get_class(neighbor) for neighbor in neighbors]
    return max(set(classes), key=classes.count)

def main():
    global N, D, K
    try:
        N = int(os.environ["N"])
        D = int(os.environ["D"])
        K = int(os.environ["K"])
    except:
        N = 8
        D = 2
        K = 3

    # Build K-d tree
    points = list(range(N))
    kd_tree = build_kd_tree(points)

    # Classify all points and build confusion matrix
    confusion_matrix = [[0, 0], [0, 0]]
    for i in range(N):
        neighbors = k_nearest_neighbors(kd_tree, i, K)
        predicted_class = majority_vote(neighbors)
        actual_class = grader.get_class(i)
        confusion_matrix[max(0, actual_class)][max(0, predicted_class)] += 1

    # Print confusion matrix
    print(f"{confusion_matrix[1][1]} {confusion_matrix[1][0]}")
    print(f"{confusion_matrix[0][1]} {confusion_matrix[0][0]}")

if __name__ == "__main__":
    main()
