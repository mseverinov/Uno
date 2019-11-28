class Node:
    def __init__(self, parentEdge, rootNode = False):
        if rootNode == False:
            self.parent = parentEdge
            if parentEdge.outcome == True:
                self.color = parentEdge.parent.color-1
                self.rest = parentEdge.parent.rest
            else:
                self.color = parentEdge.parent.color
                self.rest = parentEdge.parent.rest - 1

            self.depth = parentEdge.parent.depth + 1

        else:
            self.color = 25
            self.rest = 83
            self.depth = 0
        Que.contents.append(self)


    def addBranches(self):
        self.success = Edge(True, self)
        self.fail = Edge(False, self)

class Edge:
    def __init__(self, outcome, parentNode):
        self.parent = parentNode
        self.outcome = outcome
        self.child = Node(self)

class Que:
    contents = []

rootNode = Node(None, True)
maxDepth = 0
while len(Que.contents) != 0:
    nextNode = Que.contents[0]
    if nextNode.depth > maxDepth:
        print(maxDepth)
        maxDepth = nextNode.depth
    if nextNode.depth < 8:
        nextNode.addBranches()
    Que.contents = Que.contents[1:]

print('done')
