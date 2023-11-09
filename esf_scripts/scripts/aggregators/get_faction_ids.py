import os
import pandas as pd

from ..lib import *



def get_faction_ids():

    factions = pd.DataFrame(
        columns=['name', 'id', 'religion', 'path', 'diplomacy_path', 'government_path', 'family_path', 'technology_path'])

    for i, xml_file in enumerate(sorted(os.listdir(os.path.join(STARTPOS_DIR, 'factions')))):
        faction = Faction(os.path.join(STARTPOS_DIR, 'factions', xml_file))
        factions.loc[i] = [
            faction.get_name(),
            faction.get_id(),
            faction.get_religion(),
            xml_file,
            faction.get_diplomacy_path(),
            faction.get_government_path(),
            faction.get_family_path(),
            faction.get_technology_path()]

    cai_factions = pd.DataFrame(columns=['id', 'cai_id', 'cai_path'])

    for i, xml_file in enumerate(sorted(os.listdir(os.path.join(STARTPOS_DIR, 'cai_factions')))):
        cai_faction = CaiFaction(os.path.join(STARTPOS_DIR, 'cai_factions', xml_file))
        cai_factions.loc[i] = [cai_faction.get_faction_id(), cai_faction.get_id(), xml_file]

    governments = pd.DataFrame(columns=['government_id', 'government_type', 'government_path'])

    for i, xml_file in enumerate(sorted(os.listdir(os.path.join(STARTPOS_DIR, 'government')))):
        government = Government(os.path.join(STARTPOS_DIR, 'government', xml_file))
        governments.loc[i] = [government.get_id(), government.get_type(), xml_file]

    domestic_trade_routes = pd.DataFrame(columns=['name', 'domestic_trade_path'])

    for i, xml_file in enumerate(sorted(os.listdir(os.path.join(STARTPOS_DIR, 'domestic_trade_routes')))):
        domestic_trade_route = DomesticTradeRoute(os.path.join(STARTPOS_DIR, 'domestic_trade_routes', xml_file))
        domestic_trade_routes.loc[i] = [domestic_trade_route.get_faction_name(), xml_file]

    international_trade_routess = pd.DataFrame(columns=['name', 'international_trade_path'])

    for i, xml_file in enumerate(sorted(os.listdir(os.path.join(STARTPOS_DIR, 'international_trade_routes')))):
        international_trade_routes = InternationalTradeRoutes(os.path.join(STARTPOS_DIR, 'international_trade_routes', xml_file))
        international_trade_routess.loc[i] = [international_trade_routes.get_faction_name(), xml_file]

    victory_conditions = pd.DataFrame(columns=['name', 'victory_condition_path'])

    for i, xml_file in enumerate(sorted(os.listdir(os.path.join(STARTPOS_DIR, 'victory_conditions')))):
        victory_condition = VictoryCondition(xml_file)
        victory_conditions.loc[i] = [victory_condition.faction_name, xml_file]

    df = factions \
        .merge(cai_factions, on='id', how='outer') \
        .merge(governments, on='government_path', how='outer').sort_values('name') \
        .merge(domestic_trade_routes, on='name', how='outer') \
        .merge(international_trade_routess, on='name', how='outer') \
        .merge(victory_conditions, on='name', how='outer')

    return df



if __name__ == '__main__':

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    get_faction_ids().to_csv(FACTION_IDS_PATH, sep='\t', index=False)
