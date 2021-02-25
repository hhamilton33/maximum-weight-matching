# Maximum-Weight-Matching

## Description
A matching is a subset of a graph where at most one edge can be incident on a vertex. The maximum weighted matching optimization problem can be formulated as an integer program, where there is a binary decision variable for each edge. As linear programs are often easier to solve and can yield integer solutions, it is worth formulating this problem as a linear program. To improve the probability of obtaining an optimal integer solution, odd-set constraints of cardinalities 3 and 5 can be added to the formulation. With these constraints, at most one edge can exist within a cycle of 3 vertices and at most two edges can exist within a cycle of 5 vertices. Adding these constraints increases the computation time, especially as the number of vertices in the graph increases. The following three approaches to reduce the computation time are investigated.

1. Removing variables for edges with small weights: As an optimal solution to this problem is more likely to choose the edges which have larger weights, the first approach for reducing the computation time was to only create a variable for an edge if its corresponding weight was greater than or equal to 1.

2. Adding less odd-set constraints: As not all constraints are binding at an optimal solution, the second approach for reducing the computation time was to only add constraints that are likely to be binding at an optimal solution. For the odd-set constraints of cardinality 3, this meant only adding them if any 2 weights were greater than or equal to 1. For the odd-set constraints of cardinality 5, this meant only adding them if any 3 weights were greater than or equal to 1. The logic is that these cases need to be looked out for more than other cases because the optimization model will want to choose edges with larger weights.

3. Only using odd-set constraints when integer solution not found: The odd-set constraints serve the purpose of helping find an optimal integer solution, but at the cost of increasing the computation time. The third approach for reducing the computation time was to first try solving with the original formulation and then re-solve with the added constraints if the optimal solution is not integer.

The first approach resulted in lower computation times, but at the cost of lower probabilities of obtaining optimal integer solutions. The second approach resulted in lower computation times and no change in the probabilities of obtaining optimal integer solutions. The third approach resulted in significantly lower computation times and no change in the probabilities of obtaining optimal integer solutions.

## Installation
The following software must be installed.

-Python -Gurobi
