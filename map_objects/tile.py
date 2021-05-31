class Tile:
    def __init__(self, blocked, blocked_sight = None):
        self.blocked = blocked
        self.explored = False
        
        if blocked_sight is None:
            block_sight = blocked

        self.block_sight = block_sight