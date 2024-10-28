import json
import os
from shared.config.config import TRAINING_DATA_DIR, TEST_DATA_DIR

def load_task_data(task_id: str, data_type: str = 'train') -> dict:
    """
    Loads task data from JSON files.

    Args:
        task_id (str): The task ID.
        data_type (str): 'train' or 'test'.

    Returns:
        dict: The loaded task data.
    """
    if data_type == 'train':
        data_path = os.path.join(TRAINING_DATA_DIR, f"{task_id}.json")
    elif data_type == 'test':
        data_path = os.path.join(TEST_DATA_DIR, f"{task_id}.json")
    else:
        raise ValueError("data_type must be 'train' or 'test'.")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file {data_path} does not exist.")

    with open(data_path, 'r') as f:
        return json.load(f)
