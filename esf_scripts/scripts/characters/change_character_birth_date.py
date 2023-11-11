import argparse
import os
import pandas as pd

from ..lib import *



def change_character_birth_date(
    character_file_name: str,
    birth_season: Literal['summer', 'winter'] = None,
    birth_year: int = None):
    '''
    example:
        change_character_birth_date('westphalia-minister-0001.xml', 'winter', 1790)
    '''

    assert character_file_name in CHARACTER_IDS['path'].to_list(), f"{character_file_name} is not present in {CHARACTER_IDS_PATH}."

    # Collecting info

    character_info = CHARACTER_IDS[CHARACTER_IDS['path'].eq(character_file_name)].iloc[0]

    if not birth_season:
        birth_season = generate_season()
    if not birth_year:
        birth_year = get_starting_year() - generate_age()
    birth_date = f"{birth_season} {birth_year}"

    # Reassigning character birth date

    character = Character(os.path.join(OUTPUT_DIR, 'character', character_info['path']))

    character.set_birth_date(birth_date)

    # Applying changes

    character.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python change_character_birth_date.py westphalia-minister-0001.xml --birth_season winter --birth_year 1790')
    parser.add_argument('character_file_name', type=str, help='')
    parser.add_argument('-s', '--birth_season', type=str, choices=['summer', 'winter'], help='')
    parser.add_argument('-y', '--birth_year', type=str, help='')
    args = parser.parse_args()

    character_file_name = args.character_file_name
    birth_season = args.birth_season
    birth_year = args.birth_year

    CHARACTER_IDS = pd.read_csv(CHARACTER_IDS_PATH, delimiter='\t', dtype=str)

    change_character_birth_date(character_file_name, birth_season, birth_year)
