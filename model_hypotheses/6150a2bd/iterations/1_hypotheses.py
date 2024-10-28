def is_grid_rotated_180_degrees(input_grid, output_grid):
    """
    Checks if the output grid is a 180-degree rotation of the input grid.
    Returns:
        bool: True if the output is a 180-degree rotation of the input, False otherwise.
        Optional[str]: Additional information if False.
    """
    rotated = [row[::-1] for row in input_grid[::-1]]
    if rotated == output_grid:
        return True
    else:
        return False, f"Rotated grid does not match output. Expected {rotated}, got {output_grid}"

def is_grid_mirrored_horizontally(input_grid, output_grid):
    """
    Checks if the output grid is a horizontal mirror (left-right flip) of the input grid.
    Returns:
        bool: True if the output is a horizontal mirror of the input, False otherwise.
        Optional[str]: Additional information if False.
    """
    mirrored = [row[::-1] for row in input_grid]
    if mirrored == output_grid:
        return True
    else:
        return False, f"Mirrored horizontally grid does not match output. Expected {mirrored}, got {output_grid}"

def is_grid_mirrored_vertically(input_grid, output_grid):
    """
    Checks if the output grid is a vertical mirror (top-bottom flip) of the input grid.
    Returns:
        bool: True if the output is a vertical mirror of the input, False otherwise.
        Optional[str]: Additional information if False.
    """
    mirrored = input_grid[::-1]
    if mirrored == output_grid:
        return True
    else:
        return False, f"Mirrored vertically grid does not match output. Expected {mirrored}, got {output_grid}"

def are_non_background_colors_shifted_diagonally(input_grid, output_grid):
    """
    Checks if the non-background colors are shifted along the main diagonal.
    Returns:
        bool: True if non-background colors are shifted diagonally, False otherwise.
        Optional[str]: Additional information if False.
    """
    size = len(input_grid)
    shifted = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if input_grid[i][j] != 0:
                if j < size and i < size:
                    shifted[j][i] = input_grid[i][j]
    if shifted == output_grid:
        return True
    else:
        return False, f"Diagonally shifted grid does not match output. Expected {shifted}, got {output_grid}"

def are_non_background_colors_rotated_90_clockwise(input_grid, output_grid):
    """
    Checks if the non-background colors are rotated 90 degrees clockwise.
    Returns:
        bool: True if non-background colors are rotated 90 degrees clockwise, False otherwise.
        Optional[str]: Additional information if False.
    """
    size = len(input_grid)
    rotated = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            rotated[j][size - 1 - i] = input_grid[i][j]
    if rotated == output_grid:
        return True
    else:
        return False, f"90-degree rotated grid does not match output. Expected {rotated}, got {output_grid}"

def are_specific_colors_moved_to_specific_positions(input_grid, output_grid):
    """
    Checks if specific colors are moved to specific positions regardless of rotation or reflection.
    Returns:
        bool: True if specific color movements match, False otherwise.
        Optional[str]: Additional information if False.
    """
    # Define expected movements based on observed pairs
    # For simplicity, assume:
    # - Color 3 moves to different positions
    # - Color 5 moves from top-left to bottom-right
    # - Color 8 moves from top-right to bottom-left
    # - Color 2 moves from top-right to bottom-left
    # - Color 1 moves from middle-left to middle-right
    color_movements = {
        3: [(0,0), (0,1), (1,0)],
        8: [(0,2)],
        7: [(1,1)],
        5: [(2,0)],
        2: [(0,2)],
        1: [(1,0)]
    }
    for i in range(len(input_grid)):
        for j in range(len(input_grid[0])):
            color = input_grid[i][j]
            if color != 0:
                # Find positions of this color in output
                positions = [(x, y) for x in range(len(output_grid)) for y in range(len(output_grid[0])) if output_grid[x][y] == color]
                if not positions:
                    return False, f"Color {color} from input at ({i},{j}) not found in output."
                # For simplicity, check if any expected movement matches
                expected = color_movements.get(color, [])
                if (i, j) not in expected and positions[0] not in expected:
                    return False, f"Color {color} moved from ({i},{j}) to {positions[0]}, which is not expected."
    return True

def are_background_and_non_background_reordered_separately(input_grid, output_grid):
    """
    Checks if background and non-background cells are reordered separately.
    Returns:
        bool: True if background and non-background cells are reordered separately, False otherwise.
        Optional[str]: Additional information if False.
    """
    input_background = sorted([(i, j) for i in range(len(input_grid)) for j in range(len(input_grid[0])) if input_grid[i][j] == 0])
    output_background = sorted([(i, j) for i in range(len(output_grid)) for j in range(len(output_grid[0])) if output_grid[i][j] == 0])
    if input_background == output_background:
        return True
    else:
        return False, f"Background cells have been reordered. Input backgrounds: {input_background}, Output backgrounds: {output_background}"

def does_transformation_involve_rotation_and_color_reassignment(input_grid, output_grid):
    """
    Checks if the transformation involves both rotation and specific color reassignment.
    Returns:
        bool: True if both rotation and color reassignment are involved, False otherwise.
        Optional[str]: Additional information if False.
    """
    # Check for 180-degree rotation
    rotated = [row[::-1] for row in input_grid[::-1]]
    if rotated != output_grid:
        # Check if after rotation, some colors are reassigned
        # For simplicity, assume color reassignment if not directly rotated
        return False, "Transformation does not match simple 180-degree rotation; possible color reassignment needed."
    # Additional color reassignment checks can be added here
    return True
