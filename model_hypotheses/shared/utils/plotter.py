import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap, BoundaryNorm
from shared.utils.colors import cmap, norm, diff_cmap, diff_norm

def plot_all_examples(examples):
    """
    Plots all examples in a grid layout, showing input, expected output, and transformed output
    for each example, along with status indicators.
    
    Args:
        examples (list of dict): List of dictionaries containing example data.
            Each dictionary should have:
            - grids (list): List of grids (input, expected output, transformed output)
            - titles (list): List of titles for each grid
            - match_status (str): Status of the transformation ('Transformed Correctly' or 'Mismatch')
            - dimensions (str): Grid dimensions
            - type (str): Example type ('Training' or 'Test')
            - idx (int): Example index
    
    The function creates a figure with subplots arranged in rows (one row per example)
    and columns (input grid, expected output, transformed output, plus status column).
    Each grid is displayed with appropriate colors and titles.
    """
    num_examples = len(examples)

    # Define the grid lines color and width
    grid_lines_color = '#545454'  # Dark grey color
    grid_lines_width = 1.2        # Increased line width for better visibility

    # Determine the maximum number of grids (excluding the status column)
    max_grids = max(len(example['grids']) for example in examples)
    num_cols = max_grids + 1  # +1 for status column

    # Adjust figure size accordingly
    fig_height = 3 * num_examples

    fig, axes = plt.subplots(num_examples, num_cols, figsize=(5 * num_cols, fig_height),
                             gridspec_kw={'width_ratios': [0.5] + [5]*(num_cols -1), 'hspace': 0.5})

    if num_examples == 1:
        axes = np.expand_dims(axes, axis=0)

    for idx, example in enumerate(examples):
        grids = example['grids']
        titles = example['titles']
        match_status = example['match_status']
        dimensions = example['dimensions']
        example_type = example['type']  # 'Training' or 'Test'

        # Status symbol
        if match_status == 'Transformed Correctly':
            status_symbol = '✓'  # Green checkmark
            status_color = 'green'
        elif match_status == 'Mismatch Detected' or match_status == 'Dimensions Mismatch':
            status_symbol = '✗'  # Red cross
            status_color = 'red'
        else:
            status_symbol = ''  # For test examples without expected outputs
            status_color = 'black'

        for jdx in range(num_cols):
            ax = axes[idx][jdx]

            if jdx == 0:
                # Status indicator
                ax.text(0.5, 0.5, status_symbol, color=status_color,
                        fontsize=24, fontweight='bold', horizontalalignment='center',
                        verticalalignment='center', transform=ax.transAxes)
                ax.axis('off')
                if idx == 0:
                    ax.set_title('Status', fontweight='bold')
            else:
                grid_idx = jdx - 1
                if grid_idx >= len(grids):
                    ax.axis('off')
                    continue
                grid = grids[grid_idx]
                title = titles[grid_idx]
                dimension = dimensions[grid_idx] if grid_idx < len(dimensions) else None

                # Handle empty grids
                if grid.size == 0:
                    ax.text(0.5, 0.5, 'Empty Grid', horizontalalignment='center',
                            verticalalignment='center', transform=ax.transAxes)
                    ax.set_title(title, fontweight='bold')
                    ax.axis('off')
                    continue

                if title.startswith('Difference Grid'):
                    # For the difference grid, use a custom colormap
                    ax.imshow(grid, cmap=diff_cmap, interpolation='none', norm=diff_norm)
                else:
                    ax.imshow(grid, cmap=cmap, interpolation='none', norm=norm)

                # Add dimensions to the title
                if dimension is not None and len(dimension) == 2:
                    dimension_info = f' ({dimension[0]}x{dimension[1]})'
                else:
                    dimension_info = ''
                if grid_idx == 0:  # Input Grid
                    ax.set_title(f'{title}{dimension_info}\n{example_type} Example {example["idx"]}', fontweight='bold')
                else:
                    ax.set_title(f'{title}{dimension_info}', fontweight='bold')

                # Set up grid lines
                ax.set_xticks(np.arange(-0.5, grid.shape[1], 1), minor=True)
                ax.set_yticks(np.arange(-0.5, grid.shape[0], 1), minor=True)
                ax.grid(which='minor', color=grid_lines_color, linestyle='-', linewidth=grid_lines_width)
                ax.tick_params(which='minor', bottom=False, left=False)
                ax.tick_params(which='major', bottom=False, left=False)
                ax.set_xticklabels([])
                ax.set_yticklabels([])

        # Add extra space between examples
        if idx < num_examples - 1:
            fig.subplots_adjust(hspace=0.5)

    plt.tight_layout()
    plt.show()
