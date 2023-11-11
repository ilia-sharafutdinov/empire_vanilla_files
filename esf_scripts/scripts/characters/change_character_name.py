import argparse
import os
import pandas as pd

from ..lib import *



def change_character_name(
    character_file_name: str,
    names_group: str = None,
    gender: Literal['m', 'f'] = 'm',
    forename: str = None,
    surname: str = None,
    regnal_number: str = None):
    '''
    example:
        change_character_name('austria-General-0003.xml')
        change_character_name('barbary_states-admiral-0001.xml', 'names_muslim_general')
        change_character_name('westphalia-minister-0001.xml', 'names_german_catholic', 'm', forename='Leopold', regnal_number='I')
    '''

    assert character_file_name in CHARACTER_IDS['path'].to_list(), f"{character_file_name} is not present in {CHARACTER_IDS_PATH}."
    if names_group is not None:
        assert names_group in SUPPORTED_NAME_GROUPS, f"{names_group} is not present in names_tables."
    assert gender in ['m', 'f'], f"Gender '{gender}' is not supported. Accepted values are 'm' and 'f'."

    # Collecting info

    character_info = CHARACTER_IDS[CHARACTER_IDS['path'].eq(character_file_name)].iloc[0]

    character = Character(os.path.join(OUTPUT_DIR, 'character', character_info['path']))

    faction_info = FACTION_IDS[FACTION_IDS['name'].eq(character.get_faction())].iloc[0]

    faction = Faction(os.path.join(OUTPUT_DIR, 'factions', faction_info['path']))

    assert character_file_name in faction.get_character_paths(), f"{character_file_name} is not present in {faction_info['path']}. Please check whether faction name is set correctly in {character_file_name}."

    if not names_group:
        names_group = FACTIONS_TABLE[FACTIONS_TABLE['key'].eq(faction_info['name'])]['name_group'].iloc[0]

    ship_names_group = FACTIONS_TABLE[FACTIONS_TABLE['key'].eq(faction_info['name'])]['ship_name_group'].iloc[0]

    if forename or surname:
        new_name_info = make_name_info(names_group, forename, surname)
    else:
        new_name_info = generate_name(names_group, gender)

    # Reassigning character name

    character.set_first_name(new_name_info['forename_loc'])

    character.set_last_name(new_name_info['surname_loc'])

    if regnal_number:
        character.set_regnal_number(regnal_number)

    government = Government(os.path.join(OUTPUT_DIR, 'government', faction_info['government_path']))

    king = government.get_type() in ('gov_absolute_monarchy', 'gov_constitutional_monarchy')
    faction_leader = character.get_cabinet_id() == government.get_post('faction_leader').get_id()

    if king and faction_leader:
        family = Family(os.path.join(OUTPUT_DIR, 'family', faction_info['family_path']))
        family_member = family.get_family_members()[0]
        family_member.set_name(new_name_info['forename_loc'])

    # Reassigning army commanders' names

    if pd.notna(character_info['army_path']):
        army = Army(os.path.join(OUTPUT_DIR, 'army', character_info['army_path']))

        for i, unit in enumerate(army.get_land_units() if army.get_type() == 'ARMY' else army.get_naval_units()):
            if i == 0:
                new_commander_name_info = new_name_info
            else:
                new_commander_name_info = generate_name(names_group, gender)
            unit.set_commander_first_name(new_commander_name_info['forename'])
            unit.set_commander_last_name(new_commander_name_info['surname'])

            if army.get_type() == 'NAVY':
                new_ship_name = generate_ship_name(ship_names_group, faction_info['name'])
                unit.set_name_alloc(new_ship_name['name_loc'])

    # Applying changes

    character.write_xml()

    if king and faction_leader:
        family.write_xml()

    if pd.notna(character_info['army_path']):
        army.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:' +
        '\n  python change_character_name.py austria-General-0003.xml' +
        '\n  python change_character_name.py barbary_states-admiral-0001.xml --names_group names_muslim_general' +
        '\n  python change_character_name.py westphalia-minister-0001.xml --names_group names_german_catholic --gender m --forename Leopold --regnal_number I')
    parser.add_argument('character_file_name', type=str, help='')
    parser.add_argument('-p', '--names_group', type=str, help='Names group as found in db/names_tables/names.tsv')
    parser.add_argument('-g', '--gender', type=str, default='m', choices=['m', 'f'], help='Gender as found in db/names_tables/names.tsv')
    args_name = parser.add_argument_group('Preset name', description='Use either of the following arguments if you wish the character to have a non-random name.')
    args_name.add_argument('-f', '--forename', type=str, help='Forename as found in db/names_tables/names.tsv')
    args_name.add_argument('-l', '--surname', type=str, help='Surname as found in db/names_tables/names.tsv')
    args_name.add_argument('-r', '--regnal_number', type=str, help='Upper case roman numerals used for the titles of monarchs.')
    args = parser.parse_args()

    character_file_name = args.character_file_name
    names_group = args.names_group
    gender = args.gender
    forename = args.forename
    surname = args.surname
    regnal_number = args.regnal_number

    CHARACTER_IDS = pd.read_csv(CHARACTER_IDS_PATH, delimiter='\t', dtype=str)
    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)

    change_character_name(character_file_name, names_group, gender, forename, surname, regnal_number)
