import argparse
import os
import pandas as pd

from ..lib import *



def change_faction_capital(
    faction_name: VANILLA_FACTION_KEY_HINTS,
    new_region_name: VANILLA_REGION_KEY_HINTS,
    retake_region_name: VANILLA_REGION_KEY_HINTS = None):
    '''
    example:
        change_faction_capital('westphalia', 'flanders')
        change_faction_capital('piedmont_savoy', 'savoy', retake_region_name='the_papal_states')
    '''

    assert faction_name in FACTION_IDS['name'].to_list(), f"{faction_name} is not present in {FACTION_IDS_PATH}."
    assert new_region_name in REGION_IDS['name'].to_list(), f"{new_region_name} is not present in {REGION_IDS_PATH}."
    if retake_region_name:
        assert retake_region_name in REGION_IDS['name'].to_list(), f"{retake_region_name} is not present in {REGION_IDS_PATH}."

    # Collecting info

    faction_info = FACTION_IDS[FACTION_IDS['name'].eq(faction_name)].iloc[0]

    faction = Faction(os.path.join(OUTPUT_DIR, 'factions', faction_info['path']))

    new_region_info = REGION_IDS[REGION_IDS['name'].eq(new_region_name)].iloc[0]
    new_region_slot_id = Settlement(os.path.join(OUTPUT_DIR, 'region_slot', Region(os.path.join(OUTPUT_DIR, 'region', new_region_info['path'])).get_settlement_slot_path())).get_id()
    new_region_slot_info = REGION_SLOT_IDS[REGION_SLOT_IDS['id'].eq(new_region_slot_id)&REGION_SLOT_IDS['rec_type'].eq('SETTLEMENT')].iloc[0]

    if retake_region_name:
        retake_region_info = REGION_IDS[REGION_IDS['name'].eq(retake_region_name)].iloc[0]

    old_region_id = faction.get_current_capital_id()

    if old_region_id != '0':
        old_region_info = REGION_IDS[REGION_IDS['id'].eq(old_region_id)].iloc[0]
        old_region_slot_id = Settlement(os.path.join(OUTPUT_DIR, 'region_slot', Region(os.path.join(OUTPUT_DIR, 'region', old_region_info['path'])).get_settlement_slot_path())).get_id()
        old_region_slot_info = REGION_SLOT_IDS[REGION_SLOT_IDS['id'].eq(old_region_slot_id)&REGION_SLOT_IDS['rec_type'].eq('SETTLEMENT')].iloc[0]

    # Reassigning faction capital region

    faction.set_current_capital_id(new_region_info['id'])

    if retake_region_name:
        faction.set_original_capital_id(retake_region_info['id'])
    else:
        faction.set_original_capital_id(new_region_info['id'])

    # Reassigning CAI faction capital region

    cai_faction = CaiFaction(os.path.join(OUTPUT_DIR, 'cai_factions', faction_info['cai_path']))

    cai_faction.set_capital_region_1_id(new_region_info['cai_id'])
    cai_faction.set_capital_region_2_id(new_region_info['cai_id'])

    # Removing capital reference from the old CAI settlement

    if old_region_id != '0':
        old_cai_settlement = CaiSettlement(os.path.join(OUTPUT_DIR, 'cai_settlements', old_region_slot_info['cai_path']))

        old_cai_settlement.set_capital_faction_id('0')

    # Adding capital reference to the new CAI settlement

    new_cai_settlement = CaiSettlement(os.path.join(OUTPUT_DIR, 'cai_settlements', new_region_slot_info['cai_path']))

    new_cai_settlement.set_capital_faction_id(faction_info['cai_id'])

    # Applying changes

    faction.write_xml()
    cai_faction.write_xml()

    if old_region_id != '0':
        old_cai_settlement.write_xml()

    new_cai_settlement.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:' +
        '\n  python change_faction_capital.py westphalia flanders' +
        '\n  python change_faction_capital.py piedmont_savoy savoy --retake_region_name the_papal_states')
    parser.add_argument('faction_name', type=str, help='')
    parser.add_argument('new_region_name', type=str, help='')
    parser.add_argument('-r', '--retake_region_name', type=str, help='The capital will be moved to this region, if the faction conquers it during campaign.')
    args = parser.parse_args()

    faction_name = args.faction_name
    new_region_name = args.new_region_name
    retake_region_name = args.retake_region_name

    REGION_IDS = pd.read_csv(REGION_IDS_PATH, delimiter='\t', dtype=str)
    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)
    REGION_SLOT_IDS = pd.read_csv(REGION_SLOT_IDS_PATH, delimiter='\t', dtype=str)

    change_faction_capital(faction_name, new_region_name, retake_region_name)
