import argparse
import os
import pandas as pd

from ..lib import *



def make_war(aggressor_faction_name: VANILLA_FACTION_KEY_HINTS, victim_faction_name: VANILLA_FACTION_KEY_HINTS):
    '''
    example:
        make_war('russia', 'chechenya_dagestan')
    '''

    assert aggressor_faction_name in FACTION_IDS['name'].to_list(), f"{aggressor_faction_name} is not present in {FACTION_IDS_PATH}."
    assert victim_faction_name in FACTION_IDS['name'].to_list(), f"{victim_faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    aggressor_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(aggressor_faction_name)].iloc[0]
    victim_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(victim_faction_name)].iloc[0]

    war_info = DIPLOMACY_ATTITUDES_TABLE[DIPLOMACY_ATTITUDES_TABLE['attitude'].eq('war')].iloc[0]

    # Setting protectorate ID

    aggressor_faction = Faction(os.path.join(OUTPUT_DIR, 'factions', victim_faction_info['path']))

    if aggressor_faction.get_protectorate_id() == victim_faction_info['id']:
        aggressor_faction.set_protectorate_id('0')

    victim_faction = Faction(os.path.join(OUTPUT_DIR, 'factions', victim_faction_info['path']))

    if victim_faction.get_protectorate_id() == aggressor_faction_info['id']:
        victim_faction.set_protectorate_id('0')

    # Setting aggressor diplomatic relationships

    aggressor_diplomacy = Diplomacy(os.path.join(OUTPUT_DIR, 'diplomacy', aggressor_faction_info['diplomacy_path']))

    aggressor_relationship = aggressor_diplomacy.get_relationship(victim_faction_info['id'])

    aggressor_relationship.set_if_allied_10('0')
    aggressor_relationship.set_if_allied_20('0')
    aggressor_relationship.set_relationship('war')
    aggressor_relationship.set_relationship_with_protectorate('war')
    aggressor_relationship.get_attitudes()[1].clear()
    aggressor_relationship.get_attitudes()[5].clear()
    aggressor_relationship.make_non_trading()
    aggressor_relationship.set_military_access_turns('0')
    aggressor_relationship.set_income_from_protectorate('0')
    aggressor_relationship.set_payment_to_patron('0')

    aggressor_war = aggressor_relationship.get_attitudes()[7]
    aggressor_war.clear()
    aggressor_war.set_drift(war_info['drift'])
    aggressor_war.set_current(war_info['value'])
    aggressor_war.set_limit(war_info['cap'])
    aggressor_war.set_active1('yes')

    aggressor_relationship.update_overall_attitude()

    # Setting victim diplomatic relationships

    victim_diplomacy = Diplomacy(os.path.join(OUTPUT_DIR, 'diplomacy', victim_faction_info['diplomacy_path']))

    victim_relationship = victim_diplomacy.get_relationship(aggressor_faction_info['id'])

    victim_relationship.set_if_allied_10('0')
    victim_relationship.set_if_allied_20('0')
    victim_relationship.set_relationship('war')
    victim_relationship.set_relationship_with_protectorate('war')
    victim_relationship.get_attitudes()[1].clear()
    victim_relationship.get_attitudes()[5].clear()
    victim_relationship.make_non_trading()
    victim_relationship.set_military_access_turns('0')
    victim_relationship.set_income_from_protectorate('0')
    victim_relationship.set_payment_to_patron('0')

    victim_war = victim_relationship.get_attitudes()[7]
    victim_war.clear()
    victim_war.set_drift(war_info['drift'])
    victim_war.set_current(war_info['value'])
    victim_war.set_limit(war_info['cap'])
    victim_war.set_active1('yes')

    victim_relationship.update_overall_attitude()

    # Applying changes

    aggressor_diplomacy.write_xml()

    victim_diplomacy.write_xml()

    if aggressor_faction.get_protectorate_id() == victim_faction_info['id']:
        aggressor_faction.write_xml()

    if victim_faction.get_protectorate_id() == aggressor_faction_info['id']:
        victim_faction.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python make_war.py russia chechenya_dagestan')
    parser.add_argument('aggressor_faction_name', type=str, help='')
    parser.add_argument('victim_faction_name', type=str, help='')
    args = parser.parse_args()

    aggressor_faction_name = args.aggressor_faction_name
    victim_faction_name = args.victim_faction_name

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)

    make_war(aggressor_faction_name, victim_faction_name)
