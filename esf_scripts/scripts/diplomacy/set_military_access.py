import argparse
import os
import pandas as pd

from ..lib import *



def set_military_access(subject_faction_name: VANILLA_FACTION_KEY_HINTS, object_faction_name: VANILLA_FACTION_KEY_HINTS, turns: int = 0):
    '''
    example:
        set_military_access('venice', 'austria', 0)
    '''

    assert subject_faction_name in FACTION_IDS['name'].to_list(), f"{subject_faction_name} is not present in {FACTION_IDS_PATH}."
    assert object_faction_name in FACTION_IDS['name'].to_list(), f"{object_faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    subject_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(subject_faction_name)].iloc[0]
    object_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(object_faction_name)].iloc[0]

    turns = str(turns)

    # Setting subject diplomatic relationships

    subject_diplomacy = Diplomacy(os.path.join(OUTPUT_DIR, 'diplomacy', subject_faction_info['diplomacy_path']))

    subject_relationship = subject_diplomacy.get_relationship(object_faction_info['id'])

    subject_relationship.set_military_access_turns(turns)

    subject_relationship.update_overall_attitude()

    # Applying changes

    subject_diplomacy.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python set_military_access.py venice austria --turns 0')
    parser.add_argument('subject_faction_name', type=str, help='')
    parser.add_argument('object_faction_name', type=str, help='')
    parser.add_argument('-t', '--turns', type=int, default=0, help='')
    args = parser.parse_args()

    subject_faction_name = args.subject_faction_name
    object_faction_name = args.object_faction_name
    turns = args.turns

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)

    set_military_access(subject_faction_name, object_faction_name, turns)
