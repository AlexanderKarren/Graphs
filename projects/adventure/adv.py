from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "projects/adventure/maps/test_line.txt"
map_file = "projects/adventure/maps/test_cross.txt"
# map_file = "projects/adventure/maps/test_loop.txt"
# map_file = "projects/adventure/maps/test_loop_fork.txt"
# map_file = "projects/adventure/maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

def auto_traverse(cur_room, visited=None):
    if visited is None:
        visited = set()
    print("# of rooms:", len(world.rooms), "# of visited:", len(visited))

    exits = cur_room.get_exits()
    valid_exits = []

    last_direction = [None]
    if traversal_path:
        last_direction = traversal_path[-1]

    for i in range(len(exits)):
        if exits[i] == 'n' and cur_room.n_to.id not in visited and last_direction != 's':
            valid_exits.append(exits[i])
        elif exits[i] == 'e' and cur_room.e_to.id not in visited and last_direction != 'w':
            valid_exits.append(exits[i])
        elif exits[i] == 's' and cur_room.s_to.id not in visited and last_direction != 'n':
            valid_exits.append(exits[i])
        elif exits[i] == 'w' and cur_room.w_to.id not in visited and last_direction != 'e':
            valid_exits.append(exits[i])

    if len(valid_exits) <= 1:
        visited.add(cur_room.id)
        if len(valid_exits) < 1 and len(visited) < len(world.rooms):
            valid_exits = exits

    print(cur_room, traversal_path)
    for next_dir in valid_exits:
        if next_dir == 'n':
            traversal_path.append(next_dir)
            auto_traverse(cur_room.n_to, visited)
        elif next_dir == 'e':
            traversal_path.append(next_dir)
            auto_traverse(cur_room.e_to, visited)
        elif next_dir == 's':
            traversal_path.append(next_dir)
            auto_traverse(cur_room.s_to, visited)
        elif next_dir == 'w':
            traversal_path.append(next_dir)
            auto_traverse(cur_room.w_to, visited)

auto_traverse(player.current_room)

print(traversal_path)

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
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
