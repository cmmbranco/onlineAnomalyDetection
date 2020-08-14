
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
32.23,
65.36,
32.21,
43.01,
28.76,
23.87,
21.47]

params = ['2000','3000','4000','5000','6000','7000','8000','9000','10000']


y_pos = np.arange(len(params))


ax.set_xlabel('NAB Score')
ax.set_ylabel('Dataset size (S)')
ax.set_title('Dataset size vs Score')

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
        ## Uncomment if one is better....if all are equal it is not a good idea to paint all red
        rect.set_facecolor("red")
        pass
    width = rect.get_width()
    height = rect.get_height()
    print(rect)
    ax.text(rect.get_x() + rect.get_width() + label_padding, rect.get_y() + height/2, label, ha='center', va='center')

plt.show()
