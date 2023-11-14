import argparse
import os
import pandas as pd

from ..lib import *



def create_minister(
    faction_name: VANILLA_FACTION_KEY_HINTS,
    character_id: int,
    character_cai_id: int,
    gender: Literal['m', 'f'] = 'm',
    king: bool = False,
    government_post: Literal['faction_leader', 'head_of_government', 'finance', 'justice', 'army', 'navy', 'accident'] = None,
    names_group: str = None,
    forename: str = None,
    surname: str = None,
    regnal_number: str = None,
    birth_season: Literal['summer', 'winter'] = None,
    birth_year: int = None,
    portrait_culture: str = None,
    portrait_age: Literal['young', 'old'] = None,
    portrait_number: int = None):
    '''
    example:
        create_minister('punjab', 900001010, 990001010, government_post='faction_leader', king=True, forename='Eshwar', regnal_number='I')
        create_minister('punjab', 900001030, 990001030, government_post='finance')
        create_minister('punjab', 900001090, 990001090)
    '''

    assert faction_name in FACTION_IDS['name'].to_list(), f"{faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    faction_info = FACTION_IDS[FACTION_IDS['name'].eq(faction_name)].iloc[0]

    new_cai_character_path = f"{str(int(CHARACTER_IDS['cai_path'].max().replace('.xml', '')) + 1).zfill(4)}.xml"
    if CHARACTER_IDS[CHARACTER_IDS['faction_name'].eq(faction_info['name'])&CHARACTER_IDS['character_type'].eq('minister')].size == 0:
        new_character_path = f"{faction_info['name']}-minister-0001.xml"
    else:
        new_character_path = f"{faction_info['name']}-minister-{str(int(CHARACTER_IDS[CHARACTER_IDS['faction_name'].eq(faction_info['name'])&CHARACTER_IDS['character_type'].eq('minister')]['path'].max()[-8:-4]) + 1).zfill(4)}.xml"

    faction_culture = get_faction_culture(faction_info['name'])

    if not names_group:
        names_group = FACTIONS_TABLE[FACTIONS_TABLE['key'].eq(faction_info['name'])]['name_group'].iloc[0]

    if forename or surname:
        new_name_info = make_name_info(names_group, forename, surname)
    else:
        if king:
            new_name_info = generate_name(names_group, gender, king=True)
        else:
            new_name_info = generate_name(names_group, gender)

    if king and (gender == 'm'):
        portrait_type = 'king'
    elif king and (gender == 'f'):
        portrait_type = 'queen'
    else:
        portrait_type = 'minister'
    if not portrait_culture:
        portrait_culture = get_portrait_culture(faction_culture, portrait_type)
    if not portrait_age:
        portrait_age = generate_portrait_age()
    if not portrait_number:
        portrait_number = generate_portrait_number(portrait_culture, portrait_type)
    if not birth_season:
        birth_season = generate_season()
    if not birth_year:
        birth_year = get_starting_year() - generate_age()
    birth_date = f"{birth_season} {birth_year}"

    character_id = str(character_id)
    character_cai_id = str(character_cai_id)

    # Assigning character to government post

    if government_post:
        government = Government(os.path.join(OUTPUT_DIR, 'government', faction_info['government_path']))

        cabinet_id = government.get_post(government_post).get_id()

        government.get_post(government_post).set_character_id(character_id)

    # Creating character

    character = Character(
        os.path.join(get_module_dir(), 'templates', 'character_minister_government.xml' if government_post else 'character_minister_opposition.xml'),
        os.path.join(OUTPUT_DIR, 'character', new_character_path))

    character.set_id(character_id)
    character.set_details_character_id(character_id)

    if government_post:
        character.set_cabinet_id(cabinet_id)

    character.set_first_name(new_name_info['forename_loc'])

    character.set_last_name(new_name_info['surname_loc'])

    if regnal_number:
        character.set_regnal_number(regnal_number)

    character.set_birth_date(birth_date)

    character.set_portrait_culture(portrait_culture)
    character.set_portrait_agent_type(portrait_type)
    character.set_portrait_age(portrait_age)
    if government_post == 'faction_leader':
        character.set_portrait_number(portrait_number, faction_leader=True)
    else:
        character.set_portrait_number(portrait_number)

    character.set_faction(faction_info['name'])

    character.set_agent_onscreen_name(f"agent_culture_details_onscreen_name_minister{faction_culture}")

    # Creating CAI character

    cai_character = CaiCharacter(
        os.path.join(get_module_dir(), 'templates', 'cai_character_minister.xml'),
        os.path.join(OUTPUT_DIR, 'cai_characters', new_cai_character_path))

    cai_character.set_owned_indirect(faction_info['cai_id'])

    cai_character.set_id(character_cai_id)

    cai_character.set_character_id(character_id)

    # Giving character to faction

    faction = Faction(os.path.join(OUTPUT_DIR, 'factions', faction_info['path']))

    faction.add_character_path(new_character_path)

    # Giving character to CAI faction

    cai_faction = CaiFaction(os.path.join(OUTPUT_DIR, 'cai_factions', faction_info['cai_path']))

    cai_faction.add_character_id(character_cai_id)

    # Adding character to CAI world

    cai_world = CaiWorld(os.path.join(OUTPUT_DIR, 'cai_interface', 'cai_world.xml'))

    cai_world.add_characters_path(new_cai_character_path)

    # Reassigning faction leader portrait in preopen_map_info

    faction_leader = government_post == 'faction_leader'

    if faction_leader:
        preopen_map_info = PreopenMapInfo(os.path.join(OUTPUT_DIR, 'preopen_map_info', Esf(os.path.join(OUTPUT_DIR, 'esf.xml')).get_preopen_map_info()))

        preopen_map_info.get_faction_info(faction_info['name']).set_leader_portrait(f'ui/portraits/{portrait_culture}/cards/{portrait_type}/{portrait_age}/{str(portrait_number).zfill(3)}.tga')

    # Applying changes

    character.write_xml()
    cai_character.write_xml()

    faction.write_xml()
    cai_faction.write_xml()

    if government_post:
        government.write_xml()

    if faction_leader:
        preopen_map_info.write_xml()

    cai_world.write_xml()

    CHARACTER_IDS.loc[CHARACTER_IDS.index.size] = {
        'id': character_id,
        'faction_name': faction_name,
        'character_type': 'minister',
        'first_name': new_name_info['forename_loc'],
        'last_name': new_name_info['surname_loc'],
        'birth_date': birth_date,
        'path': new_character_path,
        'cai_id': character_cai_id,
        'cai_path': new_cai_character_path
    }



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:' +
        '\n  python create_minister.py punjab 900001010 990001010 --government_post faction_leader --king --forename Eshwar --regnal_number I' +
        '\n  python create_minister.py punjab 900001030 990001030 --government_post finance' +
        '\n  python create_minister.py punjab 900001090 990001090')
    parser.add_argument('faction_name', type=str, help='')
    parser.add_argument('character_id', type=str, help='')
    parser.add_argument('character_cai_id', type=str, help='')
    parser.add_argument('-g', '--gender', type=str, default='m', choices=['m', 'f'], help='Gender as found in db/names_tables/names.tsv')
    parser.add_argument('-k', '--king', action='store_true', help='')
    parser.add_argument('-o', '--government_post', type=str, choices=['faction_leader', 'head_of_government', 'finance', 'justice', 'army', 'navy', 'accident'], help='If no specified, the minister remains in opposition.')
    args_name = parser.add_argument_group('Preset name', description='Use either of the following arguments if you wish the character to have non-random name.')
    args_name.add_argument('-p', '--names_group', type=str, help='Names group as found in db/names_tables/names.tsv')
    args_name.add_argument('-f', '--forename', type=str, help='Forename as found in db/names_tables/names.tsv')
    args_name.add_argument('-l', '--surname', type=str, help='Surname as found in db/names_tables/names.tsv')
    args_name.add_argument('-r', '--regnal_number', type=str, help='Upper case roman numerals used for the titles of monarchs.')
    args_birth = parser.add_argument_group('Preset birth date', description='Use either of the following arguments if you wish the character to have non-random birth date.')
    args_birth.add_argument('-s', '--birth_season', type=str, choices=['summer', 'winter'], help='')
    args_birth.add_argument('-y', '--birth_year', type=str, help='')
    args_portrait = parser.add_argument_group('Preset portrait', description='Use either of the following arguments if you wish the character to have non-random birth portrait.')
    args_portrait.add_argument('-c', '--portrait_culture', type=str, help='')
    args_portrait.add_argument('-a', '--portrait_age', type=str, choices=['young', 'old'], help='')
    args_portrait.add_argument('-n', '--portrait_number', type=str, help='')
    args = parser.parse_args()

    faction_name = args.faction_name
    character_id = args.character_id
    character_cai_id = args.character_cai_id
    gender = args.gender
    king = args.king
    government_post = args.government_post
    names_group = args.names_group
    forename = args.forename
    surname = args.surname
    regnal_number = args.regnal_number
    birth_season = args.birth_season
    birth_year = args.birth_year
    portrait_culture = args.portrait_culture
    portrait_age = args.portrait_age
    portrait_number = args.portrait_number

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)
    CHARACTER_IDS = pd.read_csv(CHARACTER_IDS_PATH, delimiter='\t', dtype=str)

    create_minister(
        faction_name,
        character_id,
        character_cai_id,
        gender,
        king,
        government_post,
        names_group,
        forename,
        surname,
        regnal_number,
        birth_season,
        birth_year,
        portrait_culture,
        portrait_age,
        portrait_number)

    CHARACTER_IDS.to_csv(CHARACTER_IDS_PATH, sep='\t', index=False)
