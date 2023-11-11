import argparse
import os
import pandas as pd

from ..lib import *



def hand_over_character(character_file_name: str, new_faction_name: VANILLA_FACTION_KEY_HINTS):
    '''
    example:
        hand_over_character('austria-General-0003.xml', 'prussia')
    '''

    assert character_file_name in CHARACTER_IDS['path'].to_list(), f"{character_file_name} is not present in {CHARACTER_IDS_PATH}."
    assert new_faction_name in FACTION_IDS['name'].to_list(), f"{new_faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    character_info = CHARACTER_IDS[CHARACTER_IDS['path'].eq(character_file_name)].iloc[0]

    character = Character(os.path.join(OUTPUT_DIR, 'character', character_info['path']))

    character_type = character.get_type()

    assert character_type != 'minister', "Hand-over of 'minister' character types is not supported."

    old_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(character.get_faction())].iloc[0]
    new_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(new_faction_name)].iloc[0]

    new_culture = get_faction_culture(new_faction_info['name'])

    # TODO: Fix forts handover
    # TODO: Fix line of sight

    # Reassigning character ownership

    character.set_faction(new_faction_info['name'])

    new_agent_on_screen_name = f"agent_culture_details_onscreen_name_{character_type}{new_culture}"

    character.set_agent_onscreen_name(new_agent_on_screen_name)

    # Reassigning CAI character ownership

    cai_character = CaiCharacter(os.path.join(OUTPUT_DIR, 'cai_characters', character_info['cai_path']))

    cai_character.set_owned_indirect(new_faction_info['cai_id'])

    # Reassigning army ownership

    if pd.notna(character_info['army_path']):
        army = Army(os.path.join(OUTPUT_DIR, 'army', character_info['army_path']))

        for unit in army.get_land_units() if army.get_type() == 'ARMY' else army.get_naval_units():
            unit.set_commander_faction(new_faction_name)

    # Reassigning CAI mobile ownership

    cai_mobile = CaiMobile(os.path.join(OUTPUT_DIR, 'cai_mobiles', character_info['cai_mobile_path']))

    cai_mobile.set_owned_direct(new_faction_info['cai_id'])

    # Removing character from the old faction

    old_faction = Faction(os.path.join(OUTPUT_DIR, 'factions', old_faction_info['path']))

    old_faction.remove_character_path(character_info['path'])
    if pd.notna(character_info['army_path']):
        old_faction.remove_army_path(character_info['army_path'])

    # Removing character from the old CAI faction

    old_cai_faction = CaiFaction(os.path.join(OUTPUT_DIR, 'cai_factions', old_faction_info['cai_path']))

    old_cai_faction.remove_character_id(character_info['cai_id'])
    if pd.notna(character_info['cai_mobile_path']):
        old_cai_faction.remove_character_resource_id(character_info['cai_resource_id'])

    # Giving character to the new faction

    new_faction = Faction(os.path.join(OUTPUT_DIR, 'factions', new_faction_info['path']))

    new_faction.add_character_path(character_info['path'])
    if pd.notna(character_info['army_path']):
        new_faction.add_army_path(character_info['army_path'])

    # Giving character to the new CAI faction

    new_cai_faction = CaiFaction(os.path.join(OUTPUT_DIR, 'cai_factions', new_faction_info['cai_path']))

    new_cai_faction.add_character_id(character_info['cai_id'])
    if pd.notna(character_info['cai_mobile_path']):
        new_cai_faction.add_character_resource_id(character_info['cai_resource_id'])

    # Applying changes

    character.write_xml()
    cai_character.write_xml()

    CHARACTER_IDS.loc[CHARACTER_IDS['id'].eq(character.get_id()), 'faction_name'] = new_faction_name

    if pd.notna(character_info['army_path']):
        army.write_xml()

    cai_mobile.write_xml()

    old_faction.write_xml()
    old_cai_faction.write_xml()
    new_faction.write_xml()
    new_cai_faction.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python hand_over_character.py austria-General-0003.xml prussia')
    parser.add_argument('character_file_name', type=str, help='')
    parser.add_argument('new_faction_name', type=str, help='')
    args = parser.parse_args()

    character_file_name = args.character_file_name
    new_faction_name = args.new_faction_name

    CHARACTER_IDS = pd.read_csv(CHARACTER_IDS_PATH, delimiter='\t', dtype=str)
    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)

    hand_over_character(character_file_name, new_faction_name)

    CHARACTER_IDS.to_csv(CHARACTER_IDS_PATH, sep='\t', index=False)
