import argparse
import os
import pandas as pd

from ..lib import *



def remove_region_unit_resource(region_name: VANILLA_REGION_KEY_HINTS, new_resource: str):
    '''
    example:
        remove_region_unit_resource('georgia', 'tatars')
    '''

    # TODO: Assert region unit resource exists in DB

    assert region_name in REGION_IDS['name'].to_list(), f"{region_name} is not present in {REGION_IDS_PATH}."

    # Collecting info

    region_info = REGION_IDS[REGION_IDS['name'].eq(region_name)].iloc[0]

    # Adding region unit resource

    region = Region(os.path.join(OUTPUT_DIR, 'region', region_info['path']))

    region.add_resource(new_resource)

    # Applying changes

    region.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python remove_region_unit_resource.py georgia tatars')
    parser.add_argument('region_name', type=str, help='')
    parser.add_argument('new_resource', type=str, help='Resource as found in db/region_unit_resources_tables/region_unit_resources.tsv')
    args = parser.parse_args()

    region_name = args.region_name
    new_resource = args.new_resource

    REGION_IDS = pd.read_csv(REGION_IDS_PATH, delimiter='\t', dtype=str)

    remove_region_unit_resource(region_name, new_resource)
