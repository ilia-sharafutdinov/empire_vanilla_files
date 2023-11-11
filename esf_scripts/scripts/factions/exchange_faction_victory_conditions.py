import argparse
import os
import pandas as pd

from ..lib import *



def exchange_faction_victory_conditions(first_faction_name: VANILLA_FACTION_KEY_HINTS, second_faction_name: VANILLA_FACTION_KEY_HINTS):
    '''
    example:
        exchange_faction_victory_conditions('greece', 'venice')
    '''

    assert first_faction_name in FACTION_IDS['name'].to_list(), f"{first_faction_name} is not present in {FACTION_IDS_PATH}."
    assert second_faction_name in FACTION_IDS['name'].to_list(), f"{second_faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    first_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(first_faction_name)].iloc[0]
    second_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(second_faction_name)].iloc[0]

    if pd.isna(first_faction_info['victory_condition_path']) or pd.isna(second_faction_info['victory_condition_path']):
        raise NotImplementedError("Support for cases when one or both factions lack victory conditions are not implemented yet.")

    # TODO: Work around cases when one of the factions lack victory conditions

    # Reassigning faction victory conditions

    first_faction_victory_conditions = VictoryCondition(first_faction_info['victory_condition_path'])
    second_faction_victory_conditions = VictoryCondition(second_faction_info['victory_condition_path'])

    first_faction_victory_conditions.faction_name = second_faction_name
    second_faction_victory_conditions.faction_name = first_faction_name

    # Applying changes

    first_faction_victory_conditions.write_xml()
    second_faction_victory_conditions.write_xml()

    FACTION_IDS.loc[FACTION_IDS['name'].eq(first_faction_info['name']), 'victory_condition_path'] = second_faction_info['victory_condition_path']
    FACTION_IDS.loc[FACTION_IDS['name'].eq(second_faction_info['name']), 'victory_condition_path'] = first_faction_info['victory_condition_path']



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python exchange_faction_victory_conditions.py greece venice')
    parser.add_argument('first_faction_name', type=str, help='')
    parser.add_argument('second_faction_name', type=str, help='')
    args = parser.parse_args()

    first_faction_name = args.first_faction_name
    second_faction_name = args.second_faction_name

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)

    exchange_faction_victory_conditions(first_faction_name, second_faction_name)

    FACTION_IDS.to_csv(FACTION_IDS_PATH, sep='\t', index=False)
