import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

"""" The plan:
    Make plots which show the performance indicators for each of the algorithms in each environment.
    In the first part the environment number is the x-axis and the number of agents is fixed (not for use with
    "Ratio failed instances").
    In the second part the environment is fixed and the number of agents is the x-axis."""

criteria_options = ["Travel time", "Path distance", "Travel time ratio", "Path length ratio",
                    "Travel time standard deviation", "Ratio failed instances", "Computation time"]
criteria_option = ["Path distance"]  # Adjust this to change the criteria you want to plot

# Part 1
numb_agents = 6
#
# solvers = ["CBS", "Prioritized"]
# # Get the data we want to plot
# df1 = pd.read_csv(f"statistics_files/env1-n_agents{numb_agents}-CBS.csv")
# df1["Solver"] = "CBS"
# df1["Environment"] = 1
# df2 = pd.read_csv(f"statistics_files/env1-n_agents{numb_agents}-Prioritized.csv")
# df2["Solver"] = "Prioritized"
# df2["Environment"] = 1
# df3 = pd.read_csv(f"statistics_files/env2-n_agents{numb_agents}-CBS.csv")
# df3["Solver"] = "CBS"
# df3["Environment"] = 2
# df4 = pd.read_csv(f"statistics_files/env2-n_agents{numb_agents}-Prioritized.csv")
# df4["Solver"] = "Prioritized"
# df4["Environment"] = 2
# df5 = pd.read_csv(f"statistics_files/env3-n_agents{numb_agents}-CBS.csv")
# df5["Solver"] = "CBS"
# df5["Environment"] = 3
# df6 = pd.read_csv(f"statistics_files/env3-n_agents{numb_agents}-Prioritized.csv")
# df6["Solver"] = "Prioritized"
# df6["Environment"] = 3
# df = pd.concat([df1, df2, df3, df4, df5, df6])
# sns.boxplot(x=df["Environment"], y=df[criteria_option[0]], hue=df["Solver"])
# plt.title(f"{criteria_option[0]} performance for the algorithms \n "
#           f"for {numb_agents} agents with bi-directional traffic")
# plt.show()


# Part 2 - only intended for use with number of failed instances
# If you want to use it for other indicators, remove the "plot_data/plot_data-" from the file names.

environment = 2
df1 = pd.read_csv(f"statistics_files/plot_data/plot_data-env{environment}-n_agents3-CBS.csv")
df1["Solver"] = "CBS"
df1["Agents"] = 3
df2 = pd.read_csv(f"statistics_files/plot_data/plot_data-env{environment}-n_agents3-Prioritized.csv")
df2["Solver"] = "Prioritized"
df2["Agents"] = 3
df3 = pd.read_csv(f"statistics_files/plot_data/plot_data-env{environment}-n_agents6-CBS.csv")
df3["Solver"] = "CBS"
df3["Agents"] = 6
df4 = pd.read_csv(f"statistics_files/plot_data/plot_data-env{environment}-n_agents6-Prioritized.csv")
df4["Solver"] = "Prioritized"
df4["Agents"] = 6
df5 = pd.read_csv(f"statistics_files/plot_data/plot_data-env{environment}-n_agents9-CBS.csv")
df5["Solver"] = "CBS"
df5["Agents"] = 9
df6 = pd.read_csv(f"statistics_files/plot_data/plot_data-env{environment}-n_agents9-Prioritized.csv")
df6["Solver"] = "Prioritized"
df6["Agents"] = 9
df7 = pd.read_csv(f"statistics_files/plot_data/plot_data-env{environment}-n_agents12-CBS.csv")
df7["Solver"] = "CBS"
df7["Agents"] = 12
df8 = pd.read_csv(f"statistics_files/plot_data/plot_data-env{environment}-n_agents12-Prioritized.csv")
df8["Solver"] = "Prioritized"
df8["Agents"] = 12
df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8])
sns.boxplot(x=df["Agents"], y=df[criteria_option[0]], hue=df["Solver"])
plt.title(f"{criteria_option[0]} performance for the algorithms \n in environment "
          f"{environment} with bi-directional traffic")
plt.show()