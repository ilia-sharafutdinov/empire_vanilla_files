import argparse
import os
import pandas as pd

from ..lib import *



def change_faction_playability(faction_name: VANILLA_FACTION_KEY_HINTS, playable: Literal['yes', 'no']):
    '''
    example:
        change_faction_playability('punjab', 'yes')
    '''

    assert faction_name in FACTION_IDS['name'].to_list(), f"{faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    faction_info = FACTION_IDS[FACTION_IDS['name'].eq(faction_name)].iloc[0]

    # Reassigning faction playability

    faction = Faction(os.path.join(OUTPUT_DIR, 'factions', faction_info['path']))

    if playable == 'yes':
        faction.make_playable()
    else:
        faction.make_unplayable()

    # Reassigning faction playability in campaign_env

    campaign_setup = CampaignSetup(os.path.join(OUTPUT_DIR, 'campaign_env', Env(os.path.join(OUTPUT_DIR, 'campaign_env', 'env.xml')).get_campaign_setup()))

    if playable == 'yes':
        campaign_setup.get_player_setup(faction_info['name']).make_playable()
    else:
        campaign_setup.get_player_setup(faction_info['name']).make_non_playable()

    # Reassigning faction playability in preopen_map_info

    preopen_map_info = PreopenMapInfo(os.path.join(OUTPUT_DIR, 'preopen_map_info', Esf(os.path.join(OUTPUT_DIR, 'esf.xml')).get_preopen_map_info()))

    if playable == 'yes':
        preopen_map_info.get_player_setup(faction_info['name']).make_playable()
        preopen_map_info.get_faction_info(faction_info['name']).make_playable()
    else:
        preopen_map_info.get_player_setup(faction_info['name']).make_non_playable()
        preopen_map_info.get_faction_info(faction_info['name']).make_non_playable()

    # Applying changes

    faction.write_xml()

    campaign_setup.write_xml()

    preopen_map_info.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python change_faction_playability.py punjab yes')
    parser.add_argument('faction_name', type=str, help='')
    parser.add_argument('playable', type=str, choices=['yes', 'no'], help='')
    args = parser.parse_args()

    faction_name = args.faction_name
    playable = args.playable

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)

    change_faction_playability(faction_name, playable)
