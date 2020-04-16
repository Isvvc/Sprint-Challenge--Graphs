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
map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
#map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)


def find_shortest_path():
    opposite_direction = {"n": "s", "e": "w", "s": "n", "w": "e"}

    # Starting with test_loop, where there are no forks after the first
    # For each direction, see how long it takes to get to the end and then get back
    paths = {}
    repeated_rooms = {}
    starting_room = player.current_room
    for exit in player.current_room.get_exits():
        print(exit)
        rooms = [player.current_room.id]
        path = [exit]
        rooms.append(player.current_room)
        player.travel(exit)

        # Since with test_loop we know there are no more forks,
        # keep going forward until you reach the end
        forward = player.current_room.get_exits()[0]
        while forward is not None:
            print(forward)
            player.travel(forward)
            path.append(forward)

            room_id = player.current_room.id
            if room_id in rooms:
                # You've looped back
                # Go back to start from there
                return_from_room = rooms.index(room_id)
                forward = None
                break
            else:
                rooms.append(room_id)

            directions = player.current_room.get_exits()
            
            if opposite_direction[forward] in directions:
                directions.remove(opposite_direction[forward])
            if len(directions) == 0:
                # You've reached the end of a path
                # Turn around right here
                return_from_room = len(rooms) - 1
                forward = None
                break
            else:
                forward = directions[0]

        # Return to start
        player.current_room = starting_room
        print("reset")
        if return_from_room > 0:
            path += path[return_from_room - 1::-1]
        paths[exit] = path
        repeated_rooms[exit] = return_from_room
        

    path = []
    #longest_direction = max(repeated_rooms, key=operator.itemgetter(1))[0]
    longest_direction = max(repeated_rooms.keys(), key=(lambda k: repeated_rooms[k]))
    for direction in paths:
        if direction == longest_direction:
            continue
        path += paths[direction]
    path += paths[longest_direction][:-repeated_rooms[direction]]
    return path

print(find_shortest_path())
traversal_path = []



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
