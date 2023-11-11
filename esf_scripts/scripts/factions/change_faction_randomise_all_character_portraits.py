import argparse
import os
import pandas as pd

from ..lib import *



def change_faction_randomise_all_character_portraits(faction_name: VANILLA_FACTION_KEY_HINTS):
    '''
    example:
        change_faction_randomise_all_character_portraits('westphalia')
    '''

    assert faction_name in FACTION_IDS['name'].to_list(), f"{faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    faction_info = FACTION_IDS[FACTION_IDS['name'].eq(faction_name)].iloc[0]

    # Reassigning faction family portraits

    family = Family(os.path.join(OUTPUT_DIR, 'family', faction_info['family_path']))

    for i, family_member in enumerate(family.get_family_members()):
        if family_member.get_portrait_card() is None:
            continue

        if i == 0:
            faction_leader = True
        else:
            faction_leader = False

        if family_member.get_male() == 'yes':
            if i == 0:
                leader_gender = 'm'
            portrait_type = 'king'
        else:
            if i == 0:
                leader_gender = 'f'
            portrait_type = 'queen'
        portrait_culture = get_portrait_culture(get_faction_culture(faction_info['name']), portrait_type)

        new_portrait_info = generate_portrait(portrait_culture, portrait_type)

        family_member.set_portrait_culture(new_portrait_info['culture'])
        family_member.set_portrait_agent_type(new_portrait_info['character_type'])
        family_member.set_portrait_age(new_portrait_info['age'])
        family_member.set_portrait_number(new_portrait_info['number'], faction_leader=faction_leader)

    # Reassigning faction character portraits

    faction = Faction(os.path.join(OUTPUT_DIR, 'factions', faction_info['path']))

    government = Government(os.path.join(OUTPUT_DIR, 'government', faction_info['government_path']))

    king = government.get_type() in ('gov_absolute_monarchy', 'gov_constitutional_monarchy')

    characters = []

    for character_file_name in faction.get_character_paths():
        character_info = CHARACTER_IDS[CHARACTER_IDS['path'].eq(character_file_name)].iloc[0]

        character = Character(os.path.join(OUTPUT_DIR, 'character', character_info['path']))

        faction_leader = character.get_cabinet_id() == government.get_post('faction_leader').get_id()

        if character.get_portrait_card():
            if king and faction_leader:
                if leader_gender == 'm':
                    portrait_type = 'king'
                else:
                    portrait_type = 'queen'
            else:
                portrait_type = get_portrait_type(character.get_type())
            portrait_culture = get_portrait_culture(get_faction_culture(faction_info['name']), portrait_type)

            new_portrait_info = generate_portrait(portrait_culture, portrait_type)

            character.set_portrait_culture(new_portrait_info['culture'])
            character.set_portrait_agent_type(new_portrait_info['character_type'])
            character.set_portrait_age(new_portrait_info['age'])
            character.set_portrait_number(new_portrait_info['number'], faction_leader=faction_leader)

            characters.append(character)

            if faction_leader and king:
                family_member = family.get_family_members()[0]
                family_member.set_portrait_culture(new_portrait_info['culture'])
                family_member.set_portrait_agent_type(new_portrait_info['character_type'])
                family_member.set_portrait_age(new_portrait_info['age'])
                family_member.set_portrait_number(new_portrait_info['number'], faction_leader=faction_leader)

            # Reassigning faction leader portrait in preopen_map_info

            if faction_leader:
                preopen_map_info = PreopenMapInfo(os.path.join(OUTPUT_DIR, 'preopen_map_info', Esf(os.path.join(OUTPUT_DIR, 'esf.xml')).get_preopen_map_info()))

                preopen_map_info.get_faction_info(character.get_faction()).set_leader_portrait(f"ui/portraits/{new_portrait_info['culture']}/cards/{new_portrait_info['character_type']}/{new_portrait_info['age']}/{str(new_portrait_info['number']).zfill(3)}.tga")

    # Applying changes

    for character in characters:
        character.write_xml()

    family.write_xml()

    preopen_map_info.write_xml()



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

    change_faction_randomise_all_character_portraits(faction_name)
