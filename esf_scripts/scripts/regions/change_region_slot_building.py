import argparse
import os
import pandas as pd

from ..lib import *



def change_region_slot_building(
    slot_name: str,
    new_building_name: str,
    faction_name: VANILLA_FACTION_KEY_HINTS,
    government_type: Literal['gov_absolute_monarchy', 'gov_constitutional_monarchy', 'gov_republic'],
    remove: bool = False):
    '''
    example:
        change_region_slot_building('town:punjab:kasur', 'coaching_inn', 'punjab', 'gov_absolute_monarchy')
    '''

    assert slot_name in REGION_SLOT_IDS['name'].to_list(), f"{slot_name} is not present in {REGION_SLOT_IDS_PATH}."

    # Collecting info

    region_slot_info = REGION_SLOT_IDS[REGION_SLOT_IDS['name'].eq(slot_name)].iloc[0]

    # Reassigning building in region slot

    region_slot = RegionSlot(os.path.join(OUTPUT_DIR, 'region_slot', region_slot_info['path']))

    if not region_slot.has_building_manager():
        raise NotImplementedError('Changing buildings in towns which have not yet emerged is not implemented.')

    if region_slot.get_constructed() == 'yes':
        region_slot.remove_building()
    if not remove:
        region_slot.add_building(new_building_name, faction_name, government_type)

    # Applying changes

    region_slot.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python change_region_slot_building.py town:punjab:kasur coaching_inn punjab gov_absolute_monarchy')
    parser.add_argument('slot_name', type=str, help='')
    parser.add_argument('new_building_name', type=str, help='')
    parser.add_argument('faction_name', type=str, help='')
    parser.add_argument('government_type', type=str, help='')
    parser.add_argument('-r', '--remove', action='store_true', help='')
    args = parser.parse_args()

    slot_name = args.slot_name
    new_building_name = args.new_building_name
    faction_name = args.faction_name
    government_type = args.government_type
    remove = args.remove

    REGION_SLOT_IDS = pd.read_csv(REGION_SLOT_IDS_PATH, delimiter='\t', dtype=str)

    change_region_slot_building(slot_name, new_building_name, faction_name, government_type, remove)
