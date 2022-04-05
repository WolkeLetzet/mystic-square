import numpy as np
import copy
import itertools

class State:
  id_iter = itertools.count()
  def __init__(self, sudoku):
    self.id = next(State.id_iter) # id automatico
    self.sudoku = sudoku
    self.N=sudoku.shape[0] #tamaño del sudoku

  def __lt__(self, other):
    return self.id < other.id



  def get_valid_actions(self):
    valid_actions = []
    for i in range(self.N):
      for j in range(self.N):
        if self.sudoku[i,j] == 0:
          for num in range(1,self.N+1):
            if self.is_valid_action(i,j,num):
              valid_actions.append(Action(i,j,num))
    return valid_actions

  def is_valid_action(self, i, j, num):

    # check row and column and square
    for k in range(self.N):
      if self.sudoku[i,k] == num or self.sudoku[k,j] == num or self.sudoku[i//3*3+k//3,j//3*3+k%3] == num:
        return False

    return True
  
  def is_final_state(self):
    for i in range(self.N):
      for j in range(self.N):
        if self.sudoku[i,j] == 0:
          return False
    return True

class Action:
  def __init__(self,i,j,num):
    self.i=i
    self.j=j
    self.num=num

def transition(state, action):
  new_state = copy.deepcopy(state)
  new_state.sudoku[action.i, action.j] = action.num
  return new_state

  

from copy import deepcopy

def dfs(initial_state):
  stack = [deepcopy(initial_state)]
  iters = 0
  visited = []
  while len(stack)>0:
    iters += 1
    state = stack.pop()
    if state.is_final_state(): return state,iters
    
    if state not in visited:
      visited.append(state)
      for action in state.get_valid_actions():
        stack.append(transition(state,action))

sudoku= np.array([[0,9,0,8,6,5,2,0,0],
		            	[0,0,5,0,1,2,0,6,8],
			            [8,6,2,3,9,7,1,4,5],
			            [9,2,1,7,4,8,3,5,6],
		            	[6,7,8,5,3,1,4,2,9],
			            [4,5,3,9,2,6,8,7,1],
			            [3,8,9,6,5,4,7,1,2],
			            [2,4,6,1,7,9,5,8,3],
			            [5,1,7,2,8,3,6,9,4]])

  
#sudoku= np.array([[0,9,0,8,6,5,2,0,0],
#            	    [0,0,5,0,1,2,0,6,8],
#		            	[0,0,0,0,0,0,0,4,0],
#			            [0,0,0,0,0,8,0,5,6],
#			            [0,0,8,0,0,0,4,0,0],
#			            [4,5,0,9,0,0,0,0,0],
#			            [0,8,0,0,0,0,0,0,0],
#			            [2,4,0,1,7,0,5,0,0],
#			            [0,0,7,2,8,3,0,9,0]])



initial_state = State(sudoku)
state,iters=dfs(initial_state)
print(state.sudoku)
print("iteraciones:", iters)