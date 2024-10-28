import os
import logging

# Base Directory (assumes this script is in model_hypotheses/shared/config/)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# Directories
MODEL_HYPOTHESES_DIR = os.path.join(BASE_DIR, "model_hypotheses")
DATA_DIR = os.path.join(BASE_DIR, "data")
TRAINING_DATA_DIR = os.path.join(DATA_DIR, "training")
TEST_DATA_DIR = os.path.join(DATA_DIR, "test")
MODEL_OUTPUTS_DIR = os.path.join(BASE_DIR, "model_outputs")
SHARED_VALIDATION_DIR = os.path.join(BASE_DIR, "model_hypotheses", "shared", "validation")
SHARED_UTILS_DIR = os.path.join(BASE_DIR, "model_hypotheses", "shared", "utils")

# Logging Configuration
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "execution.log"),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
