import argparse
import os
import pandas as pd

from ..lib import *



def change_governorship_theatre(
        faction_name: VANILLA_FACTION_KEY_HINTS,
        old_governorship_name=Literal['governor_america', 'governor_europe', 'governor_india'],
        new_governorship_name=Literal['governor_america', 'governor_europe', 'governor_india']):

    assert faction_name in FACTION_IDS['name'].to_list(), f"{faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    faction_info = FACTION_IDS[FACTION_IDS['name'].eq(faction_name)].iloc[0]
    if GOVERNORSHIP_IDS[GOVERNORSHIP_IDS['faction_id'].eq(faction_info['id'])&GOVERNORSHIP_IDS['name'].eq(old_governorship_name)].size == 0:
        raise ValueError(f"{GOVERNORSHIP_IDS_PATH} does not contain a governor where faction_id = {faction_info['id']} and name = {old_governorship_name}.")

    if GOVERNORSHIP_IDS[GOVERNORSHIP_IDS['faction_id'].eq(faction_info['id'])].index.size >= 2:
        raise NotImplementedError(f"Changing governorship theatre for factions having more than one governorship is not implemented yet.")

    governorship_info = GOVERNORSHIP_IDS[GOVERNORSHIP_IDS['faction_id'].eq(faction_info['id'])&GOVERNORSHIP_IDS['name'].eq(old_governorship_name)].iloc[0]

    old_theatre_cai_id = GovernmentPost.governorships_to_theatre_cai_id[old_governorship_name]
    new_theatre_cai_id = GovernmentPost.governorships_to_theatre_cai_id[new_governorship_name]

    # TODO: Research BDI influence

    # Reassigning theatre in CAI faction

    cai_faction = CaiFaction(os.path.join(OUTPUT_DIR, 'cai_factions', faction_info['cai_path']))

    cai_faction.remove_theatre_id(old_theatre_cai_id)
    cai_faction.add_theatre_id(new_theatre_cai_id)

    # Renaming governorhip

    government = Government(os.path.join(OUTPUT_DIR, 'government', governorship_info['path']))

    government.get_post(old_governorship_name).set_title(new_governorship_name)

    # Reassigning theatre in CAI governorhip

    cai_governorship = CaiGovernorship(os.path.join(OUTPUT_DIR, 'cai_governorships', governorship_info['cai_path']))

    cai_governorship.set_theatre_id(new_theatre_cai_id)

    # Applying changes

    cai_faction.write_xml()

    government.write_xml()
    cai_governorship.write_xml()

    GOVERNORSHIP_IDS.loc[GOVERNORSHIP_IDS['faction_id'].eq(faction_info['id'])&GOVERNORSHIP_IDS['name'].eq(old_governorship_name), 'theatre'] = new_governorship_name.split('_')[1]
    GOVERNORSHIP_IDS.loc[GOVERNORSHIP_IDS['faction_id'].eq(faction_info['id'])&GOVERNORSHIP_IDS['name'].eq(old_governorship_name), 'name'] = new_governorship_name



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python change_governorship_theatre.py poland_lithuania governor_europe governor_india')
    parser.add_argument('faction_name', type=str, help='')
    parser.add_argument('old_governorship_name', type=str, choices=['governor_america', 'governor_europe', 'governor_india'], help='')
    parser.add_argument('new_governorship_name', type=str, choices=['governor_america', 'governor_europe', 'governor_india'], help='')
    args = parser.parse_args()

    faction_name = args.faction_name
    old_governorship_name = args.old_governorship_name
    new_governorship_name = args.new_governorship_name

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)
    GOVERNORSHIP_IDS = pd.read_csv(GOVERNORSHIP_IDS_PATH, delimiter='\t', dtype=str)

    change_governorship_theatre(faction_name, old_governorship_name, new_governorship_name)

    GOVERNORSHIP_IDS.to_csv(GOVERNORSHIP_IDS_PATH, sep='\t', index=False)
