import argparse
import os
import pandas as pd

from ..lib import *



def change_faction_randomise_all_character_names(faction_name: VANILLA_FACTION_KEY_HINTS):
    '''
    example:
        change_faction_randomise_all_character_names('westphalia')
    '''

    assert faction_name in FACTION_IDS['name'].to_list(), f"{faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    faction_info = FACTION_IDS[FACTION_IDS['name'].eq(faction_name)].iloc[0]

    names_group = FACTIONS_TABLE[FACTIONS_TABLE['key'].eq(faction_info['name'])]['name_group'].iloc[0]
    ship_names_group = FACTIONS_TABLE[FACTIONS_TABLE['key'].eq(faction_info['name'])]['ship_name_group'].iloc[0]

    # TODO: Rename forts

    # Reassigning faction family names

    family = Family(os.path.join(OUTPUT_DIR, 'family', faction_info['family_path']))

    for i, family_member in enumerate(family.get_family_members()):
        if family_member.get_name() is None:
            continue

        if family_member.get_male() == 'yes':
            if i == 0:
                leader_gender = 'm'
            family_member_gender = 'm'
        else:
            if i == 0:
                leader_gender = 'f'
            family_member_gender = 'f'

        new_name_info = generate_name(names_group, family_member_gender, king=True)

        family_member.set_name(new_name_info['forename_loc'])

    # Reassigning faction character names

    faction = Faction(os.path.join(OUTPUT_DIR, 'factions', faction_info['path']))

    government = Government(os.path.join(OUTPUT_DIR, 'government', faction_info['government_path']))

    king = government.get_type() in ('gov_absolute_monarchy', 'gov_constitutional_monarchy')

    characters = []
    armies = []

    for character_file_name in faction.get_character_paths():

        character_info = CHARACTER_IDS[CHARACTER_IDS['path'].eq(character_file_name)].iloc[0]

        character = Character(os.path.join(OUTPUT_DIR, 'character', character_info['path']))

        faction_leader = character.get_cabinet_id() == government.get_post('faction_leader').get_id()

        if faction_leader:
            if king:
                new_name_info = generate_name(names_group, leader_gender, king=True)
            else:
                new_name_info = generate_name(names_group, leader_gender)
        else:
            new_name_info = generate_name(names_group, 'm')

        character.set_first_name(new_name_info['forename_loc'])

        character.set_last_name(new_name_info['surname_loc'])

        characters.append(character)

        if faction_leader and king:
            family_member = family.get_family_members()[0]
            family_member.set_name(new_name_info['forename_loc'])

        # Reassigning army commanders' names

        if pd.notna(character_info['army_path']):
            army = Army(os.path.join(OUTPUT_DIR, 'army', character_info['army_path']))

            for i, unit in enumerate(army.get_land_units() if army.get_type() == 'ARMY' else army.get_naval_units()):
                if i == 0:
                    new_commander_name_info = new_name_info
                else:
                    new_commander_name_info = generate_name(names_group, 'm')
                unit.set_commander_first_name(new_commander_name_info['forename'])
                unit.set_commander_last_name(new_commander_name_info['surname'])

                if army.get_type() == 'NAVY':
                    new_ship_name = generate_ship_name(ship_names_group, faction_info['name'])
                    unit.set_name_alloc(new_ship_name['name_loc'])

            armies.append(army)

    # Applying changes

    for character in characters:
        character.write_xml()

    family.write_xml()

    for army in armies:
        army.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:' +
        '\n  python change_faction_randomise_all_character_names.py westphalia')
    parser.add_argument('faction_name', type=str, help='')
    args = parser.parse_args()

    faction_name = args.faction_name

    CHARACTER_IDS = pd.read_csv(CHARACTER_IDS_PATH, delimiter='\t', dtype=str)
    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)

    change_faction_randomise_all_character_names(faction_name)
