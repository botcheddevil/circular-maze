import cairo
import math
import networkx
import random

BASE_RADIUS = 20
LEVEL_SIZE = 15
LEVEL_COUNT = 10
DIVISIONS = 48
WIDTH = 400
HEIGHT = 400
centerX = WIDTH / 2
centerY = HEIGHT / 2
G = networkx.Graph()


def lineBetweenTwoNodes(context, levelPoints, node1, node2):
    context.set_source_rgba(0.95, 0.6, 0.3, 0.5)
    context.set_line_width(1.5)
    context.move_to(
        centerX + levelPoints[node1["level"]][node1["angle"]][0], centerY + levelPoints[node1["level"]][node1["angle"]][1])
    context.line_to(
        centerX + levelPoints[node2["level"]][node2["angle"]][0], centerY + levelPoints[node2["level"]][node2["angle"]][1])
    context.stroke()


def PointsInCircum(r, n=100):
    pi = math.pi
    return [(math.cos(2*pi/n*x)*r, math.sin(2*pi/n*x)*r) for x in range(0, n+1)]


def lineBetweenTwoLevelsAtAngle(context, levelPoints, level1, level2, angle):
    context.set_source_rgba(0.3, 0.6, 0.9, 0.8)
    context.set_line_width(1.5)
    context.move_to(
        centerX + levelPoints[level1][angle][0], centerY + levelPoints[level1][angle][1])
    context.line_to(
        centerX + levelPoints[level2][angle][0], centerY + levelPoints[level2][angle][1])
    context.stroke()

    # context.set_source_rgb(1, 0, 0)
    # context.set_font_size(3)
    # context.select_font_face("Arial",
    #                          cairo.FONT_SLANT_NORMAL,
    #                          cairo.FONT_WEIGHT_NORMAL)
    # context.move_to(
    #     centerX + levelPoints[level1][angle][0], centerY + levelPoints[level1][angle][1])
    # context.show_text(str(angle) + "," + str(level1))
    # context.move_to(
    #     centerX + levelPoints[level2][angle][0], centerY + levelPoints[level2][angle][1])
    # context.show_text(str(angle) + "," + str(level2))


def writeValueOnNode(context, levelPoints, node, value):
    context.set_source_rgb(1, 0, 0)
    context.set_font_size(4)
    context.select_font_face("Arial",
                             cairo.FONT_SLANT_NORMAL,
                             cairo.FONT_WEIGHT_NORMAL)
    context.move_to(
        centerX + levelPoints[node["level"]][node["angle"]][0], centerY + levelPoints[node["level"]][node["angle"]][1])
    context.show_text(str(value))    

def arcBetweenTwoAnglesAtLevel(context, angle1, angle2, level, divisions):
    context.set_source_rgba(0.3, 0.6, 0.9, 0.8)
    context.set_line_width(1.5)

    radius = BASE_RADIUS + (LEVEL_SIZE*level)
    angle1Radians = math.radians(360*angle1/divisions)
    angle2Radians = math.radians(360*angle2/divisions)

    context.arc(centerX, centerY, radius, angle1Radians, angle2Radians)
    context.stroke()


def dotAtCenterOfCell(levelPoints, cell):
    context.set_line_width(1)
    if cell[2] % 2 == 0:
        context.set_source_rgba(0.9, 0.1, 0.4, 0.8)
    else:
        context.set_source_rgba(0.2, 0.8, 0.8, 0.9)

    midX = (levelPoints[cell[0]][cell[2]][0] +
            levelPoints[cell[1]][cell[2]][0]) / 2
    midY = (levelPoints[cell[0]][cell[2]][1] +
            levelPoints[cell[1]][cell[2]][1]) / 2

    # context.set_source_rgb(0.5, 0.1, 0)
    # context.set_font_size(3)
    # context.select_font_face("Arial",
    #                          cairo.FONT_SLANT_NORMAL,
    #                          cairo.FONT_WEIGHT_NORMAL)
    # context.move_to(centerX + midX, centerY + midY)
    # context.show_text(str(cell[2]))

    # context.arc(centerX + midX,
    #             centerY + midY,
    #             0.8, math.radians(0), math.radians(360))
    context.stroke()


