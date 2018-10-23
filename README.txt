This program is a model of reinforcement learning, specifically Q-Learning.

In this program, a hypothetical agent traverses a 3x4 board, where each state on
the board is assigned a number 1-12, and learns to optimally traverse to the goal
state.

The board numbers are laid out as follows:
    ______________
   |9   10  11  12|
   |              |
   |5   6   7   8 |
   |              |
   |1   2   3   4 |
   |______________|
   
All states are plain and allow movement in all directions except for 3 states
whose placement on the board is decided by the user:
        1. Goal state (donut): only has an exit action, and provides +100 reward
        2. Fail state (forbidden): only has an exit action, provides -100 reward
        3. Wall state: blocks all movement into that spot on the board
        
On success or failure, the agent will be reset to the starting state and continue

A negative living reward and discounting cause the agent to try to find the goal
as quickly as possible.

Each time the agent moves, it will update the q value associated with taking that
action in the current state.

The user inputs 3 numbers, followed by a character, which is either a 'p' or a 'q'
If the character is a 'q', it is followed by one more number
(X X X p) or (X X X q X)
The first 3 numbers in both cases correspond to the position of the goal state,
fail state, and wall state, respectively.
If the character 'p' is provided after, the optimal policy at the end of the
simulation for the other 9 states is provided.
If the character 'q' is provided instead, we will return the q values for all 4
possible directions for the state number provided in the input after the 'q'.