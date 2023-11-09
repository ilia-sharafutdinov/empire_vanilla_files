import argparse
import os
import pandas as pd

from ..lib import *



def change_town_prosperity(slot_name: str, prosperity: Literal[1, 2, 3, 4, 5]):
    '''
    example:
        change_town_prosperity('town:persia:qom', 1)
    '''

    assert slot_name in REGION_SLOT_IDS['name'].to_list(), f"{slot_name} is not present in {REGION_SLOT_IDS_PATH}."

    # Collecting info

    region_slot_info = REGION_SLOT_IDS[REGION_SLOT_IDS['name'].eq(slot_name)].iloc[0]

    prosperity = str(prosperity)

    # Changing region slot prosperity

    region_slot = RegionSlot(os.path.join(OUTPUT_DIR, 'region_slot', region_slot_info['path']))

    assert region_slot.get_emerged() == 'yes', f"Town {slot_name} is not emerged yet."

    region_slot.set_town_prosperity(prosperity)

    # Applying changes

    region_slot.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python change_town_prosperity.py town:persia:qom 1')
    parser.add_argument('slot_name', type=str, help='')
    parser.add_argument('prosperity', type=int, choices=[1, 2, 3, 4, 5], help='')
    args = parser.parse_args()

    slot_name = args.slot_name
    prosperity = args.prosperity

    REGION_SLOT_IDS = pd.read_csv(REGION_SLOT_IDS_PATH, delimiter='\t', dtype=str)

    change_town_prosperity(slot_name, prosperity)
