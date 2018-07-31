    if state.ply_count < 2:
            self.queue.put(self.data[state])
    else:
            self.uct_search(state)
        
    def uct_search(self, state):
        v0 = Node(state)
        d = 0
        while True:
            v1 = self.tree(v0)
            d = d + self.default(v1.state)
            v1 = self.backup(v1, d)
            best = self.best_child(v0, 0)
            action = None
            for i in v0.state.actions():
                if v0.state.result(i) == best.state:
                    action = i
            self.queue.put(i)
        
    def tree(self, v):
        while not v.state.terminal_test():
            if len(v.state.actions()) > 0:
                return self.expand(v)
            else:
                v = self.best_child(v, 1 / math.sqrt(2))
        return v
    
    def expand(self, v):
        action = random.choice(v.state.actions())
        v1 = Node(v.state.result(action))
        v.add_child(v1.state, action)
        v1.add_parent(v.state)
        return v1
    
    def default(self, state):
        player_id = state.ply_count % 2
        while not state.terminal_test():
            action = random.choice(state.actions())
            state = state.result(action)
        return 0 if state.utility(player_id) < 0 else 1
    
    def best_child(self, v, c):
        values = []
        for i in v.children:
            values = values + [(i.Q/i.N) + (c * math.sqrt(2 * math.log(v.N)/i.N))]
        best = max(values)
        index = values.index(best)
        return v.children[index]
    
    def backup(self, v, reward):
        while v.parent is not None:
            v.N = v.N + 1
            v.Q = v.Q + reward
            reward = -reward
            v = v.parent
        return v
