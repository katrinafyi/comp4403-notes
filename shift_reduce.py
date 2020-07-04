from pprint import pprint
from dataclasses import dataclass, field
from enum import Enum, auto

class LR0Action(Enum):
    Shift = auto()
    Reduce = auto()
    Accept = auto()

# a singleton bullet
@dataclass(frozen=True)
class Bullet: 
    def __repr__(self): 
        return '*'

B = Bullet()

def find_bullet(item):
    b = item.right.index(B)
    return (b, item.right[b+1] if b+1 < len(item.right) else None)

@dataclass(frozen=True)
class LR0Item:
    left: str
    right: tuple
    
    def __repr__(self): 
        return f'{self.left} -> {" ".join(map(str, self.right))}'

@dataclass
class LR0State:
    items: set = field(default_factory=set)
    gotos: dict = field(default_factory=dict)
    action: LR0Action = field(default=None)

def derive_lr0_items(item, productions):
    b, x = find_bullet(item)

    new = set()
    for prod in productions.get(x, ()):
        new.add(LR0Item(x, (B, ) + tuple(prod)))

    return new    

def compute_lr0_states(productions, start):

    start_item = LR0Item("S'", (B, start))

    states = {}

    # set of kernel items which have not been derived yet
    new_kernels = {start_item}
    while new_kernels:
        kernel = new_kernels.pop()

        state = LR0State({kernel})
        states[kernel] = state

        # set of items in this state which have not been derived yet
        new_items = {kernel}
        while new_items:
            item = new_items.pop()
            derived = derive_lr0_items(item, productions) - state.items 

            state.items |= derived
            new_items.update(derived)

        # at this point, this kernel's state has its items fully derived.
        # next, compute goto states.
        for item in state.items:
            b = item.right.index(B)
            n = b + 1
            if n >= len(item.right): continue

            new_right = item.right[:b] + (item.right[n], B) + item.right[n+1:]
            new_kernel = LR0Item(item.left, new_right)

            x = item.right[n]
            state.gotos[x] = new_kernel
            if new_kernel not in states:
                new_kernels.add(new_kernel)

    for k, s in states.items():
        for item in s.items:
            b, x = find_bullet(item)
            if x is None:
                if item.left == start_item.left:
                    action = LR0Action.Accept
                else:
                    action = LR0Action.Reduce
            else:
                action = LR0Action.Shift
            if s.action is not None and s.action != action:
                raise RuntimeError('Parse action conflict at state ' 
                    + str(s) + ' with action ' + str(action))
            s.action = action

    for k, s in states.items():
        print(f'{k} \t[{s.action}]')
        print('    ', *s.items, sep=' | ')
        print('    ', s.gotos)
        print()
    return states, start_item

def parse_lr0(states, start, data):
    state_stack = [start]
    data_stack = []
    i = 0
    while state_stack:
        kernel = state_stack[-1]
        state = states[kernel]
        print('Currently at state:', kernel)
        print(data_stack)
        print(state_stack)
        print(state.action)
        print()
        if state.action == LR0Action.Shift:
            x = data[i]
            i += 1
        elif state.action == LR0Action.Reduce:
            goto = next(iter(state.items))
            for c in range(len(goto.right) - 1):
                state_stack.pop()
                data_stack.pop()
            x = goto.left
            state = states[state_stack[-1]]
        elif state.action == LR0Action.Accept:
            break
        data_stack.append(x)
        state_stack.append(state.gotos[x])

    print(state_stack, data_stack)



if __name__ == "__main__":
    # productions = {'S': [list('A')], 'A': [list('(A)'), list('a')]}
    # s = 'S'
    productions = {'S': [list('E')], 'E': [list('E+n'), list('n')]}
    s = 'S'

    states, start = compute_lr0_states(productions, s)
    parse_lr0(states, start, '(((a)))')