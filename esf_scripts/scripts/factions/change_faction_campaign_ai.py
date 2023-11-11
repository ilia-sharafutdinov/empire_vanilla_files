import argparse
import os
import pandas as pd

from ..lib import *



def change_faction_campaign_ai(faction_name: VANILLA_FACTION_KEY_HINTS, new_manager: str = None, new_personality: str = None):
    '''
    example:
        change_faction_campaign_ai('westphalia', new_manager='FULL')
        change_faction_campaign_ai('westphalia', new_personality='trader')
        change_faction_campaign_ai('westphalia', 'FULL', 'trader')
    '''

    assert new_manager is not None or new_personality is not None, "You need to pass either manager or personality or both as arguments to the script."
    assert faction_name in FACTION_IDS['name'].to_list(), f"{faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    faction_info = FACTION_IDS[FACTION_IDS['name'].eq(faction_name)].iloc[0]

    # Reassigning faction religion

    faction = Faction(os.path.join(OUTPUT_DIR, 'factions', faction_info['path']))

    if new_manager:
        faction.set_campaign_ai_manager_behaviour(new_manager)
    if new_personality:
        faction.set_campaign_ai_personality(new_personality)

    # Applying changes

    faction.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:' +
        '\n  python change_faction_campaign_ai.py westphalia --new_manager FULL' +
        '\n  python change_faction_campaign_ai.py westphalia --new_personality trader' +
        '\n  python change_faction_campaign_ai.py westphalia --new_manager FULL --new_personality trader')
    parser.add_argument('faction_name', type=str, help='')
    parser.add_argument('-m', '--new_manager', type=str, help='Campaign AI manager as found in db/campaign_ai_manager_behaviour_junctions_tables/campaign_ai_manager_behaviour_junctions.tsv')
    parser.add_argument('-p', '--new_personality', type=str, help='Campaign AI personality as found in db/campaign_ai_personality_junctions_tables/campaign_ai_personality_junctions.tsv')
    args = parser.parse_args()

    faction_name = args.faction_name
    new_manager = args.new_manager
    new_personality = args.new_personality

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)

    change_faction_campaign_ai(faction_name, new_manager, new_personality)
