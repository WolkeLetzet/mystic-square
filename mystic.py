import numpy as np
import copy
import itertools

class State:
  id_iter = itertools.count()
  def __init__(self, puzzle):
    self.id = next(State.id_iter) # id automatico

    self.puzzle = puzzle
    self.N=puzzle.shape[0] #tamaño del puzzle
    self.empty = [self.N-1,self.N-1] # el último cuadrito está vacío
    self.moves = []

  def __lt__(self, other):
      return self.id < other.id

  def transition(self, action):
    old_pos = copy.copy(self.empty)
    if action=='up': self.empty[0] -=1
    if action=='down': self.empty[0] +=1
    if action=='left': self.empty[1] -=1
    if action=='right': self.empty[1] +=1

    self.puzzle[old_pos[0]][old_pos[1]] = self.puzzle[self.empty[0]][self.empty[1]]
    self.puzzle[self.empty[0]][self.empty[1]] = 0
    self.moves.append(action)


  def get_valid_actions(self):
    valid_actions = []
    if self.empty[0] > 0:
      valid_actions.append('up')
    if self.empty[0] < self.N-1:
      valid_actions.append('down');
    if self.empty[1] > 0:
      valid_actions.append('left');
    if self.empty[1] < self.N-1:
      valid_actions.append('right');

    return valid_actions

  def is_final_state(self):
    k = 1
    for i in range(self.N):
      for j in range(self.N):
        if i==self.N-1 and j==self.N-1: break
        if self.puzzle[i][j] != k: return False
        k += 1
        
    return True


    import copy
def dfs(initial_state, depth_limit=10):
  stack = [copy.deepcopy(initial_state)]

  iters = 0; 
  while len(stack)>0:
    iters += 1
    state = stack.pop() #retorna y elimina ultimo elemento
    if len(state.moves)>depth_limit: continue

    if state.is_final_state(): return state, iters

    actions = state.get_valid_actions()

    for action in actions:
      new_state = copy.deepcopy(state) #ojo que debemos copiar el estado antes de modificarlo!
      new_state.transition(action)
      stack.append(new_state) #agrega al final

  return None, iters


def bfs(initial_state):
  queue = [copy.deepcopy(initial_state)]

  iters = 0
  while len(queue)>0:
    iters += 1
    state = queue.pop(0) #retorna y elimina el primer elemento

    if state.is_final_state(): return state,iters #se encontró una solución!

    actions = state.get_valid_actions()

    for action in actions:
      new_state = copy.deepcopy(state) #ojo que debemos copiar el estado antes de modificarlo!
      new_state.transition(action)
      queue.append(new_state) #agrega al final

import random

def create_initial_state(N=3, random_actions=10):

  # Se crea un puzzle resuelto
  sorted_numbers = list(range(1,N*N))
  sorted_numbers.append(0)
  sorted_numbers=np.array(sorted_numbers)
  sorted_numbers.shape=(N,N)
  state = State(sorted_numbers)

  # Se aplican acciones aleatorias
  for i in range(random_actions):
    valid_actions = state.get_valid_actions()
    random_action = random.sample(valid_actions,1)[0]
    state.transition(random_action)

  state.moves=[]
  return state

#estado inicial
initial_state=create_initial_state(3, random_actions=10)

#en profundidad
print("inital state:\n",initial_state.puzzle)
state,iters=dfs(initial_state, depth_limit=15)
print("iteraciones:", iters, "\tmoves:", len(state.moves), " ==> ", state.moves)
print("final state:\n",state.puzzle)

#anchura
print("inital state:\n",initial_state.puzzle)
state,iters=bfs(initial_state)
print("iteraciones:", iters, "\tmoves:", len(state.moves), " ==> ", state.moves)
print("final state:\n",state.puzzle)


from queue import PriorityQueue

def best_first(initial_state, heuristic_eval):
  q = PriorityQueue()

  q.put( (-1, copy.deepcopy(initial_state)) )

  iters = 0
  while not q.empty():
    iters += 1
    elem=q.get()
    state = elem[1] #retorna y elimina el primer elemento

    if state.is_final_state(): return state,iters #se encontró una solución!

    actions = state.get_valid_actions()

    for action in actions:
      new_state = copy.deepcopy(state) #ojo que debemos copiar el estado antes de modificarlo!
      new_state.transition(action)
      q.put((heuristic_eval(new_state), new_state)) #agrega al final

#cantidad de fichas en posición incorrecta
def heuristic_eval(state):
    k = 1; incorrect = 0
    for i in range(state.N):
      for j in range(state.N):
        if state.puzzle[i][j] != k: incorrect+=1
        k += 1
        
    return incorrect +len(state.moves)


state,iters=best_first(initial_state, heuristic_eval)
print("iteraciones:", iters, "\tmoves:", len(state.moves), " ==> ", state.moves)