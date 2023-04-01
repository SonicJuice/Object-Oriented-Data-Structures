

class Graph(object):

    def __init__(self):
        self.__adj_list = {}

    def addNode(self, new_node):
        if new_node not in self.__adj_list.keys():
            self.__adj_list[new_node] = {}
        else:
            print("Node already exists")

    def removeNode(self, node_to_remove):
        if node_to_remove not in self.__adj_list.keys():
            print("Node not found")
        else:
            del self.__adj_list[node_to_remove]

    def listNodes(self):
        print(*self.__adj_list.keys())

    def alterEdge(self, origin, destination, weight):
        if origin not in self.__adj_list:
            raise ValueError("Invalid origin: f{origin}")
        if destination not in self.__adj_list:
            raise ValueError(f"Invalid destination: {destination}")
        if destination not in self.__adj_list[origin]:
            raise ValueError(f"Edge from {origin} to {destination} doesn't exist.")

        self.__adj_list[origin][destination] = weight

    def addEdge(self, origin, destination, weight):
        if origin not in self.__adj_list:
            self.__adj_list[origin] = {}
        if destination not in self.__adj_list:
            self.__adj_list[destination] = {}
        if not isinstance(weight, (int, float)):
            raise ValueError(f"Invalid weight: {weight}")
        if destination in self.__adj_list[origin]:
            raise ValueError(f"Edge from {origin} to {destination} already exists.")

        self.__adj_list[origin][destination] = weight

    def removeEdge(self, origin, destination):
        if origin not in self.__adj_list:
            raise ValueError(f"Invalid origin: {origin}")
        if destination not in self.__adj_list:
            raise ValueError(f"Invalid destination: {destination}")
        if destination not in self.__adj_list[origin]:
            raise ValueError(f"Edge from {origin} to {destination} doesn't exist.")

        del self.__adj_list[origin][destination]

    def showConnection(self, origin, destination):
        if origin not in self.__adj_list:
            raise ValueError(f"Invalid origin: {origin}")
        if destination not in self.__adj_list:
            raise ValueError(f"Invalid destination: {destination}")
        if destination not in self.__adj_list[origin]:
            raise ValueError(f"Edge from {origin} to {destination} doesn't exist.")

        return f"Edge from {origin} to {destination} has weight {self.__adjList[origin][destination]}"
