from circular_graph import CircularGraph 
from visualizer import Visualizer
from generators.prims import Prims

BASE_RADIUS = 20
LEVEL_SIZE = 15
LEVEL_COUNT = 10
DIVISIONS = 48
WIDTH = 400
HEIGHT = 400

# Generate Emtpy Graph
circularGraphGenerator = CircularGraph(LEVEL_COUNT, DIVISIONS)
G = circularGraphGenerator.generate(BASE_RADIUS, LEVEL_SIZE)

# Apply Specific Algo to generate

Prims().generate(G, DIVISIONS, LEVEL_COUNT)

# Visualize

visualizer =  Visualizer(WIDTH, HEIGHT, LEVEL_COUNT, LEVEL_SIZE, DIVISIONS, BASE_RADIUS, "example.svg");
visualizer.visualize(G)