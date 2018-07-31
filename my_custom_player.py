from sample_players import DataPlayer
from node import Node

import random
import math

class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only *required* method. You can modify
    the interface for get_action by adding named parameters with default
    values, but the function MUST remain compatible with the default
    interface.

    **********************************************************************
    NOTES:
    - You should **ONLY** call methods defined on your agent class during
      search; do **NOT** add or call functions outside the player class.
      The isolation library wraps each method of this class to interrupt
      search when the time limit expires, but the wrapper only affects
      methods defined on this class.

    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.
    **********************************************************************
    """
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller is responsible for
        cutting off the function after the search time limit has expired. 

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)
        
        #max_num = 10
        if state.ply_count < 2:
            self.queue.put(self.data[state])
        else:
            self.uct_search(state)
            '''for i in range(max_num):
                self.queue.put(self.alpha_beta_search(state, depth=i))'''
            
            
            
    '''def alpha_beta_search(self, gameState, depth):
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
    '''
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
    '''    
    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)'''
