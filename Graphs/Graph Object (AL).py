


class Graph(object):
    """ for reference, a graph is a set of nodes connected by edges, which may be directed/undirected and weighted/unweighted. Here, an adjacency list is utilised for the space-efficient implementation of a sparsely connected graph. """
    def __init__(self):
        self.__adj_list = {}

    def addNode(self, new_node):
        """ if the new node isn't yet in the AL, add the new node as a key in '__adj_list' w/ an empty dictionary as its value, representing no outgoing edges from the new node. """
        if new_node not in self.__adj_list:
            self.__adj_list[new_node] = {}
        else:
            raise ValueError("Node already exists.")

    def removeNode(self, node_to_remove):
        """ if node is in the AL, delete the key-value pair from '__adj_list', effectively removing the node and all its outgoing edges from the graph. """
        if node_to_remove not in self.__adj_list:
            raise ValueError("Node not found.")
        else:
            del self.__adj_list[node_to_remove]

    def listNodes(self):
        """ print all keys in '__adj_list', representing the nodes. """
        print(*self.__adj_list.keys())

    def alterEdge(self, origin, destination, weight):
        """ check if both nodes exist, before checking if there's an edge between them and updating it. """
        if origin not in self.__adj_list:
            raise ValueError("Invalid origin.")
        if destination not in self.__adj_list:
            raise ValueError("Invalid destination.")
        if destination not in self.__adj_list[origin]:
            raise ValueError("Edge from origin to destination doesn't exist.")

        self.__adj_list[origin][destination] = weight

    def addEdge(self, origin, destination, weight):
        if origin not in self.__adj_list:
            self.__adj_list[origin] = {}
        if destination not in self.__adj_list:
            """ if either node doesn't exist, add it to the AL as empty dictionaries. If the weight is numeric and there's no pre-existing edge, add a new key-value pair to '__adj_list'.  """
            self.__adj_list[destination] = {}
        if not isinstance(weight, (int, float)):
            raise ValueError("Non-numeric weight.")
        if destination in self.__adj_list[origin]:
            raise ValueError("Edge from origin to destination already exists.")

        self.__adj_list[origin][destination] = weight

    def removeEdge(self, origin, destination):
        if origin not in self.__adj_list:
            raise ValueError("Invalid origin.")
        if destination not in self.__adj_list:
            raise ValueError(f"Invalid destination.")
        if destination not in self.__adj_list[origin]:
            raise ValueError("Edge from origin to destination doesn't exist.")

        del self.__adj_list[origin][destination]

    def showConnection(self, origin, destination):
        if origin not in self.__adj_list:
            raise ValueError("Invalid origin.")
        if destination not in self.__adj_list:
            raise ValueError("Invalid destination.")
        if destination not in self.__adj_list[origin]:
            raise ValueError("Edge from origin to destination doesn't exist.")

        return f"Edge from {origin} to {destination} has a weight of {self.__adj_list[origin][destination]}."
