import argparse
import os
import pandas as pd

from ..lib import *



def change_army_unit_type(
    character_file_name: str,
    unit_types: List[str]):
    '''
    example:
        change_army_unit_type('ottomans-colonel-0003.xml', ['euro_militia_infantry', 'euro_militia_infantry', 'euro_pikemen'])
    '''

    assert character_file_name in CHARACTER_IDS['path'].to_list(), f"{character_file_name} is not present in {CHARACTER_IDS_PATH}."

    # Collecting info

    character_info = CHARACTER_IDS[CHARACTER_IDS['path'].eq(character_file_name)].iloc[0]

    assert pd.notna(character_info['army_path']), f"Character {character_file_name} does not have an associated army assigned in {CHARACTER_IDS_PATH}."

    # Reassigning army unit types

    army = Army(os.path.join(OUTPUT_DIR, 'army', character_info['army_path']))

    if army.get_type() != 'ARMY':
        raise NotImplementedError(f"Changing unit types in armies of type '{army.get_type()}' is not implemented.")

    assert len(army.get_land_units()) == len(unit_types), f"The number of units passed as argument is different from the number of units in the army."

    for i, unit in enumerate(army.get_land_units()):
        unit_key = unit_types[i]

        assert unit_key in SUPPORTED_UNIT_KEYS, f"{unit_key} is not present in units_tables."

        unit_info = UNITS_TABLE[UNITS_TABLE['key'].eq(unit_key)].iloc[0]
        unit_stats_info = UNIT_STATS_LAND_TABLE[UNIT_STATS_LAND_TABLE['key'].eq(unit_key)].iloc[0]

        # TODO: Change unit name allocations
        unit.set_type(unit_info['key'])
        unit.set_size(f"{unit_stats_info['men']}/{unit_stats_info['men']}")
        unit.set_movement_points(unit_info['campaign_action_points'])

    # Applying changes

    army.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python change_army_unit_type.py ottomans-colonel-0003.xml euro_militia_infantry euro_militia_infantry euro_pikemen')
    parser.add_argument('character_file_name', type=str, help='')
    parser.add_argument('unit_types', type=str, nargs='+', help='Unit as found in db/units_tables/units.tsv')
    args = parser.parse_args()

    character_file_name = args.character_file_name
    unit_types = args.unit_types

    CHARACTER_IDS = pd.read_csv(CHARACTER_IDS_PATH, delimiter='\t', dtype=str)

    change_army_unit_type(character_file_name, unit_types)
