def hash_list(ancestors):
    ancestry = {}
    for i in range(len(ancestors)):
        if ancestry.get(ancestors[i][1]):
            ancestry.get(ancestors[i][1]).add(ancestors[i][0])
        else:
            ancestry.update({ancestors[i][1]: set()})
            ancestry.get(ancestors[i][1]).add(ancestors[i][0])

    return ancestry

def earliest_ancestor(ancestors, starting_node, q=None, gen=0):
    if q is None:
        q = list()
    ancestry = hash_list(ancestors)
    if ancestry.get(starting_node) is None:
        q.append((starting_node, gen))
    # print(ancestry)
    # print(starting_node, q, ancestry.get(starting_node))
    
    if ancestry.get(starting_node):
        for ancestor in ancestry.get(starting_node):
           earliest_ancestor(ancestors, ancestor, q, gen + 1)

    generations = set()
    for i in range(len(q)):
        generations.add(q[i][1])

    # print("generations:", generations)
    index = 0
    lowest_value = 100
    if len(generations) == 1:
        for i in range(len(q)):
            if q[i][0] < lowest_value:
                lowest_value = q[i][0]
                index = i
    if 0 in generations:
        return -1

    return q[index][0]


test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
print(earliest_ancestor(test_ancestors, 1)) # 10
print(earliest_ancestor(test_ancestors, 2)) # -1
print(earliest_ancestor(test_ancestors, 3)) # 10
print(earliest_ancestor(test_ancestors, 4)) # -1
print(earliest_ancestor(test_ancestors, 5)) # 4
print(earliest_ancestor(test_ancestors, 6)) # 10
print(earliest_ancestor(test_ancestors, 7)) # 4
print(earliest_ancestor(test_ancestors, 8)) # 4
print(earliest_ancestor(test_ancestors, 9)) # 4
print(earliest_ancestor(test_ancestors, 10)) # -1
print(earliest_ancestor(test_ancestors, 11)) # -1