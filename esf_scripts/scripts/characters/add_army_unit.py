import argparse
import os
import pandas as pd

from ..lib import *



def add_army_unit(character_file_name: str, unit_type: str, unit_id: int, unit_cai_id: int):
    '''
    example:
        add_army_unit('ottomans-colonel-0003.xml', 'euro_militia_infantry', 600000000, 660000000)
    '''

    assert character_file_name in CHARACTER_IDS['path'].to_list(), f"{character_file_name} is not present in {CHARACTER_IDS_PATH}."

    assert unit_type in SUPPORTED_UNIT_KEYS, f"{unit_type} is not present in units_tables."

    # Collecting info

    character_info = CHARACTER_IDS[CHARACTER_IDS['path'].eq(character_file_name)].iloc[0]

    assert pd.notna(character_info['army_path']), f"Character {character_file_name} does not have an associated army assigned in {CHARACTER_IDS_PATH}."

    character = Character(os.path.join(OUTPUT_DIR, 'character', character_info['path']))

    names_group = FACTIONS_TABLE[FACTIONS_TABLE['key'].eq(character.get_faction())]['name_group'].iloc[0]

    new_name_info = generate_name(names_group, 'm')

    unit_info = UNITS_TABLE[UNITS_TABLE['key'].eq(unit_type)].iloc[0]
    unit_stats_info = UNIT_STATS_LAND_TABLE[UNIT_STATS_LAND_TABLE['key'].eq(unit_type)].iloc[0]

    unit_id = str(unit_id)
    unit_cai_id = str(unit_cai_id)

    # Adding unit to army

    army = Army(os.path.join(OUTPUT_DIR, 'army', character_info['army_path']))

    if army.get_type() != 'ARMY':
        raise NotImplementedError(f"Adding units to armies of type '{army.get_type()}' is not implemented.")

    first_unit = army.get_land_units()[0]

    # TODO: Change unit name allocations

    unit_template = f'''
   <rec type="UNITS_ARRAY">
    <land_unit commander="{first_unit.get_commander_faction()} {new_name_info['forename']} {new_name_info['surname']}" created="{first_unit.get_creation_date()}" deaths="0" exp="0" kills="0" mp="{unit_info['campaign_action_points']}" name="" size="{unit_stats_info['men']}/{unit_stats_info['men']}" type="{unit_info['key']}" unit_id="{unit_id}"/>
   </rec>
  '''

    army.add_land_unit(parse_xml_string(unit_template))

    # Adding unit to CAI mobile

    cai_mobile = CaiMobile(os.path.join(OUTPUT_DIR, 'cai_mobiles', character_info['cai_mobile_path']))

    cai_mobile.add_unit_id(unit_cai_id)

    # Adding unit to CAI world

    cai_world = CaiWorld(os.path.join(OUTPUT_DIR, 'cai_interface', 'cai_world.xml'))

    new_cai_unit_path = f"{str(int(max(cai_world.get_units_paths()).replace('.xml', '')) + 1).zfill(4)}.xml"

    cai_world.add_units_path(new_cai_unit_path)

    # Adding unit to CAI units

    cai_unit = CaiUnit(
        os.path.join(get_module_dir(), 'templates', 'cai_unit.xml'),
        os.path.join(OUTPUT_DIR, 'cai_units', new_cai_unit_path))

    cai_unit.set_id(unit_cai_id)
    cai_unit.set_unit_id(unit_id)
    cai_unit.set_character_resource_id(cai_mobile.get_id())

    # Applying changes

    army.write_xml()
    cai_mobile.write_xml()

    cai_unit.write_xml()
    cai_world.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python add_army_unit.py ottomans-colonel-0003.xml euro_militia_infantry 600000000 660000000')
    parser.add_argument('character_file_name', type=str, help='')
    parser.add_argument('unit_type', type=str, help='Unit as found in db/units_tables/units.tsv')
    parser.add_argument('unit_id', type=str, help='')
    parser.add_argument('unit_cai_id', type=str, help='')
    args = parser.parse_args()

    character_file_name = args.character_file_name
    unit_type = args.unit_type
    unit_id = args.unit_id
    unit_cai_id = args.unit_cai_id

    CHARACTER_IDS = pd.read_csv(CHARACTER_IDS_PATH, delimiter='\t', dtype=str)

    add_army_unit(character_file_name, unit_type, unit_id, unit_cai_id)
