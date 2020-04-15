# Priority dictionary using binary heaps
# David Eppstein, UC Irvine, 8 Mar 2002

from __future__ import generators


class PriorityDict(dict):
    def __init__(self):
        self.__heap = []
        dict.__init__(self)

    def smallest(self):
        if len(self) == 0:
            raise IndexError("smallest of empty priorityDictionary")
        heap = self.__heap
        while heap[0][1] not in self or self[heap[0][1]] != heap[0][0]:
            last_item = heap.pop()
            insertion_point = 0
            while 1:
                small_child = 2 * insertion_point + 1
                if small_child + 1 < len(heap) and \
                        heap[small_child] > heap[small_child + 1]:
                    small_child += 1
                if small_child >= len(heap) or last_item <= heap[small_child]:
                    heap[insertion_point] = last_item
                    break
                heap[insertion_point] = heap[small_child]
                insertion_point = small_child
        return heap[0][1]

    def __iter__(self):
        def iter_fn():
            while len(self) > 0:
                x = self.smallest()
                yield x
                del self[x]

        return iter_fn()

    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)
        heap = self.__heap
        if len(heap) > 2 * len(self):
            self.__heap = [(v, k) for k, v in self.items()]
            self.__heap.sort()
        else:
            new_pair = (val, key)
            insertion_point = len(heap)
            heap.append(None)
            while insertion_point > 0 and new_pair < heap[(insertion_point - 1) // 2]:
                heap[insertion_point] = heap[(insertion_point - 1) // 2]
                insertion_point = (insertion_point - 1) // 2
            heap[insertion_point] = new_pair

    def set_default(self, key, val):
        if key not in self:
            self[key] = val
        return self[key]
