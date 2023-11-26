import argparse
import os
import pandas as pd

from ..lib import *



def set_total_attitude(
    subject_faction_name: VANILLA_FACTION_KEY_HINTS,
    object_faction_name: VANILLA_FACTION_KEY_HINTS,
    desired_total_attitude: int = 0,
    drift: int = 1,
    limit: int = 0):
    '''
    example:
        set_total_attitude('austria', 'piedmont_savoy', -85)
    '''

    assert subject_faction_name in FACTION_IDS['name'].to_list(), f"{subject_faction_name} is not present in {FACTION_IDS_PATH}."
    assert object_faction_name in FACTION_IDS['name'].to_list(), f"{object_faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    subject_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(subject_faction_name)].iloc[0]
    object_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(object_faction_name)].iloc[0]

    # Setting subject diplomatic relationships

    subject_diplomacy = Diplomacy(os.path.join(OUTPUT_DIR, 'diplomacy', subject_faction_info['diplomacy_path']))

    subject_relationship = subject_diplomacy.get_relationship(object_faction_info['id'])

    subject_historical_attitude = subject_relationship.get_attitudes()[17]

    current_total_attitude = subject_relationship.get_current_total()
    current_historical_attitude = int(subject_historical_attitude.get_current()) if subject_historical_attitude.get_current() else 0

    difference_to_apply = desired_total_attitude - current_total_attitude + current_historical_attitude

    drift = -drift if difference_to_apply > 0 else drift

    subject_historical_attitude.clear()
    if difference_to_apply != 0:
        subject_historical_attitude.set_drift(str(drift))
        subject_historical_attitude.set_current(str(difference_to_apply))
        subject_historical_attitude.set_limit(str(limit))
        subject_historical_attitude.set_active1('yes')

    subject_relationship.update_overall_attitude()

    # Applying changes

    subject_diplomacy.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python set_total_attitude.py austria piedmont_savoy --desired_total_attitude -85')
    parser.add_argument('subject_faction_name', type=str, help='')
    parser.add_argument('object_faction_name', type=str, help='')
    parser.add_argument('-a', '--desired_total_attitude', type=int, default=0, help='')
    parser.add_argument('-d', '--drift', type=int, default=1, help='')
    parser.add_argument('-l', '--limit', type=int, default=0, help='')
    args = parser.parse_args()

    subject_faction_name = args.subject_faction_name
    object_faction_name = args.object_faction_name
    desired_total_attitude = args.desired_total_attitude
    drift = args.drift
    limit = args.limit

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)

    set_total_attitude(subject_faction_name, object_faction_name, desired_total_attitude, drift, limit)
