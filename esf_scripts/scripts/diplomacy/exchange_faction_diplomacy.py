import argparse
import os
import pandas as pd

from ..lib import *



def exchange_faction_diplomacy(first_faction_name: VANILLA_FACTION_KEY_HINTS, second_faction_name: VANILLA_FACTION_KEY_HINTS):
    '''
    example:
        exchange_faction_diplomacy('greece', 'venice')
    '''

    assert first_faction_name in FACTION_IDS['name'].to_list(), f"{first_faction_name} is not present in {FACTION_IDS_PATH}."
    assert second_faction_name in FACTION_IDS['name'].to_list(), f"{second_faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    first_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(first_faction_name)].iloc[0]
    second_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(second_faction_name)].iloc[0]

    first_faction = Faction(os.path.join(OUTPUT_DIR, 'factions', first_faction_info['path']))
    second_faction = Faction(os.path.join(OUTPUT_DIR, 'factions', second_faction_info['path']))

    first_faction_id = first_faction.get_id()
    second_faction_id = second_faction.get_id()

    # Reassigning faction diplomacy paths and patron IDs

    first_faction_diplomacy_path = first_faction.get_diplomacy_path()
    second_faction_diplomacy_path = second_faction.get_diplomacy_path()

    first_faction.set_diplomacy_path(second_faction_diplomacy_path)
    second_faction.set_diplomacy_path(first_faction_diplomacy_path)

    first_faction_protectorate_id = first_faction.get_protectorate_id()
    second_faction_protectorate_id = second_faction.get_protectorate_id()

    first_faction.set_protectorate_id(second_faction_protectorate_id)
    second_faction.set_protectorate_id(first_faction_protectorate_id)

    # Reassigning protectorate IDs

    protectorate_factions = []

    first_faction_diplomacy = Diplomacy(os.path.join(OUTPUT_DIR, 'diplomacy', first_faction_diplomacy_path))
    second_faction_diplomacy = Diplomacy(os.path.join(OUTPUT_DIR, 'diplomacy', second_faction_diplomacy_path))

    for relationship in first_faction_diplomacy.get_relationships():
        if relationship.get_relationship() == 'patron':
            protectorate_faction_info = FACTION_IDS[FACTION_IDS['id'].eq(relationship.get_faction_id())].iloc[0]
            protectorate_faction = Faction(os.path.join(OUTPUT_DIR, 'factions', protectorate_faction_info['path']))
            protectorate_faction.set_protectorate_id(second_faction_id)
            protectorate_factions.append(protectorate_faction)

    for relationship in second_faction_diplomacy.get_relationships():
        if relationship.get_relationship() == 'patron':
            protectorate_faction_info = FACTION_IDS[FACTION_IDS['id'].eq(relationship.get_faction_id())].iloc[0]
            protectorate_faction = Faction(os.path.join(OUTPUT_DIR, 'factions', protectorate_faction_info['path']))
            protectorate_faction.set_protectorate_id(first_faction_id)
            protectorate_factions.append(protectorate_faction)

    # Reassigning faction international trade paths

    first_faction_trade = InternationalTradeRoutes(os.path.join(OUTPUT_DIR, 'international_trade_routes', first_faction_info['international_trade_path']))
    second_faction_trade = InternationalTradeRoutes(os.path.join(OUTPUT_DIR, 'international_trade_routes', second_faction_info['international_trade_path']))

    first_faction_trade.set_faction_name(second_faction_info['name'])
    second_faction_trade.set_faction_name(first_faction_info['name'])

    # Reassigning faction IDs in diplomacy

    for xml_file in os.listdir(os.path.join(OUTPUT_DIR, 'diplomacy')):
        text_replace(os.path.join(OUTPUT_DIR, 'diplomacy', xml_file),
                     f"<i>{first_faction_id}</i><!-- {first_faction_info['name']} -->",
                     f"<i>@@{second_faction_id}@@</i><!-- @@{second_faction_info['name']}@@ -->", regex=False)
        text_replace(os.path.join(OUTPUT_DIR, 'diplomacy', xml_file),
                     f"<i>{second_faction_id}</i><!-- {second_faction_info['name']} -->",
                     f"<i>{first_faction_id}</i><!-- {first_faction_info['name']} -->", regex=False)
        text_replace(os.path.join(OUTPUT_DIR, 'diplomacy', xml_file),
                     f"<i>@@{second_faction_id}@@</i><!-- @@{second_faction_info['name']}@@ -->",
                     f"<i>{second_faction_id}</i><!-- {second_faction_info['name']} -->", regex=False)

    # Applying changes

    first_faction.write_xml()
    second_faction.write_xml()

    first_faction_trade.write_xml()
    second_faction_trade.write_xml()

    for protectorate_faction in protectorate_factions:
        protectorate_faction.write_xml()

    FACTION_IDS.loc[FACTION_IDS['name'].eq(first_faction_info['name']), 'diplomacy_path'] = second_faction_diplomacy_path
    FACTION_IDS.loc[FACTION_IDS['name'].eq(second_faction_info['name']), 'diplomacy_path'] = first_faction_diplomacy_path
    FACTION_IDS.loc[FACTION_IDS['name'].eq(first_faction_info['name']), 'international_trade_path'] = second_faction_info['international_trade_path']
    FACTION_IDS.loc[FACTION_IDS['name'].eq(second_faction_info['name']), 'international_trade_path'] = first_faction_info['international_trade_path']



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python exchange_faction_diplomacy.py greece venice')
    parser.add_argument('first_faction_name', type=str, help='')
    parser.add_argument('second_faction_name', type=str, help='')
    args = parser.parse_args()

    first_faction_name = args.first_faction_name
    second_faction_name = args.second_faction_name

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)

    exchange_faction_diplomacy(first_faction_name, second_faction_name)

    FACTION_IDS.to_csv(FACTION_IDS_PATH, sep='\t', index=False)
