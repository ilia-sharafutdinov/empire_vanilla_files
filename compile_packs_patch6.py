import os
import subprocess

from dotenv import load_dotenv
load_dotenv()

gfconv_path=os.path.join(os.getenv('ETWNG_DIR'), 'gfconv', 'gfpack')
pack_path='dist/patch6.pack'
schema_path=os.getenv('RPFM_SCHEMA_PATH')
game='empire'
pack_type='movie'

db_folders= [
    'battle_personalities_tables',
    'building_chain_to_slots_tables',
    'building_chains_tables',
    'building_description_texts_tables',
    'building_effects_junction_tables',
    'building_faction_variants_tables',
    'building_levels_tables',
    'building_units_allowed_tables',
    'building_upgrades_junction_tables',
    'effect_bonus_value_building_chain_junctions_tables',
    'factions_tables',
    'gun_type_to_projectiles_tables',
    'gun_types_tables',
    'ministerial_positions_by_gov_types_tables',
    'unit_stats_land_tables',
    'unit_stats_naval_crew_to_factions_tables',
    'units_tables',
    'units_to_exclusive_faction_permissions_tables',
    'units_to_groupings_military_permissions_tables'
]

packs_main_folder = os.path.join('packs', 'main')

if os.path.exists(os.path.join(packs_main_folder, 'groupformations.bin')):
    os.remove(os.path.join(packs_main_folder, 'groupformations.bin'))

subprocess.run(f"ruby {gfconv_path}", shell=True, capture_output=True, check=True, cwd=packs_main_folder)

subprocess.run(f"rpfm_cli --game {game} pack create --pack-path {pack_path}", shell=True, capture_output=True, check=True)

subprocess.run(f"rpfm_cli --game {game} pack set-file-type --pack-path {pack_path} --file-type {pack_type}", shell=True, capture_output=True, check=True)

subprocess.run(f"rpfm_cli --game {game} pack add --pack-path {pack_path} --tsv-to-binary {schema_path} --file-path packs/local_en/text/localisation.loc.tsv", shell=True, capture_output=True, check=True)

subprocess.run(f"rpfm_cli --game {game} pack add --pack-path {pack_path} --tsv-to-binary {schema_path} --file-path packs/main/groupformations.bin", shell=True, capture_output=True, check=True)

for folder in db_folders:
    subprocess.run(f"rpfm_cli --game {game} pack add --pack-path {pack_path} --tsv-to-binary {schema_path} --folder-path packs/main/db/{folder}", shell=True, capture_output=True, check=True)
