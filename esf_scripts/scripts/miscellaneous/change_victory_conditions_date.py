import argparse
import os
import pandas as pd

from ..lib import *



def change_victory_conditions_date(campaign_type: Literal['0 (Short)', '1 (Long)', '2 (Prestige)', '3 (Global Domination)'], new_end_year: int):
    '''
    example:
        change_victory_conditions_date('1 (Long)', 1899)
    '''

    # Collecting info

    new_end_year = str(new_end_year)

    # Reassigning starting date in victory conditions

    victory_conditionss = []

    for path in os.listdir(os.path.join(OUTPUT_DIR, 'victory_conditions')):
        victory_conditions = VictoryCondition(path)

        victory_conditions.victory_conditions_blocks[campaign_type].year = new_end_year

        victory_conditionss.append(victory_conditions)

    # Applying changes

    for victory_conditions in victory_conditionss:
        victory_conditions.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python change_victory_conditions_date.py "1 (Long)" 1899')
    parser.add_argument('campaign_type', type=str, choices=['0 (Short)', '1 (Long)', '2 (Prestige)', '3 (Global Domination)'], help='')
    parser.add_argument('new_end_year', type=str, help='')
    args = parser.parse_args()

    campaign_type = args.campaign_type
    new_end_year = args.new_end_year

    change_victory_conditions_date(campaign_type, new_end_year)
