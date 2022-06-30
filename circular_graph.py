import networkx
import math

class CircularGraph:
    def __init__(self, levelCount, circularDivisions):
        self.circularDivisions = circularDivisions
        self.levelCount = levelCount
        self.G = networkx.Graph()

    
    def generate(self, baseRadius =20, levelSize=15):
        dynaDivisionsRange = list(range(self.circularDivisions))
        cells = []
        step = 1
        for x in range(self.levelCount, 0, -1):
            radius = baseRadius + (levelSize*x)
            circumference = math.pi * radius
            arclength = circumference / len(dynaDivisionsRange)

            if (arclength < 7):
                dynaDivisionsRange = dynaDivisionsRange[::2]
                print(dynaDivisionsRange)
                step *= 2

            for idx, y in enumerate(dynaDivisionsRange):
                cells.append(
                    (len(cells)+1, {"level": x-1, "angle": y, "step": step, "visited": False})
                )

        self.G.add_nodes_from(cells)
        return self.G






    #             print(len(G.nodes(data=True)))

    #     while len(visitedList) < len(G.nodes):
    #         print(currentNodeId, currentNode)
    #         neighborNodes = [x for x in G.neighbors(currentNodeId) if not G.nodes(data=True)[x]["visited"]]
    #         if (len(neighborNodes) == 0):
    #             print("No neighbors found")
    #             print("Visited", len(visitedList))
    #             currentNode, currentNodeId = self.getRandomNode(G, visitedList)
    #         else:
    #             print("Neighbors found", neighborNodes)
    #             IgnoreNeighborNode = self.getIgnoreNeighborNode(G, neighborNodes, currentNode, levelCount, topLevelEdgeRemoved)
    #             for neighborNode in neighborNodes:
    #                 if neighborNode != IgnoreNeighborNode:
    #                     print("Removed Edge", (currentNodeId, neighborNode))
    #                     G.remove_edge(currentNodeId, neighborNode)
    #             if IgnoreNeighborNode!= 0:
    #                 currentNodeId = IgnoreNeighborNode                
    #             else:
    #                 r1 = [i for i in range(1,len(G.nodes)+1) if i not in visitedList]
    #                 currentNodeId = random.choice(r1)

    #         visitedList.append(currentNodeId)
    #         currentNode = G.nodes(data=True)[currentNodeId]
    #         if currentNode["visited"] == False:
    #             currentNode["visited"] = True

    # def getRandomNode(self, G, visitedList):
    #     currentNodeId = random.choice([i for i in range(1,len(G.nodes)+1) if i not in visitedList])
    #     currentNode = G.nodes(data=True)[currentNodeId]
    #     currentNode["visited"] = True
    #     visitedList.append(currentNodeId)
    #     return currentNode, currentNodeId

    # def getIgnoreNeighborNode(self, G, neighborNodes, currentNode, levelCount, topLevelEdgeRemoved):
    #     print(currentNode, neighborNodes, topLevelEdgeRemoved)
    #     if currentNode["level"] == levelCount - 1:
    #         if topLevelEdgeRemoved[0]:
    #             neighborNodes = [x for x in neighborNodes if G.nodes(data=True)[x]["level"] != levelCount-1]
    #         else:
    #             neighborNodes = [x for x in neighborNodes if G.nodes(data=True)[x]["level"] != levelCount-1]
    #             topLevelEdgeRemoved[0] = True
    #     print("Number of neighborNodes",len(neighborNodes))
    #     if len(neighborNodes) == 0: return 0
    #     return neighborNodes[random.randrange(0, len(neighborNodes))]