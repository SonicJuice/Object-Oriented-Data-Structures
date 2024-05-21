""" a hash table is a collection of items stored alongside the index of their physical file addresses; this makes them quickly 
accessible by removing the requirement for all records to be checked. Indexes are created via the application of hashing algorithms 
to the value in each record's key field. These are bound to produce synonyms (hashes to identical memory addresses), with two 
record keys hashing to the same address being a 'collision.' """
from tabulate import tabulate
from mmh3 import hash


class HashTable:
    def __init__(self, size):
        self.num_elements = 0
        self.data = [None] * size
        self.size = size
      
    """ calculate the hash index for a given key via the non-cryptographic MurmurHash3 algorithm. 'mh3.hash()' takes a 'key' argument 
    of a string, integer or byte array to be hashed, and returns a 32-bit, unsigned integer hash value, which is also deterministic. """
    def __get_hash_index(self, key):
        hash_value = hash(str(key))
        return hash_value % self.size
      
    """ add a key-value pair to the HT, first calculating the hash index for the given key. If the HI in '__data' is None, initialise 
    it as an empty dictionary, then add the KV pair to the dictionary at the HI and increment '__num_elements'. If the load factor 
    (ratio of elements to the HT size) exceeds 0.75, trigger a resize operation. """
    def add_item(self, key, value):
        hash_index = self.__get_hash_index(key)
        if self.data[hash_index] is None:
            self.data[hash_index] = {}
        self.data[hash_index][key] = value
        self.num_elements += 1
        load_factor = self.num_elements / self.size
        if load_factor > 0.75:
            self.__resize_hash_table()

    """ if the load factor exceeds the threshold, create 'new data' double the size of the current HT and initialise it with 'None' 
    values. Then, iterate over each entry in the current hash table ('__data') and rehashe each KV pair to the new HT. Finally, update 
    '__data' and '__size' to reflect the resized HT. """
    def __resize_hash_table(self):
        new_size = 2 * self.size
        new_data = [None] * new_size

        for entry in self.data:
            if entry:
                for key, value in entry.items():
                    new_hash_index = self.__get_hash_index(key)
                    if new_data[new_hash_index] is None:
                        new_data[new_hash_index] = {}
                    new_data[new_hash_index][key] = value

        self.data = new_data
        self.size = new_size

    """ search for an entry w/ the given key in the HT, calculating the HI for it via '__getHashIndex().' Then checks if the entry 
    at that index is None and if it's not, it retrieve and return the value associated w/ the key from the dictionary at the HI. 
    If the entry is 'None', it indicates that the key doesn't exist in the HT. """
    def __find_entry(self, key):
        hash_index = self.__get_hash_index(key)
        if self.data[hash_index] is None:
            return
        return self.data[hash_index].get(key)

    """ retrieve the value associated w/ a given key from the HT by calling '__findEntry()' to check if the key exists in the HT. 
    If so, return the corresponding value. """
    def get_item(self, key):
        entry = self.__find_entry(key)
        if entry is not None:
            return entry
        raise KeyError("Key doesn't exist.")

    """ removs a KV pair from the HT by first calculating the key's HI via '__getHashIndex().' It then checks if the entry at the 
    HI is 'None' or if the key isn't present in the dictionary at the HI; if either condition is true, raise a KeyError. Otherwise, 
    delete the KV pair from the dictionary, decrement '__num_elements', and delete the KV pair from the HT. """
    def delete_item(self, key):
        hash_index = self.__get_hash_index(key)
        if self.data[hash_index] is None or key not in self.data[hash_index]:
            raise KeyError("Key doesn't exist.")

        del self.data[hash_index][key]
        self.num_elements -= 1

    """ return a list of values, whose corresponding keys contain a given substring, by iterating over each entry in the HT ('__data'), 
    and checking if the substring is present in any of the keys. If a match is found, append the corresponding value to 'matching_data'
    and return it. """
    def key_contains(self, substring):
        matching_data = []
        for entry in self.data:
            if entry:
                for key, value in entry.items():
                    if substring in str(key):
                        matching_data.append(value)
        return matching_data

    def show_hash_table(self):
        table = []
        for entry in self.data:
            if entry:
                for key, value in entry.items():
                    table.append([key, value])
        headers = ["Key", "Value"]
        return tabulate(table, headers)
