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
# Returns a tuple:
#   0: the shortest route hitting every room
#   1: the route to get back to the start from the ending room
def find_path(graph=None):
    if graph is None:
        graph = {}
    starting_room = player.current_room
    if not starting_room in graph:
        graph[starting_room] = {}
    path = []
    paths = {}
    backtrack = {}
    directions = player.current_room.get_exits()
    for direction in directions:
        if direction in graph[starting_room]:
            # Skip if we've already been down this path
            continue
        player.travel(direction)
        room = player.current_room

        # Add the connections to the graph both ways
        graph[starting_room][direction] = room
        if not room in graph:
            graph[room] = {}
        graph[room][opposite_direction[direction]] = starting_room
        
        found_path = find_path(graph)
        paths[direction] = [direction] + found_path[0]
        backtrack[direction] = found_path[1] + [opposite_direction[direction]]
        player.travel(opposite_direction[direction])

    # Travel down all of the shorter routes first, backtracking to the start,
    # then go down the longest route without backtracking since that's the end
    if len(backtrack.keys()) > 0:
        # Find the route with the longest backtrack
        longest_direction = max(backtrack.keys(), key=(lambda k: backtrack[k]))
        for direction in paths:
            # Backtrack through all of the shorter routes
            if direction == longest_direction:
                continue
            path += paths[direction]
            if direction in backtrack:
                path += backtrack[direction]
        # Don't backtrack back the longest route
        path += paths[longest_direction]
        return (path, backtrack[longest_direction])

    return (path, [])

traversal_path = find_path()[0]
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
