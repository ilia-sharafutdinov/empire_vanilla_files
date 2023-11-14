import argparse
import os
import pandas as pd

from ..lib import *



def create_governorship(
    faction_name: VANILLA_FACTION_KEY_HINTS,
    new_governorship_name: Literal['governor_america', 'governor_europe', 'governor_india'],
    character_id: int,
    governor_id: int,
    cabinet_id: int,
    character_cai_id: int,
    governor_cai_id: int,
    gender: Literal['m', 'f'] = 'm',
    names_group: str = None,
    forename: str = None,
    surname: str = None,
    birth_season: Literal['summer', 'winter'] = None,
    birth_year: int = None,
    portrait_culture: str = None,
    portrait_age: Literal['young', 'old'] = None,
    portrait_number: int = None):
    '''
    example:
        create_governorship('britain', 'governor_india', '900000000', '800000000', '700000000', '990000000', '880000000')
    '''

    assert faction_name in FACTION_IDS['name'].to_list(), f"{faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    faction_info = FACTION_IDS[FACTION_IDS['name'].eq(faction_name)].iloc[0]
    if GOVERNORSHIP_IDS[GOVERNORSHIP_IDS['faction_id'].eq(faction_info['id'])&GOVERNORSHIP_IDS['name'].eq(new_governorship_name)].size != 0:
        raise ValueError(f"{GOVERNORSHIP_IDS_PATH} already contains a governor where faction_id = {faction_info['id']} and name = {new_governorship_name}.")

    new_cai_governorship_path = f"{str(int(GOVERNORSHIP_IDS['cai_path'].max().replace('.xml', '')) + 1).zfill(4)}.xml"
    new_cai_character_path = f"{str(int(CHARACTER_IDS['cai_path'].max().replace('.xml', '')) + 1).zfill(4)}.xml"
    if CHARACTER_IDS[CHARACTER_IDS['faction_name'].eq(faction_info['name'])&CHARACTER_IDS['character_type'].eq('minister')].size == 0:
        new_character_path = f"{faction_info['name']}-minister-0001.xml"
    else:
        new_character_path = f"{faction_info['name']}-minister-{str(int(CHARACTER_IDS[CHARACTER_IDS['faction_name'].eq(faction_info['name'])&CHARACTER_IDS['character_type'].eq('minister')]['path'].max()[-8:-4]) + 1).zfill(4)}.xml"

    theatre_cai_id = GovernmentPost.governorships_to_theatre_cai_id[new_governorship_name]

    faction_culture = get_faction_culture(faction_info['name'])

    if not names_group:
        names_group = FACTIONS_TABLE[FACTIONS_TABLE['key'].eq(faction_info['name'])]['name_group'].iloc[0]

    if forename or surname:
        new_name_info = make_name_info(names_group, forename, surname)
    else:
        new_name_info = generate_name(names_group, gender)

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

    character_post_template = f'''
  <rec type="POSTS_ARRAY">
   <rec type="CHARACTER_POST">
    <i>{cabinet_id}</i><!-- Cabinet ID -->
    <s>{new_governorship_name}</s><!-- Cabinet Title -->
    <u>{character_id}</u><!-- Character ID -->
    <yes/><!-- Governor -->
    <rec type="GOVERNORSHIP">
     <gov_taxes level_lower="2" level_upper="2" rate_lower="15" rate_upper="15"/>
     <i>{governor_id}</i><!-- Governor ID -->
     <u4_ary/><!-- Region IDs -->
     <u>{faction_info['id']}</u><!-- Faction ID -->
     <no/>
     <no/>
    </rec>
    <i>{faction_info['government_id']}</i><!-- Government ID -->
   </rec>
  </rec>
 '''

    character_id = str(character_id)
    governor_id = str(governor_id)
    cabinet_id = str(cabinet_id)
    character_cai_id = str(character_cai_id)
    governor_cai_id = str(governor_cai_id)

    # TODO: Automatically change HLCIS ID
    # TODO: FIX BDI instead of removing

    # Adding governorship to faction government

    government = Government(os.path.join(OUTPUT_DIR, 'government', faction_info['government_path']))

    government.add_post(parse_xml_string(character_post_template))

    # Creating CAI governorship

    cai_governorship = CaiGovernorship(
        os.path.join(get_module_dir(), 'templates', 'cai_governorship.xml'),
        os.path.join(OUTPUT_DIR, 'cai_governorships', new_cai_governorship_path))

    cai_governorship.set_id(governor_cai_id)

    cai_governorship.set_owned_direct(faction_info['cai_id'])

    cai_governorship.set_governor_id(governor_id)

    cai_governorship.set_theatre_id(theatre_cai_id)

    cai_governorship.set_character_id(character_cai_id)

    # Creating character

    character = Character(
        os.path.join(get_module_dir(), 'templates', 'character_governor.xml'),
        os.path.join(OUTPUT_DIR, 'character', new_character_path))

    character.set_id(character_id)
    character.set_details_character_id(character_id)

    character.set_cabinet_id(cabinet_id)

    character.set_first_name(new_name_info['forename_loc'])
    character.set_last_name(new_name_info['surname_loc'])

    character.set_birth_date(birth_date)

    character.set_portrait_culture(portrait_culture)
    character.set_portrait_age(portrait_age)
    character.set_portrait_number(portrait_number)

    character.set_faction(faction_info['name'])

    character.set_agent_onscreen_name(f"agent_culture_details_onscreen_name_minister{faction_culture}")

    # Creating CAI character

    cai_character = CaiCharacter(
        os.path.join(get_module_dir(), 'templates', 'cai_character_governor.xml'),
        os.path.join(OUTPUT_DIR, 'cai_characters', new_cai_character_path))

    cai_character.set_owned_indirect(faction_info['cai_id'])

    cai_character.set_id(character_cai_id)

    cai_character.set_character_id(character_id)

    cai_character.set_governor_id(governor_cai_id)

    # Giving character and adding governorship to faction

    faction = Faction(os.path.join(OUTPUT_DIR, 'factions', faction_info['path']))

    faction.add_governor_id(governor_id)
    faction.add_character_path(new_character_path)

    # Giving character and adding governorship to CAI faction

    cai_faction = CaiFaction(os.path.join(OUTPUT_DIR, 'cai_factions', faction_info['cai_path']))

    cai_faction.add_theatre_id(theatre_cai_id)
    cai_faction.add_character_id(character_cai_id)
    cai_faction.add_governor_id(governor_cai_id)

    # Adding governorship and character to CAI world

    cai_world = CaiWorld(os.path.join(OUTPUT_DIR, 'cai_interface', 'cai_world.xml'))

    cai_world.add_governorships_path(new_cai_governorship_path)

    cai_world.add_characters_path(new_cai_character_path)

    # Applying changes

    character.write_xml()
    cai_character.write_xml()

    faction.write_xml()
    cai_faction.write_xml()

    government.write_xml()
    cai_governorship.write_xml()

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

    GOVERNORSHIP_IDS.loc[GOVERNORSHIP_IDS.index.size] = {
        'faction_id': faction_info['id'],
        'name': new_governorship_name,
        'theatre': new_governorship_name.split('_')[1],
        'id': governor_id,
        'cabinet_id': cabinet_id,
        'character_id': character_id,
        'government_type': faction_info['government_type'],
        'government_id': faction_info['government_id'],
        'path': faction_info['government_path'],
        'cai_id': governor_cai_id,
        'cai_path': new_cai_governorship_path
    }



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python create_governorship.py britain governor_india 900000000 800000000 700000000 990000000 880000000')
    parser.add_argument('faction_name', type=str, help='')
    parser.add_argument('new_governorship_name', type=str, choices=['governor_america', 'governor_europe', 'governor_india'], help='')
    parser.add_argument('character_id', type=str, help='')
    parser.add_argument('governor_id', type=str, help='')
    parser.add_argument('cabinet_id', type=str, help='')
    parser.add_argument('character_cai_id', type=str, help='')
    parser.add_argument('governor_cai_id', type=str, help='')
    parser.add_argument('-g', '--gender', type=str, default='m', choices=['m', 'f'], help='Gender as found in db/names_tables/names.tsv')
    args_name = parser.add_argument_group('Preset name', description='Use either of the following arguments if you wish the character to have non-random name.')
    args_name.add_argument('-p', '--names_group', type=str, help='Names group as found in db/names_tables/names.tsv')
    args_name.add_argument('-f', '--forename', type=str, help='Forename as found in db/names_tables/names.tsv')
    args_name.add_argument('-l', '--surname', type=str, help='Surname as found in db/names_tables/names.tsv')
    args_birth = parser.add_argument_group('Preset birth date', description='Use either of the following arguments if you wish the character to have non-random birth date.')
    args_birth.add_argument('-s', '--birth_season', type=str, choices=['summer', 'winter'], help='')
    args_birth.add_argument('-y', '--birth_year', type=str, help='')
    args_portrait = parser.add_argument_group('Preset portrait', description='Use either of the following arguments if you wish the character to have non-random birth portrait.')
    args_portrait.add_argument('-c', '--portrait_culture', type=str, help='')
    args_portrait.add_argument('-a', '--portrait_age', type=str, choices=['young', 'old'], help='')
    args_portrait.add_argument('-n', '--portrait_number', type=str, help='')
    args = parser.parse_args()

    faction_name = args.faction_name
    new_governorship_name = args.new_governorship_name
    character_id = args.character_id
    governor_id = args.governor_id
    cabinet_id = args.cabinet_id
    character_cai_id = args.character_cai_id
    governor_cai_id = args.governor_cai_id
    gender = args.gender
    names_group = args.names_group
    forename = args.forename
    surname = args.surname
    birth_season = args.birth_season
    birth_year = args.birth_year
    portrait_culture = args.portrait_culture
    portrait_age = args.portrait_age
    portrait_number = args.portrait_number

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)
    GOVERNORSHIP_IDS = pd.read_csv(GOVERNORSHIP_IDS_PATH, delimiter='\t', dtype=str)
    CHARACTER_IDS = pd.read_csv(CHARACTER_IDS_PATH, delimiter='\t', dtype=str)

    create_governorship(
        faction_name,
        new_governorship_name,
        character_id,
        governor_id,
        cabinet_id,
        character_cai_id,
        governor_cai_id,
        gender,
        names_group,
        forename,
        surname,
        birth_season,
        birth_year,
        portrait_culture,
        portrait_age,
        portrait_number)

    CHARACTER_IDS.to_csv(CHARACTER_IDS_PATH, sep='\t', index=False)
    GOVERNORSHIP_IDS.to_csv(GOVERNORSHIP_IDS_PATH, sep='\t', index=False)
