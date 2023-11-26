import argparse
import os
import pandas as pd

from ..lib import *



def make_alliance(first_faction_name: VANILLA_FACTION_KEY_HINTS, second_faction_name: VANILLA_FACTION_KEY_HINTS):
    '''
    example:
        make_alliance('maratha', 'mysore')
    '''

    assert first_faction_name in FACTION_IDS['name'].to_list(), f"{first_faction_name} is not present in {FACTION_IDS_PATH}."
    assert second_faction_name in FACTION_IDS['name'].to_list(), f"{second_faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    first_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(first_faction_name)].iloc[0]
    second_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(second_faction_name)].iloc[0]

    alliance_info = DIPLOMACY_ATTITUDES_TABLE[DIPLOMACY_ATTITUDES_TABLE['attitude'].eq('alliance')].iloc[0]

    # Setting protectorate ID

    first_faction = Faction(os.path.join(OUTPUT_DIR, 'factions', second_faction_info['path']))

    if first_faction.get_protectorate_id() == second_faction_info['id']:
        first_faction.set_protectorate_id('0')

    second_faction = Faction(os.path.join(OUTPUT_DIR, 'factions', second_faction_info['path']))

    if second_faction.get_protectorate_id() == first_faction_info['id']:
        second_faction.set_protectorate_id('0')

    # Setting first diplomatic relationships

    first_diplomacy = Diplomacy(os.path.join(OUTPUT_DIR, 'diplomacy', first_faction_info['diplomacy_path']))

    first_relationship = first_diplomacy.get_relationship(second_faction_info['id'])

    first_relationship.set_if_allied_10('10')
    first_relationship.set_if_allied_20('20')
    first_relationship.set_relationship('allied')
    first_relationship.set_relationship_with_protectorate('allied')
    first_relationship.get_attitudes()[1].clear()
    first_relationship.get_attitudes()[7].clear()
    first_relationship.set_income_from_protectorate('0')
    first_relationship.set_payment_to_patron('0')

    first_alliance = first_relationship.get_attitudes()[1]
    first_alliance.clear()
    first_alliance.set_drift(alliance_info['drift'])
    first_alliance.set_current(alliance_info['value'])
    first_alliance.set_limit(alliance_info['cap'])
    first_alliance.set_active1('yes')

    first_relationship.update_overall_attitude()

    # Setting second diplomatic relationships

    second_diplomacy = Diplomacy(os.path.join(OUTPUT_DIR, 'diplomacy', second_faction_info['diplomacy_path']))

    second_relationship = second_diplomacy.get_relationship(first_faction_info['id'])

    second_relationship.set_if_allied_10('10')
    second_relationship.set_if_allied_20('20')
    second_relationship.set_relationship('allied')
    second_relationship.set_relationship_with_protectorate('allied')
    second_relationship.get_attitudes()[7].clear()
    second_relationship.set_income_from_protectorate('0')
    second_relationship.set_payment_to_patron('0')

    second_alliance = second_relationship.get_attitudes()[1]
    second_alliance.clear()
    second_alliance.set_drift(alliance_info['drift'])
    second_alliance.set_current(alliance_info['value'])
    second_alliance.set_limit(alliance_info['cap'])
    second_alliance.set_active1('yes')

    second_relationship.update_overall_attitude()

    # Applying changes

    first_diplomacy.write_xml()

    second_diplomacy.write_xml()

    if first_faction.get_protectorate_id() == second_faction_info['id']:
        first_faction.write_xml()

    if second_faction.get_protectorate_id() == first_faction_info['id']:
        second_faction.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python make_alliance.py maratha mysore')
    parser.add_argument('first_faction_name', type=str, help='')
    parser.add_argument('second_faction_name', type=str, help='')
    args = parser.parse_args()

    first_faction_name = args.first_faction_name
    second_faction_name = args.second_faction_name

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)

    make_alliance(first_faction_name, second_faction_name)
