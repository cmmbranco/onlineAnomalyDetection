
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
scores = [78.35,52.57,35.74,54.24,52.8,16.31,28.61,15.21,13.01,48.18,49.28,27.08]

params = ['0','40','80','120','160','200','240','280','320','360','400','440']

y_pos = np.arange(len(params))


ax.set_xlabel('NAB Score')
ax.set_ylabel('Exclusion zone around point (ex_zone)')
ax.set_title('Exclusion zone vs Score')

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
