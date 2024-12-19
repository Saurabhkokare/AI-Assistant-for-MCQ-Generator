import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

log_path=os.path.join(os.getcwd(),"logs")

log_filepath=os.makedirs(log_path,exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    filename=log_filepath,
    format="[%(asctime)s %(lineno)d %(name)s - %(levelname)s - %(message)s]"
)