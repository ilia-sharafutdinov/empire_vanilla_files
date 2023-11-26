import argparse
import os
import pandas as pd

from ..lib import *



def make_protectorate(patron_faction_name: VANILLA_FACTION_KEY_HINTS, protectorate_faction_name: VANILLA_FACTION_KEY_HINTS):
    '''
    example:
        make_protectorate('russia', 'georgia')
    '''

    assert patron_faction_name in FACTION_IDS['name'].to_list(), f"{patron_faction_name} is not present in {FACTION_IDS_PATH}."
    assert protectorate_faction_name in FACTION_IDS['name'].to_list(), f"{protectorate_faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    patron_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(patron_faction_name)].iloc[0]
    protectorate_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(protectorate_faction_name)].iloc[0]

    alliance_info = DIPLOMACY_ATTITUDES_TABLE[DIPLOMACY_ATTITUDES_TABLE['attitude'].eq('alliance')].iloc[0]

    # Setting protectorate ID

    protectorate_faction = Faction(os.path.join(OUTPUT_DIR, 'factions', protectorate_faction_info['path']))

    protectorate_faction.set_protectorate_id(patron_faction_info['id'])

    # Setting protectorate diplomatic relationships

    protectorate_diplomacy = Diplomacy(os.path.join(OUTPUT_DIR, 'diplomacy', protectorate_faction_info['diplomacy_path']))

    for relationship in protectorate_diplomacy.get_relationships():
        if relationship.get_relationship() == 'protectorate':
            raise ValueError(f"Faction '{protectorate_faction_info['name']}' is already a protectorate of faction with ID = {relationship.get_faction_id()}.")

    protectorate_relationship = protectorate_diplomacy.get_relationship(patron_faction_info['id'])

    protectorate_relationship.set_if_allied_10('10')
    protectorate_relationship.set_if_allied_20('20')
    protectorate_relationship.set_relationship('protectorate')
    protectorate_relationship.set_relationship_with_protectorate('protectorate')
    protectorate_relationship.get_attitudes()[7].clear()

    protectorate_alliance = protectorate_relationship.get_attitudes()[1]
    protectorate_alliance.clear()
    protectorate_alliance.set_drift(alliance_info['drift'])
    protectorate_alliance.set_current(alliance_info['value'])
    protectorate_alliance.set_limit(alliance_info['cap'])
    protectorate_alliance.set_active1('yes')

    protectorate_relationship.update_overall_attitude()

    # Setting patron diplomatic relationships

    patron_diplomacy = Diplomacy(os.path.join(OUTPUT_DIR, 'diplomacy', patron_faction_info['diplomacy_path']))

    patron_relationship = patron_diplomacy.get_relationship(protectorate_faction_info['id'])

    patron_relationship.set_if_allied_10('10')
    patron_relationship.set_if_allied_20('20')
    patron_relationship.set_relationship('patron')
    patron_relationship.set_relationship_with_protectorate('patron')
    patron_relationship.get_attitudes()[7].clear()

    patron_alliance = patron_relationship.get_attitudes()[1]
    patron_alliance.clear()
    patron_alliance.set_drift(alliance_info['drift'])
    patron_alliance.set_current(alliance_info['value'])
    patron_alliance.set_limit(alliance_info['cap'])
    patron_alliance.set_active1('yes')

    patron_relationship.update_overall_attitude()

    # Applying changes

    protectorate_faction.write_xml()
    patron_diplomacy.write_xml()
    protectorate_diplomacy.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python make_protectorate.py russia georgia')
    parser.add_argument('patron_faction_name', type=str, help='')
    parser.add_argument('protectorate_faction_name', type=str, help='')
    args = parser.parse_args()

    patron_faction_name = args.patron_faction_name
    protectorate_faction_name = args.protectorate_faction_name

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)

    make_protectorate(patron_faction_name, protectorate_faction_name)
