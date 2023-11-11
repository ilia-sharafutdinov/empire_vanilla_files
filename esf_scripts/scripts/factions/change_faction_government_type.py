import argparse
import os
import pandas as pd

from ..lib import *



def change_faction_government_type(
    faction_name: VANILLA_FACTION_KEY_HINTS,
    new_government_type: Literal['gov_absolute_monarchy', 'gov_constitutional_monarchy', 'gov_republic']):
    '''
    example:
        change_faction_government_type('westphalia', 'gov_constitutional_monarchy')
    '''

    assert faction_name in FACTION_IDS['name'].to_list(), f"{faction_name} is not present in {FACTION_IDS_PATH}."

    # TODO: Fix colours application logic

    # Collecting info

    faction_info = FACTION_IDS[FACTION_IDS['name'].eq(faction_name)].iloc[0]

    faction_table_record = FACTIONS_TABLE[FACTIONS_TABLE['key'].eq(faction_name)].iloc[0]

    # Reassigning faction government type

    government = Government(os.path.join(OUTPUT_DIR, 'government', faction_info['government_path']))

    government.set_type(new_government_type)

    # Reassigning faction flags and colours

    faction = Faction(os.path.join(OUTPUT_DIR, 'factions', faction_info['path']))

    if pd.isna(faction_table_record['republican_flag_path']):
        faction.set_flag_path(faction_table_record['flags_path'])
        faction.set_revolutionary_flag_path(faction_table_record['flags_path'])
    elif pd.notna(faction_table_record['republican_flag_path']) and government.get_type() in ['gov_absolute_monarchy', 'gov_constitutional_monarchy']:
        faction.set_flag_path(faction_table_record['flags_path'])
        faction.set_revolutionary_flag_path(faction_table_record['republican_flag_path'])
    elif pd.notna(faction_table_record['republican_flag_path']) and (government.get_type() == 'gov_republic'):
        faction.set_flag_path(faction_table_record['republican_flag_path'])
        faction.set_revolutionary_flag_path(faction_table_record['flags_path'])
    else:
        raise ValueError(f"Can not determin flag paths. Please check the data.")

    if pd.notna(faction_table_record['primary_colour_r']):
        faction.set_primary_colour(rgb2hex(faction_table_record['primary_colour_r'], faction_table_record['primary_colour_g'], faction_table_record['primary_colour_b']))
        faction.set_secondary_colour(rgb2hex(faction_table_record['secondary_colour_r'], faction_table_record['secondary_colour_g'], faction_table_record['secondary_colour_b']))
        faction.set_uniform_colour(rgb2hex(faction_table_record['uniform_colour_r'], faction_table_record['uniform_colour_g'], faction_table_record['uniform_colour_b']))
        faction.set_revolutionary_primary_colour(rgb2hex(faction_table_record['primary_colour_r'], faction_table_record['primary_colour_g'], faction_table_record['primary_colour_b']))
        faction.set_revolutionary_secondary_colour(rgb2hex(faction_table_record['secondary_colour_r'], faction_table_record['secondary_colour_g'], faction_table_record['secondary_colour_b']))
        faction.set_revolutionary_uniform_colour(rgb2hex(faction_table_record['uniform_colour_r'], faction_table_record['uniform_colour_g'], faction_table_record['uniform_colour_b']))
    else:
        faction.set_primary_colour('#' + faction_table_record['primary_colour_hex'].lower())
        faction.set_secondary_colour('#' + faction_table_record['secondary_colour_hex'].lower())
        faction.set_uniform_colour('#' + faction_table_record['uniform_colour_hex'].lower())
        faction.set_revolutionary_primary_colour('#' + faction_table_record['primary_colour_hex'].lower())
        faction.set_revolutionary_secondary_colour('#' + faction_table_record['secondary_colour_hex'].lower())
        faction.set_revolutionary_uniform_colour('#' + faction_table_record['uniform_colour_hex'].lower())

    # Reassigning faction flag in preopen_map_info

    preopen_map_info = PreopenMapInfo(os.path.join(OUTPUT_DIR, 'preopen_map_info', Esf(os.path.join(OUTPUT_DIR, 'esf.xml')).get_preopen_map_info()))

    preopen_map_info.get_player_setup(faction_info['name']).set_name(faction_name)

    preopen_map_info.get_faction_info(faction_info['name']).set_name(faction_name)

    if pd.notna(faction_table_record['republican_flag_path']) and (government.get_type() == 'gov_republic'):
            preopen_map_info.get_faction_info(faction_info['name']).set_flag(faction_table_record['republican_flag_path'])
    else:
        preopen_map_info.get_faction_info(faction_info['name']).set_flag(faction_table_record['flags_path'])

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
                            region_slot.set_building_government(new_government_type)

                            region_slots.append(region_slot)

    # Reassigning diplomatic relationships

    faction_diplomacy = Diplomacy(os.path.join(OUTPUT_DIR, 'diplomacy', faction_info['diplomacy_path']))

    other_faction_diplomacies = []

    for index, other_faction_info in FACTION_IDS[FACTION_IDS['path'].ne('0001.xml')].iterrows():
        if other_faction_info['id'] == faction_info['id']:
            continue

        other_faction_diplomacy = Diplomacy(os.path.join(OUTPUT_DIR, 'diplomacy', other_faction_info['diplomacy_path']))

        other_faction_attitude = DIPLOMATIC_RELATIONS_GOVERNMENT_TYPE_TABLE[
            DIPLOMATIC_RELATIONS_GOVERNMENT_TYPE_TABLE['government_type_from'].eq(other_faction_info['government_type'])
            &DIPLOMATIC_RELATIONS_GOVERNMENT_TYPE_TABLE['government_type_to'].eq(new_government_type)]['base_attitude'].iloc[0]

        other_faction_diplomacy.get_relationship(faction_info['id']).get_attitudes()[16].set_current(str(other_faction_attitude))

        other_faction_diplomacies.append(other_faction_diplomacy)

        faction_attitude = DIPLOMATIC_RELATIONS_GOVERNMENT_TYPE_TABLE[
            DIPLOMATIC_RELATIONS_GOVERNMENT_TYPE_TABLE['government_type_from'].eq(new_government_type)
            &DIPLOMATIC_RELATIONS_GOVERNMENT_TYPE_TABLE['government_type_to'].eq(other_faction_info['government_type'])]['base_attitude'].iloc[0]

        faction_diplomacy.get_relationship(other_faction_info['id']).get_attitudes()[16].set_current(str(faction_attitude))

    # Applying changes

    government.write_xml()

    faction.write_xml()

    preopen_map_info.write_xml()

    for region_slot in region_slots:
        region_slot.write_xml()

    faction_diplomacy.write_xml()
    for other_faction_diplomacy in other_faction_diplomacies:
        other_faction_diplomacy.write_xml()

    FACTION_IDS.loc[FACTION_IDS['name'].eq(faction_info['name']), 'government_type'] = new_government_type



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python change_faction_government_type.py westphalia gov_constitutional_monarchy')
    parser.add_argument('faction_name', type=str, help='')
    parser.add_argument('new_government_type', type=str, choices=['gov_absolute_monarchy', 'gov_constitutional_monarchy', 'gov_republic'], help='')
    args = parser.parse_args()

    faction_name = args.faction_name
    new_government_type = args.new_government_type

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)
    REGION_IDS = pd.read_csv(REGION_IDS_PATH, delimiter='\t', dtype=str)

    change_faction_government_type(faction_name, new_government_type)

    FACTION_IDS.to_csv(FACTION_IDS_PATH, sep='\t', index=False)
