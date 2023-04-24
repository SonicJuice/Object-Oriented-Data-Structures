

class Graph(object):
    """ here, an adjacency matrix is utilised to represent a node via each row and column. This implementation suits densely connected graphs, 
    where most pairs of nodes are edged, as a sparse graph will waste memory via empty edges. """

  def __init__(self, num_nodes):
        """ '_' represents a placeholder iterator, who's value is ignored in favor of some specific number of iterations. """
        self.__adj_matrix = [[None] * num_nodes for _ in range(num_nodes)]

    def addNode(self, new_node):
        """ nodes are added by extending the AM; if the new node's index >= the current number of nodes, 'None' values are added to each row, 
        and a new row of 'None's' are appended. """
        num_nodes = len(self.__adj_matrix)
        if new_node >= num_nodes:
            for row in self.__adj_matrix:
                row.append(None)
            self.__adj_matrix.append([None] * (new_node + 1 - num_nodes))
        else:
            raise ValueError("Node already exists.")

    def removeNode(self, node_to_remove):
        num_nodes = len(self.__adj_matrix)
        if node_to_remove >= num_nodes:
            raise ValueError("Node not found.")
        else:
            """ node's corresponding column and row are deleted. """
            del self.__adj_matrix[node_to_remove]
            for row in self.__adj_matrix:
                del row[node_to_remove]

    def listNodes(self):
        """ list nodes by generating integers up to the current number of nodes. """
        return list(range(len(self.__adj_matrix)))

    def alterEdge(self, origin, destination, weight):
        num_nodes = len(self.__adj_matrix)
        """ validate origin and destination node indices, before checking that the edge between them exists. """
        if origin >= num_nodes or destination >= num_nodes:
            raise ValueError("Invalid origin or destination.")
        if self.__adj_matrix[origin][destination] is None:
            raise ValueError("Edge from origin to destination doesn't exist.")

        self.__adj_matrix[origin][destination] = weight

    def addEdge(self, origin, destination, weight):
        num_nodes = len(self.__adj_matrix)
        if origin >= num_nodes or destination >= num_nodes:
            raise ValueError("Invalid origin or destination.")
        if not isinstance(weight, (int, float)):
            raise ValueError("Non-numeric weight.")
        if self.__adj_matrix[origin][destination] is not None:
            raise ValueError("Edge from origin to destination already exists.")

        self.__adj_matrix[origin][destination] = weight

    def removeEdge(self, origin, destination):
        num_nodes = len(self.__adj_matrix)
        if origin >= num_nodes or destination >= num_nodes:
            raise ValueError("Invalid origin or destination.")
        if self.__adj_matrix[origin][destination] is None:
            raise ValueError("Edge from origin to destination doesn't exist.")

        self.__adj_matrix[origin][destination] = None

    def showConnection(self, origin, destination):
        num_nodes = len(self.__adj_matrix)
        if origin >= num_nodes or destination >= num_nodes:
            raise ValueError("Invalid origin or destination.")
        if self.__adj_matrix[origin][destination] is None:
            raise ValueError("Edge from origin to destination doesn't exist.")

        return f"Edge from {origin} to {destination} has a weight of {self.__adj_matrix[origin][destination]}."
