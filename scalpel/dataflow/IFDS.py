import networkx as nx 


class IFDS():
    """
    There are four different flow functions
    1. Normal： propgates intra-procedural flows along non-call nodes
    2. Call： propagates from caller  to callee
    3. Return：propagates from callee to caller
    4. Call-to-return: propagates intra-procedural flows over call nodes
       # most often is simply the identity function.
    source: IFDS on-the-fly algorithm by Prof. Eric Bodden. https://www.youtube.com/watch?v=beE3zPnxvkE&t=745s

    """
    def __init__(self) -> None:
        self.domains = set()
        self.i_cfgs = {}  # flattened 
        self.super_graph = nx.DiGraph()
        pass

    def call_to_return_site(self):
        pass 
    
    def call_to_start(self):
        pass 
    
    def exit_to_return_site(self):
        pass 
