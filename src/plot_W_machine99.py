
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
39.13,
23.27,
11.11,
11.11,
11.11]

params = ['48','148','248','348','448','548','648','748','848','948','1048','1148']


y_pos = np.arange(len(params))


ax.set_xlabel('NAB Score')
ax.set_ylabel('Window size (W)')
ax.set_title('Window size vs Score')

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
