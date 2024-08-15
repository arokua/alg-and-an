# -------------------------------------------------------------------
# Maze tester with data generation.
# This is the entry point to run the program.
# Refer to usage() for exact format of input expected to the program.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


import sys
import time
import random
import pandas

from typing import List

from maze.util import Coordinates
from maze.maze import Maze
from maze.arrayMaze import ArrayMaze
from maze.graphMaze import GraphMaze

from generation.mazeGenerator import MazeGenerator
from generation.recurBackGenerator import RecurBackMazeGenerator


# this checks if Visualizer has been imported properly.
# if not, likely missing some packages, e.g., matplotlib.
# in that case, regardless of visualisation flag, we should set the canVisualise flag to False which will not call the visuslisation part.
# Flag set to false for quick testing
canVisualise = True
try:
	from maze.maze_viz import Visualizer
except:
	Visualizer = None
	canVisualise = False



def usage():
	"""
	Print help/usage message.
	"""

	# On Teaching servers, use 'python3'
	# On Windows, you may need to use 'python' instead of 'python3' to get this to work
	print('python3 mazeTester_dataGen.py', '<configuration file>')
	sys.exit(1)

def generate_maze_instance():
    # Randomly generate n and m between 4 and 125
    n = random.randint(4, 125)
    m = random.randint(4, 125)
    
    # Determine the number of entrances and exits between 1 and 4
	# To add more randomness, hav
    entrances_count = random.randint(1, 4)
    exits_count = random.randint(max(1, entrances_count-2), min(4, entrances_count+2))
    
    def generate_boundary_coordinate(max_row, max_col):
        # Generate a random boundary coordinate
        if random.choice([True, False]):
            return [random.choice([-1, max_row]), random.randint(0, max_col)]
        else:
            return [random.randint(0, max_row), random.choice([-1, max_col])]
    
    # Generate entrances and exits
    entrances = [generate_boundary_coordinate(n-1, m-1) for _ in range(entrances_count)]
    exits = [generate_boundary_coordinate(n-1, m-1) for _ in range(exits_count)]
    
    # Set visualise to false to prevent block
    visualise = False
    
    # Create the JSON object
    maze_json = {
        "rowNum": n,
        "colNum": m,
        "entrances": entrances,
        "exits": exits,
        "generator": "recur",
        "visualise": visualise
    }
    
    return maze_json

def generate_mazes(num_mazes=10):
    return [generate_maze_instance() for _ in range(num_mazes)]

#
# Main.
#
if __name__ == '__main__':
	# Fetch the command line arguments
	args = sys.argv

	# if len(args) != 2:
	# 	print('Incorrect number of arguments.')
	# 	usage()
	#Files to store run output of default structure, adj list and adj matrix
	runFileName="record.csv"
	recordDF=pandas.DataFrame(columns=["DataStruct","row","col","runTime"])
	structOfRuns=["array"]#,"inc-list","inc-mat"]
	# open configuration file		
	# fileName: str = args[1]
	# with open(fileName,"r") as configFile:
	# 	# use json parser
	# 	configDict = json.load(configFile)

	# 	# assign to variables storing various parameters
	# 	dsApproach: str = configDict['dataStructure']
	# 	rowNum: int = configDict['rowNum']
	# 	colNum: int = configDict['colNum']
	# 	entrances: List[List[int]] = configDict['entrances']
	# 	exits: List[List[int]] = configDict['exits']
	# 	genApproach: str = configDict['generator']
	# 	bVisualise: bool = configDict['visualise']

		#
		# Initialise maze object (which also selects which data structure implementation is used).
		#
	
	fileRun= 10
	configs=generate_mazes(fileRun) #Empty dict to populate structure
	for dsApproach in structOfRuns:
		for i in range(fileRun):
			maze: Maze = None
			rowNum=configs[i]['rowNum']
			colNum=configs[i]['colNum']
			entrances: List[List[int]]=configs[i]['entrances']
			exits: List[List[int]]=configs[i]['exits']
			genApproach=configs[i]["generator"]
			bVisualise: bool = configs[i]['visualise']
			# recordDF.loc[i]=[dsApproach,rowNum,colNum]
			if dsApproach == 'array':
				maze = ArrayMaze(rowNum, colNum)
			elif dsApproach == 'edge-list':
				maze = GraphMaze(rowNum, colNum, dsApproach)
			elif dsApproach == 'inc-mat':
				maze = GraphMaze(rowNum, colNum, dsApproach)
			else:
				print('Unknown data structure approach specified.')
				usage()

			# add the entraces and exits
			for [r,c] in entrances:
				maze.addEntrance(Coordinates(r, c))
			for [r,c] in exits:
				maze.addExit(Coordinates(r, c))

		
			#
			# Generate maze
			#
			generator: MazeGenerator = None
			if genApproach == 'recur':
				generator = RecurBackMazeGenerator()
			else:
				print('Unknown generator approach specified.')
				usage()


			# timer for generation
			startGenTime : float = time.perf_counter()

			generator.generateMaze(maze)

			# stop timer
			endGenTime: float = time.perf_counter()
			timeRan=endGenTime - startGenTime
			print(f'Generation took {timeRan:0.4f} seconds')

			# add/generate the entrances and exits
			generator.addEntrances(maze)
			generator.addExits(maze)

			#
			# Display maze.
			#
			if bVisualise and canVisualise:
				cellSize = 1
				visualiser = Visualizer(maze, cellSize) 
				visualiser.show_maze()
			
	#Print the first part of the df
	print(recordDF.head())
