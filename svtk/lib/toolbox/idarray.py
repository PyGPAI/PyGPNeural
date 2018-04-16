import numpy as np

class IdArray(object):
    # todo: use this to expand: people.idsia.ch
    """A class used for sorting memory location for single point inserts.
    For inserting large sets of points, this class will need to be modified."""

    def __init__(self):
        self.pointers = np.array([])
        self.free_pointers = set()
        self.last_largest_id = -1

    def __getitem__(self, id):
        return self.pointers[id]

    def __repr__(self):
        """
        Prints out a string representation of this class and its variables, used with print function.
        This is helpful for figuring out how this class works, as well as testing.
        """
        str_out = "IdArray:\n"+\
        "\tPointer array:\t"+("\n\t\t" if len(self.pointers)>8 else "")+str(self.pointers)+"\n"+\
        "\tFree array locations:\t"+("\n\t\t" if len(self.free_pointers)>12 else "")+str(self.free_pointers)+"\n"+\
        "\tLast largest ID:\t"+str(self.last_largest_id)+"\n"
        return str_out

    def __len__(self):
        return len(self.pointers) - len(self.free_pointers)

    def add_ids(self, locations=None, num_ids=-1):
        if locations is None:
            for i in range(num_ids):
                self.add_id()
        else:
            for i in range(len(locations)):
                self.add_id(locations[i])

    def add_id(self, location = -1):
        if location==-1:
            location = self.last_largest_id + 1
            self.last_largest_id = location
        elif location > self.last_largest_id:
            self.last_largest_id = location

        if len(self.free_pointers) > 0:
            id = self.free_pointers.pop()
            self.pointers[id] = location
        else:
            id = len(self.pointers)
            self.pointers = np.append(self.pointers,[location])

        return id

    def del_id(self, id):
        assert(id not in self.free_pointers)
        assert(id < len(self.pointers))

        val = self.pointers[id]
        self.pointers[id] = -1
        self.free_pointers.add(id)

        self.pointers = np.where(self.pointers > val, self.pointers-1, self.pointers)
        self.last_largest_id-=1

    def pop_id(self, id):
        assert(id not in self.free_pointers)
        if id >= len(self.pointers):
            return None

        val = self.pointers[id]
        self.pointers[id] = -1
        self.free_pointers.add(id)

        self.pointers = np.where(self.pointers > val, self.pointers-1, self.pointers)
        self.last_largest_id = max(self.last_largest_id-1, -1)

        return val