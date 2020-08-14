
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
scores = [12.17,21.52,60.09,66.00,50.74,15.58,14.48,35.75,0,0]

params = ['500', '1000', '1500', '2000', '2500', '3000', '3500', '4000', '4500', '5000']


y_pos = np.arange(len(params))


ax.set_xlabel('NAB Score')
ax.set_ylabel('Dataset length (S)')
ax.set_title('Dataset length vs Score')

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
        rect.set_facecolor("red")
    width = rect.get_width()
    height = rect.get_height()
    print(rect)
    ax.text(rect.get_x() + rect.get_width() + label_padding, rect.get_y() + height/2, label, ha='center', va='center')

plt.show()