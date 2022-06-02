# This script uses morphology to detect microorganisms in microscope photos.

from skimage import io as skio
from skimage import filters
from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np
from skimage import morphology

# read the image
img = skio.imread('microtubules.tif')
img_filt = np.copy(img)

# filter the image
img_filt = filters.gaussian(img_filt, sigma=1)

# find local maxima
def local_maxima_h_convex(img, h):
    h_maxima = morphology.reconstruction(img - h, img)    
    h_convex = (img - h_maxima) >= h
    return h_convex

# experimental phase
# for i in range(1, 30):
#    h = i / 100.0
#    mask = local_maxima_h_convex(img_filt, h)
#    detections = [(x, y) for x in range(mask.shape[0]) for y in range(mask.shape[1]) if mask[x, y] != 0]
#    print(f"h: {h}, detections: {len(detections)}")

mask = local_maxima_h_convex(img_filt, h=0.03)
detections = [(x, y) for x in range(mask.shape[0]) for y in range(mask.shape[1]) if mask[x, y] != 0]

# Validate the result
assert len(detections) == 40

# visualize the result
def show_detections(coos, bcg):
    
    fig, ax = plt.subplots()        
    ax.imshow(bcg, 'gray')
    cmap = cm.get_cmap('Spectral')
    
    # plot detections
    for i, (r, c) in enumerate(coos):
        color = cmap(((i+1) % 100) / 100)
        ax.scatter(c, r, color=color, marker=',', s=1)
        ax.text(c+5, r+5, str(i+1), fontsize=12, color=color)
    plt.show()
     
# show detections
show_detections(detections, img)




