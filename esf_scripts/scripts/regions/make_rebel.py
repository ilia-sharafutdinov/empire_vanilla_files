import argparse
import os
import pandas as pd

from ..lib import *



def make_rebel(region_name: VANILLA_REGION_KEY_HINTS):
    '''
    example:
        make_rebel('baluchistan')
    '''

    assert region_name in REGION_IDS['name'].to_list(), f"{region_name} is not present in {REGION_IDS_PATH}."

    # Collecting info

    region_info = REGION_IDS[REGION_IDS['name'].eq(region_name)].iloc[0]

    region = Region(os.path.join(OUTPUT_DIR, 'region', region_info['path']))

    faction_info = FACTION_IDS[FACTION_IDS['id'].eq(region.get_faction_id())].iloc[0]

    government_type = faction_info['government_type']

    # Reassigning rebelling faction and on-screen name

    population = Population(region.get_population_path())

    if government_type in ['gov_absolute_monarchy', 'gov_republic']:
        population.social_class_lower.resistance_to_foreign_occupation = -100
        population.social_class_lower.turns_rioting = 3
    if government_type in ['gov_constitutional_monarchy', 'gov_republic']:
        population.social_class_middle.resistance_to_foreign_occupation = -100
        population.social_class_middle.turns_rioting = 3
    if government_type in ['gov_absolute_monarchy', 'gov_constitutional_monarchy']:
        population.social_class_upper.resistance_to_foreign_occupation = -100
        population.social_class_upper.turns_rioting = 3

    # Applying changes

    population.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python make_rebel.py baluchistan')
    parser.add_argument('region_name', type=str, help='')
    args = parser.parse_args()

    region_name = args.region_name

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)
    REGION_IDS = pd.read_csv(REGION_IDS_PATH, delimiter='\t', dtype=str)

    make_rebel(region_name)
