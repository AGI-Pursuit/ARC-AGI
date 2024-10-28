# run_all.py

import os
import argparse
import re
import logging
from shared.validation.validate_hypotheses import run_hypotheses
from shared.validation.validate_transformation import validate_transformation
from shared.config.config import MODEL_HYPOTHESES_DIR

def extract_iteration_info(filename: str):
    """
    Extracts iteration number and type from the filename.

    Args:
        filename (str): The name of the iteration file (e.g., '1_hypotheses.py').

    Returns:
        tuple: (iteration_number: int, iteration_type: str) or (None, None) if invalid.
    """
    match = re.match(r"(\d+)_(hypotheses|transformation)\.py$", filename)
    if match:
        iteration_number = int(match.group(1))
        iteration_type = match.group(2)
        return iteration_number, iteration_type
    else:
        return None, None

def run_specific_iteration(task_id: str, iteration_number: int, iteration_type: str):
    """
    Runs a specific iteration for a given task.

    Args:
        task_id (str): The task ID.
        iteration_number (int): The iteration number.
        iteration_type (str): The type of iteration ('hypotheses' or 'transformation').
    """
    if iteration_type == 'hypotheses':
        run_hypotheses(task_id, iteration_number, iteration_type)
    elif iteration_type == 'transformation':
        validate_transformation(task_id, iteration_number, iteration_type)
    else:
        logging.error(f"Unknown iteration type '{iteration_type}' for iteration {iteration_number} in task {task_id}.")

def run_all_tasks_and_iterations(specific_task=None, specific_iteration=None):
    """
    Iterates through all tasks and their iterations to run hypotheses and transformations.

    Args:
        specific_task (str, optional): Specific task ID to run. Runs all if None.
        specific_iteration (int, optional): Specific iteration number to run. Runs all if None.
    """
    tasks = [d for d in os.listdir(MODEL_HYPOTHESES_DIR) if os.path.isdir(os.path.join(MODEL_HYPOTHESES_DIR, d))]
    
    for task_id in tasks:
        if specific_task and task_id != specific_task:
            continue  # Skip tasks not matching the specific task

        task_iterations_dir = os.path.join(MODEL_HYPOTHESES_DIR, task_id, "iterations")
        if not os.path.exists(task_iterations_dir):
            logging.warning(f"No iterations directory found for task {task_id}. Skipping.")
            continue

        # List and sort iteration files based on iteration number
        iteration_files = [f for f in os.listdir(task_iterations_dir) if f.endswith('.py')]
        sorted_iterations = sorted(iteration_files, key=lambda x: int(re.match(r"(\d+)_.*\.py$", x).group(1)) if re.match(r"(\d+)_.*\.py$", x) else 0)
        
        for filename in sorted_iterations:
            iteration_number, iteration_type = extract_iteration_info(filename)
            if iteration_number is None:
                logging.warning(f"Skipping unrecognized file format: {filename}")
                continue

            if specific_iteration and iteration_number != specific_iteration:
                continue  # Skip iterations not matching the specific iteration

            logging.info(f"\n=== Processing Task: {task_id}, Iteration: {iteration_number} ({iteration_type}) ===")
            run_specific_iteration(task_id, iteration_number, iteration_type)

def main():
    parser = argparse.ArgumentParser(description="Run all tasks and their iterations.")
    parser.add_argument('--task_id', type=str, help='Specific task ID to run.')
    parser.add_argument('--iteration', type=int, help='Specific iteration number to run.')

    args = parser.parse_args()

    run_all_tasks_and_iterations(specific_task=args.task_id, specific_iteration=args.iteration)

if __name__ == "__main__":
    main()
