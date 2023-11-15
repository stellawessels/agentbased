import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
numb_agents = 6
env = 3
max_no_runs = 500
solvers = ["Prioritized", "CBS"]
# solvers = ["CBS"]
criteria_options = ["Travel time", "Path distance", "Travel time ratio", "Path length ratio",
                    "Travel time standard deviation", "Number of failed instances", "Computation time"]
criteria_option = ["Number of failed instances"]  # Adjust this to change the criteria you want to plot
# Get the data we want to plot
data = {solver: pd.read_csv(f"statistics_files/env{env}-n_agents{numb_agents}-{solver}.csv")
        for solver in solvers}
# print(data)
# Get the variance of the criteria per number of successful runs, for all values of number of successful runs
values_prioritized = []
values_cbs = []
values_distributed = []
# print(data[f"{solvers[0]}"][f"{criteria_option[0]}"][0])
# print(data[f"{solvers[0]}"][f"{criteria_options[5]}"])
to_be_appended = []
# print(data["Prioritized"][f"{criteria_options[5]}"].iloc[-1])
for i in range((max_no_runs + 1) - data["Prioritized"][f"{criteria_options[5]}"].iloc[-1]):
    for j in range(i):
        to_be_appended.append(data["Prioritized"][f"{criteria_option[0]}"][j])
    values_prioritized.append(list(to_be_appended))
for i in range((max_no_runs + 1) - data["CBS"][f"{criteria_options[5]}"].iloc[-1]):
    for j in range(i):
        to_be_appended.append(data["CBS"][f"{criteria_option[0]}"][j])
    values_cbs.append(list(to_be_appended))
# for i in range((max_no_runs + 1) - data["Distributed"][f"{criteria_options[5]}"].iloc[-1]):
#     for j in range(i):
#         to_be_appended.append(data["Distributed"][f"{criteria_option[0]}"][j])
#     values_distributed.append(list(to_be_appended))
# find variance of each list in values
# print(values)
variances_prioritized = []
variances_cbs = []
variances_distributed = []
for i in range(len(values_prioritized)):
    variances_prioritized.append(np.var(values_prioritized[i]))
for i in range(len(values_cbs)):
    variances_cbs.append(np.var(values_cbs[i]))
# for i in range(len(values_distributed)):
#     variances_distributed.append(np.var(values_distributed[i]))
# print(values)
# Make a line plot with number of runs on the x axis and variance on the y axis
fig, ax = plt.subplots()
ax.plot(variances_prioritized, label="Prioritized")
ax.plot(variances_cbs, label="CBS")
# ax.plot(variances_distributed, label="Distributed")
plt.title(f"{criteria_option[0]} variance for the algorithms in environment {env}")
plt.xlabel("Number of successful runs")
plt.ylabel(f"{criteria_option[0]} variance")
# plt.xticks(range(max_no_runs + 1))
plt.legend()
plt.show()


