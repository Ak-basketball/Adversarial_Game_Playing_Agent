def expand(self, node, frontier):
        for i in node.state.actions():
            new_node = Node()
            new_node.state = node.state.result(i)
            new_node.parents = new_node.parents + [node] + node.parents
            outcome = self.simulate(new_node)
            new_node = self.update(new_node, outcome)
            frontier = frontier + new_node
    
    def select(self, frontier):
        best = random.choice(frontier)
        best.score = best.num_sim + best.not_weight
        for i in frontier:
            i.score = i.not_weight + i.num_sim
            if i.score > best.score:
                 best = i
        for i in frontier:
            if i != best:
                i.not_weight = i.not_weight + 1
        return best
    
    def simulate(self, node):
        player_id = node.state.ply_count % 2
        while not node.state.terminal_test():
            node.state = node.state.result(random.choice(node.state.actions()))
        return -1 if node.state.utility(player_id) < 0 else 1
    
    def update(self, original, result):
        if result >= 0:
            for i in original.parents:
                i.num_win = i.num_win + 1
            original.num_win = original.num_win + 1
        for i in original.parents:
                i.num_sim = i.num_sim + 1
        original.num_sim = original.num_sim + 1
        return original
