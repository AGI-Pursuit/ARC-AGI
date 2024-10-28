# shared/utils/compare.py

import numpy as np
from shared.utils.colors import color_mappings


def compare_and_prepare_example(input_grid, expected_output_grid, transformed_output_grid, idx, example_type='Training'):
    """
    Compares the transformed output grid with the expected output grid, and prepares the example data for plotting.
    
    Parameters:
        input_grid (list of list of int): The input grid.
        expected_output_grid (list of list of int): The expected output grid.
        transformed_output_grid (list of list of int): The transformed output grid.
        idx (int): The index of the example.
        example_type (str): The type of example, either 'Training' or 'Test'.
    
    Returns:
        dict: A dictionary containing the example data for plotting.
    """
    # Convert grids to numpy arrays
    input_array = np.array(input_grid)
    transformed_output_array = np.array(transformed_output_grid)
    expected_output_array = np.array(expected_output_grid) if expected_output_grid is not None else np.array([[]])

    # Check dimensions
    transformed_shape = transformed_output_array.shape
    expected_shape = expected_output_array.shape

    dimensions_match = transformed_shape == expected_shape

    # Prepare match status
    if expected_output_grid is None:
        match_status = ''  # For test examples without expected outputs
    elif not dimensions_match:
        match_status = 'Dimensions Mismatch'
    else:
        if np.array_equal(transformed_output_array, expected_output_array):
            match_status = 'Transformed Correctly'
        else:
            match_status = 'Mismatch Detected'

    # Logging
    print(f"{example_type} Example {idx}:")
    print("Transformed Output Grid:")
    print(transformed_output_array)

    if expected_output_grid is not None:
        if not dimensions_match:
            print("  Dimensions differ between transformed output and expected output.")
            print(f"  Transformed Output Shape: {transformed_shape}")
            print(f"  Expected Output Shape: {expected_shape}")
            print("  Skipping detailed difference logging due to dimension mismatch.")
        elif match_status == 'Mismatch Detected':
            # Compute differences
            difference_grid = (transformed_output_array != expected_output_array).astype(int)
            differences = np.argwhere(difference_grid == 1)
            print("  The transformed output does NOT match the expected output.")
            print("  Differences at positions (row, col):")
            for pos in differences:
                row, col = pos
                transformed_value = transformed_output_array[row, col]
                expected_value = expected_output_array[row, col]
                transformed_color = color_mappings.get(transformed_value, f'Unknown({transformed_value})')
                expected_color = color_mappings.get(expected_value, f'Unknown({expected_value})')
                print(f"    At position ({row}, {col}): transformed = {transformed_color}, expected = {expected_color}")
            # Calculate match percentage
            total_cells = transformed_output_array.size
            differing_cells = differences.shape[0]
            match_percentage = 100 * (total_cells - differing_cells) / total_cells
            print(f"  Match Percentage: {match_percentage:.2f}%")
        else:
            # Transformation correct
            print("  The transformed output matches the expected output.")
    else:
        print("  No expected output provided for this test example.")

    # For visualization, prepare the grids as lists
    grids = [
        input_array.tolist(),
        expected_output_array.tolist() if expected_output_grid is not None else [],
        transformed_output_array.tolist()
    ]
    titles = [
        'Input Grid',
        'Expected Output' if expected_output_grid is not None else 'Expected Output (Not Provided)',
        'Transformed Output'
    ]
    dimensions = [input_array.shape, expected_shape, transformed_shape]

    # Add difference grid if available
    if expected_output_grid is not None and dimensions_match and match_status == 'Mismatch Detected':
        difference_grid = (transformed_output_array != expected_output_array).astype(int)
        grids.append(difference_grid.tolist())
        titles.append('Difference Grid\n(Differences in White)')
        dimensions.append(difference_grid.shape)

    example_data = {
        'grids': grids,  # Now lists instead of ndarrays
        'titles': titles,
        'match_status': match_status,
        'dimensions': dimensions,
        'type': example_type,
        'idx': idx
    }

    return example_data
