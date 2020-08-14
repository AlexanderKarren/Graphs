from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "projects/adventure/maps/test_line.txt"
# map_file = "projects/adventure/maps/test_cross.txt"
# map_file = "projects/adventure/maps/test_loop.txt"
# map_file = "projects/adventure/maps/test_loop_fork.txt"
map_file = "projects/adventure/maps/main_maze.txt"

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

done_looking = False
def auto_traverse_recursive(cur_room, visited=None):
    global done_looking
    if visited is None:
        visited = set()

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
        if len(visited) >= len(world.rooms):
            done_looking = True
        if len(valid_exits) < 1 and done_looking is False:
            valid_exits = exits

    # print(cur_room, traversal_path)
    for next_dir in valid_exits:
        if next_dir == 'n':
            traversal_path.append(next_dir)
            if done_looking is False:
                auto_traverse_recursive(cur_room.n_to, visited)
        elif next_dir == 'e':
            traversal_path.append(next_dir)
            if done_looking is False:
                auto_traverse_recursive(cur_room.e_to, visited)
        elif next_dir == 's':
            traversal_path.append(next_dir)
            if done_looking is False:
                auto_traverse_recursive(cur_room.s_to, visited)
        elif next_dir == 'w':
            traversal_path.append(next_dir)
            if done_looking is False:
                auto_traverse_recursive(cur_room.w_to, visited)

def auto_traverse(cur_room):
    # we should never come back to explored
    explored = set()
    # we can come back to visited, but those paths won't be prioritized
    visited = set()
    done_looking = False
    last_unexplored = 0
    backtrack_array = []
    
    while done_looking is False:
        visited.add(cur_room.id)
        # print(cur_room, traversal_path)
        # print("total rooms:", len(world.rooms), "visited:", len(visited))
        exits = cur_room.get_exits()
        valid_exits = []

        last_direction = [None]
        if len(traversal_path) >= 1:
            last_direction = traversal_path[-1]

        for exit in exits:
            if exit == 'n' and cur_room.n_to.id not in explored and last_direction != 's':
                valid_exits.append(exit)
            elif exit == 'e' and cur_room.e_to.id not in explored and last_direction != 'w':
                valid_exits.append(exit)
            elif exit == 's' and cur_room.s_to.id not in explored and last_direction != 'n':
                valid_exits.append(exit)
            elif exit == 'w' and cur_room.w_to.id not in explored and last_direction != 'e':
                valid_exits.append(exit)

        dir_index = 0
        for i in range(len(valid_exits)):
            if valid_exits[i] == 'n' and cur_room.n_to.id not in visited:
                dir_index = i
            elif valid_exits[i] == 'e' and cur_room.e_to.id not in visited:
                dir_index = i
            elif valid_exits[i] == 's' and cur_room.s_to.id not in visited:
                dir_index = i
            elif valid_exits[i] == 'w' and cur_room.w_to.id not in visited:
                dir_index = i

        if len(valid_exits) <= 1:
            explored.add(cur_room.id)
        
        if cur_room.id in explored:
            last_unexplored += 1
        else:
            last_unexplored = 0

        # print("last unexplored:", last_unexplored)

        if len(valid_exits) < 1 and done_looking is False and len(backtrack_array) < 1:
            valid_exits = exits[random.randint(0, len(exits) - 1)]
            # valid_exits = exits
            # backtrack_array = traversal_path[-last_unexplored:]
            # backtrack_array.reverse()
            # print(backtrack_array)
            # for i in range(len(backtrack_array)):
            #     if backtrack_array[i] == 'n':
            #         backtrack_array[i] = 's'
            #     elif backtrack_array[i] == 'e':
            #         backtrack_array[i] = 'w'
            #     elif backtrack_array[i] == 's':
            #         backtrack_array[i] = 'n'
            #     elif backtrack_array[i] == 'w':
            #         backtrack_array[i] = 'e'

        if backtrack_array:
            valid_exits = [backtrack_array.pop(0)]

        if len(explored) >= len(world.rooms):
                done_looking = True
            
        if valid_exits:
            if valid_exits[dir_index] == 'n':
                traversal_path.append('n')
                cur_room = cur_room.n_to
            elif valid_exits[dir_index] == 'e':
                traversal_path.append('e')
                cur_room = cur_room.e_to
            elif valid_exits[dir_index] == 's':
                traversal_path.append('s')
                cur_room = cur_room.s_to
            elif valid_exits[dir_index] == 'w':
                traversal_path.append('w')
                cur_room = cur_room.w_to
        

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
