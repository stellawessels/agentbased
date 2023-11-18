import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""" The plan:
    Make plots which show the performance indicators for each of the algorithms in each environment. 
    Here the environment number is the X axis and the number of agents is fixed."""

criteria_options = ["Travel time", "Path distance", "Travel time ratio", "Path length ratio",
                    "Travel time standard deviation", "Ratio failed instances", "Computation time"]
criteria_option = ["Path distance"]  # Adjust this to change the criteria you want to plot
numb_agents = 6
# num_x_ticks = int(numb_agents / 3)
env = [1, 2, 3]
solvers = ["CBS", "Prioritized"]
# Get the data we want to plot
data = {(solver, environment): pd.read_csv(f"statistics_files/plot_data/plot_data-env{environment}-n_agents{numb_agents}-{solver}.csv")
        for solver in solvers for environment in env}
# Adjust the form of the data to make it compatible with the plotting function
y_final = []
for solver in solvers:
    y = []
    for environment in env:
        for criteria in criteria_option:
            y.append(float(data[(solver, environment)][criteria]))
            y_final.append(y)
# Set the multiplier, this is used to make sure the bars are next to each other, and centered around the x-tick.
# Note that this will only work up to 3 solvers.
if len(solvers) == 2:
    multiplier = -0.5
else:
    multiplier = 0
fig, ax = plt.subplots()
for i in range(len(solvers)):
    # Select the part of y_final that belongs to the current solver
    y_final_final = y_final[i*3:i*3 + 3]
    offset = 0.25 * multiplier
    multiplier += 1
    # ax.bar(np.arange(num_x_ticks) + offset, y_final_final[0], width=0.25, label=f"{solvers[i]}")
    ax.scatter(range(1, 4), y_final_final[0], label=f"{solvers[i]}")
plt.title(f"{criteria_option[0]} performance for the algorithms for {numb_agents} agents")
plt.xlabel("Environment number")
plt.ylabel(f"{criteria_option[0]}")
# plt.xticks(np.arange(num_x_ticks), np.arange(1, num_x_ticks + 1))  # for bar plots
plt.xticks(np.arange(1, 4))  # for scatter plots
plt.legend()
plt.show()
