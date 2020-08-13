import random
import time
from queue import Queue

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        # If user tries to be friends with themselves:
        if user_id == friend_id:
            return False
        # If user-friend connection already exists
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            return False
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)
            return True

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph_linear(self, num_users, avg_friendships):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        for i in range(0, num_users):
            self.add_user(f"User {i}")

        target_friendships = (num_users * avg_friendships)
        total_friendships = 0
        collisions = 0

        while total_friendships < target_friendships:
            user_id = random.randint(1, self.last_id)
            friend_id = random.randint(1, self.last_id)

            if self.add_friendship(user_id, friend_id):
                total_friendships += 2
            else:
                collisions += 1

        print(f"Collisions: {collisions}")

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        for i in range(0, num_users):
            self.add_user(f"User {i}")

        # Create friendships
        # generate all possible friendship combinations
        possible_friendships = []

        # avoid duplicates by ensuring first num < second num
        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible_friendships.append((user_id, friend_id))

        # shuffle friendships
        random.shuffle(possible_friendships)

        # create friendships from the first N num of pairs of the list
        # N -> num_users * avg_friendships // 2
        N = num_users * avg_friendships // 2
        for i in range(N):
            friendship = possible_friendships[i]
            user_id, friend_id = friendship
            self.add_friendship(user_id, friend_id)


    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        q = []
        q.insert(0, [user_id])
        visited = {}  # Note that this is a dictionary, not a set
        
        while len(q) > 0:
            # print(q)
            path = q.pop()

            user = path[-1]

            if user not in visited:
                visited.update({user: path})
                for friend in self.friendships.get(user):
                    new_path = path.copy()

                    new_path.append(friend)

                    q.insert(0, new_path)

        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    start_time = time.time()
    sg.populate_graph_linear(10, 5)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    end_time = time.time()
    print(connections)
    print(f"Runtime: {end_time - start_time}s")
