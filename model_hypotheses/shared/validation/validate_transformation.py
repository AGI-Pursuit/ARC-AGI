# shared/validation/validate_transformation.py

import os
import json
import importlib.util
import logging
from typing import Callable
from shared.utils.data_loader import load_task_data
from shared.utils.compare import compare_and_prepare_example
from shared.utils.plotter import plot_all_examples
from shared.config.config import MODEL_HYPOTHESES_DIR

def load_transformation(transform_file: str) -> Callable:
    """
    Dynamically load the transformation function from the given file.

    Args:
        transform_file (str): Path to the transformation.py file.

    Returns:
        Callable: The transformation function.
    """
    module_name = os.path.splitext(os.path.basename(transform_file))[0]
    spec = importlib.util.spec_from_file_location(module_name, transform_file)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)  # type: ignore
    except Exception as e:
        logging.error(f"Error loading transformation module {module_name} from {transform_file}: {e}")
        return None

    # Expecting a function named 'transform_grid'
    if hasattr(module, 'transform_grid') and callable(getattr(module, 'transform_grid')):
        return getattr(module, 'transform_grid')
    else:
        logging.error(f"'transform_grid' function not found in {transform_file}.")
        return None

def validate_transformation(task_id: str, iteration_number: int, iteration_type: str):
    if iteration_type != 'transformation':
        logging.info(f"Iteration {iteration_number} is not a transformation iteration.")
        return
    
    transform_file = os.path.join(MODEL_HYPOTHESES_DIR, task_id, "iterations", f"{iteration_number}_transformation.py")
    if not os.path.exists(transform_file):
        logging.error(f"Transformation file {transform_file} does not exist.")
        return
    
    transform_func = load_transformation(transform_file)
    if not transform_func:
        logging.error(f"No valid transformation function found for iteration {iteration_number} in task {task_id}.")
        return
    
    try:
        task_data = load_task_data(task_id, data_type='train')
    except Exception as e:
        logging.error(f"Error loading training data for task {task_id}: {e}")
        return
    
    all_examples_data = []
    all_training_pass = True  # Flag to track if all training examples pass
    
    for idx, example in enumerate(task_data.get('train', [])):
        input_grid = example.get('input')
        expected_output_grid = example.get('output')
        try:
            transformed_output_grid = transform_func(input_grid)
        except Exception as e:
            logging.error(f"Error in transformation function for example {idx} in task {task_id}, iteration {iteration_number}: {e}")
            all_training_pass = False
            continue
        
        example_data = compare_and_prepare_example(
            input_grid, expected_output_grid, transformed_output_grid, idx, example_type='Training'
        )
        all_examples_data.append(example_data)
        
        if example_data['match_status'] != 'Transformed Correctly':
            all_training_pass = False
    
    # Process test examples if all training examples pass
    if all_training_pass:
        logging.info("\nAll training examples passed. Proceeding to test examples...\n")
        for idx, example in enumerate(task_data.get('test', [])):
            input_grid = example.get('input')
            expected_output_grid = example.get('output', [])
            
            try:
                transformed_output_grid = transform_func(input_grid)
            except Exception as e:
                logging.error(f"Error in transformation function for test example {idx} in task {task_id}, iteration {iteration_number}: {e}")
                continue
            
            example_data = compare_and_prepare_example(
                input_grid, expected_output_grid, transformed_output_grid, idx, example_type='Test'
            )
            all_examples_data.append(example_data)
    else:
        logging.info("\nNot all training examples passed. Please review the transformation function and try again.\n")
    
    # Plot all examples
    try:
        plot_all_examples(all_examples_data)
    except Exception as e:
        logging.error(f"Error during plotting examples for task {task_id}, iteration {iteration_number}: {e}")
    
    # Save results
    results_dir = os.path.join(MODEL_HYPOTHESES_DIR, task_id, "results")
    os.makedirs(results_dir, exist_ok=True)
    results_path = os.path.join(results_dir, f"{iteration_number}_transformation_results.json")
    try:
        with open(results_path, 'w') as f:
            json.dump(all_examples_data, f, indent=4)
        logging.info(f"Transformation results for task {task_id}, iteration {iteration_number} saved to {results_path}.")
    except Exception as e:
        logging.error(f"Error saving transformation results to {results_path}: {e}")