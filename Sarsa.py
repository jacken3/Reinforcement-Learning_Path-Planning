"""
RRT_2D
@author: huiming zhou
"""

from env import Environment
from env import final_states 
from plotting import Plotting
from agent_brain import SarsaTable


def update():
    # Resulted list for the plotting Episodes via Steps
    steps = []

    # Summed costs for all episodes in resulted list
    all_costs = []

    for episode in range(2000):
        # Initial Observation
        observation = env.reset()

        # Updating number of Steps for each Episode
        i = 0

        # Updating the cost for each episode
        cost = 0

        # RL choose action based on observation
        action = RL.choose_action(str(observation))

        while True:

            observation_, reward, done = env.step(action)

            action_ = RL.choose_action(str(observation_))

            cost += RL.learn(str(observation), action, reward, str(observation_), action_)

            observation = observation_
            action = action_

            i += 1

            if done:
                steps += [i]
                all_costs += [cost]
                break

    # Showing the final route
    env.final()

    # Showing the Q-table with values for each action
    RL.print_q_table()

    # Plotting the results
    RL.plot_results(steps, all_costs)


if __name__ == "__main__":
    x_start = (2, 2)  # Starting node
    x_goal = (30, 20)  # Goal node

    env = Environment(x_start,x_goal)
    RL = SarsaTable(actions=list(range(env.n_actions)),
                    learning_rate=0.1,
                    reward_decay=0.9,
                    e_greedy=0.9) #初始化Sarsa_table

    # rrt = Rrt(x_start, x_goal, 0.5, 0.05, 10000)
    #path = rrt.planning()
    update()
    plotting = Plotting(x_start, x_goal,env)
    path=list(final_states().values())
    path.insert(0,x_start)
    if path:
        plotting.animation([], path, "Q_Learning", True)
    else:
        print("No Path Found!")

