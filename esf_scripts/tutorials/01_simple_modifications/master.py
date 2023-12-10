import os
import shutil
import builtins
import warnings
from tqdm import tqdm

from dotenv import load_dotenv
load_dotenv()

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from scripts.lib import *

from scripts.aggregators import *
from scripts.characters import *
from scripts.diplomacy import *
from scripts.factions import *
from scripts.governments import *
from scripts.miscellaneous import *
from scripts.regions import *



try:

    # Initiating

    print_block('Initiating.')

    if OUTPUT_DIR != STARTPOS_DIR:
        print('Copying startpos.')
        if os.path.exists(OUTPUT_DIR):
            shutil.rmtree(OUTPUT_DIR)
        shutil.copytree(STARTPOS_DIR, OUTPUT_DIR)

    print('Initialising global variables.')

    # https://stackoverflow.com/questions/15959534/visibility-of-global-variables-in-imported-modules
    builtins.CHARACTER_IDS = get_character_ids()
    builtins.FACTION_IDS = get_faction_ids()
    builtins.GOVERNORSHIP_IDS = get_governorship_ids()
    builtins.REGION_IDS = get_region_ids()
    builtins.REGION_SLOT_IDS = get_region_slot_ids()






    # User-defined flow start (insert your code here) #########################################################################

    # During the course of the tutorial, the line below should start looking like:
    # change_faction_majority('denmark', 'yes')

    # User-defined flow end ###################################################################################################






except Exception as exception:

    # Rethrowing exception

    warnings.warn('A critical error happened during execution.')

    raise exception

finally:

    # Finalising

    print_block('Finalising.')

    print('Clearing recruitment manager IDs from bdi_pool.')
    remove_recruitment_ids()

    print('Writing tables.')
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    if hasattr(builtins, 'CHARACTER_IDS'):
        builtins.CHARACTER_IDS.to_csv(CHARACTER_IDS_PATH, sep='\t', index=False)
    if hasattr(builtins, 'FACTION_IDS'):
        builtins.FACTION_IDS.to_csv(FACTION_IDS_PATH, sep='\t', index=False)
    if hasattr(builtins, 'GOVERNORSHIP_IDS'):
        builtins.GOVERNORSHIP_IDS.to_csv(GOVERNORSHIP_IDS_PATH, sep='\t', index=False)
    if hasattr(builtins, 'REGION_IDS'):
        builtins.REGION_IDS.to_csv(REGION_IDS_PATH, sep='\t', index=False)
    if hasattr(builtins, 'REGION_SLOT_IDS'):
        builtins.REGION_SLOT_IDS.to_csv(REGION_SLOT_IDS_PATH, sep='\t', index=False)

    print_block('Done.')
