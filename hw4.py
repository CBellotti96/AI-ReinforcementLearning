import random, numpy

global living_reward
global discount_rate
global learning_rate
global greedy_rate
global donut_reward
global forbidden_reward

class State(object):
    def __init__(self, state_type=None):
        if state_type == None:
            state_type = "plain"
        self.state_type = "plain"
        self.actions = [0,0,0,0]
    
    def change_state_type(self,state_type):
        self.state_type = state_type
    
    def return_best_action(self):
        best = 0
        best_index = 0
        for action in range(0,3):
            if self.actions[action] > best:
                best = self.actions[action]
                best_index = action
        if best_index == 0:
            best_string = "up"
        elif best_index == 1:
            best_string = "right"
        elif best_index == 2:
            best_string = "left"
        else:
            best_string = "down"
        return best_string
            
    def print_q_values(self):
        print "up: ", self.actions[0]
        print "right: ", self.actions[1]
        print "left: ", self.actions[2]
        print "down: ", self.actions[3]

def random_move(board, row, column):
    while True:
        direction = random.randint(0,3)
        if(direction == 0):
            if(row+1 <= 2):
                if(board[row+1][column].state_type != "wall"):
                    return direction
        elif(direction == 1):
            if(column+1 <= 3): 
                if(board[row][column+1].state_type != "wall"):
                    return direction
        elif(direction == 2):
            if(column-1 >= 0):
                if(board[row][column-1].state_type != "wall"):
                    return direction
        elif(direction == 3):
            if(row-1 >= 0):
                if(board[row-1][column].state_type != "wall"):
                    return direction

def policy_move(board, row, column):
    up = [board[row][column].actions[0]]
    right = [board[row][column].actions[1]]
    left = [board[row][column].actions[2]]
    down = [board[row][column].actions[3]]
    moves_list = [left, right, up, down]
    moves_list.sort(reverse=True)
    up.append("up")
    right.append("right")
    left.append("left")
    down.append("down")
    for move in moves_list:
        if(move[1] == up[1]):
            if(row+1 <= 2):
                if(board[row+1][column].state_type != "wall"):
                    return 0
        elif(move[1] == right[1]):
            if(column+1 <= 3): 
                if(board[row][column+1].state_type != "wall"):
                    return 1
        elif(move[1] == left[1]):
            if(column-1 >= 0):
                if(board[row][column-1].state_type != "wall"):
                    return 2
        elif(move[1] == down[1]):
            if(row-1 >= 0):
                if(board[row-1][column].state_type != "wall"):
                    return 3     
    
def simulate(board):
    step = 0
    curr_run_reward = 0
    curr_row = 0 #row is either 0, 1, or 2
    curr_column = 0 #column is either 0, 1, 2, or 3
    #initialize self at start
    #determine if we will choose best movement or greedy movement
    #decide where we will move based on that
    #update q value based on formula
    while step < 10000:
        if board[curr_row][curr_column].state_type == "donut":
            curr_run_reward += 100
            new_row = 0
            new_column = 0
        
        elif board[curr_row][curr_column].state_type == "forbidden":
            curr_run_reward -= 100
            new_row = 0
            new_column = 0
        
        else:
            curr_run_reward += living_reward
            rand_num = random.uniform(0,1)
            if rand_num <= greedy_rate:
                direction = random_move(board, curr_row, curr_column)
            else:
                direction = policy_move(board, curr_row, curr_column)
            if direction == 0:
                new_row = curr_row + 1
                new_column = curr_column
            elif direction == 1:
                new_row = curr_row
                new_column = curr_column + 1
            elif direction == 2:
                new_row = curr_row
                new_column = curr_column - 1
            else:
                new_row = curr_row - 1
                new_column = curr_column
            
            if board[new_row][new_column].state_type == "donut":
                board[curr_row][curr_column].actions[direction] = ((1-learning_rate) * (board[curr_row][curr_column].actions[direction])) + (learning_rate * (living_reward + discount_rate * donut_reward)) 
                step += 1
            elif board[new_row][new_column].state_type == "forbidden":
                board[curr_row][curr_column].actions[direction] = ((1-learning_rate) * (board[curr_row][curr_column].actions[direction])) + (learning_rate * (living_reward + discount_rate * forbidden_reward))
                step += 1
            else:
                board[curr_row][curr_column].actions[direction] = ((1-learning_rate) * (board[curr_row][curr_column].actions[direction])) + (learning_rate * (living_reward + discount_rate * max(board[new_row][new_column].actions)))
        curr_row = new_row
        curr_column = new_column
    
    return board
    
if __name__ == "__main__":
    #initializing values
    living_reward = -1
    discount_rate = .5
    learning_rate = .1
    greedy_rate = .1
    donut_reward = 100
    forbidden_reward = -100
    
    #getting user input for board state
    start = raw_input("Please provide board state and return type: ").split()
    if start[3] == 'p':
        donut = int(start[0])
        forbidden = int(start[1])
        wall = int(start[2])
        output = start[3]
    elif start[3] == 'q':
        donut = int(start[0])
        forbidden = int(start[1])
        wall = int(start[2])
        output = start[3]
        output_num = int(start[4])
    else:
        print "invalid output: exiting..."
        exit()
    #initializing board based on input
    board = [[State("plain"), State("plain"), State("plain"), State("plain")],[State("plain"), State("plain"), State("plain"), State("plain")],[State("plain"), State("plain"), State("plain"), State("plain")]]
    count = 0
    for row in board:
        for state in row:
            count += 1
            if count == donut:
                state.change_state_type("donut")
            elif count == forbidden:
                state.change_state_type("forbidden")
            elif count == wall:
                state.change_state_type("wall")
    simulate(board)
    count = 0
    if start[3] == 'p':
        for row in board:
            for state in row:
                count += 1
                if state.state_type == "plain":
                    print count, " ", state.return_best_action()
    if start[3] == 'q':
        for row in board:
            for state in row:
                count += 1
                if count == output_num:
                    state.print_q_values()


    