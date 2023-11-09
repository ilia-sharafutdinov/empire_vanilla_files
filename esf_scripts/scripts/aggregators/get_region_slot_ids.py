import os
import pandas as pd

from ..lib import *



def get_region_slot_ids():

    region_slots = pd.DataFrame(columns=['id', 'name', 'rec_type', 'path'])

    for i, xml_file in enumerate(os.listdir(os.path.join(STARTPOS_DIR, 'region_slot'))):
        rec_type = read_xml(os.path.join(STARTPOS_DIR, 'region_slot', xml_file)).find('rec').get('type')
        if rec_type in ['ROAD_SLOT', 'FORTIFICATION_SLOT', 'REGION_SLOT_ARRAY']:
            region_slot = RegionSlot(os.path.join(STARTPOS_DIR, 'region_slot', xml_file))
        elif rec_type == 'SETTLEMENT':
            region_slot = Settlement(os.path.join(STARTPOS_DIR, 'region_slot', xml_file))
        elif rec_type == 'FORT_ARRAY':
            region_slot = Fort(os.path.join(STARTPOS_DIR, 'region_slot', xml_file))
        else:
            raise ValueError(f"'{rec_type}' rec type is not supported.")
        region_slots.loc[i] = [
            region_slot.get_id(),
            None if region_slot.get_type() == 'FORT_ARRAY' else region_slot.get_name(),
            region_slot.get_type(),
            xml_file]

    cai_building_slots = pd.DataFrame(columns=['id', 'cai_id', 'cai_path'])

    for i, xml_file in enumerate(os.listdir(os.path.join(STARTPOS_DIR, 'cai_building_slots'))):
        cai_building_slot = CaiBuildingSlot(os.path.join(STARTPOS_DIR, 'cai_building_slots', xml_file))
        cai_building_slots.loc[i] = [cai_building_slot.get_building_slot_id(), cai_building_slot.get_id(), xml_file]

    cai_settlements = pd.DataFrame(columns=['id', 'cai_id', 'cai_path'])

    for i, xml_file in enumerate(os.listdir(os.path.join(STARTPOS_DIR, 'cai_settlements'))):
        cai_settlement = CaiSettlement(os.path.join(STARTPOS_DIR, 'cai_settlements', xml_file))
        cai_settlements.loc[i] = [cai_settlement.get_settlement_id(), cai_settlement.get_id(), xml_file]

    cai_forts = pd.DataFrame(columns=['id', 'cai_id', 'cai_path'])

    for i, xml_file in enumerate(os.listdir(os.path.join(STARTPOS_DIR, 'cai_forts'))):
        cai_fort = get_cai_fort(os.path.join(STARTPOS_DIR, 'cai_forts', xml_file))
        cai_forts.loc[i] = [cai_fort['id'], cai_fort['cai_id'], xml_file]

    cai_region_slots = pd.DataFrame(columns=['cai_id', 'cai_region_slot_id', 'cai_region_slot_path'])

    for i, xml_file in enumerate(os.listdir(os.path.join(STARTPOS_DIR, 'cai_region_slots'))):
        cai_region_slot = get_cai_region_slot(os.path.join(STARTPOS_DIR, 'cai_region_slots', xml_file))
        cai_region_slots.loc[i] = [cai_region_slot['id'], cai_region_slot['cai_id'], xml_file]

    df = region_slots.merge(pd.concat([cai_building_slots, cai_settlements, cai_forts], ignore_index=True), on='id', how='outer') \
        .merge(cai_region_slots, on='cai_id', how='outer') \
        .sort_values(['id'])

    return df



if __name__ == '__main__':

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    get_region_slot_ids().to_csv(REGION_SLOT_IDS_PATH, sep='\t', index=False)
