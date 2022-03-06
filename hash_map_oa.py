# Name: Kevin Kraatz
# OSU Email: kraatzk@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - Portfolio Project - HashMap Implementation
# Due Date: 03/11/2022
# Description:


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
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
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def clear(self) -> None:
        """"""
        for buckets in range(0, self.capacity):
            if buckets is not None:
                tombstone = HashEntry(None, None)
                tombstone.is_tombstone = True
                for i in range(0, self.capacity):
                    self.buckets.set_at_index(i, tombstone)
        self.size = 0

    def get(self, key: str) -> object:
        """
        TODO: Write this implementation
        """
        # quadratic probing required
        initial = self.hash_function(key) % self.buckets.length()
        add_counter = 1
        next_pos = initial
        while True:
            if self.buckets.get_at_index(next_pos) is None:
                return None

            else:
                if self.buckets.get_at_index(next_pos).key == key:
                    value = self.buckets.get_at_index(next_pos).value
                    return value
                else:
                    next_pos = (initial + (add_counter ** 2)) % self.capacity  # quadratic probe equation
                    add_counter += 1

    def put(self, key: str, value: object) -> None:
        """"""
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair
        #
        # quadratic probing required
        # print(str(self.size))
        if self.table_load() >= 0.5:
            self.resize_table(self.capacity * 2)
        # print(str(self.size))
        # print(str(self.buckets.length()))
        initial = self.hash_function(key) % self.buckets.length()
        add_counter = 1
        next_pos = initial
        while True:
            # print(str(next_pos))
            # print(str(self.buckets.length()))
            if self.buckets.get_at_index(next_pos) is None:
                new_hash_entry = HashEntry(key, value)
                self.buckets.set_at_index(next_pos, new_hash_entry)
                self.size += 1
                break
            else:
                if self.buckets.get_at_index(next_pos).key == key:
                    self.buckets.get_at_index(next_pos).value = value
                    break
                else:
                    next_pos = (initial + (add_counter ** 2)) % self.capacity  # quadratic probe equation
                    add_counter += 1

    def remove(self, key: str) -> None:
        """
        TODO: Write this implementation
        """
        # quadratic probing required
        initial = self.hash_function(key) % self.buckets.length()
        add_counter = 1
        next_pos = initial
        while True:
            if self.buckets.get_at_index(next_pos) is None:
                break
            else:
                if self.buckets.get_at_index(next_pos).key == key:
                    value = self.buckets.get_at_index(next_pos).value
                    self.buckets.get_at_index(next_pos).key = HashEntry(key, value).is_tombstone
                    self.size -= 1
                else:
                    next_pos = (initial + (add_counter ** 2)) % self.capacity  # quadratic probing to check next pos
                    add_counter += 1

    def contains_key(self, key: str) -> bool:
        """
        TODO: Write this implementation
        """
        # quadratic probing required
        initial = self.hash_function(key) % self.buckets.length()
        add_counter = 1
        next_pos = initial
        while True:
            if self.buckets.get_at_index(next_pos) is None:
                return False
            else:
                if self.buckets.get_at_index(next_pos).key == key:
                    return True
                else:
                    next_pos = (initial + (add_counter ** 2)) % self.capacity  # quadratic probing to check next pos
                    add_counter += 1

    def empty_buckets(self) -> int:
        """"""
        empty_counter = 0
        for i in range(0, self.capacity):
            # print(str(self.buckets.get_at_index(i)))
            if self.buckets.get_at_index(i) is None:
                empty_counter += 1
                # print(str("None count so far is " + str(empty_counter)))
            else:
                if self.buckets.get_at_index(i).is_tombstone:
                    empty_counter += 1
        # print(str(self.size))
        return empty_counter

    def table_load(self) -> float:
        """
        TODO: Write this implementation
        """
        load = self.size / self.capacity
        return load

    def resize_table(self, new_capacity: int) -> None:
        """
        TODO: Write this implementation
        """
        # print("resize here")
        # remember to rehash non-deleted entries into new table
        if new_capacity < 1 or new_capacity < self.size:
            return
        new_map = DynamicArray()
        old_map = self.buckets
        self.buckets = new_map
        for _ in range(0, new_capacity):
            self.buckets.append(None)
        for i in range(0, old_map.length()):
            if self.buckets is not None:
                pass
            else:
                if self.buckets.is_tombstone:
                    pass
                else:
                    # print("capacity is " + str(self.capacity))
                    self.put(i.key, i.value)  # rehash all hash table links
                    # print("did it put? - " + str(self.buckets))
        self.capacity = new_capacity
        # print("capacity is now " + str(self.capacity))

    def get_keys(self) -> DynamicArray:
        """
        TODO: Write this implementation
        """
        array = DynamicArray()
        for buckets in range(0, self.capacity):
            if self.buckets.get_at_index(buckets) is None:
                pass
            else:
                array.append(self.buckets.get_at_index(buckets).key)
        return array


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
    # this test assumes that put() has already been correctly implemented
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
