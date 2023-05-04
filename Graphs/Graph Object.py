from collections import deque
from heapq import heappop, heappush

class Node:
    def __init__(self, name):
        self.__name = name
        self.edges = {}

#------------------------------------------------------------------------


class Graph:
    """ a graph is a set of nodes connected by edges, which may be directed/undirected and weighted/unweighted. 
    Here, an adjacency list is utilised for the space-efficient implementation of a sparsely connected graph. """
    def __init__(self, directed):
        self.__nodes = {}
        self.__directed = directed

    def addNode(self, new_node):
        """ if the new node isn't yet in the AL, add the new node as a key in '__nodes' w/ an empty dictionary as its value, 
      representing no outgoing edges from the new node. """
        if new_node not in self.__nodes:
            self.__nodes[new_node] = Node(new_node)
        else:
            raise ValueError("Node already exists.")

    def removeNode(self, node_to_remove):
        if node_to_remove in self.__nodes:
            del self.__nodes[node_to_remove]
        else:
            raise ValueError("Node doesn't exist.")

    def listNodes(self):
        """" print all keys representing the nodes. """
        return " ".join(self.__nodes.keys())

    """ when constructing graphs, ensure to add edges such that each node is accessible from the origin. """
    def addEdge(self, origin, destination, weight):
        if origin not in self.__nodes:
            raise ValueError("Origin doesn't exist.")
        if destination not in self.__nodes:
            raise ValueError("Destination doesn't exist.")
        if not isinstance(weight, (int)):
            raise ValueError("Non-positive integer weight.")
        self.__nodes[origin].edges[destination] = weight
        if not self.__directed:
            self.__nodes[destination].edges[origin] = weight

    def deleteEdge(self, origin, destination):
        if origin not in self.__nodes:
            raise ValueError("Origin doesn't exist.")
        if destination not in self.__nodes:
            raise ValueError("Destination doesn't exist.")
        if destination in self.__nodes[origin].edges:
            del self.__nodes[origin].edges[destination]
        if not self.__directed and origin in self.__nodes[destination].edges:
            del self.__nodes[destination].edges[origin]

    def alterEdge(self, origin, destination, weight):
        """ check if both nodes exist, before checking if there's an edge between them and updating it. 
        If the graph to be implemented is undirected, this occurs for the edge created between both nodes. """
        if origin not in self.__nodes:
            raise ValueError("Origin doesn't exist.")
        if destination not in self.__nodes:
            raise ValueError("Destination doesn't exist.")
        self.__nodes[origin].edges[destination] = weight
        if not self.__directed:
            self.__nodes[destination].edges[origin] = weight

    def showConnection(self, origin, destination):
        if origin not in self.__nodes:
            raise ValueError("Origin doesn't exist.")
        if destination not in self.__nodes:
            raise ValueError("Destination doesn't exist.")
        if destination in self.__nodes[origin].edges:
            return f"Edge from {origin} to {destination} has a weight of {self.__nodes[origin].edges[destination]}."
        else:
            raise ValueError("Edge does not exist.")

    def depthFirst(self, node, visited = None):
        """ utilises recursive calls to traverse a graph from the current node, going as far down as possible before backtracking. The given node 
        is added to 'visited'; if the neighbouring node hasn't been visited, pass it as an argument into the recursion. This continues until 
        all nodes reachable from the starting node have been visited. """
        if node not in self.__nodes:
            raise ValueError("Node doesn't exist.")
        
        if visited is None:
            visited = set()
        
        visited.add(node)
        result = str(node) + " "
        
        for neighbour in self.__nodes[node].edges:
            if neighbour not in visited:
                result += self.depthFirst(neighbour, visited)
        
        return result
    
    def breadthFirst(self, node):
        """ utilises a queue to explore nodes at the same depth before ascending. The given node is added to 'queue' and 'visited', before a loop 
        is entered until 'queue' is empty. In each iteration, dequeue the front node and explore its neighbours; for each, if it hasn't been visited, 
        enqueue it to the back and add it to 'visited'. This continues until all nodes reachable from the starting node have been visited. """
        if node not in self.__nodes:
            raise ValueError("Node doesn't exist.")

        """ 'deque' creates a double ended queue in which arguments can be appended or popped at either end. """
        visited = set()
        queue = deque([node])
        visited.add(node)
        result = str(node) + " "
        
        while queue:
            current_node = queue.popleft()
            
            for neighbour in self.__nodes[current_node].edges:
                if neighbour not in visited:
                    queue.append(neighbour)
                    visited.add(neighbour)
                    result += str(neighbour) + " "
                  
        return result

    def dijkstrasShortestPath(self, node):
        if node not in self.__nodes:
            raise ValueError("Node doesn't exist.")

        """ tracks the tentative distances from the starting node to each node in the graph; set the distance to the starting node 
        as 0 and all other distances as infinite. """
        distances = {n: float('inf') for n in self.__nodes}
        distances[node] = 0
        """ represents a heap-based priority queue, used to store nodes in order of their TDs. """
        pq = [(0, node)]

        """ while the pq isn't empty, extract the node w/ the smallest TD 'u'' from 'pq'. """
        while pq:
            """ 'heappop' removes and returns the smallest element, whilst the order is adjusted as to maintain the heap. """
            dist, current_node = heappop(pq)
        
            if dist > distances[current_node]:
                continue

            """ for each neighbor 'v' of 'u', calculate a TD 'alt' as the sum of the distance to 'u' and the weight of the edge connecting 'u' and 'v'. 
            If this is < than the current distance to 'v' in 'distances', update the distance in 'distances' and add 'v' to 'pq' w/ priority 'alt'. """
            for neighbour, weight in self.__nodes[current_node].edges.items():
                tentative_distance = dist + weight
                if tentative_distance < distances[neighbour]:
                    distances[neighbour] = tentative_distance
                    """ 'heappush' inserts an element into the heap whilst preserving OPs. """
                    heappush(pq, (tentative_distance, neighbour))
    
        return distances
