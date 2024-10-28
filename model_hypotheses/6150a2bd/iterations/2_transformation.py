def transform_grid(input_grid):
    """
    Transforms the input grid by rotating it 180 degrees.

    Args:
        input_grid (list of list of int): The input 2D grid to be transformed.

    Returns:
        list of list of int: The output grid after applying the 180-degree rotation.
    """
    # Reverse the order of the rows to rotate vertically
    reversed_rows = input_grid[::-1]
    
    # Reverse each row to rotate horizontally
    rotated_grid = [row[::-1] for row in reversed_rows]
    
    return rotated_grid
