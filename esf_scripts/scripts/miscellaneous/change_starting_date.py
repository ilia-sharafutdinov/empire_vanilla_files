import argparse
import os
import pandas as pd

from ..lib import *



def change_starting_date(
    new_starting_season: Literal['summer', 'winter'],
    new_starting_year: int,
    prevent_character_birth_dates_change: bool = False,
    prevent_victory_conditions_dates_change: bool = False):
    '''
    example:
        change_starting_date('summer', 1830)
    '''

    # Collecting info

    new_starting_date = f"{new_starting_season} {new_starting_year}"

    campaign_model = CampaignModel(os.path.join(OUTPUT_DIR, 'campaign_env', 'campaign_model.xml'))

    age_difference = int(new_starting_year) - int(campaign_model.get_year())

    # Reassigning character birth dates

    characters = []

    if not prevent_character_birth_dates_change:
        for path in os.listdir(os.path.join(OUTPUT_DIR, 'character')):
            character = Character(os.path.join(OUTPUT_DIR, 'character', path))

            character.add_years_to_age(age_difference)

            characters.append(character)

    # Reassigning army unit creation dates

    armies = []

    for path in os.listdir(os.path.join(OUTPUT_DIR, 'army')):
        army = Army(os.path.join(OUTPUT_DIR, 'army', path))

        for unit in army.get_land_units() if army.get_type() == 'ARMY' else army.get_naval_units():
            unit.set_creation_date(new_starting_date)

        armies.append(army)

    # Reassigning starting date in campaign_model

    campaign_model.set_date(new_starting_date)

    # Reassigning starting date in preopen_map_info

    preopen_map_info = PreopenMapInfo(os.path.join(OUTPUT_DIR, 'preopen_map_info', Esf(os.path.join(OUTPUT_DIR, 'esf.xml')).get_preopen_map_info()))

    preopen_map_info.set_date(new_starting_date)

    # Reassigning starting date in victory conditions

    victory_conditionss = []

    if not prevent_victory_conditions_dates_change:
        for path in os.listdir(os.path.join(OUTPUT_DIR, 'victory_conditions')):
            victory_conditions = VictoryCondition(path)

            for victory_conditions_block in victory_conditions.victory_conditions_blocks.values():
                victory_conditions_block.add_years(age_difference)

            victory_conditionss.append(victory_conditions)

    # Reassigning starting date in save_game_header

    save_game_header = SaveGameHeader(os.path.join(OUTPUT_DIR, 'save_game_header', Esf(os.path.join(OUTPUT_DIR, 'esf.xml')).get_save_game_header()))

    save_game_header.set_year(str(new_starting_year))

    save_game_header.set_season(new_starting_season.capitalize())

    # Reassigning starting date in bdi_pool

    for xml_file in os.listdir(os.path.join(OUTPUT_DIR, 'bdi_pool')):
        text_replace(os.path.join(OUTPUT_DIR, 'bdi_pool', xml_file), '<date>(summer|winter) \\d+</date>', f"<date>{new_starting_date}</date>")

    # Applying changes

    for character in characters:
        character.write_xml()

    for army in armies:
        army.write_xml()

    for victory_conditions in victory_conditionss:
        victory_conditions.write_xml()

    campaign_model.write_xml()

    preopen_map_info.write_xml()

    save_game_header.write_xml()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python change_starting_date.py summer 1830')
    parser.add_argument('new_starting_season', type=str, choices=['summer', 'winter'], help='')
    parser.add_argument('new_starting_year', type=str, help='')
    parser.add_argument('prevent_character_birth_dates_change', action='store_true', help='')
    parser.add_argument('prevent_victory_conditions_dates_change', action='store_true', help='')
    args = parser.parse_args()

    new_starting_season = args.new_starting_season
    new_starting_year = args.new_starting_year
    prevent_character_birth_dates_change = args.prevent_character_birth_dates_change
    prevent_victory_conditions_dates_change = args.prevent_victory_conditions_dates_change

    change_starting_date(new_starting_season, new_starting_year, prevent_character_birth_dates_change, prevent_victory_conditions_dates_change)
