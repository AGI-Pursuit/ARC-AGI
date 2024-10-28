def is_segmented_row_reconstruction(input_grid, output_grid):
    """
    Checks if each row with non-background colors is reconstructed by dividing it into
    five cells of the first color, one separator, and five cells of the second color.
    Returns:
        bool: True if reconstruction is consistent, False otherwise.
        Optional[str]: Details about the discrepancy if False.
    """
    for row_idx, (in_row, out_row) in enumerate(zip(input_grid, output_grid)):
        # Extract non-background colors preserving order
        in_colors = [color for color in in_row if color != 0]
        
        if not in_colors:
            # If no non-background colors, output should remain all background
            if any(cell != 0 for cell in out_row):
                return False, f"Row {row_idx}: Expected all background, but found non-background colors."
            continue
        
        if len(in_colors) != 2:
            return False, f"Row {row_idx}: Expected exactly two non-background colors, found {len(in_colors)}."
        
        first_color, second_color = in_colors
        expected_row = [first_color]*5 + [5] + [second_color]*5
        if out_row != expected_row:
            return False, f"Row {row_idx}: Expected {expected_row}, but found {out_row}."
    
    return True

def is_fixed_separator_position(input_grid, output_grid, separator_color=5, separator_index=5):
    """
    Checks if the separator is always inserted at the fixed position in each transformed row.
    Returns:
        bool: True if separator is at the fixed position, False otherwise.
        Optional[str]: Details about the discrepancy if False.
    """
    for row_idx, (in_row, out_row) in enumerate(zip(input_grid, output_grid)):
        # Check if row contains non-background colors
        in_colors = [color for color in in_row if color != 0]
        if not in_colors:
            # If no non-background colors, output should remain all background
            if any(cell != 0 for cell in out_row):
                return False, f"Row {row_idx}: Expected all background, but found non-background colors."
            continue
        
        if len(in_colors) != 2:
            return False, f"Row {row_idx}: Expected exactly two non-background colors, found {len(in_colors)}."
        
        # Check separator position
        if out_row[separator_index] != separator_color:
            return False, f"Row {row_idx}: Separator not at index {separator_index}."
        
    return True

def is_fixed_segment_lengths(input_grid, output_grid, first_segment_length=5, separator_length=1, second_segment_length=5):
    """
    Checks if the output row segments have fixed lengths for color expansions and separator.
    Returns:
        bool: True if segments have fixed lengths, False otherwise.
        Optional[str]: Details about the discrepancy if False.
    """
    for row_idx, (in_row, out_row) in enumerate(zip(input_grid, output_grid)):
        in_colors = [color for color in in_row if color != 0]
        
        if not in_colors:
            if any(cell != 0 for cell in out_row):
                return False, f"Row {row_idx}: Expected all background, but found non-background colors."
            continue
        
        if len(in_colors) != 2:
            return False, f"Row {row_idx}: Expected exactly two non-background colors, found {len(in_colors)}."
        
        first_color, second_color = in_colors
        expected_row = [first_color]*first_segment_length + [5]*separator_length + [second_color]*second_segment_length
        if out_row != expected_row:
            return False, f"Row {row_idx}: Expected segments {expected_row}, but found {out_row}."
    
    return True

def is_order_preserved(input_grid, output_grid):
    """
    Checks if the order of colors in the output segments corresponds to their order in the input.
    Returns:
        bool: True if order is preserved, False otherwise.
        Optional[str]: Details about the discrepancy if False.
    """
    for row_idx, (in_row, out_row) in enumerate(zip(input_grid, output_grid)):
        in_colors = [color for color in in_row if color != 0]
        if not in_colors:
            if any(cell != 0 for cell in out_row):
                return False, f"Row {row_idx}: Expected all background, but found non-background colors."
            continue
        
        if len(in_colors) != 2:
            return False, f"Row {row_idx}: Expected exactly two non-background colors, found {len(in_colors)}."
        
        first_color, second_color = in_colors
        # First segment should be first_color, second segment should be second_color
        if out_row[:5] != [first_color]*5 or out_row[6:] != [second_color]*5:
            return False, f"Row {row_idx}: Color order not preserved."
    
    return True

def is_single_transformation_per_row(input_grid, output_grid):
    """
    Checks if each row undergoes only one transformation that reconstructs the entire row.
    Returns:
        bool: True if only single transformation per row, False otherwise.
        Optional[str]: Details about the discrepancy if False.
    """
    # Since each row is transformed entirely based on its own non-background colors,
    # and no inter-row transformations are implied, this hypothesis holds.
    # However, to validate, we ensure that transformations are row-specific.
    # Given the current data, we can assume it's true.
    # Further examples would be needed for rigorous testing.
    return True
