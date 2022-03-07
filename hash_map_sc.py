# Name: Kevin Kraatz
# OSU Email: kraatzk@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - Portfolio Project - HashMap Implementation
# Due Date: 03/11/2022
# Description:  HashMap implementation using linked list chaining for collision resolution.
#               This is part 1 of the portfolio project for CS261 Data Structures.


from a6_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """Clears the contents of the hash map while preserving capacity."""
        for i in range(0, self.capacity):
            self.buckets.set_at_index(i, LinkedList())
        self.size = 0

    def get(self, key: str) -> object:
        """Returns the value associated with the given key. If the key is
        not located, returns None."""
        bucket_location = self.hash_function(key) % self.buckets.length()
        if self.buckets[bucket_location].contains(key):
            found_node = self.buckets[bucket_location].contains(key)
            return found_node.value

    def put(self, key: str, value: object) -> None:
        """Inserts a new key/value pair into the hash map. If the
        key already exists in the hash map, the existing value is replaced
        with the new value."""
        bucket_location = self.hash_function(key) % self.buckets.length()
        if self.buckets[bucket_location].contains(key):  # if key is found, replace old value with new
            found_node = self.buckets[bucket_location].contains(key)
            found_node.value = value
        else:
            self.buckets[bucket_location].insert(key, value)  # if key not found, insert new key/value pair
            self.size += 1  # when new key is inserted, increment map size +1

    def remove(self, key: str) -> None:
        """Removes the key and its value from the hash map. If the key does
        not exist, this method does nothing."""
        bucket_location = self.hash_function(key) % self.buckets.length()
        if self.buckets[bucket_location].contains(key):
            self.buckets[bucket_location].remove(key)  # if key is found, remove linked list node and decrement size -1
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """Returns True if the given key is in the hash map. Returns False otherwise."""
        bucket_location = self.hash_function(key) % self.buckets.length()
        if self.buckets[bucket_location].contains(key):
            return True
        else:
            return False

    def empty_buckets(self) -> int:
        """Returns the number of empty buckets in the hash map."""
        empty_counter = 0  # counting incrementer for empty buckets
        for i in range(0, self.capacity):
            if self.buckets[i].length() == 0:  # if empty, increment +1 to counter
                empty_counter += 1
        return empty_counter

    def table_load(self) -> float:
        """Returns the load factor of the hash map."""
        load = self.size / self.capacity
        return load

    def resize_table(self, new_capacity: int) -> None:
        """Changes the hash map capacity to the given integer. Existing
        key/value pairs are kept and links are rehashed. Does nothing if
        the new capacity is less than 1."""
        # do not perform table resize if new capacity is less than 1
        if new_capacity < 1:
            return
        new_map = DynamicArray()  # generate new map
        old_map = self.buckets  # swap variables from old to new
        self.buckets = new_map
        self.size = 0  # set new hash map size to zero
        for buckets in range(0, new_capacity):  # fill new map
            self.buckets.append(LinkedList())
        for buckets in range(0, self.capacity):
            for i in old_map[buckets]:
                self.put(i.key, i.value)  # rehash all hash table links in new map
        self.capacity = new_capacity  # set new capacity

    def get_keys(self) -> DynamicArray:
        """Returns an array that contains all the keys in the hash map."""
        array = DynamicArray()  # generate new array
        for buckets in range(0, self.capacity):  # iterate through buckets
            for i in self.buckets[buckets]:  # iterate through linked lists
                array.append(i.key)  # append all keys to array
        return array


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
