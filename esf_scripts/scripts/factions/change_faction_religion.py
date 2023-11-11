import argparse
import os
import pandas as pd

from ..lib import *



def change_faction_religion(faction_name: VANILLA_FACTION_KEY_HINTS, new_religion: VANILLA_RELIGION_KEY_HINTS):
    '''
    example:
        change_faction_religion('westphalia', 'rel_catholic')
    '''

    # TODO: Assert religion exists in DB

    assert faction_name in FACTION_IDS['name'].to_list(), f"{faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    faction_info = FACTION_IDS[FACTION_IDS['name'].eq(faction_name)].iloc[0]

    # Reassigning faction religion

    faction = Faction(os.path.join(OUTPUT_DIR, 'factions', faction_info['path']))

    faction.set_religion(new_religion)

    # Reassigning family religion

    family = Family(os.path.join(OUTPUT_DIR, 'family', faction_info['family_path']))

    for family_member in family.get_family_members():
        if family_member.get_religion():
            family_member.set_religion(new_religion)

    # Reassigning diplomatic relationships

    faction_diplomacy = Diplomacy(os.path.join(OUTPUT_DIR, 'diplomacy', faction_info['diplomacy_path']))

    other_faction_diplomacies = []

    for index, other_faction_info in FACTION_IDS[FACTION_IDS['path'].ne('0001.xml')].iterrows():
        if other_faction_info['id'] == faction_info['id']:
            continue

        other_faction_diplomacy = Diplomacy(os.path.join(OUTPUT_DIR, 'diplomacy', other_faction_info['diplomacy_path']))

        other_faction_attitude = DIPLOMATIC_RELATIONS_RELIGION_TABLE[
            DIPLOMATIC_RELATIONS_RELIGION_TABLE['religion_a'].eq(other_faction_info['religion'])
            &DIPLOMATIC_RELATIONS_RELIGION_TABLE['religion_b'].eq(new_religion)]['relations_modifier'].iloc[0]

        other_faction_diplomacy.get_relationship(faction_info['id']).get_attitudes()[15].set_current(str(other_faction_attitude))

        other_faction_diplomacies.append(other_faction_diplomacy)

        faction_attitude = DIPLOMATIC_RELATIONS_RELIGION_TABLE[
            DIPLOMATIC_RELATIONS_RELIGION_TABLE['religion_a'].eq(new_religion)
            &DIPLOMATIC_RELATIONS_RELIGION_TABLE['religion_b'].eq(other_faction_info['religion'])]['relations_modifier'].iloc[0]

        faction_diplomacy.get_relationship(other_faction_info['id']).get_attitudes()[15].set_current(str(faction_attitude))

    # Applying changes

    faction.write_xml()
    family.write_xml()

    faction_diplomacy.write_xml()
    for other_faction_diplomacy in other_faction_diplomacies:
        other_faction_diplomacy.write_xml()

    FACTION_IDS.loc[FACTION_IDS['name'].eq(faction_info['name']), 'religion'] = new_religion



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python change_faction_religion.py westphalia rel_catholic')
    parser.add_argument('faction_name', type=str, help='')
    parser.add_argument('new_religion', type=str, help='Religion as found in db/religions_tables/religions.tsv')
    args = parser.parse_args()

    faction_name = args.faction_name
    new_religion = args.new_religion

    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)

    change_faction_religion(faction_name, new_religion)

    FACTION_IDS.to_csv(FACTION_IDS_PATH, sep='\t', index=False)
