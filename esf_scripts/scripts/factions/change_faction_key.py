import argparse
import os
import pandas as pd

from ..lib import *



def change_faction_key(old_faction_name: VANILLA_FACTION_KEY_HINTS, new_faction_name: VANILLA_FACTION_KEY_HINTS):
    '''
    example:
        change_faction_key('piedmont_savoy', 'swiss_confederation')
    '''

    assert old_faction_name in SUPPORTED_FACTION_KEYS, f"{old_faction_name} is not present in factions_tables."
    assert new_faction_name in SUPPORTED_FACTION_KEYS, f"{new_faction_name} is not present in factions_tables."

    assert old_faction_name in FACTION_IDS['name'].to_list(), f"{old_faction_name} is not present in {FACTION_IDS_PATH}."
    assert new_faction_name not in FACTION_IDS['name'].to_list(), f"{new_faction_name} is already present in {FACTION_IDS_PATH}."

    # TODO: Fix colours application logic

    # Collecting info

    faction_info = FACTION_IDS[FACTION_IDS['name'].eq(old_faction_name)].iloc[0]

    new_faction_table_record = FACTIONS_TABLE[FACTIONS_TABLE['key'].eq(new_faction_name)].iloc[0]

    government = Government(os.path.join(OUTPUT_DIR, 'government', faction_info['government_path']))

    # Reassigning faction key

    faction = Faction(os.path.join(OUTPUT_DIR, 'factions', faction_info['path']))

    faction.set_name(new_faction_name)
    faction.set_campaign_player_setup_name(new_faction_name)

    faction.set_on_screen_name(new_faction_table_record['screen_name'])

    if pd.isna(new_faction_table_record['republican_flag_path']):
        faction.set_flag_path(new_faction_table_record['flags_path'])
        faction.set_revolutionary_flag_path(new_faction_table_record['flags_path'])
    elif pd.notna(new_faction_table_record['republican_flag_path']) and government.get_type() in ['gov_absolute_monarchy', 'gov_constitutional_monarchy']:
        faction.set_flag_path(new_faction_table_record['flags_path'])
        faction.set_revolutionary_flag_path(new_faction_table_record['republican_flag_path'])
    elif pd.notna(new_faction_table_record['republican_flag_path']) and (government.get_type() == 'gov_republic'):
        faction.set_flag_path(new_faction_table_record['republican_flag_path'])
        faction.set_revolutionary_flag_path(new_faction_table_record['flags_path'])
    else:
        raise ValueError(f"Can not determin flag paths. Please check the data.")

    if pd.notna(new_faction_table_record['primary_colour_r']):
        faction.set_primary_colour(rgb2hex(new_faction_table_record['primary_colour_r'], new_faction_table_record['primary_colour_g'], new_faction_table_record['primary_colour_b']))
        faction.set_secondary_colour(rgb2hex(new_faction_table_record['secondary_colour_r'], new_faction_table_record['secondary_colour_g'], new_faction_table_record['secondary_colour_b']))
        faction.set_uniform_colour(rgb2hex(new_faction_table_record['uniform_colour_r'], new_faction_table_record['uniform_colour_g'], new_faction_table_record['uniform_colour_b']))
        faction.set_revolutionary_primary_colour(rgb2hex(new_faction_table_record['primary_colour_r'], new_faction_table_record['primary_colour_g'], new_faction_table_record['primary_colour_b']))
        faction.set_revolutionary_secondary_colour(rgb2hex(new_faction_table_record['secondary_colour_r'], new_faction_table_record['secondary_colour_g'], new_faction_table_record['secondary_colour_b']))
        faction.set_revolutionary_uniform_colour(rgb2hex(new_faction_table_record['uniform_colour_r'], new_faction_table_record['uniform_colour_g'], new_faction_table_record['uniform_colour_b']))
    else:
        faction.set_primary_colour('#' + new_faction_table_record['primary_colour_hex'].lower())
        faction.set_secondary_colour('#' + new_faction_table_record['secondary_colour_hex'].lower())
        faction.set_uniform_colour('#' + new_faction_table_record['uniform_colour_hex'].lower())
        faction.set_revolutionary_primary_colour('#' + new_faction_table_record['primary_colour_hex'].lower())
        faction.set_revolutionary_secondary_colour('#' + new_faction_table_record['secondary_colour_hex'].lower())
        faction.set_revolutionary_uniform_colour('#' + new_faction_table_record['uniform_colour_hex'].lower())

    # Reassigning faction key in world spying array

    world = World(os.path.join(OUTPUT_DIR, 'campaign_env', 'world.xml'))

    world.get_spying_array(faction_info['name']).set_faction_name(new_faction_name)

    # Reassigning faction key in domestic trade routes

    domestic_trade_route = DomesticTradeRoute(os.path.join(OUTPUT_DIR, 'domestic_trade_routes', faction_info['domestic_trade_path']))

    domestic_trade_route.set_faction_name(new_faction_name)

    # Reassigning faction key in international trade routes

    international_trade_routes = InternationalTradeRoutes(os.path.join(OUTPUT_DIR, 'international_trade_routes', faction_info['international_trade_path']))

    international_trade_routes.set_faction_name(new_faction_name)

    # Reassigning faction key in victory conditions

    if pd.notna(faction_info['victory_condition_path']):
        victory_conditions = VictoryCondition(faction_info['victory_condition_path'])

        victory_conditions.faction_name = new_faction_name

    # Reassigning character faction keys

    characters = []

    for path in faction.get_character_paths():
        character = Character(os.path.join(OUTPUT_DIR, 'character', path))

        character.set_faction(new_faction_name)

        characters.append(character)

    # Reassigning army faction keys

    armies = []

    for path in faction.get_army_paths():
        army = Army(os.path.join(OUTPUT_DIR, 'army', path))

        for unit in army.get_land_units() if army.get_type() == 'ARMY' else army.get_naval_units():
            unit.set_commander_faction(new_faction_name)

        armies.append(army)

    # Reassigning region slot faction keys

    region_slots = []

    for governor_title in ['governor_america', 'governor_europe', 'governor_india']:
        post = government.get_post(governor_title)
        if post:
            region_ids = post.get_region_ids()

            if region_ids:
                for region_id in region_ids.split(' '):
                    region_info = REGION_IDS[REGION_IDS['id'].eq(region_id)].iloc[0]
                    region = Region(os.path.join(OUTPUT_DIR, 'region', region_info['path']))

                    for path in region.get_region_slot_paths() + region.get_road_walls_paths():
                        region_slot = RegionSlot(os.path.join(OUTPUT_DIR, 'region_slot', path))

                        if region_slot.has_building_manager() and (region_slot.get_constructed() == 'yes'):
                            region_slot.set_building_faction(new_faction_name)

                            region_slots.append(region_slot)

    # Reassigning faction key in campaign_env

    campaign_setup = CampaignSetup(os.path.join(OUTPUT_DIR, 'campaign_env', Env(os.path.join(OUTPUT_DIR, 'campaign_env', 'env.xml')).get_campaign_setup()))

    campaign_setup.get_player_setup(faction_info['name']).set_name(new_faction_name)

    # Reassigning faction key in cai history

    cai_history = CaiHistory(os.path.join(OUTPUT_DIR, 'cai_interface', 'cai_history.xml'))

    for event in cai_history.get_events(faction_info['name']):
        event.set_faction_name(new_faction_name)
        event.set_event_faction_name(new_faction_name)

    # Reassigning faction key in preopen_map_info

    preopen_map_info = PreopenMapInfo(os.path.join(OUTPUT_DIR, 'preopen_map_info', Esf(os.path.join(OUTPUT_DIR, 'esf.xml')).get_preopen_map_info()))

    preopen_map_info.get_player_setup(faction_info['name']).set_name(new_faction_name)

    preopen_map_info.get_faction_info(faction_info['name']).set_name(new_faction_name)

    if pd.notna(new_faction_table_record['republican_flag_path']) and (government.get_type() == 'gov_republic'):
            preopen_map_info.get_faction_info(faction_info['name']).set_flag(new_faction_table_record['republican_flag_path'])
    else:
        preopen_map_info.get_faction_info(faction_info['name']).set_flag(new_faction_table_record['flags_path'])

    for region_ownership in preopen_map_info.get_faction_regions(faction_info['name']):
        preopen_map_info.set_region_ownership(region_ownership['theatre'], region_ownership['region'], new_faction_name)

    # Reassigning faction key in diplomacy

    for xml_file in os.listdir(os.path.join(OUTPUT_DIR, 'diplomacy')):
        text_replace(os.path.join(OUTPUT_DIR, 'diplomacy', xml_file), f"<!-- {faction_info['name']} -->", f"<!-- {new_faction_name} -->", regex=False)

    # Applying changes

    faction.write_xml()

    world.write_xml()

    domestic_trade_route.write_xml()
    international_trade_routes.write_xml()

    if pd.notna(faction_info['victory_condition_path']):
        victory_conditions.write_xml()

    for character in characters:
        character.write_xml()
        CHARACTER_IDS.loc[CHARACTER_IDS['id'].eq(character.get_id()), 'faction_name'] = new_faction_name

    for army in armies:
        army.write_xml()

    for region_slot in region_slots:
        region_slot.write_xml()

    campaign_setup.write_xml()

    cai_history.write_xml()

    preopen_map_info.write_xml()

    FACTION_IDS.loc[FACTION_IDS['name'].eq(faction_info['name']), 'name'] = new_faction_name



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python change_faction_key.py piedmont_savoy swiss_confederation')
    parser.add_argument('old_faction_name', type=str, help='')
    parser.add_argument('new_faction_name', type=str, help='')
    args = parser.parse_args()

    old_faction_name = args.old_faction_name
    new_faction_name = args.new_faction_name

    CHARACTER_IDS = pd.read_csv(CHARACTER_IDS_PATH, delimiter='\t', dtype=str)
    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)
    REGION_IDS = pd.read_csv(REGION_IDS_PATH, delimiter='\t', dtype=str)

    change_faction_key(old_faction_name, new_faction_name)

    CHARACTER_IDS.to_csv(CHARACTER_IDS_PATH, sep='\t', index=False)
    FACTION_IDS.to_csv(FACTION_IDS_PATH, sep='\t', index=False)
