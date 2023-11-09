import os
import pandas as pd

from ..lib import *



def get_character_ids():

    characters = pd.DataFrame(columns=['id', 'faction_name', 'character_type', 'first_name', 'last_name', 'birth_date', 'path'])

    for i, xml_file in enumerate(os.listdir(os.path.join(STARTPOS_DIR, 'character'))):
        character = Character(os.path.join(STARTPOS_DIR, 'character', xml_file))
        characters.loc[i] = [character.get_id(), character.get_faction(), character.get_type(), character.get_first_name(), character.get_last_name(), character.get_birth_date(), xml_file]

    cai_characters = pd.DataFrame(columns=['id', 'cai_id', 'cai_resource_id', 'cai_path'])

    for i, xml_file in enumerate(os.listdir(os.path.join(STARTPOS_DIR, 'cai_characters'))):
        cai_character = CaiCharacter(os.path.join(STARTPOS_DIR, 'cai_characters', xml_file))
        cai_characters.loc[i] = [cai_character.get_character_id(), cai_character.get_id(), cai_character.get_resource_id(), xml_file]

    cai_mobiles = pd.DataFrame(columns=['cai_resource_id', 'cai_id', 'army_id', 'cai_mobile_path'])

    for i, xml_file in enumerate(os.listdir(os.path.join(STARTPOS_DIR, 'cai_mobiles'))):
        cai_mobile = CaiMobile(os.path.join(STARTPOS_DIR, 'cai_mobiles', xml_file))
        cai_mobiles.loc[i] = [cai_mobile.get_id(), cai_mobile.get_character_id(), cai_mobile.get_army_id(), xml_file]

    armies = pd.DataFrame(columns=['id', 'army_id', 'army_rec_type', 'army_path'])

    for i, xml_file in enumerate(os.listdir(os.path.join(STARTPOS_DIR, 'army'))):
        army = Army(os.path.join(STARTPOS_DIR, 'army', xml_file))
        armies.loc[i] = [army.get_character_id(), army.get_id(), army.get_type(), xml_file]

    df = characters.merge(cai_characters, on='id', how='outer') \
        .merge(cai_mobiles, on=['cai_resource_id', 'cai_id'], how='outer') \
        .merge(armies, on=['id', 'army_id'], how='outer') \
        .sort_values(['faction_name', 'character_type', 'id'])

    return df



if __name__ == '__main__':

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    get_character_ids().to_csv(CHARACTER_IDS_PATH, sep='\t', index=False)
