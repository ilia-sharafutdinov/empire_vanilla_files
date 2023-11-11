import argparse
import os
import pandas as pd

from ..lib import *



def change_character_portrait(
    character_file_name: str,
    faction_leader = False,
    gender: Literal['m', 'f'] = 'm',
    king: bool = False,
    portrait_culture: str = None,
    portrait_age: Literal['young', 'old'] = None,
    portrait_number: int = None):
    '''
    example:
        change_character_portrait('westphalia-minister-0001.xml', faction_leader=True, king=True, portrait_age='old', portrait_number=3)
    '''

    assert character_file_name in CHARACTER_IDS['path'].to_list(), f"{character_file_name} is not present in {CHARACTER_IDS_PATH}."

    # Collecting info

    character_info = CHARACTER_IDS[CHARACTER_IDS['path'].eq(character_file_name)].iloc[0]

    character = Character(os.path.join(OUTPUT_DIR, 'character', character_info['path']))

    faction_info = FACTION_IDS[FACTION_IDS['name'].eq(character.get_faction())].iloc[0]

    faction = Faction(os.path.join(OUTPUT_DIR, 'factions', faction_info['path']))

    assert character_file_name in faction.get_character_paths(), f"{character_file_name} is not present in {faction_info['path']}. Please check whether faction name is set correctly in {character_file_name}."

    faction_culture = get_faction_culture(faction_info['name'])

    if king and (gender == 'm'):
        portrait_type = 'king'
    elif king and (gender == 'f'):
        portrait_type = 'queen'
    else:
        portrait_type = get_portrait_type(character.get_type())
    if not portrait_culture:
        portrait_culture = get_portrait_culture(faction_culture, portrait_type)
    if not portrait_age:
        portrait_age = generate_portrait_age()
    if not portrait_number:
        portrait_number = generate_portrait_number(portrait_culture, portrait_type)

    # Reassigning character portrait

    character.set_portrait_culture(portrait_culture)
    character.set_portrait_agent_type(portrait_type)
    character.set_portrait_age(portrait_age)
    if king:
        character.set_portrait_number(portrait_number, faction_leader=True)
    else:
        character.set_portrait_number(portrait_number)

    government = Government(os.path.join(OUTPUT_DIR, 'government', faction_info['government_path']))

    king = government.get_type() in ('gov_absolute_monarchy', 'gov_constitutional_monarchy')
    faction_leader = character.get_cabinet_id() == government.get_post('faction_leader').get_id()

    if king and faction_leader:
        family = Family(os.path.join(OUTPUT_DIR, 'family', faction_info['family_path']))
        family_member = family.get_family_members()[0]
        family_member.set_portrait_culture(portrait_culture)
        family_member.set_portrait_agent_type(portrait_type)
        family_member.set_portrait_age(portrait_age)
        family_member.set_portrait_number(portrait_number, faction_leader=faction_leader)

    # Reassigning faction leader portrait in preopen_map_info

    if faction_leader:
        preopen_map_info = PreopenMapInfo(os.path.join(OUTPUT_DIR, 'preopen_map_info', Esf(os.path.join(OUTPUT_DIR, 'esf.xml')).get_preopen_map_info()))

        preopen_map_info.get_faction_info(faction_info['name']).set_leader_portrait(f'ui/portraits/{portrait_culture}/cards/{portrait_type}/{portrait_age}/{str(portrait_number).zfill(3)}.tga')


    # Applying changes

    character.write_xml()

    if king and faction_leader:
        family.write_xml()

    if faction_leader:
        preopen_map_info.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python change_character_portrait.py westphalia-minister-0001.xml --faction_leader --king --portrait_age old --portrait_number 3')
    parser.add_argument('character_file_name', type=str, help='')
    parser.add_argument('-o', '--faction_leader', type=str, help='')
    parser.add_argument('-g', '--gender', type=str, default='m', choices=['m', 'f'], help='Gender as found in db/names_tables/names.tsv')
    parser.add_argument('-k', '--king', action='store_true', help='')
    parser.add_argument('-c', '--portrait_culture', type=str, help='')
    parser.add_argument('-a', '--portrait_age', type=str, choices=['young', 'old'], help='')
    parser.add_argument('-n', '--portrait_number', type=str, help='')
    args = parser.parse_args()

    character_file_name = args.character_file_name
    faction_leader = args.faction_leader
    gender = args.gender
    king = args.king
    portrait_culture = args.portrait_culture
    portrait_age = args.portrait_age
    portrait_number = args.portrait_number

    CHARACTER_IDS = pd.read_csv(CHARACTER_IDS_PATH, delimiter='\t', dtype=str)
    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)

    change_character_portrait(character_file_name, faction_leader, gender, king, portrait_culture, portrait_age, portrait_number)
