import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

im = np.array(Image.open('first.jpg'), dtype=np.uint8)

# Create figure and axes
fig,ax = plt.subplots(1)

# Display the image
ax.imshow(im)

# ground_truth_content = open('TownCentre-groundtruth.csv')
pred_content = open('../output/1b.csv')
frame_number = "1"
factor = 1.5
for index,line in enumerate(pred_content):
    # if index != 0:
    line = line.strip()
    # personNumber, frameNumber, headValid, bodyValid, headLeft, headTop, headRight, headBottom, bodyLeft, bodyTop, bodyRight, bodyBottom = line.split(",")
    personNumber, frameNumber,bodyValid,bodyLeft, bodyTop, bodyRight, bodyBottom = line.split(",")
    if frameNumber == frame_number:
        print(bodyLeft)
        print(bodyRight)
        rect = patches.Rectangle((float(bodyLeft)*factor,float(bodyTop)*factor),float(bodyRight)*factor-float(bodyLeft)*factor,float(bodyBottom)*factor-float(bodyTop)*factor,linewidth=1,edgecolor='r',facecolor='none')
        ax.add_patch(rect)

plt.show()
