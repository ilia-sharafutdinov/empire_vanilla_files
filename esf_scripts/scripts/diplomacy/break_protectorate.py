import argparse
import os
import pandas as pd

from ..lib import *



def break_protectorate(protectorate_faction_name: VANILLA_FACTION_KEY_HINTS):
    '''
    example:
        break_protectorate('barbary_states')
    '''

    assert protectorate_faction_name in FACTION_IDS['name'].to_list(), f"{protectorate_faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info
    protectorate_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(protectorate_faction_name)].iloc[0]

    protectorate_faction = Faction(os.path.join(OUTPUT_DIR, 'factions', protectorate_faction_info['path']))

    patron_faction_id = protectorate_faction.get_protectorate_id()

    assert patron_faction_id != '0', f"Patron faction ID is zero in {protectorate_faction_info['path']}."

    patron_faction_info = FACTION_IDS[FACTION_IDS['id'].eq(patron_faction_id)].iloc[0]

    # Setting protectorate ID

    protectorate_faction.set_protectorate_id('0')

    # Setting protectorate diplomatic relationships

    protectorate_diplomacy = Diplomacy(os.path.join(OUTPUT_DIR, 'diplomacy', protectorate_faction_info['diplomacy_path']))

    protectorate_relationship = protectorate_diplomacy.get_relationship(patron_faction_info['id'])

    protectorate_relationship.set_if_allied_10('0')
    protectorate_relationship.set_if_allied_20('0')
    protectorate_relationship.set_relationship('neutral')
    protectorate_relationship.set_relationship_with_protectorate('neutral')
    protectorate_relationship.set_payment_to_patron('0')
    protectorate_relationship.get_attitudes()[1].clear()

    protectorate_relationship.update_overall_attitude()

    # Setting patron diplomatic relationships

    patron_diplomacy = Diplomacy(os.path.join(OUTPUT_DIR, 'diplomacy', patron_faction_info['diplomacy_path']))

    patron_relationship = patron_diplomacy.get_relationship(protectorate_faction_info['id'])

    patron_relationship.set_if_allied_10('0')
    patron_relationship.set_if_allied_20('0')
    patron_relationship.set_relationship('neutral')
    patron_relationship.set_relationship_with_protectorate('neutral')
    patron_relationship.set_income_from_protectorate('0')
    patron_relationship.get_attitudes()[1].clear()

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
        '  python break_protectorate.py barbary_states')
    parser.add_argument('protectorate_faction_name', type=str, help='')
    args = parser.parse_args()

    protectorate_faction_name = args.protectorate_faction_name

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)

    break_protectorate(protectorate_faction_name)
