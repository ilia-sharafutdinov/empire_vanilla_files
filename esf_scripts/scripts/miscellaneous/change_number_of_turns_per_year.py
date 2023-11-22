import argparse
import os
import pandas as pd

from ..lib import *



def change_number_of_turns_per_year(new_number_of_turns_per_year: int):
    '''
    example:
        change_number_of_turns_per_year(4)
    '''

    # Collecting info

    new_number_of_turns_per_year = str(new_number_of_turns_per_year)

    # Reassigning number of turns per year

    campaign_model = CampaignModel(os.path.join(OUTPUT_DIR, 'campaign_env', 'campaign_model.xml'))

    campaign_model.set_turns_per_year(new_number_of_turns_per_year)

    # Applying changes

    campaign_model.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python change_number_of_turns_per_year.py 4')
    parser.add_argument('new_number_of_turns_per_year', type=int, help='')
    args = parser.parse_args()

    new_number_of_turns_per_year = args.new_number_of_turns_per_year

    change_number_of_turns_per_year(new_number_of_turns_per_year)
