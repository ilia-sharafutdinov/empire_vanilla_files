import os
import pandas as pd

from ..lib import *



def get_region_ids():

    regions = pd.DataFrame(columns=['name', 'id', 'faction_id', 'governor_id', 'theatre', 'recruitment_id', 'path'])

    for i, xml_file in enumerate(os.listdir(os.path.join(STARTPOS_DIR, 'region'))):
        region = Region(os.path.join(STARTPOS_DIR, 'region', xml_file))
        regions.loc[i] = [
            region.get_name(),
            region.get_id(),
            region.get_faction_id(),
            region.get_governor_id(),
            region.get_theatre(),
            region.get_recruitment_id(),
            xml_file]

    preopen_map_info = PreopenMapInfo(os.path.join(OUTPUT_DIR, 'preopen_map_info', Esf(os.path.join(OUTPUT_DIR, 'esf.xml')).get_preopen_map_info()))
    region_preopen_theatres = pd.DataFrame(columns=['name', 'preopen_theatre'])

    for i, preopen_region_ownership in enumerate(preopen_map_info.get_region_ownerships()):
        region_preopen_theatres.loc[i] = [preopen_region_ownership['region'], preopen_region_ownership['theatre']]

    cai_regions = pd.DataFrame(columns=['name', 'id', 'cai_id', 'cai_path'])

    for i, xml_file in enumerate(os.listdir(os.path.join(STARTPOS_DIR, 'cai_regions'))):
        cai_region = CaiRegion(os.path.join(STARTPOS_DIR, 'cai_regions', xml_file))
        cai_regions.loc[i] = [cai_region.get_name(), cai_region.get_region_id(), cai_region.get_id(), xml_file]

    df = regions.merge(region_preopen_theatres, on='name', how='outer').merge(cai_regions, on=['name', 'id'], how='outer').sort_values('name')

    return df



if __name__ == '__main__':

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    get_region_ids().to_csv(REGION_IDS_PATH, sep='\t', index=False)
