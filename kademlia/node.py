from operator import itemgetter
import heapq


class Node:
    def __init__(self, id, ip=None, port=None):
        self.id = id
        self.ip = ip
        self.port = port
        self.long_id = long(id.encode('hex'), 16)

    def sameHomeAs(self, node):
        return self.ip == node.ip and self.port == node.port

    def distanceTo(self, node):
        return self.long_id ^ node.long_id

    def __iter__(self):
        """
        Enables use of Node as a tuple - i.e., tuple(node) works.
        """
        return iter([self.ip, self.port, self.id])

    def __repr__(self):
        return repr([self.long_id, self.ip, self.port])

    def __str__(self):
        return "%s:%s" % (self.ip, str(self.port))


class NodeHeap(object):
    def __init__(self, maxsize):
        self.heap = []
        self.contacted = set()
        self.maxsize = maxsize

    def remove(self, peerIDs):
        """
        Remove a list of peer ids from this heap.  Note that while this
        heap retains a constant visible size (based on the iterator), it's
        actual size may be quite a bit larger than what's exposed.  Therefore,
        removal of nodes may not change the visible size as previously added
        nodes suddenly become visible.
        """
        peerIDs = set(peerIDs)
        if len(peerIDs) == 0:
            return
        nheap = []
        for distance, node in self.heap:
            if not node.id in peerIDs:
                heapq.heappush(nheap, (distance, node))
        self.heap = nheap

    def allBeenContacted(self):
        return len(self.getUncontacted()) == 0

    def getIDs(self):
        return [n.id for n in self]

    def markContacted(self, node):
        self.contacted.add(node.id)

    def push(self, distance, node):
        heapq.heappush(self.heap, (distance, node))

    def __len__(self):
        return min(len(self.heap), self.maxsize)

    def __iter__(self):
        nodes = heapq.nsmallest(self.maxsize, self.heap)
        return iter(map(itemgetter(1), nodes))

    def getUncontacted(self):
        return [n for n in self if not n.id in self.contacted]
