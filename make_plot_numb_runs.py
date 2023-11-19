import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""" This file is used to make plots of the number of runs vs the criteria. In the assignment we show the number of 
failed instances vs total number of runs as well as a comparison of the number of failres and the number of agents 
(average).
The first part of the code should be run while the second part of the code is commented out, and visa versa."""

# First part of the code
numb_agents = 9
env = 1
max_no_runs = 500
solvers = ["Prioritized", "CBS"]
criteria_options = ["Travel time", "Path distance", "Travel time ratio", "Path length ratio",
                    "Travel time standard deviation", "Number of failed instances", "Computation time"]
criteria_option = ["Number of failed instances"]  # Adjust this to change the criteria you want to plot
# Get the data we want to plot
data = {solver: pd.read_csv(f"saved/env{env}-n_agents{numb_agents}-{solver}.csv")
        for solver in solvers}
# Get the variance of the criteria per number of successful runs, for all values of number of successful runs
values_prioritized = []
values_cbs = []
values_distributed = []
to_be_appended = []
for i in range((max_no_runs + 1) - data["Prioritized"][f"{criteria_options[5]}"].iloc[-1]):
    for j in range(i):
        to_be_appended.append(data["Prioritized"][f"{criteria_option[0]}"][j])
    values_prioritized.append(list(to_be_appended))
for i in range((max_no_runs + 1) - data["CBS"][f"{criteria_options[5]}"].iloc[-1]-5):
    for j in range(i):
        to_be_appended.append(data["CBS"][f"{criteria_option[0]}"][j])
    values_cbs.append(list(to_be_appended))
# for i in range((max_no_runs + 1) - data["Distributed"][f"{criteria_options[5]}"].iloc[-1]):
#     for j in range(i):
#         to_be_appended.append(data["Distributed"][f"{criteria_option[0]}"][j])
#     values_distributed.append(list(to_be_appended))

# Find variance of each list in values
variances_prioritized = []
variances_cbs = []
variances_distributed = []
for i in range(len(values_prioritized)):
    variances_prioritized.append(np.var(values_prioritized[i]))
for i in range(len(values_cbs)):
    variances_cbs.append(np.var(values_cbs[i]))
# for i in range(len(values_distributed)):
#     variances_distributed.append(np.var(values_distributed[i]))

# Make a line plot with number of runs on the x-axis and variance on the y-axis.
fig, ax = plt.subplots()
ax.plot(variances_prioritized, label="Prioritized")
ax.plot(variances_cbs, label="CBS")
# ax.plot(variances_distributed, label="Distributed")

plt.title(f"Variance of average {criteria_option[0]} for the algorithms \n in environment {env}, with {numb_agents} agents")
plt.xlabel("Number of successful runs")
plt.ylabel(f"Variance of average {criteria_option[0]}")
plt.legend()
plt.show()

# Second part of the code (comment out when running the first part)

# env = 1
# df1 = pd.read_csv(f"statistics_files/env{env}-n_agents3-Prioritized.csv")
# df1["Agents"] = 3
# df2 = pd.read_csv(f"statistics_files/env{env}-n_agents6-Prioritized.csv")
# df2["Agents"] = 6
# df3 = pd.read_csv(f"statistics_files/env{env}-n_agents9-Prioritized.csv")
# df3["Agents"] = 9
# df4 = pd.read_csv(f"statistics_files/env{env}-n_agents12-Prioritized.csv")
# df4["Agents"] = 12
# df5 = pd.concat([df1.iloc[-1], df2.iloc[-1], df3.iloc[-1], df4.iloc[-1]])
# df6 = pd.read_csv(f"statistics_files/env{env}-n_agents3-CBS.csv")
# df6["Agents"] = 3
# df7 = pd.read_csv(f"statistics_files/env{env}-n_agents6-CBS.csv")
# df7["Agents"] = 6
# df8 = pd.read_csv(f"statistics_files/env{env}-n_agents9-CBS.csv")
# df8["Agents"] = 9
# df9 = pd.read_csv(f"statistics_files/env{env}-n_agents12-CBS.csv")
# df9["Agents"] = 12
# df10 = pd.concat([df6.iloc[-1], df7.iloc[-1], df8.iloc[-1], df9.iloc[-1]])
# plt.scatter(y=df10["Number of failed instances"]/250, x=df10["Agents"], label="CBS")
# plt.scatter(y=df5["Number of failed instances"]/250, x=df5["Agents"], label="Prioritized")
#
# plt.title(f"Ratio of failed instances for the algorithms \n in environment {env}")
# plt.xlabel("Number of agents")
# plt.ylabel("Ratio of failed instances")
# plt.xticks(df5["Agents"])
# plt.legend()
# plt.show()