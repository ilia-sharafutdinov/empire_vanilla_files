import argparse
import os
import pandas as pd

from ..lib import *



def set_historical_attitude(
    subject_faction_name: VANILLA_FACTION_KEY_HINTS,
    object_faction_name: VANILLA_FACTION_KEY_HINTS,
    historical_attitude: int = 0,
    drift: int = 1,
    limit: int = 0):
    '''
    example:
        set_historical_attitude('russia', 'georgia', -90)
    '''

    assert subject_faction_name in FACTION_IDS['name'].to_list(), f"{subject_faction_name} is not present in {FACTION_IDS_PATH}."
    assert object_faction_name in FACTION_IDS['name'].to_list(), f"{object_faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    subject_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(subject_faction_name)].iloc[0]
    object_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(object_faction_name)].iloc[0]

    drift = -drift if historical_attitude > 0 else drift

    # Setting subject diplomatic relationships

    subject_diplomacy = Diplomacy(os.path.join(OUTPUT_DIR, 'diplomacy', subject_faction_info['diplomacy_path']))

    subject_relationship = subject_diplomacy.get_relationship(object_faction_info['id'])

    subject_historical_attitude = subject_relationship.get_attitudes()[17]
    subject_historical_attitude.clear()
    if historical_attitude != 0:
        subject_historical_attitude.set_drift(str(drift))
        subject_historical_attitude.set_current(str(historical_attitude))
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
        '  python set_historical_attitude.py russia georgia --historical_attitude -90')
    parser.add_argument('subject_faction_name', type=str, help='')
    parser.add_argument('object_faction_name', type=str, help='')
    parser.add_argument('-a', '--historical_attitude', type=int, default=0, help='')
    parser.add_argument('-d', '--drift', type=int, default=1, help='')
    parser.add_argument('-l', '--limit', type=int, default=0, help='')
    args = parser.parse_args()

    subject_faction_name = args.subject_faction_name
    object_faction_name = args.object_faction_name
    historical_attitude = args.historical_attitude
    drift = args.drift
    limit = args.limit

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)

    set_historical_attitude(subject_faction_name, object_faction_name, historical_attitude, drift, limit)
