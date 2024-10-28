color_mappings = {
    -1: 'Missing',  # Special value for padding
    0: 'Black',     # Usually used as background color
    1: 'Blue',
    2: 'Red',
    3: 'Green',
    4: 'Yellow',
    5: 'Gray',
    6: 'Pink',
    7: 'Orange',
    8: 'Cyan',
    9: 'Maroon'
}

# Define the actual colors corresponding to the color mappings for plotting
color_palette = [
    '#212121',  # -1: Missing (dark gray)
    '#000000',  # 0: Black
    '#0173d9',  # 1: Blue
    '#ff4236',  # 2: Red
    '#2fcc41',  # 3: Green
    '#ffdc03',  # 4: Yellow
    '#a9a9a9',  # 5: Gray
    '#ef12be',  # 6: Pink
    '#ff841b',  # 7: Orange
    '#7edbff',  # 8: Cyan
    '#860b25',  # 9: Maroon
]

from matplotlib.colors import ListedColormap, BoundaryNorm
import numpy as np

cmap = ListedColormap(color_palette)
norm = BoundaryNorm(np.arange(-1.5, 10), cmap.N)  # For integer colors from -1 to 9

# For difference grid plotting
diff_color_palette = [
    '#A9A9A9',  # -1: Dark Gray (Missing)
    '#000000',  # 0: Black
    '#FFFFFF'   # 1: White (Differences)
]
diff_cmap = ListedColormap(diff_color_palette)
diff_norm = BoundaryNorm([-1.5, -0.5, 0.5, 1.5], diff_cmap.N)
