from room import Room
from player import Player
from world import World

import operator
import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)


opposite_direction = {"n": "s", "e": "w", "s": "n", "w": "e"}
def find_path(graph=None, origin_direction=None):
    if graph is None:
        graph = {}
    starting_room = player.current_room
    if not starting_room in graph:
        graph[starting_room] = {}
    path = []
    directions = player.current_room.get_exits()
    for direction in directions:
        if direction in graph[starting_room]:
            continue
        player.travel(direction)
        room = player.current_room
        graph[starting_room][direction] = room
        if not room in graph:
            graph[room] = {}
        graph[room][opposite_direction[direction]] = starting_room
        path += [direction] + find_path(graph) + [opposite_direction[direction]]
        player.travel(opposite_direction[direction])
    return path

traversal_path = find_path()
#print(traversal_path)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
