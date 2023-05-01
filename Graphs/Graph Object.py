from collections import deque
from heapq import heappop, heappush

class Node:
    def __init__(self, name):
        self.__name = name
        self.edges = {}

    def createEdge(self, destination, weight):
        if destination not in self.edges:
            self.edges[destination] = weight
        else:
            raise ValueError("Edge already exists.")

    def removeEdge(self, destination):
        if destination in self.edges:
            del self.edges[destination]
        else:
            raise ValueError("Edge does not exist.")

    def getConnection(self, destination):
        if destination in self.edges:
            return f"Edge from {self.__name} to {destination} has a weight of {self.edges[destination]}."
        else:
            raise ValueError("Edge does not exist.")

#-------------------------------------------------------------


class Graph:
    """ a graph is a set of nodes connected by edges, which may be directed/undirected and weighted/unweighted. 
    Here, an adjacency list is utilised for the space-efficient implementation of a sparsely connected graph. """
    def __init__(self, directed = True):
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


    def addEdge(self, origin, destination, weight):
        if origin not in self.__nodes:
            raise ValueError("Origin doesn't exist.")
        if destination not in self.__nodes:
            raise ValueError("Destination doesn't exist.")
        if not isinstance(weight, (int, float)):
            raise ValueError("Non-numeric weight.")
        self.__nodes[origin].createEdge(destination, weight)
        if not self.__directed:
            self.__nodes[destination].createEdge(origin, weight)

    def deleteEdge(self, origin, destination):
        if origin not in self.__nodes:
            raise ValueError("Origin doesn't exist.")
        if destination not in self.__nodes:
            raise ValueError("Destination doesn't exist.")
        self.__nodes[origin].removeEdge(destination)
        if not self.__directed:
            self.__nodes[destination].removeEdge(origin)

    def alterEdge(self, origin, destination, weight):
        """ check if both nodes exist, before checking if there's an edge between them and updating it. If the graph to be implemented is undirected, this occurs for the edge created between both nodes. """
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
        return self.__nodes[origin].getConnection(destination)

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
        
        visited = set()
        """ 'deque' creates a double ended queue in which arguments can be appended or popped at either end. """
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
        """ dictionary is initialised wi/ the source as the key, and its distance from itself as 0; all other node distances are set to infinity. """
        if node not in self.__nodes:
            raise ValueError("Node doesn't exist.")
            
        distances = {node: 0}
        for n in self.__nodes:
            if n != node:
                distances[n] = float('inf')
        pq = [(0, node)]
        visited = {}

        while pq:
            """ heap utilised to implement a priority queue; 'heappop' removes and returns the smallest element, whilst the order is adjusted 
            to maintain the order properties (as mentioned in 'Priority Queue Object.py'). """
            distance, current_node = heappop(pq)
            if current_node in visited:
                continue
            visited[current_node] = True

            for neighbour, weight in self.__nodes[current_node].edges.items():
                tentative_distance = distances[current_node] + weight
                if tentative_distance < distances[neighbour]:
                    distances[neighbour] = tentative_distance
                    """ 'heappush' inserts an element into the heap whilst preserving OPs. """
                    heappush(pq, (tentative_distance, neighbour))

        return distances
