import argparse
import os
import pandas as pd

from ..lib import *



def change_character_location(character_file_name: str, new_region_name: VANILLA_REGION_KEY_HINTS, x: float, y: float):
    '''
    example:
        change_character_location('maratha-General-0001.xml', 'bengal', 619.239990234375, 172.52999877929688)
    '''

    assert character_file_name in CHARACTER_IDS['path'].to_list(), f"{character_file_name} is not present in {CHARACTER_IDS_PATH}."
    assert new_region_name in REGION_IDS['name'].to_list(), f"{new_region_name} is not present in {REGION_IDS_PATH}."

    # Collecting info

    character_info = CHARACTER_IDS[CHARACTER_IDS['path'].eq(character_file_name)].iloc[0]

    character = Character(os.path.join(OUTPUT_DIR, 'character', character_info['path']))

    assert character.get_type() != 'minister', "Changing location of 'minister' character types is not supported."
    if character.get_type() not in ('General', 'colonel'):
        raise NotImplementedError(f"Changing location of '{character.get_type()}' character types is not implemented yet.")

    cai_mobile = CaiMobile(os.path.join(OUTPUT_DIR, 'cai_mobiles', character_info['cai_mobile_path']))

    old_region_cai_id = cai_mobile.get_region_id()

    old_region_info = REGION_IDS[REGION_IDS['cai_id'].eq(old_region_cai_id)].iloc[0]
    new_region_info = REGION_IDS[REGION_IDS['name'].eq(new_region_name)].iloc[0]

    x = str(x)
    y = str(y)

    # TODO: Fix forts handover
    # TODO: Fix army in building slot ID

    # Reassigning character location

    if character.get_building_slot_id() != '0':
        raise NotImplementedError(f"Changing location of characters inside slots is not implemented yet.")

    if pd.notna(character_info['army_path']):
        army = Army(os.path.join(OUTPUT_DIR, 'army', character_info['army_path']))

        if army.get_building_slot_id() != '0':
            raise NotImplementedError(f"Changing location of armies inside slots is not implemented yet.")

    character.set_x(x)
    character.set_y(y)

    character.clear_v2x()

    # Removing character from old region

    old_cai_region = CaiRegion(os.path.join(OUTPUT_DIR, 'cai_regions', old_region_info['cai_path']))

    old_cai_region.remove_character_resource_id(cai_mobile.get_id())

    # Adding character to new region

    new_cai_region = CaiRegion(os.path.join(OUTPUT_DIR, 'cai_regions', new_region_info['cai_path']))

    new_cai_region.add_character_resource_id(cai_mobile.get_id())

    # Reassigning CAI mobile location

    new_region = Region(os.path.join(OUTPUT_DIR, 'region', new_region_info['path']))

    new_settlement_info = REGION_SLOT_IDS[REGION_SLOT_IDS['path'].eq(new_region.get_settlement_slot_path())].iloc[0]

    new_cai_settlement = CaiSettlement(os.path.join(OUTPUT_DIR, 'cai_settlements', new_settlement_info['cai_path']))

    cai_mobile.set_x(x)
    cai_mobile.set_y(y)
    cai_mobile.set_region_id(new_region_info['cai_id'])
    cai_mobile.set_theatre_id(THEATRE_TO_CAI_ID[new_region_info['theatre']])
    cai_mobile.set_area_id(new_cai_settlement.get_area_id())

    # cai_mobile.clear_bdi()

    # Applying changes

    character.write_xml()
    cai_mobile.write_xml()
    old_cai_region.write_xml()
    new_cai_region.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python change_character_location.py maratha-General-0001.xml bengal 619.239990234375 172.52999877929688')
    parser.add_argument('character_file_name', type=str, help='')
    parser.add_argument('new_region_name', type=str, help='')
    parser.add_argument('x', type=str, help='')
    parser.add_argument('y', type=str, help='')
    args = parser.parse_args()

    character_file_name = args.character_file_name
    new_region_name = args.new_region_name
    x = args.x
    y = args.y

    CHARACTER_IDS = pd.read_csv(CHARACTER_IDS_PATH, delimiter='\t', dtype=str)
    REGION_IDS = pd.read_csv(REGION_IDS_PATH, delimiter='\t', dtype=str)
    REGION_SLOT_IDS = pd.read_csv(REGION_SLOT_IDS_PATH, delimiter='\t', dtype=str)

    change_character_location(character_file_name, new_region_name, x, y)
