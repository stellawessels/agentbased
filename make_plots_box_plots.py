import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

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
data = {(solver, environment): pd.read_csv(f"statistics_files/env{environment}-n_agents{numb_agents}-{solver}.csv")
        for solver in solvers for environment in env}
plot_dictionary = {}
for solver in solvers:
    for environment in env:
        plot_dictionary[(solver, environment)] = data[(solver, environment)][criteria_option[0]]
# plot_dictionary["0"] = [0] * 249
df = pd.DataFrame(plot_dictionary)
# sns.boxplot(data=df[[("CBS", 1), ("Prioritized", 1),
#     ("CBS", 2), ("Prioritized", 2),
#     ("CBS", 3), ("Prioritized", 3)]
#     ], fill=False)
df[[("CBS", 1), ("Prioritized", 1),
    ("CBS", 2), ("Prioritized", 2),
    ("CBS", 3), ("Prioritized", 3)]
    ].plot(kind='box')
#
plt.title(f"{criteria_option[0]} performance for the algorithms for {numb_agents} agents")
plt.xlabel("1                                  2                                     3 \n Environment number")
plt.ylabel(f"{criteria_option[0]}")
plt.xticks(np.arange(1, 7), labels=["CBS", "Prioritized", "CBS", "Prioritized", "CBS", "Prioritized"])
plt.show()

















#
#
# # Your existing data preparation code remains unchanged up to the creation of df
#
# # Assuming df is the dataframe you created from your CSV files.
# # You'll need to make sure it's in the correct format expected by seaborn, which is usually "long-form" or "tidy" data.
# # For seaborn, you typically need to have one column for the x-axis (categories), one for the y-axis (values),
# # and optionally one for the hue (colors representing different categories within the x-axis categories).
#
# # First, ensure that the dataframe is melted into long form if it's not already
# df_long = df.melt(var_name='Algorithm', value_name='Path distance', ignore_index=False)
# df_long['Environment'] = df_long.index.get_level_values(1)  # Extract environment number
# df_long['Algorithm'] = df_long['Algorithm'].map(lambda x: x[0])  # Extract algorithm name
#
# # Now, use seaborn to plot
# sns.set_theme(style="whitegrid")  # This sets the theme for the plots
#
# plt.figure(figsize=(12, 6))  # You can adjust the size of the figure
# boxplot = sns.boxplot(x='Environment', y='Path distance', hue='Algorithm', data=df_long,
#                       palette=["blue", "orange"])  # Specify the colors for each algorithm
#
# # Set the titles and labels
# boxplot.set_title(f'Path distance performance for the algorithms for {numb_agents} agents')
# boxplot.set_xlabel('Environment number')
# boxplot.set_ylabel('Path distance')
#
# # If you want to have custom tick labels, you can set them like this
# boxplot.set_xticklabels(['1', '2', '3'])
#
# plt.show()  # Display the plot