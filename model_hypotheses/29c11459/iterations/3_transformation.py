def transform_grid(input_grid):
    """
    Transforms the input grid by reconstructing each row based on the following rules:
        - If a row contains exactly two non-background colors:
            - The first five cells are filled with the first color.
            - The sixth cell is filled with the separator color (5 - Gray).
            - The last five cells are filled with the second color.
        - If a row contains no non-background colors:
            - The row remains entirely as background (0).
        - If a row contains exactly one non-background color:
            - The first five cells are filled with the color.
            - The sixth cell is filled with the separator color (5 - Gray).
            - The last five cells are filled with the same color.
        - Any other cases are considered invalid based on the current examples.
    
    Args:
        input_grid (list of list of int): The input 2D grid.
    
    Returns:
        list of list of int: The transformed output grid.
    """
    output_grid = []
    separator_color = 5  # Gray
    first_segment_length = 5
    separator_length = 1
    second_segment_length = 5

    for row_idx, in_row in enumerate(input_grid):
        # Extract non-background colors preserving order
        in_colors = [color for color in in_row if color != 0]
        
        if not in_colors:
            # Row remains all background
            out_row = [0]*11
        elif len(in_colors) == 1:
            # Single color: fill first five and last five with the same color, separator in the middle
            color = in_colors[0]
            out_row = [color]*first_segment_length + [separator_color] + [color]*second_segment_length
        elif len(in_colors) == 2:
            # Two colors: fill first five with first color, separator, last five with second color
            first_color, second_color = in_colors
            out_row = [first_color]*first_segment_length + [separator_color] + [second_color]*second_segment_length
        else:
            # For more than two colors, based on current examples, we cannot determine the transformation
            # Hence, raise an exception or handle accordingly
            raise ValueError(f"Row {row_idx}: Unsupported number of non-background colors ({len(in_colors)}).")
        
        output_grid.append(out_row)
    
    return output_grid
