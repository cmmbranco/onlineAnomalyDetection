
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns; sns.set()



sns.set(rc={'figure.figsize':(12, 8)})


# Make fake dataset
height = []
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



label_padding = 2.5


fig, ax = plt.subplots()

# Bring some raw data.
scores = [11.11,
11.11,
11.11,
11.11,
11.11,
11.11,
11.11,
11.11,
11.11,
11.11,
11.11,
11.11,
11.11,
11.11,
11.11,
11.11,
11.11,
11.11,
11.11,
11.11]

params = ['0.8','0.81','0.82','0.83','0.84','0.85','0.86','0.87','0.88','0.89','0.9','0.91','0.92','0.93','0.94','0.95','0.96','0.97','0.98','0.99']

y_pos = np.arange(len(params))


ax.set_xlabel('NAB Score')
ax.set_ylabel('Discord similarity threshold (disc_sim)')
ax.set_title('Discord Similarity Threshold vs Score')

# Create horizontal bars
ax.barh(y_pos, scores)

# Create names on the y-axis
ax.set_yticks(y_pos)
ax.set_yticklabels(params)

ax.set_xlim(0, 100)
# Show graphic
# plt.show()
rects = ax.patches

# Make some labels.
labels = [i for i in scores]

for rect, label in zip(rects, labels):

    if(label == max(scores)):
        #rect.set_facecolor("red")
        pass
    width = rect.get_width()
    height = rect.get_height()
    print(rect)
    ax.text(rect.get_x() + rect.get_width() + label_padding, rect.get_y() + height/2, label, ha='center', va='center')

plt.show()
