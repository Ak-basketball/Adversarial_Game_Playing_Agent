from isolation import Isolation
from collections import defaultdict, Counter

import pickle
import random

class Opening():
    def run(self):
        state = Isolation()
        num_rounds = 100
        book = defaultdict(Counter)
        for i in range(num_rounds):
            self.build_tree(state, book)
        opening_book = {k: max(v, key=v.get) for k, v in book.items()}
        with open("data.pickle", "wb") as f:
            pickle.dump(opening_book, f)
    
    def build_tree(self, state, book, depth = 2):
        if depth <= 0 or state.terminal_test():
            return -self.simulate(state)
        action = random.choice(state.actions())
        reward = self.build_tree(state.result(action), book, depth - 1)
        book[state][action] += reward
        return 0
    
    def simulate(self, state):
        player_id = state.ply_count % 2
        while not state.terminal_test():
            state = state.result(random.choice(state.actions()))
        return -1 if state.utility(player_id) < 0 else 1
