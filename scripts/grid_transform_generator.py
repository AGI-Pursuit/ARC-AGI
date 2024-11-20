import numpy as np
import matplotlib.pyplot as plt
import random
from copy import deepcopy
import json
from matplotlib.colors import ListedColormap

color_palette = [
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

custom_cmap = ListedColormap(color_palette)

def generate_grid_size(min_size=5, max_size=10):
    """Randomly generate grid size within specified bounds."""
    rows = random.randint(min_size, max_size)
    cols = random.randint(min_size, max_size)
    return rows, cols

def get_neighbors(cell, rows, cols):
    """Retrieve neighboring cells (up, down, left, right) for a given cell."""
    r, c = cell
    neighbors = []
    if r > 0:
        neighbors.append((r - 1, c))
    if r < rows - 1:
        neighbors.append((r + 1, c))
    if c > 0:
        neighbors.append((r, c - 1))
    if c < cols - 1:
        neighbors.append((r, c + 1))
    return neighbors

def generate_random_shape(rows, cols, min_size=3, max_size=15):
    """
    Generate a random contiguous shape within the grid.
    Ensures that the shape is centrally located to accommodate vertical flips without exceeding boundaries.
    """
    grid = np.zeros((rows, cols), dtype=int)
    shape_size = random.randint(min_size, max_size)
    
    # Starting point: center or near-center to allow flipping
    start_r = rows // 2 + random.randint(-1, 1) if rows > 5 else rows // 2
    start_c = cols // 2 + random.randint(-1, 1) if cols > 5 else cols // 2
    grid[start_r, start_c] = 1  # Temporary marker for the shape
    
    shape_cells = [(start_r, start_c)]
    
    for _ in range(shape_size - 1):
        if not shape_cells:
            break
        current_cell = random.choice(shape_cells)
        neighbors = get_neighbors(current_cell, rows, cols)
        random.shuffle(neighbors)
        for neighbor in neighbors:
            nr, nc = neighbor
            if grid[nr, nc] == 0:
                grid[nr, nc] = 1
                shape_cells.append((nr, nc))
                break  # Add one cell at a time
    
    return grid

def assign_random_color(grid):
    """Assign a random non-black color (1-9) to the shape."""
    color = random.randint(1, 9)  # Colors 1-9
    grid_colored = deepcopy(grid)
    grid_colored[grid_colored == 1] = color
    return grid_colored, color

def flip_grid_vertically(grid):
    """Perform a vertical flip (mirror along the vertical axis) of the grid."""
    return np.fliplr(grid)

def change_shape_color(grid, current_color):
    """Change the shape's color to a different non-black color."""
    available_colors = list(range(1, 10))
    if current_color in available_colors:
        available_colors.remove(current_color)
    new_color = random.choice(available_colors)
    grid_changed = deepcopy(grid)
    grid_changed[grid_changed == current_color] = new_color
    return grid_changed, new_color

def generate_vertical_flip_pair():
    """
    Generate a pair of grids where the output is the vertically flipped version of the input.
    """
    rows, cols = generate_grid_size()
    grid = generate_random_shape(rows, cols)
    grid_colored, color = assign_random_color(grid)
    
    # Flip the grid vertically
    flipped_grid = flip_grid_vertically(grid_colored)
    
    # Convert numpy arrays to lists for JSON serialization
    input_grid = grid_colored.tolist()
    output_grid = flipped_grid.tolist()
    
    return {
        "input": input_grid,
        "output": output_grid,
        "transformation": "vertical_flip"
    }

def generate_color_change_pair():
    """
    Generate a pair of grids where the output has the shape's color changed.
    """
    rows, cols = generate_grid_size()
    grid = generate_random_shape(rows, cols)
    grid_colored, color = assign_random_color(grid)
    
    # Change the color
    changed_grid, new_color = change_shape_color(grid_colored, color)
    
    # Convert numpy arrays to lists for JSON serialization
    input_grid = grid_colored.tolist()
    output_grid = changed_grid.tolist()
    
    return {
        "input": input_grid,
        "output": output_grid,
        "transformation": "color_change"
    }

def generate_dataset(num_pairs_per_transformation=100):
    """
    Generate a dataset containing grid pairs for each transformation type.
    
    Parameters:
        num_pairs_per_transformation (int): Number of pairs to generate for each transformation.
        
    Returns:
        list of dict: The dataset containing all grid pairs with labels.
    """
    dataset = []
    
    # Generate vertical flip pairs
    print("Generating vertical flip pairs...")
    for _ in range(num_pairs_per_transformation):
        pair = generate_vertical_flip_pair()
        dataset.append(pair)
    
    # Generate color change pairs
    print("Generating color change pairs...")
    for _ in range(num_pairs_per_transformation):
        pair = generate_color_change_pair()
        dataset.append(pair)
    
    return dataset

def save_dataset_to_json(dataset, filename="arc_grid_dataset.json"):
    """
    Save the dataset to a JSON file.
    
    Parameters:
        dataset (list of dict): The dataset to save.
        filename (str): The name of the JSON file.
    """
    with open(filename, 'w') as f:
        json.dump(dataset, f, indent=4)
    print(f"Dataset saved to {filename}")

def visualize_pair(input_grid, output_grid, transformation_type):
    """
    Visualize the input and output grids side by side using the custom color palette.
    """
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    
    # Input Grid Visualization
    axes[0].imshow(input_grid, cmap=custom_cmap, interpolation='nearest', vmin=0, vmax=9)
    axes[0].set_title('Input Grid')
    axes[0].axis('off')
    
    # Output Grid Visualization
    axes[1].imshow(output_grid, cmap=custom_cmap, interpolation='nearest', vmin=0, vmax=9)
    axes[1].set_title(f'Output Grid ({transformation_type})')
    axes[1].axis('off')
    
    plt.tight_layout()
    plt.show()


def main():
    # Set random seed for reproducibility
    random.seed(42)
    np.random.seed(42)
    
    # Generate the dataset
    dataset = generate_dataset(num_pairs_per_transformation=100)
    
    # Save the dataset to a JSON file
    save_dataset_to_json(dataset, filename="arc_grid_dataset.json")
    
    # Visualize a few examples from both transformations
    num_examples_to_visualize = 4
    print(f"Visualizing {num_examples_to_visualize} examples from each transformation...")
    
    for i in range(num_examples_to_visualize):
        # Access vertical_flip pair
        flip_pair = dataset[i]
        print(f"Vertical Flip Pair {i+1}: Transformation - {flip_pair['transformation']}")
        visualize_pair(flip_pair['input'], flip_pair['output'], flip_pair['transformation'])
        
        # Access color_change pair
        color_change_pair = dataset[100 + i]
        print(f"Color Change Pair {i+1}: Transformation - {color_change_pair['transformation']}")
        visualize_pair(color_change_pair['input'], color_change_pair['output'], color_change_pair['transformation'])


if __name__ == "__main__":
    main()
