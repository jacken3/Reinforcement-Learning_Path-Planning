from env import Environment
from env import final_states 
from plotting import Plotting
from agent_brain import QLearningTable


def update():
    # Resulted list for the plotting Episodes via Steps
    steps = []

    # Summed costs for all episodes in resulted list
    all_costs = []

    for episode in range(2000):
        # Initial Observation
        observation = env.reset() #将机器人放在（0，0）处并清空d字典

        # Updating number of Steps for each Episode
        i = 0

        # Updating the cost for each episode
        cost = 0

        while True:

            # RL chooses action based on observation当前机器人的坐标位置
            action = RL.choose_action(str(observation)) #寻找动作的依据为以一定概率选择目前状态下动作值函数最大的动作，以一定概率随机选择（随机选择的目的是增加探索率）

            # RL takes an action and get the next observation and reward
            observation_, reward, done = env.step(action) #将该动作执行，得到奖励值，下个状态以及是否结束寻路标志

            # RL learns from this transition and calculating the cost
            cost += RL.learn(str(observation), action, reward, str(observation_))

            # Swapping the observations - current and next
            observation = observation_

            # Calculating number of Steps in the current Episode
            i += 1

            # Break while loop when it is the end of current Episode
            # When agent reached the goal or obstacle
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

    env = Environment(x_start,x_goal) #环境初始化
    RL = QLearningTable(actions=list(range(env.n_actions)),
                    learning_rate=0.1,
                    reward_decay=0.9,
                    e_greedy=0.9) #初始化
    update() #学习过程
    plotting = Plotting(x_start, x_goal,env) #初始化绘图工具
    path=list(final_states().values()) #获得路径
    path.insert(0,x_start)
    if path:
        plotting.animation([], path, "Q_Learning", True)
    else:
        print("No Path Found!")

