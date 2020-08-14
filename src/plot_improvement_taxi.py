
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns; sns.set()



# Make fake dataset
height = []
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



sns.set_style("whitegrid")

# Color palette
blue, = sns.color_palette("muted", 1)

label_padding = 2.5


# Bring some raw data.
scores = [66,64.5,78.35,78.15,78.5,78.35]

params = ['dataset_size','window_size','discord_sim_threshold', 'ttl', 'n_discords_extract', 'exclusion_zone']


# Make the plot
fig, ax = plt.subplots()
ax.plot(params, scores, color=blue, lw=3)
ax.fill_between(params, 0, scores, alpha=.3)
ax.set(xlim=(0, len(params) - 1), ylim=(0, 100), xticks=params)

ax.set_xlabel('NAB Score')
ax.set_ylabel('Variables')
ax.set_title('Variable impact on score')


#
# # Create names on the y-axis
# ax.set_xticks(y_pos)
# ax.set_xticklabels(params)
#
# ax.set_ylim((0, 100))
#
#
# # Area plot
# ax.fill_between(params,scores)
#
plt.xticks(rotation=25)

ax.tick_params(axis='x', which='major', labelsize=10)
plt.tight_layout()

#
# y_pos = np.arange(len(params))
#
#
# ax.set_xlabel('NAB Score')
# ax.set_ylabel('Time to live (TTL)')
# ax.set_title('TTL vs Score')
#
# # Create horizontal bars
# ax.barh(y_pos, scores)
#
# # Create names on the y-axis
# ax.set_yticks(y_pos)
# ax.set_yticklabels(params)
#
# ax.set_xlim(0, 100)
# # Show graphic
# # plt.show()
# rects = ax.patches
#
# # Make some labels.
# labels = [i for i in scores]
#
# for rect, label in zip(rects, labels):
#
#     if(label == max(scores)):
#         rect.set_facecolor("red")
#     width = rect.get_width()
#     height = rect.get_height()
#     print(rect)
#     ax.text(rect.get_x() + rect.get_width() + label_padding, rect.get_y() + height/2, label, ha='center', va='center')

plt.show()
