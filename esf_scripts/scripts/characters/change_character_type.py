import argparse
import os
import pandas as pd

from ..lib import *



def change_character_type(character_file_name: str, new_type: str):
    '''
    example:
        change_character_type('georgia-gentleman-0001.xml', 'orthodox_missionary')
    '''

    assert character_file_name in CHARACTER_IDS['path'].to_list(), f"{character_file_name} is not present in {CHARACTER_IDS_PATH}."

    # TODO: Reassign abilities and attributes

    # Collecting info

    character_info = CHARACTER_IDS[CHARACTER_IDS['path'].eq(character_file_name)].iloc[0]

    unsupported_types = dict.fromkeys(['admiral', 'bandit', 'captain', 'colonel', 'General', 'minister', 'pirate'])
    if character_info['character_type'] in unsupported_types or new_type in unsupported_types:
        raise NotImplementedError(f"Changing to/from type {', '.join(unsupported_types)} is not implemented yet.")

    agent_to_agent_attributes_info = AGENT_TO_AGENT_ATTRIBUTES_TABLE[AGENT_TO_AGENT_ATTRIBUTES_TABLE['agent'].eq(new_type)]

    agent_to_agent_abilities_info = AGENT_TO_AGENT_ABILITIES_TABLE[AGENT_TO_AGENT_ABILITIES_TABLE['agent'].eq(new_type)].merge(
        ABILITIES_TABLE, how='inner', on='ability')

    # Reassigning character type

    character = Character(os.path.join(OUTPUT_DIR, 'character', character_info['path']))

    old_type = character.get_type()

    character.set_type(new_type)

    agent_culture = character.get_agent_onscreen_name().replace(f"agent_culture_details_onscreen_name_{old_type}", '')
    new_agent_on_screen_name = f"agent_culture_details_onscreen_name_{new_type}{agent_culture}"

    character.set_agent_onscreen_name(new_agent_on_screen_name)

    character.clear_traits()
    character.clear_ancillaries()

    character.clear_agent_attribute_values()

    for index, attribute_info in agent_to_agent_attributes_info.iterrows():
        character.set_agent_attribute_value(attribute_info['attribute'], attribute_info['default_value'])

    character.clear_agent_abilities()

    for index, ability_info in agent_to_agent_abilities_info.iterrows():
        ability = character.get_agent_ability(ability_info['ability'])
        ability.set_attribute('' if pd.isna(ability_info['associated_attribute']) else ability_info['associated_attribute'])
        ability.set_level(ability_info['default_value'])

    # Applying changes

    character.write_xml()

    CHARACTER_IDS.loc[CHARACTER_IDS['path'].eq(character_file_name), 'character_type'] = new_type



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python change_character_type.py georgia-gentleman-0001.xml orthodox_missionary')
    parser.add_argument('character_file_name', type=str, help='')
    parser.add_argument('new_type', type=str, help='')
    args = parser.parse_args()

    character_file_name = args.character_file_name
    new_type = args.new_type

    CHARACTER_IDS = pd.read_csv(CHARACTER_IDS_PATH, delimiter='\t', dtype=str)

    change_character_type(character_file_name, new_type)

    CHARACTER_IDS.to_csv(CHARACTER_IDS_PATH, sep='\t', index=False)
