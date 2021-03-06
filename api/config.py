import os
import sys
import configparser


# Dict parsed from config file
CONFIG = configparser.ConfigParser()

# Root directory of the bot
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to config file
CONFIG_FILE = os.path.join(BASE_DIR, 'config.ini')

# Where to store static data files
DATA_DIR = os.path.join(BASE_DIR, 'data')


# def create_output_dir():
#     try:
#         os.mkdir(OUT_DIR)
#         logger.info(f"Created output directory at {OUT_DIR}.")
#     except FileExistsError:
#         logger.info(f"Output directory already exists at {OUT_DIR}.")


def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            CONFIG.read_file(f)
    except IOError:
        sys.exit(0)


load_config()