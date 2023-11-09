import os
import pandas as pd

from ..lib import *



def get_governorship_ids():

    governorships = pd.DataFrame(columns=['faction_id', 'name', 'theatre', 'id', 'cabinet_id', 'character_id', 'government_type', 'government_id', 'path'])

    i = 0
    for xml_file in sorted(os.listdir(os.path.join(STARTPOS_DIR, 'government'))):
        government = Government(os.path.join(STARTPOS_DIR, 'government', xml_file))
        for governorship_name in ['governor_europe', 'governor_america', 'governor_india']:
            governorship = government.get_post(governorship_name)
            if governorship is not None:
                governorships.loc[i] = [
                    governorship.get_faction_id(),
                    governorship.get_title(),
                    governorship.get_theatre(),
                    governorship.get_governor_id(),
                    governorship.get_id(),
                    governorship.get_character_id(),
                    government.get_type(),
                    governorship.get_government_id(),
                    xml_file]
                i += 1

    cai_governorships = pd.DataFrame(columns=['id', 'cai_id', 'cai_path'])

    for i, xml_file in enumerate(sorted(os.listdir(os.path.join(STARTPOS_DIR, 'cai_governorships')))):
        cai_governorship = CaiGovernorship(os.path.join(STARTPOS_DIR, 'cai_governorships', xml_file))
        cai_governorships.loc[i] = [cai_governorship.get_governor_id(), cai_governorship.get_id(), xml_file]

    df = governorships.merge(cai_governorships, on='id', how='outer').sort_values(['faction_id', 'name'])

    return df



if __name__ == '__main__':

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    get_governorship_ids().to_csv(GOVERNORSHIP_IDS_PATH, sep='\t', index=False)
