

class PriorityQueue(object):
    def __init__(self, q_size):
        self.q = []
        self.size = 0
        self.max_size = q_size

    def insert(self, item, priority):
        if self.is_full():
            raise ValueError("Queue is full.")
        else:
            self.size += 1
            i = self.size - 1
            self.q.append((item, priority))
            """ append a tuple containing the item and its priority, then perform a heapify operation by swapping the new item w/ 
            its parent until the parent has a higher priority, or the item becomes the root. This ensures that the highest priority 
            item is always at the root. """
            while i > 0 and priority <= self.q[(i - 1) // 2][1]:
                self.q[i], self.q[(i - 1) // 2] = self.q[(i - 1) // 2], self.q[i]
                """ represent parent index. """
                i = (i - 1) // 2

    def delete(self):
        if self.isEmpty():
            raise ValueError("Queue is empty.")
        else:
            item, priority = self.q[0]
            self.q[0] = self.q[-1]
            self.q.pop()
            self.size -= 1
            i = 0

            """ store the item and its priority from the root, replace the root with the last item in the heap, and remove the 
            last item from the heap. Then perform a heapify operation by swapping the root w/ its smallest child until the root 
            has a lower priority than its children, or it becomes a leaf node. """
            while i >= 0:
                """ represents child indexes. """
                left = 2 * i + 1
                right = 2 * i + 2
                smallest = i
                if left < self.size and self.q[left][1] <= self.q[smallest][1]:
                    smallest = left
                if right < self.size and self.q[right][1] <= self.q[smallest][1]:
                    smallest = right
                if smallest == i:
                    i = -1
                else:
                    self.q[i], self.q[smallest] = self.q[smallest], self.q[i]
                    i = smallest
            return item, priority

    def alter_priority(self, item, new_priority):
        if self.isEmpty():
            raise ValueError("Queue is empty.")
        found = False
        i = 0
        while i < self.size and not found:
            if self.q[i][0] == item:
                found = True
            else:
                i += 1
        if not found:
            raise ValueError("Item doesn't exist.")
        old_priority = self.q[i][1]
        self.q[i] = (item, new_priority)
        if new_priority > old_priority:
            while i > 0 and new_priority <= self.q[(i - 1) // 2][1]:
                self.q[i], self.q[(i - 1) // 2] = self.q[(i - 1) // 2], self.q[i]
                i = (i - 1) // 2

    def is_full(self):
        return self.size == self.max_size

    def is_empty(self):
        return self.size == 0

    def show_queue(self):
        """ prints str() representation of contents in descending priority order by mapping 'reverse' to each item. """
        sorted_q = sorted(self.q, key = lambda x: x[1], reverse = True)
        return " ".join(str(item) for item in sorted_q)
