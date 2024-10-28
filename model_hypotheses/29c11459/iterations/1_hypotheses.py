def is_horizontal_expansion(input_grid, output_grid):
    """
    Checks if single colored cells in a row are expanded horizontally into multiple consecutive cells of the same color.
    Returns:
        bool: True if horizontal expansion is consistent, False otherwise.
        Optional[str]: Details about the discrepancy if False.
    """
    for row_idx, (in_row, out_row) in enumerate(zip(input_grid, output_grid)):
        in_colors = [color for color in in_row if color != 0]
        out_colors = [color for color in out_row if color != 0]
        if not in_colors and not out_colors:
            continue
        if len(in_colors) != len(out_colors) - 1:  # Accounting for separator
            return False, f"Row {row_idx}: Number of colors after expansion does not match expectation."
    return True

def is_separator_inserted(input_grid, output_grid):
    """
    Checks if a separator color (5) is inserted between different color expansions within the same row.
    Returns:
        bool: True if separator is correctly inserted, False otherwise.
        Optional[str]: Details about the discrepancy if False.
    """
    separator = 5
    for row_idx, (in_row, out_row) in enumerate(zip(input_grid, output_grid)):
        in_colors = [color for color in in_row if color != 0]
        if len(in_colors) <= 1:
            continue  # No separator needed
        # Find positions of colors in output
        out_non_zero = [color for color in out_row if color != 0]
        expected = []
        for color in in_colors:
            expected.extend([color] * 5)
            expected.append(separator)
        expected = expected[:-1]  # Remove last separator
        if out_non_zero != expected:
            return False, f"Row {row_idx}: Separator not correctly inserted."
    return True

def is_fixed_expansion_factor(input_grid, output_grid, factor=5):
    """
    Checks if each single colored cell in the input is expanded into exactly 'factor' consecutive cells in the output.
    Returns:
        bool: True if expansion factor is consistent, False otherwise.
        Optional[str]: Details about the discrepancy if False.
    """
    for row_idx, (in_row, out_row) in enumerate(zip(input_grid, output_grid)):
        in_colors = [color for color in in_row if color != 0]
        out_non_zero = [color for color in out_row if color != 0]
        expected = []
        for color in in_colors:
            expected.extend([color] * factor)
            expected.append(5)  # Separator
        expected = expected[:-1]  # Remove last separator if exists
        if out_non_zero != expected:
            return False, f"Row {row_idx}: Expansion factor mismatch."
    return True

def is_row_wise_transformation(input_grid, output_grid):
    """
    Checks if the transformation is applied independently to each row without affecting other rows.
    Returns:
        bool: True if transformation is row-wise, False otherwise.
        Optional[str]: Details about the discrepancy if False.
    """
    for row_idx, (in_row, out_row) in enumerate(zip(input_grid, output_grid)):
        if in_row.count(0) != out_row.count(0):
            return False, f"Row {row_idx}: Background cells altered."
    return True

def is_color_preserved(input_grid, output_grid):
    """
    Checks if the original colors in the input are preserved in the output after expansion and separator insertion.
    Returns:
        bool: True if colors are preserved, False otherwise.
        Optional[str]: Details about the discrepancy if False.
    """
    for row_idx, (in_row, out_row) in enumerate(zip(input_grid, output_grid)):
        in_colors = set(color for color in in_row if color != 0)
        out_colors = set(color for color in out_row if color != 0)
        expected_colors = in_colors.union({5})  # Separator is 5
        if not out_colors.issuperset(in_colors):
            return False, f"Row {row_idx}: Colors not preserved."
    return True

def is_single_separator_insertion(input_grid, output_grid):
    """
    Checks if only one separator (5) is inserted between multiple color expansions within a row.
    Returns:
        bool: True if only single separators are inserted, False otherwise.
        Optional[str]: Details about the discrepancy if False.
    """
    separator = 5
    for row_idx, (in_row, out_row) in enumerate(zip(input_grid, output_grid)):
        in_colors = [color for color in in_row if color != 0]
        if len(in_colors) <= 1:
            continue
        out_non_zero = [color for color in out_row if color != 0]
        separator_count = out_non_zero.count(separator)
        expected_separators = len(in_colors) - 1
        if separator_count != expected_separators:
            return False, f"Row {row_idx}: Incorrect number of separators."
    return True

def is_no_rotation_or_scaling(input_grid, output_grid):
    """
    Checks if the transformation does not involve rotation or scaling of the grid.
    Returns:
        bool: True if no rotation or scaling is involved, False otherwise.
        Optional[str]: Details about the discrepancy if False.
    """
    if len(input_grid) != len(output_grid):
        return False, "Grid height changed."
    for in_row, out_row in zip(input_grid, output_grid):
        if len(in_row) != len(out_row):
            return False, "Grid width changed."
    return True

def is_background_preserved(input_grid, output_grid):
    """
    Checks if background cells (0) remain unchanged in both input and output grids.
    Returns:
        bool: True if background is preserved, False otherwise.
        Optional[str]: Details about the discrepancy if False.
    """
    for row_idx, (in_row, out_row) in enumerate(zip(input_grid, output_grid)):
        for col_idx, (in_cell, out_cell) in enumerate(zip(in_row, out_row)):
            if in_cell == 0 and out_cell != 0:
                return False, f"Row {row_idx}, Column {col_idx}: Background altered."
    return True
