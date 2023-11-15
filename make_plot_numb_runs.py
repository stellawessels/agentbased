import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
numb_agents = 1
env = 1
max_no_runs = 10
solvers = ["CBS"]
criteria_options = ["Travel time", "Path distance", "Travel time ratio", "Path length ratio",
                    "Travel time standard deviation", "Ratio failed instances", "Computation time"]
criteria_option = ["Travel time"]  # Adjust this to change the criteria you want to plot
# Get the data we want to plot
data = {solver: pd.read_csv(f"statistics_files/env{env}-n_agents{agent}-{solver}.csv")
        for solver in solvers for agent in range(1, numb_agents + 1)}
# Get the variance of the criteria per number of successful runs, for all values of number of successful runs
values = []
print(data[f"{solvers[0]}"][f"{criteria_option[0]}"][0])
to_be_appended = []
for solver in solvers:
    for i in range(max_no_runs + 1):
        for j in range(i):
            to_be_appended.append(data[f"{solver}"][f"{criteria_option[0]}"][j])
        values.append(list(to_be_appended))
# find variance of each list in values
# print(values)
variances = []
for i in range(len(values)):
    variances.append(np.var(values[i]))
print(values)
# Make a line plot with number of runs on the x axis and variance on the y axis
fig, ax = plt.subplots()
ax.plot(variances)
plt.title(f"{criteria_option[0]} variance for the algorithms in environment {env}")
plt.xlabel("Number of successful runs")
plt.ylabel(f"{criteria_option[0]} variance")
plt.xticks(range(max_no_runs + 1))
plt.show()


