import argparse
import os
import pandas as pd

from ..lib import *



def emerge_town(slot_name: str, prosperity: Literal[1, 2, 3, 4, 5]):
    '''
    example:
        emerge_town('town:persia:qom', 1)
    '''

    assert slot_name in REGION_SLOT_IDS['name'].to_list(), f"{slot_name} is not present in {REGION_SLOT_IDS_PATH}."

    # Collecting info

    region_slot_info = REGION_SLOT_IDS[REGION_SLOT_IDS['name'].eq(slot_name)].iloc[0]

    prosperity = str(prosperity)

    # Emerging region slot

    region_slot = RegionSlot(os.path.join(OUTPUT_DIR, 'region_slot', region_slot_info['path']))

    assert region_slot.get_emerged() == 'no', f"Town {slot_name} already emerged."

    region_slot.set_town_prosperity(prosperity)

    region_slot.make_emerged()

    # Emerging CAI region slot

    cai_building_slot = CaiBuildingSlot(os.path.join(OUTPUT_DIR, 'cai_building_slots', region_slot_info['cai_path']))

    cai_building_slot.make_emerged()

    # Applying changes

    region_slot.write_xml()

    cai_building_slot.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python emerge_town.py town:persia:qom 1')
    parser.add_argument('slot_name', type=str, help='')
    parser.add_argument('prosperity', type=int, choices=[1, 2, 3, 4, 5], help='')
    args = parser.parse_args()

    slot_name = args.slot_name
    prosperity = args.prosperity

    REGION_SLOT_IDS = pd.read_csv(REGION_SLOT_IDS_PATH, delimiter='\t', dtype=str)

    emerge_town(slot_name, prosperity)
