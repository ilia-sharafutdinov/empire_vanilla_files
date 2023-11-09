import argparse
import os
import pandas as pd

from ..lib import *



def hand_over_region(
    region_name: VANILLA_REGION_KEY_HINTS,
    new_faction_name: VANILLA_FACTION_KEY_HINTS,
    ignore_not_enough_regions: bool = False):
    '''
    example:
        hand_over_region('silesia', 'prussia')
    '''

    assert region_name in REGION_IDS['name'].to_list(), f"{region_name} is not present in {REGION_IDS_PATH}."
    assert new_faction_name in FACTION_IDS['name'].to_list(), f"{new_faction_name} is not present in {FACTION_IDS_PATH}."

    # Collecting info

    region_info = REGION_IDS[REGION_IDS['name'].eq(region_name)].iloc[0]
    new_faction_info = FACTION_IDS[FACTION_IDS['name'].eq(new_faction_name)].iloc[0]
    if GOVERNORSHIP_IDS[GOVERNORSHIP_IDS['faction_id'].eq(new_faction_info['id'])&GOVERNORSHIP_IDS['theatre'].eq(region_info['theatre'])].size == 0:
        raise ValueError(f"{GOVERNORSHIP_IDS_PATH} does not contain a governor where faction_id = {new_faction_info['id']} and theatre = {region_info['theatre']}.")
    new_governorship_info = GOVERNORSHIP_IDS[GOVERNORSHIP_IDS['faction_id'].eq(new_faction_info['id'])&GOVERNORSHIP_IDS['theatre'].eq(region_info['theatre'])].iloc[0]

    region = Region(os.path.join(OUTPUT_DIR, 'region', region_info['path']))

    region_recruitment_id = region.get_recruitment_id()

    old_faction_info = FACTION_IDS[FACTION_IDS['id'].eq(region.get_faction_id())].iloc[0]
    old_governorship_info = GOVERNORSHIP_IDS[GOVERNORSHIP_IDS['faction_id'].eq(old_faction_info['id'])&GOVERNORSHIP_IDS['theatre'].eq(region_info['theatre'])].iloc[0]

    settlement = Settlement(os.path.join(OUTPUT_DIR, 'region_slot', region.get_settlement_slot_path()))

    settlement_info = REGION_SLOT_IDS[REGION_SLOT_IDS['id'].eq(settlement.get_id())].iloc[0]

    region_slot_ids = []

    for path in region.get_region_slot_paths() + region.get_road_walls_paths():
        region_slot = RegionSlot(os.path.join(OUTPUT_DIR, 'region_slot', path))
        region_slot_ids.append(region_slot.get_id())

    region_slots_info = REGION_SLOT_IDS[REGION_SLOT_IDS['id'].isin(region_slot_ids)]

    # TODO: Automatically change HLCIS ID
    # TODO: Fix BDI instead of removing
    # TODO: Fix forts handover
    # TODO: Rename forts
    # TODO: Check whether clearing region_slot bdi is needed
    # TODO: Check whether clearing region bdi is needed
    # TODO: Check whether clearing settlement bdi is needed
    # TODO: Check whether clearing forts bdi is needed

    # Reassigning region ownership and governorship

    region.set_faction_id(new_faction_info['id'])
    region.set_governor_id(new_governorship_info['id'])

    # Reassigning CAI region governorship

    cai_region = CaiRegion(os.path.join(OUTPUT_DIR, 'cai_regions', region_info['cai_path']))

    cai_region.set_governor_id(new_governorship_info['cai_id'])

    # Removing region from the old CAI faction

    old_cai_faction = CaiFaction(os.path.join(OUTPUT_DIR, 'cai_factions', old_faction_info['cai_path']))

    old_cai_faction.remove_region_id(region_info['cai_id'])

    # Giving region to the new CAI faction

    new_cai_faction = CaiFaction(os.path.join(OUTPUT_DIR, 'cai_factions', new_faction_info['cai_path']))

    new_cai_faction.add_region_id(region_info['cai_id'])

    # Removing region from the old governorhip

    old_government = Government(os.path.join(OUTPUT_DIR, 'government', old_governorship_info['path']))

    if not ignore_not_enough_regions:
        assert len(old_government.get_post(old_governorship_info['name']).get_region_ids().split(' ')) >= 2, f"Previous governor '{old_governorship_info['name']}' doesn't have enough regions left in '{old_governorship_info['path']}'."

    old_government.get_post(old_governorship_info['name']).remove_region_id(region_info['id'])

    # Removing region from the old CAI governorhip

    old_cai_governorship = CaiGovernorship(os.path.join(OUTPUT_DIR, 'cai_governorships', old_governorship_info['cai_path']))

    old_cai_governorship.remove_region_id(region_info['cai_id'])

    # Giving region to the new governorhip

    new_government = Government(os.path.join(OUTPUT_DIR, 'government', new_governorship_info['path']))

    new_government.get_post(new_governorship_info['name']).add_region_id(region_info['id'])

    # Giving region to the new CAI governorhip

    new_cai_governorship = CaiGovernorship(os.path.join(OUTPUT_DIR, 'cai_governorships', new_governorship_info['cai_path']))

    new_cai_governorship.add_region_id(region_info['cai_id'])

    # Reassigning settlement ownership

    settlement.set_garrison_faction_id(new_faction_info['id'])

    # Reassigning CAI settlement ownership

    cai_settlement = CaiSettlement(os.path.join(OUTPUT_DIR, 'cai_settlements', settlement_info['cai_path']))

    cai_settlement.set_owned_direct(new_faction_info['cai_id'])

    # Reassigning fort ownership

    forts = [Fort(os.path.join(OUTPUT_DIR, 'region_slot', path)) for path in region.get_fort_paths()]

    for fort in forts:
        fort.set_faction_id(new_faction_info['id'])
        fort.set_fort_faction_id(new_faction_info['id'])
        fort.set_garrison_faction_id(new_faction_info['id'])

    # Reassigning region slot ownership and building variant

    region_slots = []
    region_slot_recruitment_ids = []
    cai_building_slots = []

    for i, region_slot_info in region_slots_info.iterrows():
        region_slot = RegionSlot(os.path.join(OUTPUT_DIR, 'region_slot', region_slot_info['path']))

        region_slot.set_garrison_faction_id(new_faction_info['id'])
        if region_slot.has_building_manager() and (region_slot.get_constructed() == 'yes'):
            region_slot.set_building_faction(new_faction_info['name'])
            region_slot.set_building_government(new_governorship_info['government_type'])

        recruitment_id = region_slot.get_recruitment_id()
        if recruitment_id is not None:
            region_slot_recruitment_ids.append(recruitment_id)

        region_slots.append(region_slot)

        # Clearing CAI building slot BDIs

        cai_building_slot = CaiBuildingSlot(os.path.join(OUTPUT_DIR, 'cai_building_slots', region_slot_info['cai_path']))

        cai_building_slot.clear_bdi()

        cai_building_slots.append(cai_building_slot)

    # Reassigning region ownership and factions' region counts in preopen_map_info

    preopen_map_info = PreopenMapInfo(os.path.join(OUTPUT_DIR, 'preopen_map_info', Esf(os.path.join(OUTPUT_DIR, 'esf.xml')).get_preopen_map_info()))

    preopen_map_info.get_faction_info(old_faction_info['name']).decrement_n_provinces()
    preopen_map_info.get_faction_info(new_faction_info['name']).increment_n_provinces()

    preopen_map_info.set_region_ownership(region_info['preopen_theatre'], region_info['name'], new_faction_info['name'])

    # Applying changes

    region.write_xml()
    cai_region.write_xml()

    REGION_IDS.loc[REGION_IDS['name'].eq(region_info['name']), 'faction_id'] = new_faction_info['id']
    REGION_IDS.loc[REGION_IDS['name'].eq(region_info['name']), 'governor_id'] = new_governorship_info['id']

    old_cai_faction.write_xml()
    new_cai_faction.write_xml()

    old_government.write_xml()
    old_cai_governorship.write_xml()
    new_government.write_xml()
    new_cai_governorship.write_xml()

    preopen_map_info.write_xml()

    settlement.write_xml()
    cai_settlement.write_xml()

    for fort in forts:
        fort.write_xml()

    for region_slot in region_slots:
        region_slot.write_xml()

    for cai_building_slot in cai_building_slots:
        cai_building_slot.write_xml()

    HANDED_OVER_REGION_RECRUITMENT_MANAGER_IDS.append(region_recruitment_id)
    for region_slot_recruitment_id in region_slot_recruitment_ids:
        HANDED_OVER_REGION_SLOT_RECRUITMENT_MANAGER_IDS.append(region_slot_recruitment_id)



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='',
        epilog='example:\n' +
        '  python hand_over_region.py silesia prussia')
    parser.add_argument('region_name', type=str, help='')
    parser.add_argument('new_faction_name', type=str, help='')
    parser.add_argument('-i', '--ignore_not_enough_regions', action='store_true', help='')
    args = parser.parse_args()

    region_name = args.region_name
    new_faction_name = args.new_faction_name
    ignore_not_enough_regions = args.ignore_not_enough_regions

    REGION_IDS = pd.read_csv(REGION_IDS_PATH, delimiter='\t', dtype=str)
    FACTION_IDS = pd.read_csv(FACTION_IDS_PATH, delimiter='\t', dtype=str)
    GOVERNORSHIP_IDS = pd.read_csv(GOVERNORSHIP_IDS_PATH, delimiter='\t', dtype=str)
    REGION_SLOT_IDS = pd.read_csv(REGION_SLOT_IDS_PATH, delimiter='\t', dtype=str)

    hand_over_region(region_name, new_faction_name, ignore_not_enough_regions)

    # Clearing recruitment manager IDs from bdi_pool

    remove_recruitment_ids()

    REGION_IDS.to_csv(REGION_IDS_PATH, sep='\t', index=False)
