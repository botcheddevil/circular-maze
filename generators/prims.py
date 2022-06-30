import random 

class Prims:

    def getRandomNode(self, G, visitedList):
        currentNodeId = random.choice([i for i in range(1,len(G.nodes)+1) if i not in visitedList])
        currentNode = G.nodes(data=True)[currentNodeId]
        currentNode["visited"] = True
        visitedList.append(currentNodeId)
        return (currentNodeId, currentNode)

    def removeEdge(self, G, currentNode, neighborNode):
        G.remove_edge(neighborNode, currentNode[0])
        G.nodes(data=True)[neighborNode]["visited"] = True
        currentNode = (neighborNode, G.nodes(data=True)[neighborNode])

    def generate(self, G, circularDivision, levelCount):
        for node in G.nodes(data=True):

            # Add North
            northNodes = [x for x in G.nodes(data=True)  if x[1]["angle"] == node[1]["angle"] and x[1]["level"] == node[1]["level"]+1]
            print("northNodes", northNodes)
            if (len(northNodes) != 0): G.add_edge(node[0], northNodes[0][0])

            # Add East
            eastNodes = [x for x in G.nodes(data=True)  if (x[1]["angle"] == node[1]["angle"]+node[1]["step"] or x[1]["angle"] == node[1]["angle"]+node[1]["step"] - circularDivision) and x[1]["level"] == node[1]["level"]]
            if (len(eastNodes) != 0 ): G.add_edge(node[0], eastNodes[0][0])


        # Find A Random Node
        print("============= Remove Nodes")
        visitedList = []
        currentNode = self.getRandomNode(G, visitedList)
        topLevelEdgeRemoved = [False]

        while len(visitedList) < G.number_of_nodes():
            neighborNodes = [x for x in G.neighbors(currentNode[0]) if not G.nodes(data=True)[x]["visited"]]
            if (len(neighborNodes) == 0):
                currentNode = self.getRandomNode(G, visitedList)
            else:
                if currentNode[1]["level"] == levelCount - 1:
                    if topLevelEdgeRemoved[0]:
                        topLevelEdgeRemoved[0] = True
                    else:
                        # Find South Node Edge and Remove it
                        for neighborNode in neighborNodes:
                            if G.nodes(data=True)[neighborNode]["level"] == currentNode[1]["level"] - 1:
                                G.remove_edge(neighborNode, currentNode[0])
                                G.nodes(data=True)[removedNode]["visited"] = True
                                currentNode = (neighborNode, G.nodes(data=True)[neighborNode])
                                break
                        topLevelEdgeRemoved[0] = True
                else:
                    removedNode = random.choice(neighborNodes)
                    G.remove_edge(currentNode[0], removedNode)
                    G.nodes(data=True)[removedNode]["visited"] = True
                    currentNode = (removedNode, G.nodes(data=True)[removedNode])