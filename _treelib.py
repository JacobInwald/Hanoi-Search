import numpy as np


class state:

    def __init__(self, locs, max, min, prev_state):
        self.n_rings = len(locs)   # number of rings, indexed from 1
        self.n_poles = len(max)         # number of poles, inderced from 0
        self.locs = locs      # The location of each ring
                                        # i.e {1:0, 2:0, 3:0}
        self.max = max                  # The maximum ring on each pole
                                        # i.e {0:3, 1:-1, 2:-1}
        self.min = min                  # The minimum ring on each pole
                                        # i.e {0:1, 0:-1, 0:-1}
        self.p = prev_state             # state that generated this one
        self.id = self.get_id()         # generate id of state

        if self.p:                      # increment path cost
            self.g = prev_state.g + 1
        else:
            self.g = 0
        self.f = self.h() + self.g      # calculates f(n)

    def get_id(self):
        # encodes the states to a base num_poles integer, with num_rings
        # digits
        # (self.n_poles ^ ring-1) * self.locs[ring]
        return sum([((self.n_poles) ** i) * self.locs[i+1]
                    for i in range(self.n_rings)])

    def goal_check(self):
        # checks if the state is a goal state
        return self.id == (self.n_poles**self.n_rings - 1)

    def h(self):
        # uses difference of ids, which does work quite well due to exponential nature
        # of the id lending more import to the larger rings being in the right place
        return (self.n_poles**self.n_rings - 1) - self.id

    def expand(self):
        # returns the next states that are reachable from the current state
        next_states = []

        for ring in range(1, self.n_rings+1):
            loc = self.locs[ring]           # get location of ring
            if not self.min[loc] == ring:   # check if ring is moveable
                continue
            
            # creates copies of the state to edit so we don't change the state object
            next_loc = self.locs.copy()
            next_min = self.min.copy()
            next_max = self.max.copy()
            
            for target in range(self.n_poles):
                # ? case: ring doesn't fit on target tower
                if target == loc or \
                    (ring > self.min[target] and self.min[target] != -1):
                    # print("case: ring doesn't fit on target tower")
                    continue
                
                # used to prevent unnecesary copying - we can revert any
                #   changes in O(1) time
                π_next_max_loc = next_max[loc]
                π_next_min_loc = next_min[loc]
                π_next_loc_ring = next_loc[ring]
                π_next_min_target = next_min[target]
                π_next_max_target = next_max[target]
                
                # * REMOVE RING FROM TOWER
                # ? case: ring is the last one left in tower
                if self.max[loc] == ring:
                    next_max[loc] = -1
                    next_min[loc] = -1
                    # print("case: ring is the last one left in tower")
                # ? case: ring is top one on tower
                else:
                    # next_max[loc] doesn't change
                    next_min[loc] = -1  # find the next minimum ring on the tower
                    for r in range(ring+1, self.n_rings+1):
                        if self.locs[r] == loc:
                            next_min[loc] = r
                            break
                    # print("case: ring is top one on tower")

                # * ADD RING TO TOWER
                next_loc[ring] = target 
                next_min[target] = ring
                if ring > self.max[target]: next_max[target] = ring
                
                # We need to make copies because otherwise python data
                # fuckery changes the states afterwards
                if self.p and next_loc == self.p.locs:  # skip parent
                    continue
                new_loc = next_loc.copy()
                new_max = next_max.copy()
                new_min = next_min.copy()
                next_states.append(state(new_loc, new_max, new_min, self))

                # * RESET STATE TO PARENT
                next_max[loc] = π_next_max_loc
                next_min[loc] = π_next_min_loc
                next_max[target] = π_next_max_target
                next_loc[ring] = π_next_loc_ring
                next_min[target] = π_next_min_target
                
        return next_states
    
    # ! PYTHON OPERATIONS FOR EASY USE

    def __lt__(self, other):
        return self.id < other.id

    def __eq__(self, other):
        return self.id == other.id
    
    def __gt__(self, other):
        return self.id > other.id

    # Pretty prints the state
    def __str__(self):
        space = ' '
        π = '-' if not self.p else str(self.p.id)
        string ='Node ID:  ' +str(self.id) + '\n' +   \
                'loc:      ' + self.locs.__str__() + '\n' + \
                'maxs:     ' +self.max.__str__() + '\n'+ \
                'mins:     ' +self.min.__str__() + '\n' + \
                'f:        ' +str(self.f)+ '\n' + \
                'π:        ' +π + '\n'
        
        half_width = self.n_rings + 1 // 2
        for i in range(self.n_poles):
            string += space*half_width + '|' + space*half_width + '\t'
        string += '\n'
        poles= [[] for i in range(self.n_poles)]
        for pole in range(self.n_poles):
            for ring in range(1,self.n_rings+1):
                if self.locs[ring] == pole:
                    odd = (ring%2==1 and ring!=1)
                    poles[pole].append(space*(half_width-ring+1) +
                                    (ring-1)*'-' + '-' +  (ring-1)*'-' + 
                                    space*(half_width-ring+1))
                else:
                    poles[pole].append(space*(half_width)+ '|' +
                                    space*(half_width))
                    
        poles = np.transpose(poles)

        for row in poles:
            for col in row:
                string += col
                string += '\t'
            string += '\n'
                
        return string
    