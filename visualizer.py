
import cairo
import math


class Visualizer:
    def __init__(self, width, height, levelCount, levelSize, circularDivisions, baseRadius, svgFileName):
        self.levelCount = levelCount
        self.circularDivisions = circularDivisions
        self.centerX = width / 2
        self.centerY = height / 2
        self.baseRadius = baseRadius
        self.levelSize = levelSize

        surface = cairo.SVGSurface(svgFileName, width, height)
        self.context = cairo.Context(surface)
        self.levelPoints = []
        self.levelMidPoints = []

        for x in range(levelCount):
            radius = baseRadius + (levelSize*x)
            self.levelPoints.append(self.pointsInCircum(radius, circularDivisions))
            self.levelMidPoints.append(self.pointsInCircum(radius, circularDivisions * 2))

            # Draw concentric circle guides
            self.context.arc(self.centerX, self.centerY, radius, math.radians(0), math.radians(360))
            self.context.set_source_rgba(1, 0.2, 0.2, 0.1)
            self.context.set_line_width(1)
            self.context.stroke()

        for level in range(levelCount):
            for angle in range(circularDivisions):
                self.showAtAngleLevel(angle, level, str(angle) + "," + str(level))

    def lineBetweenTwoLevelsAtAngle(self, levelPoints, level1, level2, angle):
        self.context.new_path()
        self.context.set_source_rgba(0.3, 0.6, 0.9, 0.9)
        self.context.set_line_width(1.5)
        self.context.set_line_cap(cairo.LINE_CAP_ROUND)
        print(levelPoints[level1][angle])
        print(levelPoints[level2][angle])
        self.context.move_to(
            self.centerX + levelPoints[level1][angle][0], self.centerY + levelPoints[level1][angle][1])
        self.context.line_to(
            self.centerX + levelPoints[level2][angle][0], self.centerY + levelPoints[level2][angle][1])
        self.context.stroke()


    def arcBetweenTwoAnglesAtLevel(self, angle1, angle2, step, level, divisions):
        self.context.new_path()
        self.context.set_source_rgba(0.3, 0.6, 0.9, 0.8)
        self.context.set_line_width(1.5)

        if abs(angle1 - angle2) != step:
            angle1 = max(angle1, angle2)
        else:
            angle1 = min(angle1, angle2)

        angle2 = angle1 + step
        radius = self.baseRadius + (self.levelSize*level)
        angle1Radians = math.radians(360*angle1/divisions)
        angle2Radians = math.radians(360*angle2/divisions)

        self.context.set_line_cap(cairo.LINE_CAP_ROUND)
        self.context.arc(self.centerX, self.centerY, radius, angle1Radians, angle2Radians)
        self.context.stroke()
 

    def pointsInCircum(self, r, n=100):
        pi = math.pi
        return [(math.cos(2*pi/n*x)*r, math.sin(2*pi/n*x)*r) for x in range(0, n+1)]
    

    def visualize(self, G):
        for edge in G.edges:
            if G.nodes[edge[0]]["angle"] == G.nodes[edge[1]]["angle"]:
                print(G.nodes[edge[1]]["angle"], "Same angle", G.nodes[edge[0]]["level"], G.nodes[edge[1]]["level"])
                self.lineBetweenTwoLevelsAtAngle(self.levelPoints, G.nodes[edge[0]]["level"], G.nodes[edge[1]]["level"], G.nodes[edge[1]]["angle"])
            
            if G.nodes[edge[0]]["level"] == G.nodes[edge[1]]["level"]:
                print(G.nodes[edge[1]]["level"], "Same level", G.nodes[edge[0]]["angle"], G.nodes[edge[1]]["angle"])
                self.arcBetweenTwoAnglesAtLevel(G.nodes[edge[0]]["angle"], G.nodes[edge[1]]["angle"], G.nodes[edge[0]]["step"], G.nodes[edge[0]]["level"], self.circularDivisions)


    #  Methods for writting values on grid

    def writeValueOnNode(self, node, value):
        self.context.set_source_rgb(1, 0, 0)
        self.context.set_font_size(4)
        self.context.select_font_face("Arial",
                                cairo.FONT_SLANT_NORMAL,
                                cairo.FONT_WEIGHT_NORMAL)
        self.context.move_to(
            self.centerX + self.levelPoints[node["level"]][node["angle"]][0], self.centerY + self.levelPoints[node["level"]][node["angle"]][1])
        self.context.show_text(str(value))   


    def showAtAngleLevel(self, angle, level, str, r=0, g=0.7, b=0.5 ):
        self.context.set_source_rgb(r, b, g)
        self.context.set_font_size(3)
        self.context.select_font_face("Arial",
                                 cairo.FONT_SLANT_NORMAL,
                                 cairo.FONT_WEIGHT_NORMAL)
        self.context.move_to(
            self.centerX + self.levelPoints[level][angle][0], self.centerY + self.levelPoints[level][angle][1])
        self.context.show_text(str)


    #  Methods for Visualizing paths

    def dotAtCenterOfCell(self, levelPoints, cell):
        self.context.set_line_width(1)
        if cell[2] % 2 == 0:
            self.context.set_source_rgba(0.9, 0.1, 0.4, 0.8)
        else:
            self.context.set_source_rgba(0.2, 0.8, 0.8, 0.9)

        midX = (levelPoints[cell[0]][cell[2]][0] +
                levelPoints[cell[1]][cell[2]][0]) / 2
        midY = (levelPoints[cell[0]][cell[2]][1] +
                levelPoints[cell[1]][cell[2]][1]) / 2

        self.context.stroke()


    def lineBetweenTwoNodes(self, levelPoints, node1, node2):
        self.context.set_source_rgba(0.95, 0.6, 0.3, 0.5)
        self.context.set_line_width(1.5)
        self.context.move_to(
            self.centerX + levelPoints[node1["level"]][node1["angle"]][0], self.centerY + levelPoints[node1["level"]][node1["angle"]][1])
        self.context.line_to(
            self.centerX + levelPoints[node2["level"]][node2["angle"]][0], self.centerY + levelPoints[node2["level"]][node2["angle"]][1])
        self.context.stroke()