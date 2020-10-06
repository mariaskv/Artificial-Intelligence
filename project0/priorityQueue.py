import heapq

class PriorityQueue:

    'initialize pq with a member heap and a counter of the members it contains'
    def __init__(self):
        self.heap = []
        self.size = 0
    
    'push an entry into pq using its priority and his id into the heap'
    def push(self,item,priority):
        entry = (priority,self.size,item)
        heapq.heappush(self.heap,entry)
        self.size+=1
    
    'pop out the entry with the smallest priority'
    def pop(self):
        if(self.size > 0):
            priority, counter, item = heapq.heappop(self.heap)
            self.size += -1
            return item
        else:
            return "Attention.There is no item to remove"

    'ind out wheather the heap is empty based on its size'
    def isEmpty(self):
        if(self.size == 0):
            return True
        else:
            return False

    'check if an entry belongs to the pq and update it or push it if needed'
    def update(self,item,priority):
        i = 0
        flag = False

        if(self.size > 0):
            while(i < self.size):
                f_priority, f_counter, f_item = self.heap[i]

                if(f_item == item):
                    flag = True

                    if(f_priority > priority):
                        del self.heap[i]
                        self.push(item,priority)
                    
                    break

                i += 1

            if not flag:
                self.push(item,priority)


if __name__ == "__main__":
    q = PriorityQueue()
