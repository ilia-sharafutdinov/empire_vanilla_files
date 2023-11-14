import argparse
import os
import pandas as pd

from ..lib import *



def remove_governorship(
    faction_name: VANILLA_FACTION_KEY_HINTS,
    governor_title: Literal['governor_america', 'governor_europe', 'governor_india']):
    '''
    example:
        remove_governorship('safavids', 'governor_india')
    '''

    assert faction_name in FACTION_IDS['name'].to_list(), f"{faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    faction_info = FACTION_IDS[FACTION_IDS['name'].eq(faction_name)].iloc[0]

    government = Government(os.path.join(OUTPUT_DIR, 'government', faction_info['government_path']))

    post = government.get_post(governor_title)

    assert post is not None, f"{faction_name} does not have a {governor_title} governor."
    assert post.get_governor_id() in GOVERNORSHIP_IDS['id'].to_list(), f"{faction_name} is not present in {GOVERNORSHIP_IDS_PATH}."

    governoship_info = GOVERNORSHIP_IDS[GOVERNORSHIP_IDS['id'].eq(post.get_governor_id())].iloc[0]

    character_info = CHARACTER_IDS[CHARACTER_IDS['id'].eq(post.get_character_id())].iloc[0]

    theatre_cai_id = GovernmentPost.governorships_to_theatre_cai_id[governor_title]

    # Removing government post

    government.remove_post(governor_title)

    # Removing governor and character from faction

    faction = Faction(os.path.join(OUTPUT_DIR, 'factions', faction_info['path']))

    faction.remove_governor_id(post.get_governor_id())

    faction.remove_character_path(character_info['path'])

    # Removing governor, theatre and character from CAI faction

    cai_faction = CaiFaction(os.path.join(OUTPUT_DIR, 'cai_factions', faction_info['cai_path']))

    cai_faction.remove_governor_id(governoship_info['cai_id'])

    cai_faction.remove_theatre_id(theatre_cai_id)

    cai_faction.remove_character_id(character_info['cai_id'])

    # Removing governor and character from CAI world

    cai_world = CaiWorld(os.path.join(OUTPUT_DIR, 'cai_interface', 'cai_world.xml'))

    cai_world.remove_governorships_path(governoship_info['cai_path'])

    cai_world.remove_characters_path(character_info['cai_path'])

    # Applying changes

    government.write_xml()

    faction.write_xml()

    cai_faction.write_xml()

    cai_world.write_xml()

    os.remove(os.path.join(OUTPUT_DIR, 'character', character_info['path']))
    os.remove(os.path.join(OUTPUT_DIR, 'cai_characters', character_info['cai_path']))
    os.remove(os.path.join(OUTPUT_DIR, 'cai_governorships', governoship_info['cai_path']))



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python remove_governorship.py safavids governor_india')
    parser.add_argument('faction_name', type=str, help='')
    parser.add_argument('governor_title', type=str, choices=['governor_america', 'governor_europe', 'governor_india'], help='')
    args = parser.parse_args()

    faction_name = args.faction_name
    governor_title = args.governor_title

    CHARACTER_IDS = pd.read_csv(CHARACTER_IDS_PATH, delimiter='\t', dtype=str)
    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)
    GOVERNORSHIP_IDS = pd.read_csv(GOVERNORSHIP_IDS_PATH, delimiter='\t', dtype=str)

    remove_governorship(faction_name, governor_title)
