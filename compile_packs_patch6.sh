#!/bin/bash

gfconv_path="/home/ilia/GitHub/etwng/gfconv/gfpack"
pack_path="dist/patch6.pack"
schema_path="/home/ilia/.config/rpfm/schemas/schema_emp.ron"
game="empire"
pack_type="movie"

db_folders=(
    "battle_personalities_tables"
    "building_chain_to_slots_tables"
    "building_chains_tables"
    "building_description_texts_tables"
    "building_effects_junction_tables"
    "building_faction_variants_tables"
    "building_levels_tables"
    "building_units_allowed_tables"
    "building_upgrades_junction_tables"
    "effect_bonus_value_building_chain_junctions_tables"
    "factions_tables"
    "gun_type_to_projectiles_tables"
    "gun_types_tables"
    "ministerial_positions_by_gov_types_tables"
    "unit_stats_land_tables"
    "unit_stats_naval_crew_to_factions_tables"
    "units_tables"
    "units_to_exclusive_faction_permissions_tables"
    "units_to_groupings_military_permissions_tables"
)

pushd packs/main
rm -f groupformations.bin
$gfconv_path
popd

rpfm_cli --game $game pack create --pack-path $pack_path

rpfm_cli --game $game pack set-file-type --pack-path $pack_path --file-type $pack_type

rpfm_cli --game $game pack add --pack-path $pack_path --tsv-to-binary $schema_path --file-path packs/local_en/text/localisation.loc.tsv

rpfm_cli --game $game pack add --pack-path $pack_path --tsv-to-binary $schema_path --file-path packs/main/groupformations.bin

for folder in "${db_folders[@]}"
do
    rpfm_cli --game $game pack add --pack-path $pack_path --tsv-to-binary $schema_path --folder-path packs/main/db/$folder
done