with cairo.SVGSurface("example.svg", WIDTH, HEIGHT) as surface:
    context = cairo.Context(surface)
    levelPoints = []
    levelMidPoints = []
    for x in range(LEVEL_COUNT):
        radius = BASE_RADIUS + (LEVEL_SIZE*x)
        levelPoints.append(PointsInCircum(radius, DIVISIONS))
        levelMidPoints.append(PointsInCircum(radius, DIVISIONS * 2))
        # context.arc(centerX, centerY, radius,
        #             math.radians(0), math.radians(360))
        # context.set_source_rgba(1, 0.2, 0.2, 0.1)
        # context.set_line_width(1)
        # context.stroke()

    dynaDivisionsRange = list(range(DIVISIONS))
    cells = []
    step = 1
    for x in range(LEVEL_COUNT-1, 0, -1):
        radius = BASE_RADIUS + (LEVEL_SIZE*x)
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
            # lineBetweenTwoLevelsAtAngle(context, levelPoints, x-1, x, y)

    G.add_nodes_from(cells)
    print("Total Number of nodes " + str(G.number_of_nodes()))
    for node in G.nodes(data=True):

        # Add North and South
        # find North Node
        northNodes = [x for x in G.nodes(data=True)  if x[1]["angle"] == node[1]["angle"] and x[1]["level"] == node[1]["level"]+1]
        if (len(northNodes) != 0):
            G.add_edge(node[0], northNodes[0][0])

        # Add East
        eastNodes = [x for x in G.nodes(data=True)  if (x[1]["angle"] == node[1]["angle"]+node[1]["step"] or x[1]["angle"] == node[1]["angle"]+node[1]["step"] - DIVISIONS) and x[1]["level"] == node[1]["level"]]
        print(eastNodes)
        if (len(eastNodes) != 0 ):
            G.add_edge(node[0], eastNodes[0][0])


    print("Total Number of edges " + str(G.number_of_edges()))

    # for edge in G.edges:
        # print(edge)
        # print(G.nodes[edge[0]])
        # lineBetweenTwoNodes(context, levelPoints, G.nodes[edge[0]], G.nodes[edge[1]])


    # Find A Random Node

    currentNodeId = random.randrange(0,len(G.nodes))
    currentNode = G.nodes(data=True)[currentNodeId]
    currentNode["visited"] = True;
    visited = 1
    print(currentNodeId)
    print(currentNode)
    while visited < len(G.nodes):
        
        neighborNodes = [x for x in G.neighbors(currentNodeId) if not G.nodes(data=True)[x]["visited"]]
        if (len(neighborNodes) == 0):
            print("No neighbors found")
            currentNodeId = random.randrange(1,len(G.nodes)+1)
        else:
            currentNeighborNode = neighborNodes[random.randrange(0, len(neighborNodes))]
            print(currentNeighborNode)
            for neighborNode in neighborNodes:
                if neighborNode != currentNeighborNode:
                    G.remove_edge(currentNodeId, neighborNode)
            currentNodeId = currentNeighborNode
        print(currentNodeId)
        currentNode = G.nodes(data=True)[currentNodeId]
        if currentNode["visited"] == False:
            currentNode["visited"] = True;
            visited += 1
            writeValueOnNode(context, levelPoints, currentNode, visited)



    for edge in G.edges:
        if G.nodes[edge[0]]["angle"] == G.nodes[edge[1]]["angle"]:
            lineBetweenTwoLevelsAtAngle(context, levelPoints, G.nodes[edge[0]]["level"], G.nodes[edge[1]]["level"], G.nodes[edge[1]]["angle"])
        else:
            arcBetweenTwoAnglesAtLevel(context, G.nodes[edge[0]]["angle"], G.nodes[edge[1]]["angle"], G.nodes[edge[0]]["level"], DIVISIONS)