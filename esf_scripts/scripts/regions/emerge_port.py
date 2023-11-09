import argparse
import os
import pandas as pd

from ..lib import *



def emerge_port(slot_name: str, prosperity: Literal[1, 2, 3, 4, 5], new_recruitment_manager_id: int):
    '''
    example:
        emerge_port('port:denmark:lubeck', 1, 500000000)
    '''

    assert slot_name in REGION_SLOT_IDS['name'].to_list(), f"{slot_name} is not present in {REGION_SLOT_IDS_PATH}."

    # Collecting info

    region_slot_info = REGION_SLOT_IDS[REGION_SLOT_IDS['name'].eq(slot_name)].iloc[0]

    template_recruitment_manager = f'''
  <rec type="REGION_RECRUITMENT_MANAGER">
   <ary type="REGION_RECRUITMENT_ITEM_ARRAY"/>
   <no/>
   <i>{new_recruitment_manager_id}</i>
  </rec>
  <rec type="PORT_GARRISON_MANAGER">
   <u>0</u>
   <u>0</u>
   <no/>
  </rec>
  '''

    prosperity = str(prosperity)

    # Emerging region slot

    region_slot = RegionSlot(os.path.join(OUTPUT_DIR, 'region_slot', region_slot_info['path']))

    assert region_slot.get_emerged() == 'no', f"Port {slot_name} already emerged."

    region_slot.set_town_prosperity(prosperity)

    region_slot.make_emerged()

    region_slot.add_recruitment_manager(parse_xml_string(template_recruitment_manager))

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
        '  python emerge_port.py port:denmark:lubeck 1 500000000')
    parser.add_argument('slot_name', type=str, help='')
    parser.add_argument('prosperity', type=int, choices=[1, 2, 3, 4, 5], help='')
    parser.add_argument('new_recruitment_manager_id', type=int, help='')
    args = parser.parse_args()

    slot_name = args.slot_name
    prosperity = args.prosperity
    new_recruitment_manager_id = args.new_recruitment_manager_id

    REGION_SLOT_IDS = pd.read_csv(REGION_SLOT_IDS_PATH, delimiter='\t', dtype=str)

    emerge_port(slot_name, prosperity, new_recruitment_manager_id)
