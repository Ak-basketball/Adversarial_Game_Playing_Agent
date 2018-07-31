import random

class Node():
    def __init__(self, state):
        self.state = state
        self.children = []
        self.parent = None
        self.action = None
        self.N = 0
        self.Q = 0
        
    def add_child(self, state, action):
        v1 = Node(state)
        v1.action = action
        self.children = self.children + [v1]
        
    def add_parent(self, state):
        v = Node(state)
        self.parent = v
