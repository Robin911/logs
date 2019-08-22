from queue import Queue
import random

q = Queue()

q.put(random.randint(1, 100))
q.put(random.randint(1, 100))

print(q.get())
print(q.get())