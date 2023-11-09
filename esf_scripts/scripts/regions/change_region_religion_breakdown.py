import argparse
import os
import pandas as pd

from ..lib import *



def change_region_religion_breakdown(region_name: VANILLA_REGION_KEY_HINTS, religion_breakdown: Population.ReligiousBreakdown):
    '''
    example:
        change_region_religion_breakdown('persia', {'rel_islamic': 0.1, 'rel_shia': 0.9})
    '''

    assert region_name in REGION_IDS['name'].to_list(), f"{region_name} is not present in {REGION_IDS_PATH}."

    # Collecting info

    region_info = REGION_IDS[REGION_IDS['name'].eq(region_name)].iloc[0]

    region = Region(os.path.join(OUTPUT_DIR, 'region', region_info['path']))

    # Reassigning religion breakdown

    population = Population(region.get_population_path())

    population.religion_breakdown = religion_breakdown

    # Applying changes

    population.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python change_region_religion_breakdown.py persia rel_islamic 0.1 rel_shia 0.9')
    parser.add_argument('region_name', type=str, help='')
    parser.add_argument('religion_breakdown', type=str, nargs='+', help='')
    args = parser.parse_args()

    region_name = args.region_name
    religion_breakdown = args.religion_breakdown

    assert (len(religion_breakdown) % 2) == 0, f"Wrong number of arguments. Please ensure religion breakdown is passed correctly."

    for population_percentage in religion_breakdown[1::2]:
        try:
            float(population_percentage)
        except:
            raise ValueError(f"'{population_percentage}' can not be cast to float.")

    religion_breakdown = dict(zip(religion_breakdown[0::2], religion_breakdown[1::2]))

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)
    REGION_IDS = pd.read_csv(REGION_IDS_PATH, delimiter='\t', dtype=str)

    change_region_religion_breakdown(region_name, religion_breakdown)
