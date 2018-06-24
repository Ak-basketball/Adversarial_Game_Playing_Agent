    def alpha_beta_search(self, gameState, depth):
        def min_value(gameState, alpha, beta, depth, action):
            if gameState.terminal_test():
                return gameState.utility(0)
            if depth <= 0: return self.score(gameState)
            v = float("inf")
            for a in gameState.actions():
                v = min(v, max_value(gameState.result(a), alpha, beta, depth-1, action))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v
        
        def max_value(gameState, alpha, beta, depth, action):
            if gameState.terminal_test():
                return gameState.utility(0)
            if depth <= 0: return self.score(gameState)
            v = float("-inf")
            for a in gameState.actions():
                v = max(v, min_value(gameState.result(a), alpha, beta, depth-1, action))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v
        alpha = float("-inf")
        beta = float("inf")
        best_score = float("-inf")
        best_move = None
        for a in gameState.actions():
            v = min_value(gameState.result(a), alpha, beta, depth-1, a)
            alpha = max(alpha, v)
            if v > best_score:
                best_score = v
                best_move = a
        return best_move
    
    
    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)
        
        
        
    def run(self):
        state = Isolation()
        num_rounds = 100
        from collections import defaultdict, Counter
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
        
    for i in range(max_depth):
                self.queue.put(self.alpha_beta_search(state, depth=i))
