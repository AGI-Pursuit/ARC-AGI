# shared/validation/validate_hypotheses.py

import os
import json
import importlib.util
import logging
from typing import Callable, Dict
from shared.utils.data_loader import load_task_data
from shared.config.config import MODEL_HYPOTHESES_DIR

def load_hypotheses(hypotheses_file: str) -> Dict[str, Callable]:
    """
    Dynamically load all hypothesis functions from the given file.

    Args:
        hypotheses_file (str): Path to the hypotheses.py file.

    Returns:
        Dict[str, Callable]: Mapping from function names to functions.
    """
    hypotheses = {}
    module_name = os.path.splitext(os.path.basename(hypotheses_file))[0]
    spec = importlib.util.spec_from_file_location(module_name, hypotheses_file)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)  # type: ignore
    except Exception as e:
        logging.error(f"Error loading module {module_name} from {hypotheses_file}: {e}")
        return hypotheses

    # Iterate through all attributes of the module to find callable functions
    for attr_name in dir(module):
        if not attr_name.startswith("__"):
            attr = getattr(module, attr_name)
            if callable(attr):
                hypotheses[attr_name] = attr

    if not hypotheses:
        logging.warning(f"No callable hypothesis functions found in {hypotheses_file}.")

    return hypotheses

def run_hypotheses(task_id: str, iteration_number: int, iteration_type: str):
    """
    Runs all hypotheses for a specific task and iteration.

    Args:
        task_id (str): The task ID.
        iteration_number (int): The iteration number.
        iteration_type (str): The type of iteration ('hypotheses' or 'transformation').
    """
    if iteration_type != 'hypotheses':
        logging.info(f"Iteration {iteration_number} is not a hypotheses iteration.")
        return

    hypotheses_file = os.path.join(MODEL_HYPOTHESES_DIR, task_id, "iterations", f"{iteration_number}_hypotheses.py")
    if not os.path.exists(hypotheses_file):
        logging.error(f"Hypotheses file {hypotheses_file} does not exist.")
        return

    hypotheses = load_hypotheses(hypotheses_file)
    if not hypotheses:
        logging.warning(f"No hypotheses to run for iteration {iteration_number} in task {task_id}.")
        return

    try:
        task_data = load_task_data(task_id, data_type='train')
    except Exception as e:
        logging.error(f"Error loading task data for task {task_id}: {e}")
        return

    results = []
    for idx, example in enumerate(task_data.get('train', [])):
        input_grid = example.get('input')
        output_grid = example.get('output')
        example_result = {'example_index': idx}

        for name, func in hypotheses.items():
            try:
                result = func(input_grid, output_grid)
            except Exception as e:
                result = f"Error: {e}"
                logging.error(f"Error running hypothesis '{name}' for example {idx} in task {task_id}, iteration {iteration_number}: {e}")
            example_result[name] = result

        results.append(example_result)

    # Save results
    results_dir = os.path.join(MODEL_HYPOTHESES_DIR, task_id, "results")
    os.makedirs(results_dir, exist_ok=True)
    results_path = os.path.join(results_dir, f"{iteration_number}_hypotheses_results.json")
    try:
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=4)
        logging.info(f"Hypotheses results for task {task_id}, iteration {iteration_number} saved to {results_path}.")
    except Exception as e:
        logging.error(f"Error saving hypotheses results to {results_path}: {e}")
