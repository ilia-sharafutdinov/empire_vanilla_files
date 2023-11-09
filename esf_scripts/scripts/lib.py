import os
import sys
import warnings
import re
from typing import Literal, get_args, List, TypedDict, Pattern, Dict, Union
from functools import cached_property
import numpy as np
from scipy import stats
import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup
from bs4.formatter import XMLFormatter, HTMLFormatter
from xml.sax.saxutils import escape

def get_script_dir():
    return os.path.dirname(os.path.abspath(sys.argv[0]))

def get_module_dir():
    return os.path.dirname(os.path.abspath(__file__))

def get_module_parent_dir():
    return os.path.dirname(get_module_dir())

def get_absolute_path(base_dir, relative_path):
    return os.path.normpath(os.path.join(base_dir, relative_path))

STARTPOS_DIR = get_absolute_path(get_script_dir(), os.getenv('STARTPOS_DIR'))

OUTPUT_DIR = get_absolute_path(get_script_dir(), os.getenv('OUTPUT_DIR')) if os.getenv('OUTPUT_DIR') != '' else STARTPOS_DIR

VANILLA_FILES_DB_DIR = get_absolute_path(get_script_dir(), os.getenv('VANILLA_FILES_DB_DIR'))

MOD_FILES_DB_DIRS = [get_absolute_path(get_script_dir(), path) for path in os.getenv('MOD_FILES_DB_DIRS').split(',') if path.strip() != '']

TEMP_DIR = get_absolute_path(get_script_dir(), os.getenv('TEMP_DIR'))

CHARACTER_IDS_PATH = os.path.join(TEMP_DIR, 'character_ids.tsv')
FACTION_IDS_PATH = os.path.join(TEMP_DIR, 'faction_ids.tsv')
GOVERNORSHIP_IDS_PATH = os.path.join(TEMP_DIR, 'governorship_ids.tsv')
REGION_IDS_PATH = os.path.join(TEMP_DIR, 'region_ids.tsv')
REGION_SLOT_IDS_PATH = os.path.join(TEMP_DIR, 'region_slot_ids.tsv')

def read_rpfm_table(table_path):
    return pd.read_csv(table_path, sep='\t', skiprows=[1])

def read_rpfm_tables(subdirectory: str, default_file_name: str, primary_key: List[str]):
    found = False
    for mod_files_db_dir in MOD_FILES_DB_DIRS[::-1] + [VANILLA_FILES_DB_DIR]:
        base_table_path = os.path.join(mod_files_db_dir, subdirectory, default_file_name)
        if os.path.exists(base_table_path):
            found = True
            break

    assert found, f"'{os.path.join(subdirectory, default_file_name)}' file not found in any of {', '.join([VANILLA_FILES_DB_DIR] + MOD_FILES_DB_DIRS)}."

    df = read_rpfm_table(base_table_path)

    for mod_files_db_dir in MOD_FILES_DB_DIRS:
        table_dir = os.path.join(mod_files_db_dir, subdirectory)
        if not os.path.exists(table_dir):
            continue

        for table_name in sorted(os.listdir(table_dir)):
            other_df = read_rpfm_table(os.path.join(table_dir, table_name))
            df = pd.concat([df, other_df], names=primary_key)

    df = df.drop_duplicates(subset=primary_key, keep='last').reset_index(drop=True)
    return df

ABILITIES_TABLE = read_rpfm_tables('abilities_tables', 'abilities.tsv', ['ability'])
AGENT_TO_AGENT_ABILITIES_TABLE = read_rpfm_tables('agent_to_agent_abilities_tables', 'agent_to_agent_abilities.tsv', ['agent', 'ability'])
AGENT_TO_AGENT_ATTRIBUTES_TABLE = read_rpfm_tables('agent_to_agent_attributes_tables', 'agent_to_agent_attributes.tsv', ['attribute', 'agent'])
AGENTS_TABLE = read_rpfm_tables('agents_tables', 'agents.tsv', ['key'])
CULTURES_TABLE = read_rpfm_tables('cultures_tables', 'cultures.tsv', ['key'])
CULTURES_SUBCULTURES_TABLE = read_rpfm_tables('cultures_subcultures_tables', 'cultures_subcultures.tsv', ['subculture'])
DIPLOMACY_ATTITUDES_TABLE = read_rpfm_tables('diplomacy_attitudes_tables', 'diplomacy_attitudes.tsv', ['attitude'])
DIPLOMATIC_RELATIONS_ATTITUDES_TABLE = read_rpfm_tables('diplomatic_relations_attitudes_tables', 'diplomatic_relations_attitudes.tsv', ['attitude'])
DIPLOMATIC_RELATIONS_GOVERNMENT_TYPE_TABLE = read_rpfm_tables('diplomatic_relations_government_type_tables', 'diplomatic_relations_government_type.tsv', ['government_type_from', 'government_type_to'])
DIPLOMATIC_RELATIONS_RELIGION_TABLE = read_rpfm_tables('diplomatic_relations_religion_tables', 'diplomatic_relations_religion.tsv', ['religion_a', 'religion_b'])
FACTIONS_TABLE = read_rpfm_tables('factions_tables', 'factions.tsv', ['key'])
NAMES_TABLE = read_rpfm_tables('names_tables', 'names.tsv', ['names_group', 'name', 'type'])
SHIP_NAMES_TABLE = read_rpfm_tables('ship_names_tables', 'ship_names.tsv', ['key'])
UNIT_STATS_LAND_TABLE = read_rpfm_tables('unit_stats_land_tables', 'unit_stats_land.tsv', ['key'])
UNITS_TABLE = read_rpfm_tables('units_tables', 'units.tsv', ['key'])

HANDED_OVER_REGION_RECRUITMENT_MANAGER_IDS = []
HANDED_OVER_REGION_SLOT_RECRUITMENT_MANAGER_IDS = []

SUPPORTED_FACTION_KEYS = dict.fromkeys(FACTIONS_TABLE['key'].values.tolist())
SUPPORTED_NAME_GROUPS = dict.fromkeys(NAMES_TABLE['names_group'].values.tolist())
SUPPORTED_UNIT_KEYS = dict.fromkeys(UNITS_TABLE['key'].values.tolist())

XML_ENCODING = 'utf-8'

THRESHOLD_HOSTILE = DIPLOMATIC_RELATIONS_ATTITUDES_TABLE[DIPLOMATIC_RELATIONS_ATTITUDES_TABLE['attitude'].eq('hostile')]['value'].iloc[0]
THRESHOLD_UNFRIENDLY = DIPLOMATIC_RELATIONS_ATTITUDES_TABLE[DIPLOMATIC_RELATIONS_ATTITUDES_TABLE['attitude'].eq('unfriendly')]['value'].iloc[0]
THRESHOLD_NEUTRAL = DIPLOMATIC_RELATIONS_ATTITUDES_TABLE[DIPLOMATIC_RELATIONS_ATTITUDES_TABLE['attitude'].eq('neutral')]['value'].iloc[0]
THRESHOLD_FRIENDLY = DIPLOMATIC_RELATIONS_ATTITUDES_TABLE[DIPLOMATIC_RELATIONS_ATTITUDES_TABLE['attitude'].eq('friendly')]['value'].iloc[0]
THRESHOLD_VERY_FRIENDLY = DIPLOMATIC_RELATIONS_ATTITUDES_TABLE[DIPLOMATIC_RELATIONS_ATTITUDES_TABLE['attitude'].eq('very_friendly')]['value'].iloc[0]

def get_diplomatic_relations_attitude(current_total):
    if current_total < (THRESHOLD_HOSTILE + THRESHOLD_UNFRIENDLY) / 2:
        return THRESHOLD_HOSTILE
    elif current_total < (THRESHOLD_UNFRIENDLY + THRESHOLD_NEUTRAL) / 2:
        return THRESHOLD_UNFRIENDLY
    elif current_total <= (THRESHOLD_NEUTRAL + THRESHOLD_FRIENDLY) / 2:
        return THRESHOLD_NEUTRAL
    elif current_total <= (THRESHOLD_FRIENDLY + THRESHOLD_VERY_FRIENDLY) / 2:
        return THRESHOLD_FRIENDLY
    else:
        return THRESHOLD_VERY_FRIENDLY

THEATRE_TO_CAI_ID = {
    'america': '33',
    'europe': '34',
    'india': '35'
}

VANILLA_RELIGION_KEY_HINTS = Literal[
    'rel_animist',
    'rel_buddhist',
    'rel_catholic',
    'rel_hindu',
    'rel_islamic',
    'rel_nonconformist',
    'rel_orthodox',
    'rel_protestant',
    'rel_sikh'
]

VANILLA_FACTION_KEY_HINTS = Literal[
    'afghanistan',
    'american_rebels',
    'amerind_rebels',
    'austria',
    'austrian_rebels',
    'barbary_rebels',
    'barbary_states',
    'bavaria',
    'britain',
    'british_rebels',
    'british_settler_rebels',
    'chechenya_dagestan',
    'cherokee',
    'cherokee_playable',
    'colombia',
    'cossack_rebels',
    'courland',
    'crimean_khanate',
    'denmark',
    'dutch_rebels',
    'european_settler_rebels',
    'france',
    'french_rebels',
    'french_settler_rebels',
    'genoa',
    'georgia',
    'greece',
    'greek_rebels',
    'hannover',
    'hessen',
    'holstein_gottorp',
    'hungary',
    'huron',
    'huron_playable',
    'india_settler_rebels',
    'inuit',
    'ireland',
    'iroquoi',
    'iroquoi_playable',
    'italian_rebels',
    'khanate_khiva',
    'knights_stjohn',
    'louisiana',
    'mamelukes',
    'maratha',
    'maratha_rebels',
    'mecklenburg',
    'mexico',
    'middle_east_settler_rebels',
    'morocco',
    'mughal',
    'mughal_rebels',
    'mysore',
    'naples_sicily',
    'netherlands',
    'new_spain',
    'norway',
    'ottoman_rebels',
    'ottomans',
    'papal_states',
    'persian_rebels',
    'piedmont_savoy',
    'pirates',
    'plains',
    'plains_playable',
    'poland_lithuania',
    'portugal',
    'portugese_rebels',
    'powhatan',
    'prussia',
    'prussian_rebels',
    'pueblo',
    'pueblo_playable',
    'punjab',
    'quebec',
    'russia',
    'safavids',
    'saxony',
    'scandinavian_rebels',
    'scotland',
    'sikh_rebels',
    'slavic_rebels',
    'spain',
    'spanish_rebels',
    'spanish_settler_rebels',
    'sweden',
    'swiss_confederation',
    'thirteen_colonies',
    'tuscany',
    'united_states',
    'venice',
    'virginia',
    'virginia_colonists',
    'westphalia',
    'wurttemberg'
]

VANILLA_REGION_KEY_HINTS = Literal[
    'acadia',
    'adriatic_sea',
    'afghanistan',
    'ahmadnagar',
    'algiers',
    'algonquin_territory',
    'all',
    'alps',
    'alsace',
    'amazonas',
    'anatolia',
    'arabia',
    'arabian_sea',
    'arctic_ocean',
    'arctic_w_ocean',
    'arkhangelsk',
    'armenia',
    'astrakhan',
    'atlantic_ocean_e',
    'atlantic_ocean_ne',
    'atlantic_ocean_nw',
    'atlantic_ocean_se',
    'atlantic_ocean_sw',
    'atlantic_ocean_w',
    'austria',
    'azerbaijan',
    'bahamas',
    'baltic_sea',
    'baluchistan',
    'bashkira',
    'bavaria',
    'bay_of_bengal',
    'bay_of_biscay',
    'beaver_territory',
    'belarus',
    'bengal',
    'berar',
    'bijapur',
    'black_sea',
    'bohemia',
    'bosnia',
    'brazil_coast',
    'bulgaria',
    'carnatica',
    'carolinas',
    'caspian_sea',
    'central_africa',
    'central_italy',
    'ceylon',
    'chechenya-dagestan',
    'cherokee_territory',
    'china',
    'congo_impassable',
    'corsica',
    'courland',
    'crimea',
    'croatia',
    'cuba',
    'curacao',
    'denmark',
    'doldrums',
    'don_voisko',
    'dutch_guyana',
    'east_africa',
    'east_indies',
    'egypt',
    'england',
    'english_channel',
    'estonia_and_livonia',
    'finland',
    'flanders',
    'florida',
    'france',
    'french_guyana',
    'galicia',
    'genoa',
    'georgia',
    'georgia_usa',
    'gibraltar',
    'great_lakes',
    'great_plains',
    'greece',
    'greenland',
    'greenland_sea',
    'guatemala',
    'gujarat',
    'gulf_of_mexico',
    'hannover',
    'hausa',
    'himalayas',
    'hindukush',
    'hindustan',
    'hispaniola',
    'hudson_bay',
    'hungary',
    'huron_territory',
    'hyderabad',
    'iceland',
    'impassable',
    'indian_ocean',
    'indochina',
    'ingria',
    'ireland',
    'irish_sea',
    'iroquois_territory',
    'ivory_coast',
    'jamaica',
    'kaintuck_territory',
    'kalahari',
    'karelia',
    'kashmir',
    'komi',
    'labrador',
    'lakes',
    'leeward_islands',
    'lithuania',
    'lower_louisiana',
    'maine',
    'malabar',
    'malta',
    'malwa',
    'maryland',
    'mediterranean_sea',
    'mesopotamia',
    'michigan_territory',
    'milan',
    'moldavia',
    'morea',
    'morocco',
    'muscovy',
    'mysore',
    'naples',
    'netherlands',
    'new_andalusia',
    'new_england',
    'new_france',
    'new_grenada',
    'new_mexico',
    'new_spain',
    'new_york',
    'newfoundland',
    'north_sea',
    'northwest_territories',
    'norway',
    'norwegian_sea',
    'ontario',
    'orissa',
    'pacific_ocean',
    'palestine',
    'panama',
    'pennsylvania',
    'persia',
    'persian_gulf',
    'poland',
    'portugal',
    'prussia',
    'punjab',
    'rajpootana',
    'red_sea',
    'rhineland',
    'rift_valley',
    'rumelia',
    'ruperts_land',
    'sahara',
    'sardinia',
    'savoy',
    'saxony',
    'scotland',
    'serbia',
    'siberia',
    'silesia',
    'sindh',
    'south_africa',
    'south_china_sea',
    'southern_ocean',
    'spain',
    'straits_of_mozambique',
    'sweden',
    'syria',
    'tatariya',
    'tejas',
    'the_caribbean_sea',
    'the_papal_states',
    'transylvania',
    'trinidad_tobago',
    'tripoli',
    'tunis',
    'turkoman',
    'ukraine',
    'unexplorable',
    'upper_louisiana',
    'venice',
    'virginia',
    'west_pommerania',
    'west_prussia',
    'western_plain',
    'wilderness_arabia',
    'wilderness_canada',
    'wilderness_great_plains',
    'wilderness_hudsonsbay',
    'wilderness_khiva',
    'wilderness_mexico',
    'wilderness_tejas',
    'windward_islands',
    'wurttemberg'
]

# TODO: Use esf portrait allocator instead of dictionary
PORTRAIT_OPTIONS_MAPPING = {
    'european': {
        'admiral': 300,
        'General': 300,
        'king': 100,
        'minister': 300,
        'missionary_catholic': 100,
        'missionary_orthodox': 100,
        'missionary_protestant': 100,
        'queen': 100,
        'rake': 50
    },
    'indian': {
        'admiral': 100,
        'assassin': 50,
        'Brahmin': 100,
        'General': 100,
        'king': 100,
        'minister': 100,
        'queen': 100,
        'scholar': 100
    },
    'middle_east': {
        'General': 100,
        'imam': 50,
        'scholar': 100
    },
    'tribal': {
        'General': 100,
        'king': 10,
        'minister': 10
    }
}



def print_block(string):
    print(f"{string:*^80}")

class UnsortedAttributes(HTMLFormatter):
    def attributes(self, tag):
        for k, v in tag.attrs.items():
            yield k, v

def get_base_name_from_path(path):
    return os.path.basename(os.path.normpath(path))

def text_replace(xml_path: str, pattern: Pattern[str], repl: str, regex=True):
    with open(xml_path, 'r', encoding=XML_ENCODING) as file:
        content = file.read()
    if regex:
        content = re.sub(pattern, repl, content)
    else:
        content = content.replace(pattern, repl)
    with open(xml_path, 'w', encoding=XML_ENCODING) as file:
        file.write(content)

def parse_xml_string(string: str):
    soup = BeautifulSoup('<pre>' + string + '</pre>', 'lxml')
    return soup

def read_xml(xml_path: str):
    with open(xml_path, 'r', encoding=XML_ENCODING) as file:
        content = file.read()
    soup = parse_xml_string(content)
    return soup

def write_xml(xml_path: str, soup: BeautifulSoup, create_new=False):
    # TODO: Apply .encode(formatter=UnsortedAttributes(), encoding=XML_ENCODING).decode(encoding=XML_ENCODING)
    formatted_output = str(soup)
    formatted_output = formatted_output.replace('<html><body><pre>', '')
    formatted_output = formatted_output.replace('</pre></body></html>', '')
    formatted_output = re.sub('></\\w+>', '/>', formatted_output)
    formatted_output = re.sub('\n +\n', '\n', formatted_output)
    mode = 'x' if create_new else 'w'
    with open(xml_path, mode, encoding=XML_ENCODING) as file:
        file.write(formatted_output)

def found_in_all_files(rootdir: str, string: str, warn=True, return_first_name=False):
    found = False
    for root, dirs, files in os.walk(rootdir):
        for name in files:
            if name.endswith('.xml'):
                with open(os.path.join(root, name), 'r', encoding=XML_ENCODING) as file:
                    if str(string) in ''.join(file.readlines()):
                        found = True
                        if warn:
                            warnings.warn(f'WARNING: {string} found in {name}.')
                        if return_first_name:
                            return name
    return found

def insert_tag(soup: BeautifulSoup, children_name: str, tag: BeautifulSoup, n_spaces: int):
    n_children = len(soup.find_all(children_name, recursive=False))
    soup.insert(n_children * 2, '\n' + ''.join([' '] * n_spaces))
    soup.insert(n_children * 2 + 1, tag)
    if n_children == 0:
        soup.insert(n_children * 2 + 3, '\n' + ''.join([' '] * (n_spaces - 1)))

def append_id_to_tag_string(tag: BeautifulSoup, id: str, sep=' ', sort=True):
    if tag.string:
        ids = tag.string.split(sep)
        if id in ids:
            warnings.warn(f'ID {id} is already in tag string. Skipping.')
        else:
            if sort:
                tag.string = sep.join(sorted(ids + [id]))
            else:
                tag.string = sep.join(ids + [id])
    else:
        tag.string = id

def remove_id_from_tag_string(tag: BeautifulSoup, id: str, sep=' '):
    ids = tag.string.split(sep)
    ids.remove(id)
    tag.string = sep.join(ids)

def append_id_to_tag_text(tag: etree._Element, id: int, sep=' ', sort=True):
    id = str(id)
    if tag.text is not None:
        ids = tag.text.split(sep)
        if id in ids:
            warnings.warn(f'ID {id} is already in tag text. Skipping.')
        else:
            ids.append(id)
            if sort:
                tag.text = sep.join(sorted(ids))
            else:
                tag.text = sep.join(ids)
    else:
        tag.text = id

def remove_id_from_tag_text(tag: etree._Element, id: int, sep=' '):
    id = str(id)
    ids = tag.text.split(sep)
    ids.remove(id)
    if len(ids) >= 1:
        tag.text = sep.join(ids)
    else:
        tag.text = None

def get_faction_subculture(faction_name):
    return FACTIONS_TABLE[FACTIONS_TABLE['key'].eq(faction_name)]['subculture'].iloc[0]

def get_faction_culture(faction_name):
    return CULTURES_SUBCULTURES_TABLE[CULTURES_SUBCULTURES_TABLE['subculture'].eq(get_faction_subculture(faction_name))]['culture'].iloc[0]

def make_name_info(names_group: str, forename: str, surname: str):
    normalise_name = lambda name: escape(name).replace(' ', '_')
    name_info = pd.Series({
        'forename': normalise_name(forename) if forename else '',
        'surname': normalise_name(surname) if surname else '',
        'forename_loc': f"names_name_{names_group}{normalise_name(forename)}" if forename else '',
        'surname_loc': f"names_name_{names_group}{normalise_name(surname)}" if surname else ''
    })
    return name_info

def generate_name(names_group: str, gender: Literal['m', 'f'], king=False):
    names = NAMES_TABLE.copy()
    assert names_group in names['names_group'].to_list(), f"{names_group} is not present in names_tables."
    names = names[names['names_group'].eq(names_group)&names['gender'].isin([gender, 'b'])]
    forename = names[names['type'].eq('forename')].sample(weights='frequency')['name'].iloc[0]
    surname = names[names['type'].eq('surname')].sample(weights='frequency')['name'].iloc[0]
    name_info = make_name_info(names_group, forename, surname)
    if king:
        name_info['surname'] = ''
        name_info['surname_loc'] = ''
    return name_info

def make_ship_name_info(key: str, name: str):
    name_info = pd.Series({
        'key': key,
        'name': name,
        'name_loc': f"ship_names_Ship_Name_{key}"
    })
    return name_info

def generate_ship_name(names_group: str, faction_name: str):
    names = SHIP_NAMES_TABLE.copy()
    assert names_group in names['name_group'].to_list(), f"{names_group} is not present in ship_names_tables."
    names = names[
        names['name_group'].eq(names_group)&
        (names['exclusive_to_faction'].isna()|
         names['exclusive_to_faction'].eq(faction_name))]
    name_sample = names.sample().iloc[0]
    name = name_sample['ship_name']
    key = name_sample['key']
    name_info = make_ship_name_info(key, name)
    return name_info

def make_portrait_info(culture: str, character_type: str, age: str, number: int):
    portrait_info = pd.Series({
        'culture': culture,
        'character_type': character_type,
        'age': age,
        'number': str(number)
    })
    return portrait_info

def generate_portrait_age():
    return np.random.choice(['young', 'old'])

def get_portrait_type(character_type: str):
    portrait_override = AGENTS_TABLE[AGENTS_TABLE['key'].eq(character_type)]['portrait_override'].iloc[0]
    portrait_type = character_type if pd.isna(portrait_override) else portrait_override
    return portrait_type

def get_portrait_culture(culture: Literal['european', 'indian', 'middle_east', 'tribal'], portrait_type: str):
    fallback_ui_culture = CULTURES_TABLE[CULTURES_TABLE['key'].eq(culture)]['fallback_ui_culture'].iloc[0]
    portrait_culture = culture if portrait_type in PORTRAIT_OPTIONS_MAPPING[culture] else fallback_ui_culture
    return portrait_culture

def generate_portrait_number(portrait_culture: Literal['european', 'indian', 'middle_east', 'tribal'], portrait_type: str):
    if portrait_culture not in PORTRAIT_OPTIONS_MAPPING:
        raise ValueError(f"Culture '{portrait_culture}' is not present in the dictionary.")
    if portrait_type not in PORTRAIT_OPTIONS_MAPPING[portrait_culture]:
        raise ValueError(f"Culture '{portrait_type}' is not present in '{portrait_culture}' section of the dictionary.")
    return np.random.randint(0, PORTRAIT_OPTIONS_MAPPING[portrait_culture][portrait_type] + 1)

def generate_portrait(culture: str, character_type: str):
    return make_portrait_info(culture, character_type, generate_portrait_age(), generate_portrait_number(culture, character_type))

def generate_season():
    return np.random.choice(['summer', 'winter'])

def generate_age():
    # TODO: Approximate better
    fit_alpha = 131.89287086982398
    fit_loc = -98.17321177602771
    fit_beta = 1.0195464028818084

    age = 0
    while age < 18 or age > 85:
        age = int(round(stats.gamma.rvs(fit_alpha, loc=fit_loc, scale=fit_beta)))
    return age

def get_year_from_date(date: str):
    return int(date.split(' ')[1])

def add_years_to_date(date: str, years: int):
    season, year = date.split(' ')
    return f"{season} {int(year) + years}"

def get_starting_year():
    return CampaignModel(os.path.join(OUTPUT_DIR, 'campaign_env', 'campaign_model.xml')).get_year()

def rgb2hex(r: int, g: int, b: int):
    def clamp(x):
        return max(0, min(int(x), 255))
    return "#{:02x}{:02x}{:02x}".format(clamp(r), clamp(g), clamp(b))

def remove_recruitment_ids():
    if (len(HANDED_OVER_REGION_RECRUITMENT_MANAGER_IDS) == 0) and (len(HANDED_OVER_REGION_SLOT_RECRUITMENT_MANAGER_IDS) == 0):
        print('No IDs to remove. Skipping.')
        return

    bdi_pool = BdiPool('0001.xml')

    handed_over_region_recruitment_manager_ids_set = set(HANDED_OVER_REGION_RECRUITMENT_MANAGER_IDS)
    handed_over_region_slot_recruitment_manager_ids_set = set(HANDED_OVER_REGION_SLOT_RECRUITMENT_MANAGER_IDS)

    for unit_availability in bdi_pool.get_unit_availabilities_region_group() + bdi_pool.get_unit_availabilities_faction():

        existing_land_recruitment_ids = unit_availability.land_recruitment_ids
        existing_land_recruitment_ids = set() if existing_land_recruitment_ids is None else set(existing_land_recruitment_ids.split(' '))
        for region_recruitment_id in handed_over_region_recruitment_manager_ids_set:
            if region_recruitment_id in existing_land_recruitment_ids:
                unit_availability.remove_land_recruitment_id(region_recruitment_id)

        existing_naval_recruitment_ids = unit_availability.naval_recruitment_ids
        existing_naval_recruitment_ids = set() if existing_naval_recruitment_ids is None else set(existing_naval_recruitment_ids.split(' '))
        for region_slot_recruitment_id in handed_over_region_slot_recruitment_manager_ids_set:
            if region_slot_recruitment_id in existing_naval_recruitment_ids:
                unit_availability.remove_naval_recruitment_id(region_slot_recruitment_id)

    bdi_pool.write_xml()

    HANDED_OVER_REGION_RECRUITMENT_MANAGER_IDS.clear()
    HANDED_OVER_REGION_SLOT_RECRUITMENT_MANAGER_IDS.clear()



class EsfXmlSoup:
    def __init__(self, read_xml_path, write_xml_path=None):
        self._read_xml_path = read_xml_path
        self._write_xml_path = write_xml_path
        self._soup = self._read_xml()

    def __str__(self):
        return '\n'.join([
            f'read_xml_path                 : {self._read_xml_path}',
            f'write_xml_path                : {self._write_xml_path}'
        ])

    def print(self):
        print(str(self))

    def _read_xml(self):
        with open(self._read_xml_path, 'r', encoding=XML_ENCODING) as file:
            content = file.read()
        soup = parse_xml_string(content)
        return soup

    def write_xml(self):
        if self._write_xml_path:
            write_xml(self._write_xml_path, self._soup, create_new=True)
        else:
            write_xml(self._read_xml_path, self._soup)



class EsfXmlEtree:
    def __init__(
        self,
        read_xml_path: os.PathLike,
        write_xml_path: os.PathLike = None,
        sub_dir: os.PathLike = None,
        create_new: bool = False):

        self._sub_dir = sub_dir
        self._read_xml_path = self._complete_path_to_xml(read_xml_path)
        self._write_xml_path = self._complete_path_to_xml(write_xml_path) if write_xml_path is not None else self._read_xml_path
        self._create_new = create_new
        self._tree = self._read_xml()

    def _complete_path_to_xml(self, xml_name) -> os.PathLike:
        if self._sub_dir is not None:
            path = os.path.join(OUTPUT_DIR, self._sub_dir, xml_name)
        else:
            path = os.path.join(OUTPUT_DIR, xml_name)
        return path

    def _read_xml(self) -> etree._ElementTree:
        tree = etree.parse(self._read_xml_path, etree.XMLParser(encoding=XML_ENCODING))
        return tree

    def write_xml(self):
        mode = 'x' if self._create_new else 'w'
        formatted_output = '<?xml version="1.0"?>\n' + etree.tostring(self._tree, encoding=XML_ENCODING).decode(XML_ENCODING) + '\n'
        with open(self._write_xml_path, mode, encoding=XML_ENCODING) as file:
            file.write(formatted_output)



# startpos/factions/

class Faction(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._id = self._get_id_tag().string
        self._name = self._get_name_tag().string
        self._on_screen_name = self._get_on_screen_name_tag().string
        self._flag_path = self._get_flag_and_colours_tag().get('path')
        self._revolutionary_flag_path = self._get_revolutionary_flag_and_colours_tag().get('path')
        self._primary_colour = self._get_flag_and_colours_tag().get('color1')
        self._secondary_colour = self._get_flag_and_colours_tag().get('color2')
        self._uniform_colour = self._get_flag_and_colours_tag().get('color3')
        self._revolutionary_primary_colour = self._get_revolutionary_flag_and_colours_tag().get('color1')
        self._revolutionary_secondary_colour = self._get_revolutionary_flag_and_colours_tag().get('color2')
        self._revolutionary_uniform_colour = self._get_revolutionary_flag_and_colours_tag().get('color3')
        self._campaign_player_setup_name = self._get_campaign_player_setup_name_tag().string
        self._campaign_player_setup_playable = self._get_campaign_player_setup_playable_tag().name
        self._majority = self._get_majority_tag().name
        self._emergency = self._get_emergency_tag().name
        self._religion = self._get_religion_tag().string
        self._campaign_ai_manger_behaviour = self._get_campaign_ai_manager_behaviour_tag().string
        self._campaign_ai_personality = self._get_campaign_ai_personality_tag().string
        self._current_capital_id = self._get_current_capital_id_tag().string
        self._original_capital_id = self._get_original_capital_id_tag().string
        self._protectorate_id = self._get_protectorate_id_tag().string
        self._governor_ids = self._get_governor_ids_tag().string
        if self._name is None:
            self._diplomacy_path = None
            self._government_path = None
            self._family_path = None
            self._technology_path = None
        else:
            self._diplomacy_path = get_base_name_from_path(self._get_diplomacy_path_tag().get('path'))
            self._government_path = get_base_name_from_path(self._get_government_path_tag().get('path'))
            self._family_path = get_base_name_from_path(self._get_family_path_tag().get('path'))
            self._technology_path = get_base_name_from_path(self._get_technology_path_tag().get('path'))
        self._character_paths = [get_base_name_from_path(character_array_soup.get('path')) for character_array_soup in self._get_character_array_soups()]
        self._army_paths = [get_base_name_from_path(army_array_soup.get('path')) for army_array_soup in self._get_army_array_soups()]

    def __str__(self):
        return '\n'.join([
            f'id                            : {self.get_id()}',
            f'name                          : {self.get_name()}',
            f'on_screen_name                : {self.get_on_screen_name()}',
            f'flag_path                     : {self.get_flag_path()}',
            f'revolutionary_flag_path       : {self.get_revolutionary_flag_path()}',
            f'campaign_player_setup_name    : {self.get_campaign_player_setup_name()}',
            f'campaign_player_setup_playable: {self.get_campaign_player_setup_playable()}',
            f'majority                      : {self.get_majority()}',
            f'emergency                     : {self.get_emergency()}',
            f'religion                      : {self.get_religion()}',
            f'campaign_ai_manager_behaviour : {self.get_campaign_ai_manager_behaviour()}',
            f'campaign_ai_personality       : {self.get_campaign_ai_personality()}',
            f'current_capital_id            : {self.get_current_capital_id()}',
            f'original_capital_id           : {self.get_original_capital_id()}',
            f'protectorate_id               : {self.get_protectorate_id()}',
            f'governor_ids                  : {self.get_governor_ids()}',
            f'diplomacy_path                : {self.get_diplomacy_path()}',
            f'government_path               : {self.get_government_path()}',
            f'family_path                   : {self.get_family_path()}',
            f'technology_path               : {self.get_technology_path()}'
        ])


    def _get_id_tag(self):
        return self._soup.find('rec', {'type': 'FACTION'}).find('i', recursive=False)

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._get_id_tag().string = id
        self._id = id


    def _get_name_tag(self):
        return self._soup.find('rec', {'type': 'FACTION'}).find('s', recursive=False)

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._get_name_tag().string = name
        self._name = name


    def _get_on_screen_name_tag(self):
        return self._soup.find('rec', {'type': 'FACTION'}).find_all('s', recursive=False)[1]

    def get_on_screen_name(self):
        return self._on_screen_name

    def set_on_screen_name(self, on_screen_name):
        self._get_on_screen_name_tag().string = on_screen_name
        self._on_screen_name = on_screen_name


    def _get_flag_and_colours_tag(self):
        return self._soup.find('rec', {'type': 'FACTION'}).find_all('flag_and_colours', recursive=False)[0]

    def get_flag_path(self):
        return self._flag_path

    def set_flag_path(self, flag_path):
        self._get_flag_and_colours_tag()['path'] = flag_path
        self._flag_path = flag_path

    def get_primary_colour(self):
        return self._primary_colour

    def set_primary_colour(self, primary_colour):
        self._get_flag_and_colours_tag()['color1'] = primary_colour
        self._primary_colour = primary_colour

    def get_secondary_colour(self):
        return self._secondary_colour

    def set_secondary_colour(self, secondary_colour):
        self._get_flag_and_colours_tag()['color2'] = secondary_colour
        self._secondary_colour = secondary_colour

    def get_uniform_colour(self):
        return self._uniform_colour

    def set_uniform_colour(self, uniform_colour):
        self._get_flag_and_colours_tag()['color3'] = uniform_colour
        self._uniform_colour = uniform_colour


    def _get_revolutionary_flag_and_colours_tag(self):
        return self._soup.find('rec', {'type': 'FACTION'}).find_all('flag_and_colours', recursive=False)[1]

    def get_revolutionary_flag_path(self):
        return self._revolutionary_flag_path

    def set_revolutionary_flag_path(self, revolutionary_flag_path):
        self._get_revolutionary_flag_and_colours_tag()['path'] = revolutionary_flag_path
        self._revolutionary_flag_path = revolutionary_flag_path

    def get_revolutionary_primary_colour(self):
        return self._revolutionary_primary_colour

    def set_revolutionary_primary_colour(self, revolutionary_primary_colour):
        self._get_revolutionary_flag_and_colours_tag()['color1'] = revolutionary_primary_colour
        self._revolutionary_primary_colour = revolutionary_primary_colour

    def get_revolutionary_secondary_colour(self):
        return self._revolutionary_secondary_colour

    def set_revolutionary_secondary_colour(self, revolutionary_secondary_colour):
        self._get_revolutionary_flag_and_colours_tag()['color2'] = revolutionary_secondary_colour
        self._revolutionary_secondary_colour = revolutionary_secondary_colour

    def get_revolutionary_uniform_colour(self):
        return self._revolutionary_uniform_colour

    def set_revolutionary_uniform_colour(self, revolutionary_uniform_colour):
        self._get_revolutionary_flag_and_colours_tag()['color3'] = revolutionary_uniform_colour
        self._revolutionary_uniform_colour = revolutionary_uniform_colour


    def _get_campaign_player_setup_name_tag(self):
        return self._soup.find('rec', {'type': 'FACTION'}).find('rec', {'type': 'CAMPAIGN_PLAYER_SETUP'}, recursive=False).find('s', recursive=False)

    def get_campaign_player_setup_name(self):
        return self._campaign_player_setup_name

    def set_campaign_player_setup_name(self, campaign_player_setup_name):
        self._get_campaign_player_setup_name_tag().string = campaign_player_setup_name
        self._campaign_player_setup_name = campaign_player_setup_name


    def _get_campaign_player_setup_playable_tag(self):
        return self._soup.find('rec', {'type': 'FACTION'}).find('rec', {'type': 'CAMPAIGN_PLAYER_SETUP'}, recursive=False).find_all(['yes', 'no'], recursive=False)[1]

    def get_campaign_player_setup_playable(self):
        return self._campaign_player_setup_playable

    def _set_campaign_player_setup_playable(self, campaign_player_setup_playable):
        self._get_campaign_player_setup_playable_tag().name = campaign_player_setup_playable
        self._campaign_player_setup_playable = campaign_player_setup_playable

    def make_playable(self):
        self._set_campaign_player_setup_playable('yes')

    def make_unplayable(self):
        self._set_campaign_player_setup_playable('no')


    def _get_majority_tag(self):
        return self._soup.find('rec', {'type': 'FACTION'}).find_all(['yes', 'no'], recursive=False)[2]

    def get_majority(self):
        return self._majority

    def _set_majority(self, majority):
        self._get_majority_tag().name = majority
        self._majority = majority

    def make_major(self):
        self._set_majority('yes')

    def make_minor(self):
        self._set_majority('no')


    def _get_emergency_tag(self):
        return self._soup.find('rec', {'type': 'FACTION'}).find_all(['yes', 'no'], recursive=False)[6]

    def get_emergency(self):
        return self._emergency

    def _set_emergency(self, emergency):
        self._get_emergency_tag().name = emergency
        self._emergency = emergency

    def make_emergent(self):
        self._set_emergency('yes')

    def make_non_emergent(self):
        self._set_emergency('no')


    def _get_religion_tag(self):
        return self._soup.find('rec', {'type': 'FACTION'}).find_all('s', recursive=False)[2]

    def get_religion(self):
        return self._religion

    def set_religion(self, religion):
        self._get_religion_tag().string = religion
        self._religion = religion


    def _get_campaign_ai_manager_behaviour_tag(self):
        return self._soup.find('rec', {'type': 'FACTION'}).find_all('s', recursive=False)[3]

    def get_campaign_ai_manager_behaviour(self):
        return self._campaign_ai_manger_behaviour

    def set_campaign_ai_manager_behaviour(self, campaign_ai_manger_behaviour):
        self._get_campaign_ai_manager_behaviour_tag().string = campaign_ai_manger_behaviour
        self._campaign_ai_manger_behaviour = campaign_ai_manger_behaviour


    def _get_campaign_ai_personality_tag(self):
        return self._soup.find('rec', {'type': 'FACTION'}).find_all('s', recursive=False)[4]

    def get_campaign_ai_personality(self):
        return self._campaign_ai_personality

    def set_campaign_ai_personality(self, campaign_ai_personality):
        self._get_campaign_ai_personality_tag().string = campaign_ai_personality
        self._campaign_ai_personality = campaign_ai_personality


    def _get_current_capital_id_tag(self):
        return self._soup.find('rec', {'type': 'FACTION'}).find_all('i', recursive=False)[1]

    def get_current_capital_id(self):
        return self._current_capital_id

    def set_current_capital_id(self, current_capital_id):
        self._get_current_capital_id_tag().string = current_capital_id
        self._current_capital_id = current_capital_id


    def _get_original_capital_id_tag(self):
        return self._soup.find('rec', {'type': 'FACTION'}).find_all('i', recursive=False)[2]

    def get_original_capital_id(self):
        return self._original_capital_id

    def set_original_capital_id(self, original_capital_id):
        self._get_original_capital_id_tag().string = original_capital_id
        self._original_capital_id = original_capital_id


    def _get_protectorate_id_tag(self):
        return self._soup.find('rec', {'type': 'FACTION'}).find_all('i', recursive=False)[5]

    def get_protectorate_id(self):
        return self._protectorate_id

    def set_protectorate_id(self, protectorate_id):
        self._get_protectorate_id_tag().string = protectorate_id
        self._protectorate_id = protectorate_id


    def _get_governor_ids_tag(self):
        return self._soup.find('rec', {'type': 'FACTION'}).find('u4_ary', recursive=False)

    def get_governor_ids(self):
        return self._governor_ids

    def remove_governor_id(self, governor_id):
        remove_id_from_tag_string(self._get_governor_ids_tag(), governor_id)
        self._governor_ids = self._get_governor_ids_tag().string

    def add_governor_id(self, governor_id):
        append_id_to_tag_string(self._get_governor_ids_tag(), governor_id, sort=False)
        self._governor_ids = self._get_governor_ids_tag().string


    def _get_diplomacy_path_tag(self):
        return self._soup.find('rec', {'type': 'FACTION'}).find_all('xml_include', recursive=False)[0]

    def get_diplomacy_path(self):
        return self._diplomacy_path

    def set_diplomacy_path(self, path):
        self._get_diplomacy_path_tag()['path'] = 'diplomacy/' + path
        self._diplomacy_path = path


    def _get_government_path_tag(self):
        return self._soup.find('rec', {'type': 'FACTION'}).find_all('xml_include', recursive=False)[1]

    def get_government_path(self):
        return self._government_path

    def set_government_path(self, path):
        self._get_government_path_tag()['path'] = 'government/' + path
        self._government_path = path


    def _get_family_path_tag(self):
        return self._soup.find('rec', {'type': 'FACTION'}).find_all('xml_include', recursive=False)[2]

    def get_family_path(self):
        return self._family_path

    def set_family_path(self, path):
        self._get_family_path_tag()['path'] = 'family/' + path
        self._family_path = path


    def _get_technology_path_tag(self):
        return self._soup.find('rec', {'type': 'FACTION'}).find_all('xml_include', recursive=False)[4]

    def get_technology_path(self):
        return self._technology_path

    def set_technology_path(self, path):
        self._get_technology_path_tag()['path'] = 'technology/' + path
        self._technology_path = path


    def _get_character_array_tag(self):
        return self._soup.find('rec', {'type': 'FACTION'}).find('ary', {'type': 'CHARACTER_ARRAY'}, recursive=False)

    def _get_character_array_soups(self):
        return self._get_character_array_tag().find_all('xml_include', recursive=False)

    def get_character_paths(self):
        return self._character_paths

    def remove_character_path(self, path):
        self._get_character_array_tag().find('xml_include', {'path': 'character/' + path}, recursive=False).decompose()
        self._character_paths.remove(path)

    def add_character_path(self, path):
        insert_tag(self._get_character_array_tag(), 'xml_include', self._soup.new_tag('xml_include', attrs={'path': 'character/' + path}), 2)
        self._character_paths.append(path)


    def _get_army_array_tag(self):
        return self._soup.find('rec', {'type': 'FACTION'}).find('ary', {'type': 'ARMY_ARRAY'}, recursive=False)

    def _get_army_array_soups(self):
        return self._get_army_array_tag().find_all('xml_include', recursive=False)

    def get_army_paths(self):
        return self._army_paths

    def remove_army_path(self, path):
        self._get_army_array_tag().find('xml_include', {'path': 'army/' + path}, recursive=False).decompose()
        self._army_paths.remove(path)

    def add_army_path(self, path):
        insert_tag(self._get_army_array_tag(), 'xml_include', self._soup.new_tag('xml_include', attrs={'path': 'army/' + path}), 2)
        self._army_paths.append(path)



# startpos/cai_factions/

class CaiFaction(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._id = self._get_id_tag().string
        self._owned_direct = self._get_owned_direct_tag().string
        self._hlcis_id = self._get_hlcis_id_tag().string
        self._region_ids = self._get_region_ids_tag().string
        self._theatre_ids = self._get_theatre_ids_tag().string
        self._hlcis_ids = self._get_hlcis_ids_tag().string
        self._character_resource_ids = self._get_character_resource_ids_tag().string
        self._character_ids = self._get_character_ids_tag().string
        self._capital_region_1_id = self._get_capital_region_1_id_tag().string
        self._faction_id = self._get_faction_id_tag().string
        self._technology_id = self._get_technology_id_tag().string
        self._governor_ids = self._get_governor_ids_tag().string
        self._unknown_id = self._get_unknown_id_tag().string
        self._capital_region_2_id = self._get_capital_region_2_id_tag().string
        self._victory_region_ids = self._get_victory_region_ids_tag().string

    def __str__(self):
        return '\n'.join([
            f'id                            : {self.get_id()}',
            f'owned_direct                  : {self.get_owned_direct()}',
            f'hlcis_id                      : {self.get_hlcis_id()}',
            f'region_ids                    : {self.get_region_ids()}',
            f'theatre_ids                   : {self.get_theatre_ids()}',
            f'hlcis_ids                     : {self.get_hlcis_ids()}',
            f'character_resource_ids        : {self.get_character_resource_ids()}',
            f'character_ids                 : {self.get_character_ids()}',
            f'capital_region_1_id           : {self.get_capital_region_1_id()}',
            f'faction_id                    : {self.get_faction_id()}',
            f'technology_id                 : {self.get_technology_id()}',
            f'governor_ids                  : {self.get_governor_ids()}',
            f'unknown_id                    : {self.get_unknown_id()}',
            f'capital_region_2_id           : {self.get_capital_region_2_id()}',
            f'victory_region_ids            : {self.get_victory_region_ids()}'
        ])


    def _get_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_FACTIONS'}).find('u', recursive=False)

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._get_id_tag().string = id
        self._id = id


    def _get_owned_direct_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_FACTIONS'}).find('owned_direct', recursive=False)

    def get_owned_direct(self):
        return self._owned_direct

    def set_owned_direct(self, owned_direct):
        self._get_owned_direct_tag().string = owned_direct
        self._owned_direct = owned_direct


    def _get_hlcis_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_FACTIONS'}).find_all('u', recursive=False)[3]

    def get_hlcis_id(self):
        return self._hlcis_id

    def set_hlcis_id(self, hlcis_id):
        self._get_hlcis_id_tag().string = hlcis_id
        self._hlcis_id = hlcis_id


    def _get_region_ids_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_FACTIONS'}).find('rec', {'type': 'CAI_FACTION'}).find_all('u4_ary', recursive=False)[0]

    def get_region_ids(self):
        return self._region_ids

    def remove_region_id(self, region_id):
        remove_id_from_tag_string(self._get_region_ids_tag(), region_id)
        self._region_ids = self._get_region_ids_tag().string

    def add_region_id(self, region_id):
        append_id_to_tag_string(self._get_region_ids_tag(), region_id)
        self._region_ids = self._get_region_ids_tag().string


    def _get_theatre_ids_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_FACTIONS'}).find('rec', {'type': 'CAI_FACTION'}).find_all('u4_ary', recursive=False)[1]

    def get_theatre_ids(self):
        return self._theatre_ids

    def remove_theatre_id(self, theatre_id):
        remove_id_from_tag_string(self._get_theatre_ids_tag(), theatre_id)
        self._theatre_ids = self._get_theatre_ids_tag().string

    def add_theatre_id(self, theatre_id):
        append_id_to_tag_string(self._get_theatre_ids_tag(), theatre_id, sort=False)
        self._theatre_ids = self._get_theatre_ids_tag().string


    def _get_hlcis_ids_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_FACTIONS'}).find('rec', {'type': 'CAI_FACTION'}).find_all('u4_ary', recursive=False)[2]

    def get_hlcis_ids(self):
        return self._hlcis_ids

    def remove_hlcis_id(self, hlcis_id):
        remove_id_from_tag_string(self._get_hlcis_ids_tag(), hlcis_id)
        self._hlcis_ids = self._get_hlcis_ids_tag().string

    def add_hlcis_id(self, hlcis_id):
        append_id_to_tag_string(self._get_hlcis_ids_tag(), hlcis_id, sort=False)
        self._hlcis_ids = self._get_hlcis_ids_tag().string


    def _get_character_resource_ids_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_FACTIONS'}).find('rec', {'type': 'CAI_FACTION'}).find_all('u4_ary', recursive=False)[3]

    def get_character_resource_ids(self):
        return self._character_resource_ids

    def remove_character_resource_id(self, character_resource_id):
        remove_id_from_tag_string(self._get_character_resource_ids_tag(), character_resource_id)
        self._character_resource_ids = self._get_character_resource_ids_tag().string

    def add_character_resource_id(self, character_resource_id):
        append_id_to_tag_string(self._get_character_resource_ids_tag(), character_resource_id)
        self._character_resource_ids = self._get_character_resource_ids_tag().string


    def _get_character_ids_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_FACTIONS'}).find('rec', {'type': 'CAI_FACTION'}).find_all('u4_ary', recursive=False)[4]

    def get_character_ids(self):
        return self._character_ids

    def remove_character_id(self, character_id):
        remove_id_from_tag_string(self._get_character_ids_tag(), character_id)
        self._character_ids = self._get_character_ids_tag().string

    def add_character_id(self, character_id):
        append_id_to_tag_string(self._get_character_ids_tag(), character_id)
        self._character_ids = self._get_character_ids_tag().string


    def _get_capital_region_1_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_FACTIONS'}).find('rec', {'type': 'CAI_FACTION'}).find_all('u', recursive=False)[0]

    def get_capital_region_1_id(self):
        return self._capital_region_1_id

    def set_capital_region_1_id(self, capital_region_1_id):
        self._get_capital_region_1_id_tag().string = capital_region_1_id
        self._capital_region_1_id = capital_region_1_id


    def _get_faction_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_FACTIONS'}).find('rec', {'type': 'CAI_FACTION'}).find_all('u', recursive=False)[1]

    def get_faction_id(self):
        return self._faction_id

    def set_faction_id(self, faction_id):
        self._get_faction_id_tag().string = faction_id
        self._faction_id = faction_id


    def _get_technology_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_FACTIONS'}).find('rec', {'type': 'CAI_FACTION'}).find_all('u', recursive=False)[2]

    def get_technology_id(self):
        return self._technology_id

    def set_technology_id(self, technology_id):
        self._get_technology_id_tag().string = technology_id
        self._technology_id = technology_id


    def _get_governor_ids_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_FACTIONS'}).find('rec', {'type': 'CAI_FACTION'}).find_all('u4_ary', recursive=False)[7]

    def get_governor_ids(self):
        return self._governor_ids

    def remove_governor_id(self, governor_id):
        remove_id_from_tag_string(self._get_governor_ids_tag(), governor_id)
        self._governor_ids = self._get_governor_ids_tag().string

    def add_governor_id(self, governor_id):
        append_id_to_tag_string(self._get_governor_ids_tag(), governor_id)
        self._governor_ids = self._get_governor_ids_tag().string


    def _get_unknown_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_FACTIONS'}).find('rec', {'type': 'CAI_FACTION'}).find_all('u', recursive=False)[3]

    def get_unknown_id(self):
        return self._unknown_id

    def set_unknown_id(self, unknown_id):
        self._get_unknown_id_tag().string = unknown_id
        self._unknown_id = unknown_id


    def _get_capital_region_2_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_FACTIONS'}).find('rec', {'type': 'CAI_FACTION'}).find_all('u', recursive=False)[10]

    def get_capital_region_2_id(self):
        return self._capital_region_2_id

    def set_capital_region_2_id(self, capital_region_2_id):
        self._get_capital_region_2_id_tag().string = capital_region_2_id
        self._capital_region_2_id = capital_region_2_id


    def _get_victory_region_ids_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_FACTIONS'}).find('rec', {'type': 'CAI_FACTION'}).find_all('u4_ary', recursive=False)[16]

    def get_victory_region_ids(self):
        return self._victory_region_ids

    def set_victory_region_ids(self, victory_region_ids):
        self._get_victory_region_ids_tag().string = victory_region_ids
        self._victory_region_ids = victory_region_ids

    def remove_victory_region_id(self, victory_region_id):
        remove_id_from_tag_string(self._get_victory_region_ids_tag(), victory_region_id)
        self._victory_region_ids = self._get_victory_region_ids_tag().string

    def add_victory_region_id(self, victory_region_id):
        append_id_to_tag_string(self._get_victory_region_ids_tag(), victory_region_id)
        self._victory_region_ids = self._get_victory_region_ids_tag().string



# startpos/family/

class FamilyMember(EsfXmlSoup):
    def __init__(self, soup: BeautifulSoup):
        self._soup = soup
        self._name = self._get_name_tag().string
        self._n_children = self._get_n_children_tag().string
        self._male = self._get_male_tag().name
        self._age = self._get_age_tag().string
        self._regnal_number = self._get_regnal_number_tag().string
        self._portrait_card = self._get_portrait_tag().get('card')
        self._portrait_template = self._get_portrait_tag().get('template')
        self._portrait_info = self._get_portrait_tag().get('info')
        self._portrait_number = self._get_portrait_tag().get('number')
        self._religion = self._get_religion_tag().string
        self._faction_id_1 = self._get_faction_id_1_tag().string
        self._faction_id_2 = self._get_faction_id_2_tag().string

    def __str__(self):
        return '\n'.join([
            f'name                          : {self.get_name()}',
            f'male                          : {self.get_male()}',
            f'n_children                    : {self.get_n_children()}',
            f'age                           : {self.get_age()}',
            f'regnal_number                 : {self.get_regnal_number()}',
            f'portrait_card                 : {self.get_portrait_card()}',
            f'portrait_template             : {self.get_portrait_template()}',
            f'portrait_info                 : {self.get_portrait_info()}',
            f'portrait_number               : {self.get_portrait_number()}',
            f'religion                      : {self.get_religion()}',
            f'faction_id_1                  : {self.get_faction_id_1()}',
            f'faction_id_2                  : {self.get_faction_id_2()}'
        ])

    def print(self):
        print(str(self))


    def _get_name_tag(self):
        return self._soup.find('loc', recursive=False)

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._get_name_tag().string = name
        self._name = name


    def _get_n_children_tag(self):
        return self._soup.find('byte', recursive=False)

    def get_n_children(self):
        return self._n_children

    def set_n_children(self, n_children):
        self._get_n_children_tag().string = n_children
        self._n_children = n_children


    def _get_male_tag(self):
        return self._soup.find(['yes', 'no'], recursive=False)

    def get_male(self):
        return self._male

    def _set_male(self, male: Literal['yes', 'no']):
        self._get_male_tag().name = male
        self._male = male

    def make_male(self):
        self._set_male('yes')

    def make_female(self):
        self._set_male('no')


    def _get_age_tag(self):
        return self._soup.find_all('i', recursive=False)[1]

    def get_age(self):
        return self._age

    def set_age(self, age):
        self._get_age_tag().string = age
        self._age = age


    def _get_regnal_number_tag(self):
        return self._soup.find_all('i', recursive=False)[2]

    def get_regnal_number(self):
        return self._regnal_number

    def set_regnal_number(self, regnal_number):
        self._get_regnal_number_tag().string = regnal_number
        self._regnal_number = regnal_number


    def _get_portrait_tag(self):
        return self._soup.find('portrait_details', recursive=False)

    def get_portrait_card(self):
        return self._portrait_card

    def _set_portrait_card(self, card):
        self._get_portrait_tag()['card'] = card
        self._portrait_card = card

    def get_portrait_template(self):
        return self._portrait_template

    def _set_portrait_template(self, template):
        self._get_portrait_tag()['template'] = template
        self._portrait_template = template

    def get_portrait_info(self):
        return self._portrait_info

    def _set_portrait_info(self, info):
        self._get_portrait_tag()['info'] = info
        self._portrait_info = info

    def get_portrait_number(self):
        return self._portrait_number

    def _set_portrait_number(self, number):
        self._get_portrait_tag()['number'] = number
        self._portrait_number = number

    def set_portrait_culture(self, culture):
        card = self.get_portrait_card().split('/')
        info = self.get_portrait_info().split('/')
        card[2] = culture
        info[2] = culture
        card = '/'.join(card)
        info = '/'.join(info)
        self._set_portrait_card(card)
        self._set_portrait_info(info)

    def set_portrait_agent_type(self, agent_type):
        card = self.get_portrait_card().split('/')
        info = self.get_portrait_info().split('/')
        card[4] = agent_type
        info[4] = agent_type
        card = '/'.join(card)
        info = '/'.join(info)
        self._set_portrait_card(card)
        self._set_portrait_info(info)

    def set_portrait_age(self, age: Literal['young', 'old']):
        card = self.get_portrait_card().split('/')
        info = self.get_portrait_info().split('/')
        card[5] = age
        info[5] = age
        card = '/'.join(card)
        info = '/'.join(info)
        self._set_portrait_card(card)
        self._set_portrait_info(info)

    def set_portrait_number(self, number: int, faction_leader=False):
        number = str(number)
        card = self.get_portrait_card().split('/')
        info = self.get_portrait_info().split('/')
        card[-1] = f"{number.zfill(3)}.tga"
        info[-1] = f"{number.zfill(3)}.jpg"
        card = '/'.join(card)
        info = '/'.join(info)
        self._set_portrait_card(card)
        self._set_portrait_info(info)
        if faction_leader:
            self._set_portrait_number('-1')
        else:
            self._set_portrait_number(number)


    def _get_religion_tag(self):
        return self._soup.find('s', recursive=False)

    def get_religion(self):
        return self._religion

    def set_religion(self, religion):
        self._get_religion_tag().string = religion
        self._religion = religion


    def _get_faction_id_1_tag(self):
        return self._soup.find_all('u', recursive=False)[0]

    def get_faction_id_1(self):
        return self._faction_id_1

    def set_faction_id_1(self, faction_id_1):
        self._get_faction_id_1_tag().string = faction_id_1
        self._faction_id_1 = faction_id_1


    def _get_faction_id_2_tag(self):
        return self._soup.find_all('u', recursive=False)[1]

    def get_faction_id_2(self):
        return self._faction_id_2

    def set_faction_id_2(self, faction_id_2):
        self._get_faction_id_2_tag().string = faction_id_2
        self._faction_id_2 = faction_id_2



class Family(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._family_members = []
        self._ordinal_pairs = {}
        for family_member_soup in self._get_family_member_soups():
            family_member = FamilyMember(family_member_soup)
            self._family_members.append(family_member)
        for ordinal_pair_soup in self._get_ordinal_pair_soups():
            self._ordinal_pairs[ordinal_pair_soup.get('name')] = ordinal_pair_soup.get('number')


    def _get_family_member_soups(self):
        return self._soup.find('rec', {'type': 'FAMILY'}).find_all('rec', {'type': 'FAMILY::MONARCHY_INFO_CHARACTER'}, recursive=False)


    def _get_ordinal_pair_soups(self):
        return self._soup.find('rec', {'type': 'FAMILY'}).find('ary', {'type': 'ORDINAL_PAIR'}, recursive=False).find_all('ordinal_pair', recursive=False)


    def get_family_members(self) -> List[FamilyMember]:
        return self._family_members


    def get_ordinal_pairs(self) -> Dict[str, str]:
        return self._ordinal_pairs



# startpos/government/

class GovernmentPost:
    governorships_to_theatre_cai_id = {
        'governor_america': '33',
        'governor_europe': '34',
        'governor_india': '35'
    }

    def __init__(self, soup: BeautifulSoup):
        self._soup = soup
        self._id = self._get_id_tag().string
        self._title = self._get_title_tag().string
        self._character_id = self._get_character_id_tag().string
        self._governor = self._get_governor_tag().name
        self._government_id = self._get_government_id_tag().string
        self._taxes_level_lower = None
        self._taxes_level_upper = None
        self._taxes_rate_lower = None
        self._taxes_rate_upper = None
        self._governor_id = None
        self._region_ids = None
        self._faction_id = None
        self._unknown_yesno_1 = None
        self._unknown_yesno_2 = None
        if self._governor == 'yes':
            self._taxes_level_lower = self._get_taxes_tag().get('level_lower')
            self._taxes_level_upper = self._get_taxes_tag().get('level_upper')
            self._taxes_rate_lower = self._get_taxes_tag().get('rate_lower')
            self._taxes_rate_upper = self._get_taxes_tag().get('rate_upper')
            self._governor_id = self._get_governor_id_tag().string
            self._region_ids = self._get_region_ids_tag().string
            self._faction_id = self._get_faction_id_tag().string
            self._unknown_yesno_1 = self._get_unknown_yesno_1_tag().name
            self._unknown_yesno_2 = self._get_unknown_yesno_2_tag().name

    def __str__(self):
        return '\n'.join([
            f'id                            : {self.get_id()}',
            f'title                         : {self.get_title()}',
            f'theatre                       : {self.get_theatre()}',
            f'character_id                  : {self.get_character_id()}',
            f'governor                      : {self.get_governor()}',
            f'government_id                 : {self.get_government_id()}',
            f'taxes_level_lower             : {self.get_taxes_level_lower()}',
            f'taxes_level_upper             : {self.get_taxes_level_upper()}',
            f'taxes_rate_lower              : {self.get_taxes_rate_lower()}',
            f'taxes_rate_upper              : {self.get_taxes_rate_upper()}',
            f'governor_id                   : {self.get_governor_id()}',
            f'region_ids                    : {self.get_region_ids()}',
            f'faction_id                    : {self.get_faction_id()}',
            f'unknown_yesno_1               : {self.get_unknown_yesno_1()}',
            f'unknown_yesno_2               : {self.get_unknown_yesno_2()}'
        ])

    def print(self):
        print(str(self))


    def _get_id_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_POST'}).find('i', recursive=False)

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._get_id_tag().string = id
        self._id = id


    def _get_title_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_POST'}).find('s', recursive=False)

    def get_title(self):
        return self._title

    def set_title(self, title):
        self._get_title_tag().string = title
        self._title = title


    def get_theatre(self):
        return self._title.split('_')[1]


    def _get_character_id_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_POST'}).find('u', recursive=False)

    def get_character_id(self):
        return self._character_id

    def set_character_id(self, character_id):
        self._get_character_id_tag().string = character_id
        self._character_id = character_id


    def _get_governor_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_POST'}).find(['yes', 'no'], recursive=False)

    def get_governor(self):
        return self._governor

    def _set_governor(self, governor):
        self._get_governor_tag().name = governor
        self._governor = governor

    def make_governor(self):
        self._set_governor('yes')

    def make_non_governor(self):
        self._set_governor('no')


    def _get_government_id_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_POST'}).find_all('i', recursive=False)[1]

    def get_government_id(self):
        return self._government_id

    def set_government_id(self, government_id):
        self._get_government_id_tag().string = government_id
        self._government_id = government_id


    def _get_taxes_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_POST'}).find('rec', {'type': 'GOVERNORSHIP'}, recursive=False).find('gov_taxes', recursive=False)

    def get_taxes_level_lower(self):
        return self._taxes_level_lower

    def set_taxes_level_lower(self, level_lower):
        self._get_taxes_tag()['level_lower'] = level_lower
        self._taxes_level_lower = level_lower

    def get_taxes_level_upper(self):
        return self._taxes_level_upper

    def set_taxes_level_upper(self, level_upper):
        self._get_taxes_tag()['level_upper'] = level_upper
        self._taxes_level_upper = level_upper

    def get_taxes_rate_lower(self):
        return self._taxes_rate_lower

    def set_taxes_rate_lower(self, rate_lower):
        self._get_taxes_tag()['rate_lower'] = rate_lower
        self._taxes_rate_lower = rate_lower

    def get_taxes_rate_upper(self):
        return self._taxes_rate_upper

    def set_taxes_rate_upper(self, rate_upper):
        self._get_taxes_tag()['rate_upper'] = rate_upper
        self._taxes_rate_upper = rate_upper


    def _get_governor_id_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_POST'}).find('rec', {'type': 'GOVERNORSHIP'}, recursive=False).find('i', recursive=False)

    def get_governor_id(self):
        return self._governor_id

    def set_governor_id(self, governor_id):
        self._get_governor_id_tag().string = governor_id
        self._governor_id = governor_id


    def _get_region_ids_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_POST'}).find('rec', {'type': 'GOVERNORSHIP'}, recursive=False).find('u4_ary', recursive=False)

    def get_region_ids(self):
        return self._region_ids

    def remove_region_id(self, region_id):
        remove_id_from_tag_string(self._get_region_ids_tag(), region_id)
        self._region_ids = self._get_region_ids_tag().string

    def add_region_id(self, region_id):
        append_id_to_tag_string(self._get_region_ids_tag(), region_id, sort=False)
        self._region_ids = self._get_region_ids_tag().string


    def _get_faction_id_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_POST'}).find('rec', {'type': 'GOVERNORSHIP'}, recursive=False).find('u', recursive=False)

    def get_faction_id(self):
        return self._faction_id

    def set_faction_id(self, faction_id):
        self._get_faction_id_tag().string = faction_id
        self._faction_id = faction_id


    def _get_unknown_yesno_1_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_POST'}).find('rec', {'type': 'GOVERNORSHIP'}, recursive=False).find_all(['yes', 'no'], recursive=False)[0]

    def get_unknown_yesno_1(self):
        return self._unknown_yesno_1

    def _set_unknown_yesno_1(self, unknown_yesno_1):
        self._get_unknown_yesno_1_tag().name = unknown_yesno_1
        self._unknown_yesno_1 = unknown_yesno_1


    def _get_unknown_yesno_2_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_POST'}).find('rec', {'type': 'GOVERNORSHIP'}, recursive=False).find_all(['yes', 'no'], recursive=False)[1]

    def get_unknown_yesno_2(self):
        return self._unknown_yesno_2

    def _set_unknown_yesno_2(self, unknown_yesno_2):
        self._get_unknown_yesno_2_tag().name = unknown_yesno_2
        self._unknown_yesno_2 = unknown_yesno_2



class Government(EsfXmlSoup):
    _supported_types = Literal['gov_absolute_monarchy', 'gov_constitutional_monarchy', 'gov_republic']
    _supported_titles = Literal['faction_leader', 'head_of_government', 'finance', 'justice', 'army', 'navy', 'accident', 'governor_america', 'governor_europe', 'governor_india']

    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._id = self._get_id_tag().string
        self._type = self._get_type_tag().string
        self._popularity = self._get_popularity_tag().string
        self._elections_due = None
        self._had_elections = None
        self._minister_changes = None
        self._term = None
        if self._type in ['gov_constitutional_monarchy', 'gov_republic']:
            self._elections_due = self._get_elections_tag().get('elections_due')
            self._had_elections = self._get_elections_tag().get('had_elections')
            self._minister_changes = self._get_elections_tag().get('minister_changes')
        if self._type == 'gov_republic':
            self._term = self._get_elections_tag().get('term')
        self.post_faction_leader = None
        self.post_head_of_government = None
        self.post_finance = None
        self.post_justice = None
        self.post_army = None
        self.post_navy = None
        self.post_accident = None
        self.post_governor_america = None
        self.post_governor_europe = None
        self.post_governor_india = None
        for government_post_soup in self._get_government_post_soups():
            government_post = GovernmentPost(government_post_soup)
            title = government_post.get_title()
            if title == 'faction_leader':
                self.post_faction_leader = government_post
            if title == 'head_of_government':
                self.post_head_of_government = government_post
            if title == 'finance':
                self.post_finance = government_post
            if title == 'justice':
                self.post_justice = government_post
            if title == 'army':
                self.post_army = government_post
            if title == 'navy':
                self.post_navy = government_post
            if title == 'accident':
                self.post_accident = government_post
            if title == 'governor_america':
                self.post_governor_america = government_post
            if title == 'governor_europe':
                self.post_governor_europe = government_post
            if title == 'governor_india':
                self.post_governor_india = government_post

    def __str__(self):
        def __get_post_cabinet_id(post):
            return None if post is None else post.get_id()
        return '\n'.join([
            f'id                            : {self.get_id()}',
            f'type                          : {self.get_type()}',
            f'popularity                    : {self.get_popularity()}',
            f'elections_due                 : {self.get_elections_due()}',
            f'had_elections                 : {self.get_had_elections()}',
            f'minister_changes              : {self.get_minister_changes()}',
            f'term                          : {self.get_term()}',
            f'cabinet_id_faction_leader     : {__get_post_cabinet_id(self.get_post("faction_leader"))}',
            f'cabinet_id_head_of_government : {__get_post_cabinet_id(self.get_post("head_of_government"))}',
            f'cabinet_id_finance            : {__get_post_cabinet_id(self.get_post("finance"))}',
            f'cabinet_id_justice            : {__get_post_cabinet_id(self.get_post("justice"))}',
            f'cabinet_id_army               : {__get_post_cabinet_id(self.get_post("army"))}',
            f'cabinet_id_navy               : {__get_post_cabinet_id(self.get_post("navy"))}',
            f'cabinet_id_accident           : {__get_post_cabinet_id(self.get_post("accident"))}',
            f'cabinet_id_governor_america   : {__get_post_cabinet_id(self.get_post("governor_america"))}',
            f'cabinet_id_governor_europe    : {__get_post_cabinet_id(self.get_post("governor_europe"))}',
            f'cabinet_id_governor_india     : {__get_post_cabinet_id(self.get_post("governor_india"))}'
        ])


    def _get_id_tag(self):
        return self._soup.find('rec', {'type': 'GOVERNMENT'}).find('i', recursive=False)

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._get_id_tag().string = id
        self._id = id


    def _get_popularity_tag(self):
        return self._soup.find('rec', {'type': 'GOVERNMENT'}).find_all('i', recursive=False)[1]

    def get_popularity(self):
        return self._popularity

    def set_popularity(self, popularity):
        self._get_popularity_tag().string = popularity
        self._popularity = popularity


    def _get_elections_tag(self):
        return self._soup.find('rec', {'type': 'GOVERNMENT'}).find(get_args(self._supported_types), recursive=False)

    def get_minister_changes(self):
        return self._minister_changes

    def set_minister_changes(self, minister_changes):
        elections = self._get_elections_tag()
        if elections.has_attr('minister_changes'):
            elections['minister_changes'] = minister_changes
            self._minister_changes = minister_changes
        else:
            raise ValueError(f"minister_changes property missing.")

    def get_had_elections(self):
        return self._had_elections

    def set_had_elections(self, had_elections):
        elections = self._get_elections_tag()
        if elections.has_attr('had_elections'):
            elections['had_elections'] = had_elections
            self._had_elections = had_elections
        else:
            raise ValueError(f"had_elections property missing.")

    def get_elections_due(self):
        return self._elections_due

    def set_elections_due(self, elections_due):
        elections = self._get_elections_tag()
        if elections.has_attr('elections_due'):
            elections['elections_due'] = elections_due
            self._elections_due = elections_due
        else:
            raise ValueError(f"elections_due property missing.")

    def get_term(self):
        return self._term

    def set_term(self, term):
        elections = self._get_elections_tag()
        if elections.has_attr('term'):
            elections['term'] = term
            self._term = term
        else:
            raise ValueError(f"term property missing.")


    def _get_type_tag(self):
        return self._soup.find('rec', {'type': 'GOVERNMENT'}).find('s', recursive=False)

    def get_type(self) -> _supported_types:
        return self._type

    def set_type(self, type: _supported_types):
        assert type in get_args(self._supported_types), f"'{type}' government type is not supported."
        self._get_type_tag().string = type
        self._type = type
        elections = self._get_elections_tag()
        for attribute in ['elections_due', 'had_elections', 'minister_changes', 'term']:
            if elections.has_attr(attribute):
                del elections[attribute]
        elections.name = type
        if type == 'gov_constitutional_monarchy':
            elections['minister_changes'] = None
            elections['had_elections'] = None
            elections['elections_due'] = None
            self.set_minister_changes('0')
            self.set_had_elections('no')
            self.set_elections_due('10')
        if type == 'gov_republic':
            elections['minister_changes'] = None
            elections['had_elections'] = None
            elections['elections_due'] = None
            elections['term'] = None
            self.set_minister_changes('0')
            self.set_had_elections('no')
            self.set_elections_due('8')
            self.set_term('0')


    def _get_government_post_soups(self):
        return self._soup.find('rec', {'type': 'GOVERNMENT'}).find('ary', {'type': 'POSTS_ARRAY'}, recursive=False).find_all('rec', {'type': 'POSTS_ARRAY'}, recursive=False)


    def add_post(self, post_soup):
        self._soup.find('rec', {'type': 'GOVERNMENT'}).find('ary', {'type': 'POSTS_ARRAY'}, recursive=False).append(post_soup)


    def get_post(self, title: _supported_titles) -> GovernmentPost:
        assert title in get_args(self._supported_titles), f"'{title}' cabinet title is not supported."
        if title == 'faction_leader':
            return self.post_faction_leader
        if title == 'head_of_government':
            return self.post_head_of_government
        if title == 'finance':
            return self.post_finance
        if title == 'justice':
            return self.post_justice
        if title == 'army':
            return self.post_army
        if title == 'navy':
            return self.post_navy
        if title == 'accident':
            return self.post_accident
        if title == 'governor_america':
            return self.post_governor_america
        if title == 'governor_europe':
            return self.post_governor_europe
        if title == 'governor_india':
            return self.post_governor_india


    def remove_post(self, title: _supported_titles):
        assert title in get_args(self._supported_titles), f"'{title}' cabinet title is not supported."
        if title == 'faction_leader':
            if self.post_faction_leader is None:
                raise ValueError(f"faction_leader post is not preset in {self._read_xml_path}.")
            self.post_faction_leader._soup.decompose()
            self.post_faction_leader = None
        if title == 'head_of_government':
            if self.post_head_of_government is None:
                raise ValueError(f"head_of_government post is not preset in {self._read_xml_path}.")
            self.post_head_of_government._soup.decompose()
            self.post_head_of_government = None
        if title == 'finance':
            if self.post_finance is None:
                raise ValueError(f"finance post is not preset in {self._read_xml_path}.")
            self.post_finance._soup.decompose()
            self.post_finance = None
        if title == 'justice':
            if self.post_justice is None:
                raise ValueError(f"justice post is not preset in {self._read_xml_path}.")
            self.post_justice._soup.decompose()
            self.post_justice = None
        if title == 'army':
            if self.post_army is None:
                raise ValueError(f"army post is not preset in {self._read_xml_path}.")
            self.post_army._soup.decompose()
            self.post_army = None
        if title == 'navy':
            if self.post_navy is None:
                raise ValueError(f"navy post is not preset in {self._read_xml_path}.")
            self.post_navy._soup.decompose()
            self.post_navy = None
        if title == 'accident':
            if self.post_accident is None:
                raise ValueError(f"accident post is not preset in {self._read_xml_path}.")
            self.post_accident._soup.decompose()
            self.post_accident = None
        if title == 'governor_america':
            if self.post_governor_america is None:
                raise ValueError(f"governor_america post is not preset in {self._read_xml_path}.")
            self.post_governor_america._soup.decompose()
            self.post_governor_america = None
        if title == 'governor_europe':
            if self.post_governor_europe is None:
                raise ValueError(f"governor_europe post is not preset in {self._read_xml_path}.")
            self.post_governor_europe._soup.decompose()
            self.post_governor_europe = None
        if title == 'governor_india':
            if self.post_governor_india is None:
                raise ValueError(f"governor_india post is not preset in {self._read_xml_path}.")
            self.post_governor_india._soup.decompose()
            self.post_governor_india = None



# startpos/cai_governorships/

class CaiGovernorship(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._id = self._get_id_tag().string
        self._owned_direct = self._get_owned_direct_tag().string # Faction AI ID
        self._governor_id = self._get_governor_id_tag().string
        self._theatre_id = self._get_theatre_id_tag().string
        self._character_id = self._get_character_id_tag().string
        self._region_ids = self._get_region_ids_tag().string

    def __str__(self):
        return '\n'.join([
            f'id                            : {self.get_id()}',
            f'owned_direct                  : {self.get_owned_direct()}',
            f'governor_id                   : {self.get_governor_id()}',
            f'theatre_id                    : {self.get_theatre_id()}',
            f'character_id                  : {self.get_character_id()}',
            f'region_ids                    : {self.get_region_ids()}'
        ])


    def _get_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_GOVERNORSHIPS'}).find('u', recursive=False)

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._get_id_tag().string = id
        self._id = id


    def _get_owned_direct_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_GOVERNORSHIPS'}).find('owned_direct', recursive=False)

    def get_owned_direct(self):
        return self._owned_direct

    def set_owned_direct(self, owned_direct):
        self._get_owned_direct_tag().string = owned_direct
        self._owned_direct = owned_direct


    def _get_governor_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_GOVERNORSHIPS'}).find('rec', {'type': 'CAI_GOVERNORSHIP'}).find_all('u', recursive=False)[0]

    def get_governor_id(self):
        return self._governor_id

    def set_governor_id(self, governor_id):
        self._get_governor_id_tag().string = governor_id
        self._governor_id = governor_id


    def _get_theatre_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_GOVERNORSHIPS'}).find('rec', {'type': 'CAI_GOVERNORSHIP'}).find_all('u', recursive=False)[1]

    def get_theatre_id(self):
        return self._theatre_id

    def set_theatre_id(self, theatre_id):
        self._get_theatre_id_tag().string = theatre_id
        self._theatre_id = theatre_id


    def _get_character_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_GOVERNORSHIPS'}).find('rec', {'type': 'CAI_GOVERNORSHIP'}).find_all('u', recursive=False)[2]

    def get_character_id(self):
        return self._character_id

    def set_character_id(self, character_id):
        self._get_character_id_tag().string = character_id
        self._character_id = character_id


    def _get_region_ids_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_GOVERNORSHIPS'}).find('rec', {'type': 'CAI_GOVERNORSHIP'}).find('u4_ary', recursive=False)

    def get_region_ids(self):
        return self._region_ids

    def remove_region_id(self, region_id):
        remove_id_from_tag_string(self._get_region_ids_tag(), region_id)
        self._region_ids = self._get_region_ids_tag().string

    def add_region_id(self, region_id):
        append_id_to_tag_string(self._get_region_ids_tag(), region_id, sort=False)
        self._region_ids = self._get_region_ids_tag().string


    def _get_bdi_1_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_GOVERNORSHIPS'}).find_all('u4_ary', recursive=False)[1]

    def _get_bdi_3_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_GOVERNORSHIPS'}).find_all('u4_ary', recursive=False)[3]

    def clear_bdi(self):
        self._get_bdi_1_tag().string = ''
        self._get_bdi_3_tag().string = ''



# startpos/character/

class AgentAbility:
    def __init__(self, soup: BeautifulSoup):
        self._soup = soup
        self._ability = self._soup.get('ability')
        self._level = self._soup.get('level')
        self._attribute = self._soup.get('attribute')

    def __str__(self):
        return '\n'.join([
            f'ability                       : {self.get_ability()}',
            f'level                         : {self.get_level()}',
            f'attribute                     : {self.get_attribute()}'
        ])

    def print(self):
        print(str(self))


    def get_ability(self):
        return self._ability

    def set_ability(self, ability):
        self._soup['ability'] = ability
        self._ability = ability

    def get_level(self):
        return self._level

    def set_level(self, level):
        self._soup['level'] = level
        self._level = level

    def get_attribute(self):
        return self._attribute

    def set_attribute(self, attribute):
        self._soup['attribute'] = attribute
        self._attribute = attribute



class Character(EsfXmlSoup):
    class AttributeValue(TypedDict):
        attribute: str
        value: int

    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._id = self._get_id_tag().string
        self._type = self._get_type_tag().string
        self._army_id = self._get_army_id_tag().string
        self._unit_id = self._get_unit_id_tag().string
        self._building_slot_id = self._get_building_slot_id_tag().string
        self._cabinet_id = self._get_cabinet_id_tag().string
        self._traits = self._get_traits_tag().string
        self._ancillaries = self._get_ancillaries_tag().string
        self._first_name = self._get_first_name_tag().string
        self._last_name = self._get_last_name_tag().string
        self._regnal_number = self._get_regnal_number_tag().string
        self._birth_date = self._get_birth_date_tag().string
        self._portrait_card = self._get_portrait_tag().get('card')
        self._portrait_template = self._get_portrait_tag().get('template')
        self._portrait_info = self._get_portrait_tag().get('info')
        self._portrait_number = self._get_portrait_tag().get('number')
        self._faction = self._get_faction_tag().string
        self._details_character_id = self._get_details_character_id_tag().string
        self._agent_onscreen_name = self._get_agent_onscreen_name_tag().string
        self._agent_abilities = {}
        for ability_soup in self._get_agent_ability_soups():
            ability = AgentAbility(ability_soup)
            self._agent_abilities[ability.get_ability()] = ability

    def __str__(self):
        return '\n'.join([
            f'id                            : {self.get_id()}',
            f'type                          : {self.get_type()}',
            f'army_id                       : {self.get_army_id()}',
            f'unit_id                       : {self.get_unit_id()}',
            f'building_slot_id              : {self.get_building_slot_id()}',
            f'cabinet_id                    : {self.get_cabinet_id()}',
            f'first_name                    : {self.get_first_name()}',
            f'last_name                     : {self.get_last_name()}',
            f'regnal_number                 : {self.get_regnal_number()}',
            f'birth_date                    : {self.get_birth_date()}',
            f'portrait_card                 : {self.get_portrait_card()}',
            f'portrait_template             : {self.get_portrait_template()}',
            f'portrait_info                 : {self.get_portrait_info()}',
            f'portrait_number               : {self.get_portrait_number()}',
            f'faction                       : {self.get_faction()}',
            f'details_character_id          : {self.get_details_character_id()}',
            f'agent_onscreen_name           : {self.get_agent_onscreen_name()}'
        ])


    def _get_id_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_ARRAY'}).find('rec', {'type': 'CHARACTER'}, recursive=False).find('i', recursive=False)

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._get_id_tag().string = id
        self._id = id


    def _get_type_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_ARRAY'}).find('rec', {'type': 'CHARACTER'}, recursive=False).find('s', recursive=False)

    def get_type(self):
        return self._type

    def set_type(self, type):
        self._get_type_tag().string = type
        self._type = type


    def _get_army_id_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_ARRAY'}).find('rec', {'type': 'CHARACTER'}, recursive=False).find_all('u', recursive=False)[0]

    def get_army_id(self):
        return self._army_id

    def set_army_id(self, army_id):
        self._get_army_id_tag().string = army_id
        self._army_id = army_id


    def _get_unit_id_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_ARRAY'}).find('rec', {'type': 'CHARACTER'}, recursive=False).find_all('u', recursive=False)[1]

    def get_unit_id(self):
        return self._unit_id

    def set_unit_id(self, unit_id):
        self._get_unit_id_tag().string = unit_id
        self._unit_id = unit_id


    def _get_building_slot_id_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_ARRAY'}).find('rec', {'type': 'CHARACTER'}, recursive=False).find_all('u', recursive=False)[3]

    def get_building_slot_id(self):
        return self._building_slot_id

    def set_building_slot_id(self, building_slot_id):
        self._get_building_slot_id_tag().string = building_slot_id
        self._building_slot_id = building_slot_id


    def _get_cabinet_id_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_ARRAY'}).find('rec', {'type': 'CHARACTER'}, recursive=False).find_all('u', recursive=False)[4]

    def get_cabinet_id(self):
        return self._cabinet_id

    def set_cabinet_id(self, cabinet_id):
        self._get_cabinet_id_tag().string = cabinet_id
        self._cabinet_id = cabinet_id


    def _get_xy_1_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_ARRAY'}).find('rec', {'type': 'CHARACTER'}, recursive=False).find('rec', {'type': 'LOCOMOTABLE'}, recursive=False).find_all('v2x', recursive=False)[0]

    def _get_xy_2_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_ARRAY'}).find('rec', {'type': 'CHARACTER'}, recursive=False).find('rec', {'type': 'LOCOMOTABLE'}, recursive=False).find_all('v2x', recursive=False)[1]

    def set_x(self, x):
        self._get_xy_1_tag()['x'] = x
        self._get_xy_2_tag()['x'] = x

    def set_y(self, y):
        self._get_xy_1_tag()['y'] = y
        self._get_xy_2_tag()['y'] = y


    def _get_traits_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_ARRAY'}).find('rec', {'type': 'CHARACTER'}, recursive=False).find('rec', {'type': 'CHARACTER_DETAILS'}, recursive=False).find('traits', recursive=False)

    def get_traits(self):
        return self._traits

    def _set_traits(self, traits):
        self._get_traits_tag().string = traits
        self._traits = traits

    def clear_traits(self):
        self._set_traits('')


    def _get_ancillaries_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_ARRAY'}).find('rec', {'type': 'CHARACTER'}, recursive=False).find('rec', {'type': 'CHARACTER_DETAILS'}, recursive=False).find('agent_ancillaries', recursive=False)

    def get_ancillaries(self):
        return self._ancillaries

    def _set_ancillaries(self, ancillaries):
        self._get_ancillaries_tag().string = ancillaries
        self._ancillaries = ancillaries

    def clear_ancillaries(self):
        self._set_ancillaries('')


    def _get_first_name_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_ARRAY'}).find('rec', {'type': 'CHARACTER'}, recursive=False).find('rec', {'type': 'CHARACTER_DETAILS'}, recursive=False).find_all('loc', recursive=False)[0]

    def get_first_name(self):
        return self._first_name

    def set_first_name(self, first_name):
        self._get_first_name_tag().string = first_name
        self._first_name = first_name


    def _get_last_name_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_ARRAY'}).find('rec', {'type': 'CHARACTER'}, recursive=False).find('rec', {'type': 'CHARACTER_DETAILS'}, recursive=False).find_all('loc', recursive=False)[1]

    def get_last_name(self):
        return self._last_name

    def set_last_name(self, last_name):
        self._get_last_name_tag().string = last_name
        self._last_name = last_name


    def _get_regnal_number_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_ARRAY'}).find('rec', {'type': 'CHARACTER'}, recursive=False).find('rec', {'type': 'CHARACTER_DETAILS'}, recursive=False).find_all('s', recursive=False)[0]

    def get_regnal_number(self):
        return self._regnal_number

    def set_regnal_number(self, regnal_number):
        self._get_regnal_number_tag().string = regnal_number
        self._regnal_number = regnal_number


    def _get_birth_date_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_ARRAY'}).find('rec', {'type': 'CHARACTER'}, recursive=False).find('rec', {'type': 'CHARACTER_DETAILS'}, recursive=False).find('date', recursive=False)

    def get_birth_date(self):
        return self._birth_date

    def set_birth_date(self, birth_date):
        self._get_birth_date_tag().string = birth_date
        self._birth_date = birth_date

    def add_years_to_age(self, years: int):
        self.set_birth_date(add_years_to_date(self.get_birth_date(), years))


    def _get_portrait_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_ARRAY'}).find('rec', {'type': 'CHARACTER'}, recursive=False).find('rec', {'type': 'CHARACTER_DETAILS'}, recursive=False).find('portrait_details', recursive=False)

    def get_portrait_card(self):
        return self._portrait_card

    def _set_portrait_card(self, card):
        self._get_portrait_tag()['card'] = card
        self._portrait_card = card

    def get_portrait_template(self):
        return self._portrait_template

    def _set_portrait_template(self, template):
        self._get_portrait_tag()['template'] = template
        self._portrait_template = template

    def get_portrait_info(self):
        return self._portrait_info

    def _set_portrait_info(self, info):
        self._get_portrait_tag()['info'] = info
        self._portrait_info = info

    def get_portrait_number(self):
        return self._portrait_number

    def _set_portrait_number(self, number):
        self._get_portrait_tag()['number'] = number
        self._portrait_number = number

    def set_portrait_culture(self, culture):
        card = self.get_portrait_card().split('/')
        info = self.get_portrait_info().split('/')
        card[2] = culture
        info[2] = culture
        card = '/'.join(card)
        info = '/'.join(info)
        self._set_portrait_card(card)
        self._set_portrait_info(info)

    def set_portrait_agent_type(self, agent_type):
        card = self.get_portrait_card().split('/')
        info = self.get_portrait_info().split('/')
        card[4] = agent_type
        info[4] = agent_type
        card = '/'.join(card)
        info = '/'.join(info)
        self._set_portrait_card(card)
        self._set_portrait_info(info)

    def set_portrait_age(self, age: Literal['young', 'old']):
        card = self.get_portrait_card().split('/')
        info = self.get_portrait_info().split('/')
        card[5] = age
        info[5] = age
        card = '/'.join(card)
        info = '/'.join(info)
        self._set_portrait_card(card)
        self._set_portrait_info(info)

    def set_portrait_number(self, number: int, faction_leader=False):
        number = str(number)
        card = self.get_portrait_card().split('/')
        info = self.get_portrait_info().split('/')
        card[-1] = f"{number.zfill(3)}.tga"
        info[-1] = f"{number.zfill(3)}.jpg"
        card = '/'.join(card)
        info = '/'.join(info)
        self._set_portrait_card(card)
        self._set_portrait_info(info)
        if faction_leader:
            self._set_portrait_number('-1')
        else:
            self._set_portrait_number(number)


    def _get_faction_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_ARRAY'}).find('rec', {'type': 'CHARACTER'}, recursive=False).find('rec', {'type': 'CHARACTER_DETAILS'}, recursive=False).find_all('s', recursive=False)[1]

    def get_faction(self):
        return self._faction

    def set_faction(self, faction):
        self._get_faction_tag().string = faction
        self._faction = faction


    def _get_details_character_id_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_ARRAY'}).find('rec', {'type': 'CHARACTER'}, recursive=False).find('rec', {'type': 'CHARACTER_DETAILS'}, recursive=False).find('u', recursive=False)

    def get_details_character_id(self):
        return self._details_character_id

    def set_details_character_id(self, details_character_id):
        self._get_details_character_id_tag().string = details_character_id
        self._details_character_id = details_character_id


    def _get_agent_onscreen_name_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_ARRAY'}).find('rec', {'type': 'CHARACTER'}, recursive=False).find('rec', {'type': 'CHARACTER_DETAILS'}, recursive=False).find_all('loc', recursive=False)[3]

    def get_agent_onscreen_name(self):
        return self._agent_onscreen_name

    def set_agent_onscreen_name(self, agent_onscreen_name):
        self._get_agent_onscreen_name_tag().string = agent_onscreen_name
        self._agent_onscreen_name = agent_onscreen_name


    def _get_agent_attributes_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_ARRAY'}).find('rec', {'type': 'CHARACTER'}, recursive=False).find('rec', {'type': 'CHARACTER_DETAILS'}, recursive=False).find('agent_attributes', recursive=False)

    def get_attribute_values(self) -> List[AttributeValue]:
        attribute_values = []
        for string in self._get_agent_attributes_tag().string.split('\n'):
            string = string.strip()
            if not string == '':
                attribute, value = string.split('=')
                attribute_values.append({'attribute': attribute, 'value': value})
        return attribute_values

    def set_agent_attribute_value(self, attribute: str, value: int):
        attribute_values = self._get_agent_attributes_tag().string
        attribute_values = re.sub(f"{attribute}=.*", f"{attribute}={value}", attribute_values)
        self._get_agent_attributes_tag().string = attribute_values

    def clear_agent_attribute_values(self):
        for attribute_value in self.get_attribute_values():
            self.set_agent_attribute_value(attribute_value['attribute'], -1)


    def _get_agent_ability_soups(self):
        return self._soup.find('rec', {'type': 'CHARACTER_ARRAY'}).find('rec', {'type': 'CHARACTER'}, recursive=False).find('rec', {'type': 'CHARACTER_DETAILS'}, recursive=False).find('ary', {'type': 'AgentAbilities'}, recursive=False).find_all('agent_ability')


    def get_agent_abilities(self) -> Dict[str, AgentAbility]:
        return self._agent_abilities

    def get_agent_ability(self, ability) -> AgentAbility:
        return self._agent_abilities.get(ability)

    def clear_agent_abilities(self):
        for ability in self._agent_abilities.values():
            ability.set_level('-1')
            ability.set_attribute('')


    def _get_v2x_tag(self):
        return self._soup.find('rec', {'type': 'CHARACTER_ARRAY'}).find('rec', {'type': 'CHARACTER'}, recursive=False).find('v2x_ary', recursive=False)

    def clear_v2x(self):
        self._get_v2x_tag().string = ''



# startpos/cai_characters/

class CaiCharacter(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._id = self._get_id_tag().string
        self._owned_indirect = self._get_owned_indirect_tag().string # Faction AI ID
        self._leader_resource_id = self._get_leader_resource_id_tag().string
        self._unit_id = self._get_unit_id_tag().string
        self._resource_id = self._get_resource_id_tag().string
        self._character_id = self._get_character_id_tag().string
        self._governor_id = self._get_governor_id_tag().string

    def __str__(self):
        return '\n'.join([
            f'id                            : {self.get_id()}',
            f'owned_indirect                : {self.get_owned_indirect()}',
            f'leader_resource_id            : {self.get_leader_resource_id()}',
            f'unit_id                       : {self.get_unit_id()}',
            f'resource_id                   : {self.get_resource_id()}',
            f'character_id                  : {self.get_character_id()}',
            f'governor_id                   : {self.get_governor_id()}'
        ])


    def _get_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_CHARACTERS'}).find('u', recursive=False)

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._get_id_tag().string = id
        self._id = id


    def _get_owned_indirect_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_CHARACTERS'}).find('owned_indirect', recursive=False)

    def get_owned_indirect(self):
        return self._owned_indirect

    def set_owned_indirect(self, owned_indirect):
        self._get_owned_indirect_tag().string = owned_indirect
        self._owned_indirect = owned_indirect


    def _get_leader_resource_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_CHARACTERS'}).find('rec', {'type': 'CAI_CHARACTER'}).find_all('u', recursive=False)[0]

    def get_leader_resource_id(self):
        return self._leader_resource_id

    def set_leader_resource_id(self, leader_resource_id):
        self._get_leader_resource_id_tag().string = leader_resource_id
        self._leader_resource_id = leader_resource_id


    def _get_unit_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_CHARACTERS'}).find('rec', {'type': 'CAI_CHARACTER'}).find_all('u', recursive=False)[1]

    def get_unit_id(self):
        return self._unit_id

    def set_unit_id(self, unit_id):
        self._get_unit_id_tag().string = unit_id
        self._unit_id = unit_id


    def _get_resource_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_CHARACTERS'}).find('rec', {'type': 'CAI_CHARACTER'}).find_all('u', recursive=False)[2]

    def get_resource_id(self):
        return self._resource_id

    def set_resource_id(self, resource_id):
        self._get_resource_id_tag().string = resource_id
        self._resource_id = resource_id


    def _get_character_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_CHARACTERS'}).find('rec', {'type': 'CAI_CHARACTER'}).find_all('u', recursive=False)[3]

    def get_character_id(self):
        return self._character_id

    def set_character_id(self, character_id):
        self._get_character_id_tag().string = character_id
        self._character_id = character_id


    def _get_governor_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_CHARACTERS'}).find('rec', {'type': 'CAI_CHARACTER'}).find_all('u', recursive=False)[4]

    def get_governor_id(self):
        return self._governor_id

    def set_governor_id(self, governor_id):
        self._get_governor_id_tag().string = governor_id
        self._governor_id = governor_id



# startpos/army/

class LandUnit:
    def __init__(self, soup: BeautifulSoup):
        self._soup = soup
        self._id = self._get_land_unit_tag().get('unit_id')
        self._commander_id = self._get_land_unit_tag().get('commander_id')
        self._commander = self._get_land_unit_tag().get('commander')
        self._commander_faction = self._commander.split(' ')[0]
        self._creation_date = self._get_land_unit_tag().get('created')
        self._deaths = self._get_land_unit_tag().get('deaths')
        self._experience = self._get_land_unit_tag().get('exp')
        self._kills = self._get_land_unit_tag().get('kills')
        self._movement_points = self._get_land_unit_tag().get('mp')
        self._name_alloc = self._get_land_unit_tag().get('name')
        self._size = self._get_land_unit_tag().get('size')
        self._type = self._get_land_unit_tag().get('type')

    def __str__(self):
        return '\n'.join([
            f'id                            : {self.get_id()}',
            f'commander_id                  : {self.get_commander_id()}',
            f'commander                     : {self.get_commander()}',
            f'commander_faction             : {self.get_commander_faction()}',
            f'creation_date                 : {self.get_creation_date()}',
            f'deaths                        : {self.get_deaths()}',
            f'experience                    : {self.get_experience()}',
            f'kills                         : {self.get_kills()}',
            f'movement_points               : {self.get_movement_points()}',
            f'name_alloc                    : {self.get_name_alloc()}',
            f'size                          : {self.get_size()}',
            f'type                          : {self.get_type()}'
        ])

    def print(self):
        print(str(self))


    def _get_land_unit_tag(self):
        return self._soup.find('land_unit', recursive=False)

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._get_land_unit_tag()['unit_id'] = id
        self._id = id

    def get_commander_id(self):
        return self._commander_id

    def set_commander_id(self, commander_id):
        self._get_land_unit_tag()['commander_id'] = commander_id
        self._commander_id = commander_id

    def get_commander(self):
        return self._commander

    def get_commander_faction(self):
        return self._commander_faction

    def _set_commander(self, commander):
        self._get_land_unit_tag()['commander'] = commander
        self._commander = commander
        self._commander_faction = commander.split(' ')[0]

    def set_commander_faction(self, faction):
        commander = self.get_commander().split(' ')
        commander[0] = faction
        commander = ' '.join(commander)
        self._set_commander(commander)

    def set_commander_first_name(self, commander_first_name):
        commander = self.get_commander().split(' ')
        commander[1] = commander_first_name
        commander = ' '.join(commander)
        self._set_commander(commander)

    def set_commander_last_name(self, commander_last_name):
        commander = self.get_commander().split(' ')
        if len(commander) >= 3:
            commander[2] = commander_last_name
        else:
            commander.append(commander_last_name)
        commander = ' '.join(commander)
        self._set_commander(commander)

    def get_creation_date(self):
        return self._creation_date

    def set_creation_date(self, creation_date):
        self._get_land_unit_tag()['created'] = creation_date
        self._creation_date = creation_date

    def add_years_to_creation_date(self, years: int):
        self.set_creation_date(add_years_to_date(self.get_creation_date(), years))

    def get_deaths(self):
        return self._deaths

    def set_deaths(self, deaths):
        self._get_land_unit_tag()['deaths'] = deaths
        self._deaths = deaths

    def get_experience(self):
        return self._experience

    def set_experience(self, experience):
        self._get_land_unit_tag()['exp'] = experience
        self._experience = experience

    def get_kills(self):
        return self._kills

    def set_kills(self, kills):
        self._get_land_unit_tag()['kills'] = kills
        self._kills = kills

    def get_movement_points(self):
        return self._movement_points

    def set_movement_points(self, movement_points):
        self._get_land_unit_tag()['mp'] = movement_points
        self._movement_points = movement_points

    def get_name_alloc(self):
        return self._name_alloc

    def set_name_alloc(self, name_alloc):
        self._get_land_unit_tag()['name'] = name_alloc
        self._name_alloc = name_alloc

    def get_size(self):
        return self._size

    def set_size(self, size):
        self._get_land_unit_tag()['size'] = size
        self._size = size

    def get_type(self):
        return self._type

    def set_type(self, type):
        self._get_land_unit_tag()['type'] = type
        self._type = type



class NavalUnit:
    def __init__(self, soup: BeautifulSoup):
        self._soup = soup
        self._id = self._get_id_tag().string
        self._commander_id = self._get_commander_id_tag().string
        self._commander = self._get_commander_tag().string
        self._creation_date = self._get_creation_date_tag().string
        self._name_alloc = self._get_name_alloc_tag().string
        self._type = self._get_type_tag().string

    def __str__(self):
        return '\n'.join([
            f'id                            : {self.get_id()}',
            f'commander_id                  : {self.get_commander_id()}',
            f'commander                     : {self.get_commander()}',
            f'creation_date                 : {self.get_creation_date()}',
            f'name_alloc                    : {self.get_name_alloc()}',
            f'type                          : {self.get_type()}'
        ])

    def print(self):
        print(str(self))


    def _get_id_tag(self):
        return self._soup.find('rec', {'type': 'NAVAL_UNIT'}).find('rec', {'type': 'UNIT'}, recursive=False).find('i', recursive=False)

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._get_id_tag().string = id
        self._id = id


    def _get_commander_id_tag(self):
        return self._soup.find('rec', {'type': 'NAVAL_UNIT'}).find('rec', {'type': 'UNIT'}, recursive=False).find_all('u', recursive=False)[4]

    def get_commander_id(self):
        return self._commander_id

    def set_commander_id(self, commander_id):
        self._get_commander_id_tag().string = commander_id
        self._commander_id = commander_id


    def _get_commander_tag(self):
        return self._soup.find('rec', {'type': 'NAVAL_UNIT'}).find('rec', {'type': 'UNIT'}, recursive=False).find('commander', recursive=False)

    def get_commander(self):
        return self._commander

    def _set_commander(self, commander):
        self._get_commander_tag().string = commander
        self._commander = commander

    def set_commander_faction(self, faction):
        commander = self.get_commander().split(' ')
        commander[0] = faction
        commander = ' '.join(commander)
        self._set_commander(commander)

    def set_commander_first_name(self, commander_first_name):
        commander = self.get_commander().split(' ')
        commander[1] = commander_first_name
        commander = ' '.join(commander)
        self._set_commander(commander)

    def set_commander_last_name(self, commander_last_name):
        commander = self.get_commander().split(' ')
        commander[2] = commander_last_name
        commander = ' '.join(commander)
        self._set_commander(commander)


    def _get_creation_date_tag(self):
        return self._soup.find('rec', {'type': 'NAVAL_UNIT'}).find('rec', {'type': 'UNIT'}, recursive=False).find('unit_history', recursive=False)

    def get_creation_date(self):
        return self._creation_date

    def set_creation_date(self, creation_date):
        self._get_creation_date_tag().string = creation_date
        self._creation_date = creation_date

    def add_years_to_creation_date(self, years: int):
        self.set_creation_date(add_years_to_date(self.get_creation_date(), years))


    def _get_name_alloc_tag(self):
        return self._soup.find('rec', {'type': 'NAVAL_UNIT'}).find('rec', {'type': 'UNIT'}, recursive=False).find('loc', recursive=False)

    def get_name_alloc(self):
        return self._name_alloc

    def set_name_alloc(self, name_alloc):
        self._get_name_alloc_tag().string = name_alloc
        self._name_alloc = name_alloc


    def _get_type_tag(self):
        return self._soup.find('rec', {'type': 'NAVAL_UNIT'}).find('rec', {'type': 'UNIT'}, recursive=False).find('unit_key', recursive=False)

    def get_type(self):
        return self._type

    def set_type(self, type):
        self._get_type_tag().string = type
        self._type = type



class Army(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._type = self._soup.find('rec', {'type': 'ARMY_ARRAY'}).find('rec', recursive=False).get('type')
        self._id = self._get_id_tag().string
        self._character_id = self._get_character_id_tag().string
        self._army_id = None
        self._building_slot_id = None
        self._besieged = None
        self._transport_fleet_id = None
        self._unknown = None
        self._transported_army_id = None
        self._land_units = {}
        self._naval_units = {}
        if self._type == 'ARMY':
            self._army_id = self._get_army_id_tag().string
            self._building_slot_id = self._get_building_slot_id_tag().string
            self._besieged = self._get_besieged_tag().name
            self._transport_fleet_id = self._get_transport_fleet_id_tag().string
            self._unknown = self._get_unknown_tag().name
            for land_unit_soup in self._get_land_unit_soups():
                land_unit = LandUnit(land_unit_soup)
                self._land_units[land_unit.get_id()] = land_unit
        if self._type == 'NAVY':
            self._transported_army_id = None
            for naval_unit_soup in self._get_naval_unit_soups():
                naval_unit = NavalUnit(naval_unit_soup)
                self._naval_units[naval_unit.get_id()] = naval_unit

    def __str__(self):
        return '\n'.join([
            f'type                          : {self.get_type()}',
            f'id                            : {self.get_id()}',
            f'character_id                  : {self.get_character_id()}',
            f'army_id                       : {self.get_army_id()}',
            f'building_slot_id              : {self.get_building_slot_id()}',
            f'besieged                      : {self.get_besieged()}',
            f'transport_fleet_id            : {self.get_transport_fleet_id()}',
            f'unknown                       : {self.get_unknown()}',
            f'transported_army_id           : {self.get_transported_army_id()}'
        ])


    def get_type(self):
        return self._type


    def _get_id_tag(self):
        return self._soup.find('rec', {'type': 'ARMY_ARRAY'}).find('rec', {'type': self._type}, recursive=False).find('rec', {'type': 'MILITARY_FORCE'}, recursive=False).find_all('u', recursive=False)[0]

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._get_id_tag().string = id
        self._id = id


    def _get_character_id_tag(self):
        return self._soup.find('rec', {'type': 'ARMY_ARRAY'}).find('rec', {'type': self._type}, recursive=False).find('rec', {'type': 'MILITARY_FORCE'}, recursive=False).find_all('u', recursive=False)[1]

    def get_character_id(self):
        return self._character_id

    def set_character_id(self, character_id):
        self._get_character_id_tag().string = character_id
        self._character_id = character_id


    def _get_army_id_tag(self):
        return self._soup.find('rec', {'type': 'ARMY_ARRAY'}).find('rec', {'type': 'ARMY'}, recursive=False).find('i', recursive=False)

    def get_army_id(self):
        return self._army_id

    def set_army_id(self, army_id):
        self._get_army_id_tag().string = army_id
        self._army_id = army_id


    def _get_building_slot_id_tag(self):
        return self._soup.find('rec', {'type': 'ARMY_ARRAY'}).find('rec', {'type': 'ARMY'}, recursive=False).find_all('u', recursive=False)[0]

    def get_building_slot_id(self):
        return self._building_slot_id

    def set_building_slot_id(self, building_slot_id):
        self._get_building_slot_id_tag().string = building_slot_id
        self._building_slot_id = building_slot_id


    def _get_besieged_tag(self):
        return self._soup.find('rec', {'type': 'ARMY_ARRAY'}).find('rec', {'type': 'ARMY'}, recursive=False).find_all(['yes', 'no'], recursive=False)[0]

    def get_besieged(self):
        return self._besieged

    def _set_besieged(self, besieged):
        self._get_besieged_tag().name = besieged
        self._besieged = besieged

    def make_besieged(self):
        self._set_besieged('yes')

    def make_non_besieged(self):
        self._set_besieged('no')


    def _get_transport_fleet_id_tag(self):
        return self._soup.find('rec', {'type': 'ARMY_ARRAY'}).find('rec', {'type': 'ARMY'}, recursive=False).find_all('u', recursive=False)[1]

    def get_transport_fleet_id(self):
        return self._transport_fleet_id

    def set_transport_fleet_id(self, transport_fleet_id):
        self._get_transport_fleet_id_tag().string = transport_fleet_id
        self._transport_fleet_id = transport_fleet_id


    def _get_unknown_tag(self):
        return self._soup.find('rec', {'type': 'ARMY_ARRAY'}).find('rec', {'type': 'ARMY'}, recursive=False).find_all(['yes', 'no'], recursive=False)[1]

    def get_unknown(self):
        return self._unknown

    def set_unknown(self, unknown):
        self._get_unknown_tag().name = unknown
        self._unknown = unknown


    def _get_transported_army_id_tag(self):
        return self._soup.find('rec', {'type': 'ARMY_ARRAY'}).find('rec', {'type': 'NAVY'}, recursive=False).find('rec', {'type': 'NAVY'}, recursive=False).find_all('u', recursive=False)[0]

    def get_transported_army_id(self):
        return self._transported_army_id

    def set_transported_army_id(self, transported_army_id):
        self._get_transported_army_id_tag().string = transported_army_id
        self._transported_army_id = transported_army_id


    def _get_land_unit_soups(self):
        return self._soup.find('rec', {'type': 'ARMY_ARRAY'}).find('rec', {'type': 'ARMY'}, recursive=False).find('ary', {'type': 'UNITS_ARRAY'}, recursive=False).find_all('rec', {'type': 'UNITS_ARRAY'}, recursive=False)

    def get_land_units(self) -> List[LandUnit]:
        return list(self._land_units.values())

    def get_land_unit(self, id) -> LandUnit:
        return self._land_units.get(id)

    def add_land_unit(self, post_soup):
        self._soup.find('rec', {'type': 'ARMY_ARRAY'}).find('rec', {'type': 'ARMY'}, recursive=False).find('ary', {'type': 'UNITS_ARRAY'}, recursive=False).append(post_soup)


    def _get_naval_unit_soups(self):
        return self._soup.find('rec', {'type': 'ARMY_ARRAY'}).find('rec', {'type': 'NAVY'}, recursive=False).find('ary', {'type': 'UNITS_ARRAY'}, recursive=False).find_all('rec', {'type': 'UNITS_ARRAY'}, recursive=False)

    def get_naval_units(self) -> List[NavalUnit]:
        return list(self._naval_units.values())

    def get_naval_unit(self, id) -> NavalUnit:
        return self._naval_units.get(id)



# startpos/cai_mobiles/

class CaiMobile(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._id = self._get_id_tag().string
        self._owned_direct = self._get_owned_direct_tag().string # Faction AI ID
        self._region_id = self._get_cai_situated_tag().get('region_id')
        self._character_id = self._get_character_id_tag().string
        self._settlement_id = self._get_settlement_id_tag().string
        self._settlement_character_id = self._get_settlement_character_id_tag().string
        self._character_ids = self._get_character_ids_tag().string
        self._unit_ids = self._get_unit_ids_tag().string
        self._army_id = self._get_army_id_tag().string

    def __str__(self):
        return '\n'.join([
            f'id                            : {self.get_id()}',
            f'owned_direct                  : {self.get_owned_direct()}',
            f'character_id                  : {self.get_character_id()}',
            f'settlement_id                 : {self.get_settlement_id()}',
            f'settlement_character_id       : {self.get_settlement_character_id()}',
            f'character_ids                 : {self.get_character_ids()}',
            f'unit_ids                      : {self.get_unit_ids()}',
            f'army_id                       : {self.get_army_id()}'
        ])


    def _get_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_RESOURCE_MOBILES'}).find('u', recursive=False)

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._get_id_tag().string = id
        self._id = id


    def _get_owned_direct_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_RESOURCE_MOBILES'}).find('owned_direct', recursive=False)

    def get_owned_direct(self):
        return self._owned_direct

    def set_owned_direct(self, owned_direct):
        self._get_owned_direct_tag().string = owned_direct
        self._owned_direct = owned_direct


    def _get_cai_situated_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_RESOURCE_MOBILES'}).find('cai_situated', recursive=False)

    def set_x(self, x):
        self._get_cai_situated_tag()['x'] = x

    def set_y(self, y):
        self._get_cai_situated_tag()['y'] = y

    def get_region_id(self):
        return self._region_id

    def set_region_id(self, region_id):
        self._get_cai_situated_tag()['region_id'] = region_id
        self._region_id = region_id

    def set_theatre_id(self, theatre_id):
        self._get_cai_situated_tag()['theatre_id'] = theatre_id

    def set_area_id(self, area_id):
        self._get_cai_situated_tag()['area_id'] = area_id


    def _get_character_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_RESOURCE_MOBILES'}).find('rec', {'type': 'CAI_RESOURCE_MOBILE'}).find_all('u', recursive=False)[0]

    def get_character_id(self):
        return self._character_id

    def set_character_id(self, character_id):
        self._get_character_id_tag().string = character_id
        self._character_id = character_id


    def _get_settlement_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_RESOURCE_MOBILES'}).find('rec', {'type': 'CAI_RESOURCE_MOBILE'}).find_all('u', recursive=False)[1]

    def get_settlement_id(self):
        return self._settlement_id

    def set_settlement_id(self, settlement_id):
        self._get_settlement_id_tag().string = settlement_id
        self._settlement_id = settlement_id


    def _get_settlement_character_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_RESOURCE_MOBILES'}).find('rec', {'type': 'CAI_RESOURCE_MOBILE'}).find_all('u', recursive=False)[2]

    def get_settlement_character_id(self):
        return self._settlement_character_id

    def set_settlement_character_id(self, settlement_character_id):
        self._get_settlement_character_id_tag().string = settlement_character_id
        self._settlement_character_id = settlement_character_id


    def _get_army_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_RESOURCE_MOBILES'}).find('rec', {'type': 'CAI_RESOURCE_MOBILE'}).find_all('u', recursive=False)[4]

    def get_army_id(self):
        return self._army_id

    def set_army_id(self, army_id):
        self._get_army_id_tag().string = army_id
        self._army_id = army_id


    def _get_character_ids_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_RESOURCE_MOBILES'}).find('rec', {'type': 'CAI_RESOURCE_MOBILE'}).find_all('u4_ary', recursive=False)[0]

    def get_character_ids(self):
        return self._character_ids

    def remove_character_id(self, character_id):
        remove_id_from_tag_string(self._get_character_ids_tag(), character_id)
        self._character_ids = self._get_character_ids_tag().string

    def add_character_id(self, character_id):
        append_id_to_tag_string(self._get_character_ids_tag(), character_id, sort=False)
        self._character_ids = self._get_character_ids_tag().string


    def _get_unit_ids_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_RESOURCE_MOBILES'}).find('rec', {'type': 'CAI_RESOURCE_MOBILE'}).find_all('u4_ary', recursive=False)[1]

    def get_unit_ids(self):
        return self._unit_ids

    def remove_unit_id(self, unit_id):
        remove_id_from_tag_string(self._get_unit_ids_tag(), unit_id)
        self._unit_ids = self._get_unit_ids_tag().string

    def add_unit_id(self, unit_id):
        append_id_to_tag_string(self._get_unit_ids_tag(), unit_id, sort=False)
        self._unit_ids = self._get_unit_ids_tag().string


    def _get_bdi_blocks_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_RESOURCE_MOBILES'}).find('ary', {'type': 'CAI_BDI_COMPONENT_BLOCK_OWNS'}, recursive=False)

    def _get_bdi_1_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_RESOURCE_MOBILES'}).find_all('u4_ary', recursive=False)[1]

    def _get_bdi_3_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_RESOURCE_MOBILES'}).find_all('u4_ary', recursive=False)[3]

    def _get_bdi_4_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_RESOURCE_MOBILES'}).find_all('u4_ary', recursive=False)[4]

    def _get_bdi_7_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_RESOURCE_MOBILES'}).find_all('u4_ary', recursive=False)[7]

    def clear_bdi(self):
        self._get_bdi_blocks_tag().string = ''
        self._get_bdi_1_tag().string = ''
        self._get_bdi_3_tag().string = ''
        self._get_bdi_4_tag().string = ''
        self._get_bdi_7_tag().string = ''



# startpos/cai_units/

class CaiUnit(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._id = self._get_id_tag().string
        self._character_id = self._get_character_id_tag().string
        self._unit_id = self._get_unit_id_tag().string
        self._character_resource_id = self._get_character_resource_id_tag().string

    def __str__(self):
        return '\n'.join([
            f'id                            : {self.get_id()}',
            f'character_id                  : {self.get_character_id()}',
            f'unit_id                       : {self.get_unit_id()}',
            f'character_resource_id         : {self.get_character_resource_id()}'
        ])


    def _get_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_UNITS'}).find('u', recursive=False)

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._get_id_tag().string = id
        self._id = id


    def _get_character_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_UNITS'}).find('rec', {'type': 'CAI_UNIT'}).find_all('u', recursive=False)[0]

    def get_character_id(self):
        return self._character_id

    def set_character_id(self, character_id):
        self._get_character_id_tag().string = character_id
        self._character_id = character_id


    def _get_unit_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_UNITS'}).find('rec', {'type': 'CAI_UNIT'}).find_all('u', recursive=False)[1]

    def get_unit_id(self):
        return self._unit_id

    def set_unit_id(self, unit_id):
        self._get_unit_id_tag().string = unit_id
        self._unit_id = unit_id


    def _get_character_resource_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_UNITS'}).find('rec', {'type': 'CAI_UNIT'}).find_all('u', recursive=False)[2]

    def get_character_resource_id(self):
        return self._character_resource_id

    def set_character_resource_id(self, character_resource_id):
        self._get_character_resource_id_tag().string = character_resource_id
        self._character_resource_id = character_resource_id



# startpos/diplomacy/

class Attitude(EsfXmlSoup):
    def __init__(self, soup: BeautifulSoup):
        self._soup = soup
        self._drift = self._soup.get('drift')
        self._current = self._soup.get('current')
        self._limit = self._soup.get('limit')
        self._active1 = self._soup.get('active1')
        self._extra = self._soup.get('extra')
        self._active2 = self._soup.get('active2')

    def __str__(self):
        return '\n'.join([
            f'drift                         : {self.get_drift()}',
            f'current                       : {self.get_current()}',
            f'limit                         : {self.get_limit()}',
            f'active1                       : {self.get_active1()}',
            f'extra                         : {self.get_extra()}',
            f'active2                       : {self.get_active2()}'
        ])

    def print(self):
        print(str(self))


    def get_drift(self):
        return self._drift

    def set_drift(self, drift):
        self._soup['drift'] = drift
        self._drift = drift

    def get_current(self):
        return self._current

    def set_current(self, current):
        self._soup['current'] = current
        self._current = current

    def get_limit(self):
        return self._limit

    def set_limit(self, limit):
        self._soup['limit'] = limit
        self._limit = limit

    def get_active1(self):
        return self._active1

    def set_active1(self, active1):
        self._soup['active1'] = active1
        self._active1 = active1

    def get_extra(self):
        return self._extra

    def set_extra(self, extra):
        self._soup['extra'] = extra
        self._extra = extra

    def get_active2(self):
        return self._active2

    def set_active2(self, active2):
        self._soup['active2'] = active2
        self._active2 = active2

    def clear(self):
        for attribute in ['drift', 'current', 'limit', 'active1', 'extra', 'active2']:
            if self._soup.has_attr(attribute):
                del self._soup[attribute]
        self._drift = None
        self._current = None
        self._limit = None
        self._active1 = None
        self._extra = None
        self._active2 = None



class Relationship(EsfXmlSoup):
    _supported_relationships = Literal['neutral', 'allied', 'war', 'protectorate', 'patron']
    
    def __init__(self, soup: BeautifulSoup):
        self._soup = soup
        self._faction_id = self._get_faction_id_tag().string
        self._trading = self._get_trading_tag().name
        self._military_access_turns = self._get_military_access_turns_tag().string
        self._relationship = self._get_relationship_tag().string
        self._if_allied_20 = self._get_if_allied_20_tag().string
        self._payment_to_patron = self._get_payment_to_patron_tag().string
        self._income_from_protectorate = self._get_income_from_protectorate_tag().string
        self._if_allied_10 = self._get_if_allied_10_tag().string
        self._relationship_with_protectorate = self._get_relationship_with_protectorate_tag().string
        self._overall_attitude = self._get_overall_attitude_tag().string
        self._trading_2 = self._get_trading_2_tag().name
        self._attitudes = []
        for attitude_soup in self._get_attitudes_soups():
            attitude = Attitude(attitude_soup)
            self._attitudes.append(attitude)

    def __str__(self):
        return '\n'.join([
            f'faction_id                    : {self.get_faction_id()}',
            f'trading                       : {self.get_trading()}',
            f'military_access_turns         : {self.get_military_access_turns()}',
            f'relationship                  : {self.get_relationship()}',
            f'if_allied_20                  : {self.get_if_allied_20()}',
            f'payment_to_patron             : {self.get_payment_to_patron()}',
            f'income_from_protectorate      : {self.get_income_from_protectorate()}',
            f'if_allied_10                  : {self.get_if_allied_10()}',
            f'relationship_with_protectorate: {self.get_relationship_with_protectorate()}',
            f'overall_attitude              : {self.get_overall_attitude()}',
            f'trading_2                     : {self.get_trading_2()}'
        ])

    def print(self):
        print(str(self))


    def _get_faction_id_tag(self):
        return self._soup.find('rec', {'type': 'DIPLOMACY_RELATIONSHIP'}, recursive=False).find('i', recursive=False)

    def get_faction_id(self):
        return self._faction_id

    def set_faction_id(self, faction_id):
        self._get_faction_id_tag().string = faction_id
        self._faction_id = faction_id


    def _get_trading_tag(self):
        return self._soup.find('rec', {'type': 'DIPLOMACY_RELATIONSHIP'}, recursive=False).find(['yes', 'no'], recursive=False)

    def get_trading(self):
        return self._trading

    def _set_trading(self, trading):
        self._get_trading_tag().name = trading
        self._trading = trading

    def make_trading(self):
        self._set_trading('yes')

    def make_non_trading(self):
        self._set_trading('no')


    def _get_military_access_turns_tag(self):
        return self._soup.find('rec', {'type': 'DIPLOMACY_RELATIONSHIP'}, recursive=False).find_all('i', recursive=False)[1]

    def get_military_access_turns(self):
        return self._military_access_turns

    def set_military_access_turns(self, military_access_turns):
        self._get_military_access_turns_tag().string = military_access_turns
        self._military_access_turns = military_access_turns


    def _get_relationship_tag(self):
        return self._soup.find('rec', {'type': 'DIPLOMACY_RELATIONSHIP'}, recursive=False).find('s', recursive=False)

    def get_relationship(self) -> _supported_relationships:
        return self._relationship

    def set_relationship(self, relationship: _supported_relationships):
        assert relationship in get_args(self._supported_relationships), f"'{relationship}' relationship is not supported."
        self._get_relationship_tag().string = relationship
        self._relationship = relationship


    def _get_if_allied_20_tag(self):
        return self._soup.find('rec', {'type': 'DIPLOMACY_RELATIONSHIP'}, recursive=False).find_all('u', recursive=False)[0]

    def get_if_allied_20(self):
        return self._if_allied_20

    def set_if_allied_20(self, if_allied_20):
        self._get_if_allied_20_tag().string = if_allied_20
        self._if_allied_20 = if_allied_20


    def _get_payment_to_patron_tag(self):
        return self._soup.find('rec', {'type': 'DIPLOMACY_RELATIONSHIP'}, recursive=False).find_all('i', recursive=False)[4]

    def get_payment_to_patron(self):
        return self._payment_to_patron

    def set_payment_to_patron(self, payment_to_patron):
        self._get_payment_to_patron_tag().string = payment_to_patron
        self._payment_to_patron = payment_to_patron


    def _get_income_from_protectorate_tag(self):
        return self._soup.find('rec', {'type': 'DIPLOMACY_RELATIONSHIP'}, recursive=False).find_all('i', recursive=False)[5]

    def get_income_from_protectorate(self):
        return self._income_from_protectorate

    def set_income_from_protectorate(self, income_from_protectorate):
        self._get_income_from_protectorate_tag().string = income_from_protectorate
        self._income_from_protectorate = income_from_protectorate


    def _get_if_allied_10_tag(self):
        return self._soup.find('rec', {'type': 'DIPLOMACY_RELATIONSHIP'}, recursive=False).find_all('u', recursive=False)[3]

    def get_if_allied_10(self):
        return self._if_allied_10

    def set_if_allied_10(self, if_allied_10):
        self._get_if_allied_10_tag().string = if_allied_10
        self._if_allied_10 = if_allied_10


    def _get_relationship_with_protectorate_tag(self):
        return self._soup.find('rec', {'type': 'DIPLOMACY_RELATIONSHIP'}, recursive=False).find_all('s', recursive=False)[1]

    def get_relationship_with_protectorate(self) -> _supported_relationships:
        return self._relationship_with_protectorate

    def set_relationship_with_protectorate(self, relationship_with_protectorate: _supported_relationships):
        assert relationship_with_protectorate in get_args(self._supported_relationships), f"'{relationship_with_protectorate}' relationship is not supported."
        self._get_relationship_with_protectorate_tag().string = relationship_with_protectorate
        self._relationship_with_protectorate = relationship_with_protectorate


    def _get_overall_attitude_tag(self):
        return self._soup.find('rec', {'type': 'DIPLOMACY_RELATIONSHIP'}, recursive=False).find_all('i', recursive=False)[8]

    def get_overall_attitude(self):
        return self._overall_attitude

    def set_overall_attitude(self, overall_attitude):
        self._get_overall_attitude_tag().string = overall_attitude
        self._overall_attitude = overall_attitude

    def update_overall_attitude(self):
        current_total = self.get_current_total()
        overall_attitude = str(get_diplomatic_relations_attitude(current_total))
        self.set_overall_attitude(overall_attitude)


    def _get_trading_2_tag(self):
        return self._soup.find('rec', {'type': 'DIPLOMACY_RELATIONSHIP'}, recursive=False).find_all(['yes', 'no'], recursive=False)[2]

    def get_trading_2(self):
        return self._trading_2

    def _set_trading_2(self, trading_2):
        self._get_trading_2_tag().name = trading_2
        self._trading_2 = trading_2

    def make_trading_2(self):
        self._set_trading_2('yes')

    def make_non_trading_2(self):
        self._set_trading_2('no')


    def _get_attitudes_soups(self):
        return self._soup.find('rec', {'type': 'DIPLOMACY_RELATIONSHIP'}) \
            .find('ary', {'type': 'DIPLOMACY_RELATIONSHIP_ATTITUDES_ARRAY'}, recursive=False) \
            .find_all('draa', recursive=False)


    def get_attitudes(self) -> List[Attitude]:
        return self._attitudes

    def get_current_total(self):
        return sum([int(attitude.get_current()) for attitude in self._attitudes if attitude.get_current()])



class Diplomacy(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._unknown_1 = self._get_unknown_1_tag().string
        self._unknown_2 = self._get_unknown_2_tag().string
        self._unknown_3 = self._get_unknown_3_tag().string
        self._relationships = {}
        for relationship_soup in self._get_relationship_soups():
            relationship = Relationship(relationship_soup)
            self._relationships[relationship.get_faction_id()] = relationship

    def __str__(self):
        return '\n'.join([
            f'unknown_1                     : {self.get_unknown_1()}',
            f'unknown_2                     : {self.get_unknown_2()}',
            f'unknown_3                     : {self.get_unknown_3()}'
        ])


    def _get_unknown_1_tag(self):
        return self._soup.find('rec', {'type': 'DIPLOMACY_MANAGER'}).find_all('u', recursive=False)[0]

    def get_unknown_1(self):
        return self._unknown_1

    def set_unknown_1(self, unknown_1):
        self._get_unknown_1_tag().string = unknown_1
        self._unknown_1 = unknown_1


    def _get_unknown_2_tag(self):
        return self._soup.find('rec', {'type': 'DIPLOMACY_MANAGER'}).find_all('u', recursive=False)[1]

    def get_unknown_2(self):
        return self._unknown_2

    def set_unknown_2(self, unknown_2):
        self._get_unknown_2_tag().string = unknown_2
        self._unknown_2 = unknown_2


    def _get_unknown_3_tag(self):
        return self._soup.find('rec', {'type': 'DIPLOMACY_MANAGER'}).find_all('u', recursive=False)[2]

    def get_unknown_3(self):
        return self._unknown_3

    def set_unknown_3(self, unknown_3):
        self._get_unknown_3_tag().string = unknown_3
        self._unknown_3 = unknown_3


    def _get_relationship_soups(self):
        return self._soup.find('rec', {'type': 'DIPLOMACY_MANAGER'}) \
            .find('ary', {'type': 'DIPLOMACY_RELATIONSHIPS_ARRAY'}, recursive=False) \
            .find_all('rec', {'type': 'DIPLOMACY_RELATIONSHIPS_ARRAY'}, recursive=False)


    def get_relationships(self) -> List[Relationship]:
        return list(self._relationships.values())

    def get_relationship(self, faction_id) -> Relationship:
        return self._relationships.get(faction_id)



# startpos/region/

class Region(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._id = self._get_id_tag().string
        self._name = self._get_name_tag().string
        self._population_path = get_base_name_from_path(self._get_population_path_tag().get('path'))
        self._settlement_slot_path = get_base_name_from_path(self._get_settlement_slot_path_tag().get('path'))
        self._region_slot_paths = [get_base_name_from_path(region_slot_soup.get('path')) for region_slot_soup in self._get_region_slot_soups()]
        self._road_walls_paths = [get_base_name_from_path(road_walls_soup.get('path')) for road_walls_soup in self._get_road_walls_soups()]
        self._faction_id = self._get_faction_id_tag().string
        self._governor_id = self._get_governor_id_tag().string
        self._theatre = self._get_theatre_tag().string
        self._emergent_faction = self._get_emergent_faction_tag().string
        self._rebels_on_screen_name = self._get_rebels_on_screen_name_tag().string
        self._subculture = self._get_subculture_tag().string
        self._recruitment_id = self._get_recruitment_id_tag().string
        self._fort_paths = [get_base_name_from_path(fort_soup.get('path')) for fort_soup in self._get_fort_soups()]
        self._resources = [resource.strip() for resource in self._get_resources_array_tag().string.split('\n')[1:-1]]

    def __str__(self):
        return '\n'.join([
            f'id                            : {self.get_id()}',
            f'name                          : {self.get_name()}',
            f'population                    : {self.get_population_path()}',
            f'settlement_slot_path          : {self.get_settlement_slot_path()}',
            f'faction_id                    : {self.get_faction_id()}',
            f'governor_id                   : {self.get_governor_id()}',
            f'theatre                       : {self.get_theatre()}',
            f'emergent_faction              : {self.get_emergent_faction()}',
            f'rebels_on_screen_name         : {self.get_rebels_on_screen_name()}',
            f'subculture                    : {self.get_subculture()}',
            f'recruitment_id                : {self.get_recruitment_id()}'
        ])


    def _get_id_tag(self):
        return self._soup.find('rec', {'type': 'REGION'}).find('i', recursive=False)

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._get_id_tag().string = id
        self._id = id


    def _get_name_tag(self):
        return self._soup.find('rec', {'type': 'REGION'}).find('s', recursive=False)

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._get_name_tag().string = name
        self._name = name


    def _get_population_path_tag(self):
        return self._soup.find('rec', {'type': 'REGION'}).find_all('xml_include', recursive=False)[0]

    def get_population_path(self):
        return self._population_path

    def set_population_path(self, population_path):
        self._get_population_path_tag()['path'] = 'population/' + population_path
        self._population_path = population_path


    def _get_settlement_slot_path_tag(self):
        return self._soup.find('rec', {'type': 'REGION'}).find_all('xml_include', recursive=False)[1]

    def get_settlement_slot_path(self):
        return self._settlement_slot_path

    def set_settlement_slot_path(self, settlement_slot_path):
        self._get_settlement_slot_path_tag()['path'] = 'region_slot/' + settlement_slot_path
        self._settlement_slot_path = settlement_slot_path


    def _get_region_slot_array_tag(self):
        return self._soup.find('rec', {'type': 'REGION'}).find('rec', {'type': 'REGION_SLOT_MANAGER'}, recursive=False).find('ary', {'type': 'REGION_SLOT_ARRAY'}, recursive=False)

    def _get_region_slot_soups(self) -> List[BeautifulSoup]:
        return self._get_region_slot_array_tag().find_all('xml_include', recursive=False)

    def get_region_slot_paths(self):
        return self._region_slot_paths

    def remove_region_slot_path(self, path):
        self._get_region_slot_array_tag().find('xml_include', {'path': 'region_slot/' + path}, recursive=False).decompose()
        self._region_slot_paths.remove(path)

    def add_region_slot_path(self, path):
        insert_tag(self._get_region_slot_array_tag(), 'xml_include', self._soup.new_tag('xml_include', attrs={'path': 'region_slot/' + path}), 2)
        self._region_slot_paths.append(path)


    def _get_road_walls_tag(self):
        return self._soup.find('rec', {'type': 'REGION'}).find('rec', {'type': 'REGION_SLOT_MANAGER'}, recursive=False)

    def _get_road_walls_soups(self) -> List[BeautifulSoup]:
        return self._get_road_walls_tag().find_all('xml_include', recursive=False)

    def get_road_walls_paths(self):
        return self._road_walls_paths

    def remove_road_walls_path(self, path):
        self._get_road_walls_tag().find('xml_include', {'path': 'region_slot/' + path}, recursive=False).decompose()
        self._road_walls_paths.remove(path)

    def add_road_walls_path(self, path):
        insert_tag(self._get_road_walls_tag(), 'xml_include', self._soup.new_tag('xml_include', attrs={'path': 'region_slot/' + path}), 2)
        self._road_walls_paths.append(path)


    def _get_fort_array_tag(self):
        return self._soup.find('rec', {'type': 'REGION'}).find('ary', {'type': 'FORT_ARRAY'}, recursive=False)

    def _get_fort_soups(self) -> List[BeautifulSoup]:
        return self._get_fort_array_tag().find_all('xml_include', recursive=False)

    def get_fort_paths(self):
        return self._fort_paths


    def _get_faction_id_tag(self):
        return self._soup.find('rec', {'type': 'REGION'}).find_all('u', recursive=False)[9]

    def get_faction_id(self):
        return self._faction_id

    def set_faction_id(self, faction_id):
        self._get_faction_id_tag().string = faction_id
        self._faction_id = faction_id


    def _get_governor_id_tag(self):
        return self._soup.find('rec', {'type': 'REGION'}).find_all('u', recursive=False)[10]

    def get_governor_id(self):
        return self._governor_id

    def set_governor_id(self, governor_id):
        self._get_governor_id_tag().string = governor_id
        self._governor_id = governor_id


    def _get_theatre_tag(self):
        return self._soup.find('rec', {'type': 'REGION'}).find_all('s', recursive=False)[1]

    def get_theatre(self):
        return self._theatre

    def set_theatre(self, theatre):
        self._get_theatre_tag().string = theatre
        self._theatre = theatre


    def _get_emergent_faction_tag(self):
        return self._soup.find('rec', {'type': 'REGION'}).find_all('s', recursive=False)[2]

    def get_emergent_faction(self):
        return self._emergent_faction

    def set_emergent_faction(self, emergent_faction):
        self._get_emergent_faction_tag().string = emergent_faction
        self._emergent_faction = emergent_faction


    def _get_rebels_on_screen_name_tag(self):
        return self._soup.find('rec', {'type': 'REGION'}).find_all('s', recursive=False)[3]

    def get_rebels_on_screen_name(self):
        return self._rebels_on_screen_name

    def set_rebels_on_screen_name(self, rebels_on_screen_name):
        self._get_rebels_on_screen_name_tag().string = rebels_on_screen_name
        self._rebels_on_screen_name = rebels_on_screen_name


    def _get_subculture_tag(self):
        return self._soup.find('rec', {'type': 'REGION'}).find_all('s', recursive=False)[4]

    def get_subculture(self):
        return self._subculture

    def set_subculture(self, subculture):
        self._get_subculture_tag().string = subculture
        self._subculture = subculture


    def _get_recruitment_id_tag(self):
        return self._soup.find('rec', {'type': 'REGION'}).find('rec', {'type': 'REGION_RECRUITMENT_MANAGER'}, recursive=False).find('i', recursive=False)

    def get_recruitment_id(self):
        return self._recruitment_id

    def set_recruitment_id(self, recruitment_id):
        self._get_recruitment_id_tag().string = recruitment_id
        self._recruitment_id = recruitment_id


    def _get_resources_array_tag(self):
        return self._soup.find('rec', {'type': 'REGION'}).find('resources_array', recursive=False)

    def _set_resources_array(self, resources_array):
        self._get_resources_array_tag().string = resources_array

    def get_resources(self):
        return self._resources

    def add_resource(self, resource):
        assert resource not in self._resources, f"'{resource}' unit resource is already present in '{self._read_xml_path}'."
        self._resources.append(resource)
        string = '\n  ' + '\n  '.join(self._resources) + '\n '
        self._get_resources_array_tag().string = string

    def remove_resource(self, resource):
        assert resource in self._resources, f"'{resource}' unit resource is not present in '{self._read_xml_path}'."
        self._resources.remove(resource)
        string = '\n  ' + '\n  '.join(self._resources) + '\n ' if len(self._resources) >= 1 else ''
        self._get_resources_array_tag().string = string



# startpos/cai_regions/

class CaiRegion(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._id = self._get_id_tag().string
        self._owned_indirect = self._get_owned_indirect_tag().string
        self._theatre_ids = self._get_theatre_ids_tag().string
        self._hlcis_ids = self._get_hlcis_ids_tag().string
        self._settlement_id = self._get_settlement_id_tag().string
        self._region_slot_ids = self._get_region_slot_ids_tag().string
        self._character_resource_ids = self._get_character_resource_ids_tag().string
        self._name = self._get_name_tag().string
        self._region_id = self._get_region_id_tag().string
        self._governor_id = self._get_governor_id_tag().string
        self._faction_ids = self._get_faction_ids_tag().string

    def __str__(self):
        return '\n'.join([
            f'id                            : {self.get_id()}',
            f'owned_indirect                : {self.get_owned_indirect()}',
            f'theatre_ids                   : {self.get_theatre_ids()}',
            f'settlement_id                 : {self.get_settlement_id()}',
            f'hlcis_ids                     : {self.get_hlcis_ids()}',
            f'region_slot_ids               : {self.get_region_slot_ids()}',
            f'character_resource_ids        : {self.get_character_resource_ids()}',
            f'name                          : {self.get_name()}',
            f'region_id                     : {self.get_region_id()}',
            f'governor_id                   : {self.get_governor_id()}',
            f'faction_ids                   : {self.get_faction_ids()}'
        ])


    def _get_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_REGIONS'}).find('u', recursive=False)

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._get_id_tag().string = id
        self._id = id


    def _get_owned_indirect_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_REGIONS'}).find('owned_indirect', recursive=False)

    def get_owned_indirect(self):
        return self._owned_indirect

    def set_owned_indirect(self, owned_indirect):
        self._get_owned_indirect_tag().string = owned_indirect
        self._owned_indirect = owned_indirect


    def _get_theatre_ids_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_REGIONS'}).find('rec', {'type': 'CAI_REGION'}, recursive=False).find_all('u4_ary', recursive=False)[0]

    def get_theatre_ids(self):
        return self._theatre_ids

    def remove_theatre_id(self, theatre_id):
        remove_id_from_tag_string(self._get_theatre_ids_tag(), theatre_id)
        self._theatre_ids = self._get_theatre_ids_tag().string

    def add_theatre_id(self, theatre_id):
        append_id_to_tag_string(self._get_theatre_ids_tag(), theatre_id, sort=False)
        self._theatre_ids = self._get_theatre_ids_tag().string


    def _get_hlcis_ids_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_REGIONS'}).find('rec', {'type': 'CAI_REGION'}, recursive=False).find_all('u4_ary', recursive=False)[1]

    def get_hlcis_ids(self):
        return self._hlcis_ids

    def remove_hlcis_id(self, hlcis_id):
        remove_id_from_tag_string(self._get_hlcis_ids_tag(), hlcis_id)
        self._hlcis_ids = self._get_hlcis_ids_tag().string

    def add_hlcis_id(self, hlcis_id):
        append_id_to_tag_string(self._get_hlcis_ids_tag(), hlcis_id, sort=False)
        self._hlcis_ids = self._get_hlcis_ids_tag().string


    def _get_settlement_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_REGIONS'}).find('rec', {'type': 'CAI_REGION'}, recursive=False).find_all('u', recursive=False)[0]

    def get_settlement_id(self):
        return self._settlement_id

    def set_settlement_id(self, settlement_id):
        self._get_settlement_id_tag().string = settlement_id
        self._settlement_id = settlement_id


    def _get_region_slot_ids_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_REGIONS'}).find('rec', {'type': 'CAI_REGION'}, recursive=False).find_all('u4_ary', recursive=False)[2]

    def get_region_slot_ids(self):
        return self._region_slot_ids

    def remove_region_slot_id(self, region_slot_id):
        remove_id_from_tag_string(self._get_region_slot_ids_tag(), region_slot_id)
        self._region_slot_ids = self._get_region_slot_ids_tag().string

    def add_region_slot_id(self, region_slot_id):
        append_id_to_tag_string(self._get_region_slot_ids_tag(), region_slot_id)
        self._region_slot_ids = self._get_region_slot_ids_tag().string


    def _get_character_resource_ids_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_REGIONS'}).find('rec', {'type': 'CAI_REGION'}, recursive=False).find_all('u4_ary', recursive=False)[5]

    def get_character_resource_ids(self):
        return self._character_resource_ids

    def remove_character_resource_id(self, character_resource_id):
        remove_id_from_tag_string(self._get_character_resource_ids_tag(), character_resource_id)
        self._character_resource_ids = self._get_character_resource_ids_tag().string

    def add_character_resource_id(self, character_resource_id):
        append_id_to_tag_string(self._get_character_resource_ids_tag(), character_resource_id)
        self._character_resource_ids = self._get_character_resource_ids_tag().string


    def _get_name_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_REGIONS'}).find('rec', {'type': 'CAI_REGION'}, recursive=False).find('s', recursive=False)

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._get_name_tag().string = name
        self._name = name


    def _get_region_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_REGIONS'}).find('rec', {'type': 'CAI_REGION'}, recursive=False).find_all('u', recursive=False)[1]

    def get_region_id(self):
        return self._region_id

    def set_region_id(self, region_id):
        self._get_region_id_tag().string = region_id
        self._region_id = region_id


    def _get_governor_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_REGIONS'}).find('rec', {'type': 'CAI_REGION'}, recursive=False).find_all('u', recursive=False)[2]

    def get_governor_id(self):
        return self._governor_id

    def set_governor_id(self, governor_id):
        self._get_governor_id_tag().string = governor_id
        self._governor_id = governor_id


    def _get_faction_ids_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_REGIONS'}).find('rec', {'type': 'CAI_REGION'}, recursive=False).find_all('u4_ary', recursive=False)[6]

    def get_faction_ids(self):
        return self._faction_ids

    def remove_faction_id(self, faction_id):
        remove_id_from_tag_string(self._get_faction_ids_tag(), faction_id)
        self._faction_ids = self._get_faction_ids_tag().string

    def add_faction_id(self, faction_id):
        append_id_to_tag_string(self._get_faction_ids_tag(), faction_id)
        self._faction_ids = self._get_faction_ids_tag().string



# startpos/population/

class PopulationClass:
    supported_classes = Literal['lower', 'middle', 'upper']

    def __init__(self, element: etree._Element):
        self._element = element

    @property
    def social_class(self) -> supported_classes:
        return self._element.attrib['Social_Class']

    @social_class.setter
    def social_class(self, value: supported_classes):
        self._element.attrib['Social_Class'] = value

    @property
    def turns_rioting(self) -> int:
        return int(self._element.attrib['Turns_Rioting'])

    @turns_rioting.setter
    def turns_rioting(self, value: int):
        self._element.attrib['Turns_Rioting'] = str(value)

    @property
    def resistance_to_foreign_occupation(self) -> int:
        return int(self._element.attrib['Resistance_To_Foreign_Occupation'])

    @resistance_to_foreign_occupation.setter
    def resistance_to_foreign_occupation(self, value: int):
        self._element.attrib['Resistance_To_Foreign_Occupation'] = str(value)



class Population(EsfXmlEtree):
    class ReligiousBreakdown(TypedDict):
        religion: VANILLA_RELIGION_KEY_HINTS
        population_percentage: float

    def __init__(self, read_xml_path: os.PathLike, write_xml_path: os.PathLike = None, create_new: bool = False):
        super().__init__(read_xml_path, write_xml_path, sub_dir='population', create_new=create_new)

    @property
    def minimum_population_for_recruitment(self) -> Dict[str, float]:
        return int(self._tree.xpath("/rec[@type='POPULATION']/u")[0].text)

    @minimum_population_for_recruitment.setter
    def minimum_population_for_recruitment(self, value: int):
        self._tree.xpath("/rec[@type='POPULATION']/u")[0].text = str(value)

    @property
    def base_population(self) -> int:
        return int(self._tree.xpath("/rec[@type='POPULATION']/u")[1].text)

    @base_population.setter
    def base_population(self, value: int):
        self._tree.xpath("/rec[@type='POPULATION']/u")[1].text = str(value)

    @property
    def new_minimum_population_when_settlement_emerges(self) -> int:
        return int(self._tree.xpath("/rec[@type='POPULATION']/u")[2].text)

    @new_minimum_population_when_settlement_emerges.setter
    def new_minimum_population_when_settlement_emerges(self, value: int):
        self._tree.xpath("/rec[@type='POPULATION']/u")[2].text = str(value)

    def _get_population_class_element(self, social_class: PopulationClass.supported_classes) -> etree._Element:
        return self._tree.xpath("/rec[@type='POPULATION']/rec[@type='REGION_FACTORS']/ary[@type='POPULATION CLASSES']/population_class[@Social_Class=$social_class]", social_class=social_class)[0]

    @cached_property
    def social_class_lower(self):
        return PopulationClass(self._get_population_class_element('lower'))

    @cached_property
    def social_class_middle(self):
        return PopulationClass(self._get_population_class_element('middle'))

    @cached_property
    def social_class_upper(self):
        return PopulationClass(self._get_population_class_element('upper'))

    @property
    def factor_current_population(self) -> int:
        return int(self._tree.xpath("/rec[@type='POPULATION']/rec[@type='REGION_FACTORS']/u")[0].text)

    @factor_current_population.setter
    def factor_current_population(self, value: int):
        self._tree.xpath("/rec[@type='POPULATION']/rec[@type='REGION_FACTORS']/u")[0].text = str(value)

    @property
    def factor_max_supported_population(self) -> int:
        return int(self._tree.xpath("/rec[@type='POPULATION']/rec[@type='REGION_FACTORS']/u")[1].text)

    @factor_max_supported_population.setter
    def factor_max_supported_population(self, value: int):
        self._tree.xpath("/rec[@type='POPULATION']/rec[@type='REGION_FACTORS']/u")[1].text = str(value)

    @property
    def factor_base_population(self) -> int:
        return int(self._tree.xpath("/rec[@type='POPULATION']/rec[@type='REGION_FACTORS']/u")[2].text)

    @factor_base_population.setter
    def factor_base_population(self, value: int):
        self._tree.xpath("/rec[@type='POPULATION']/rec[@type='REGION_FACTORS']/u")[2].text = str(value)

    @property
    def religion_breakdown(self) -> ReligiousBreakdown:
        religion_breakdown = {}
        lines = self._tree.xpath("/rec[@type='POPULATION']/rec[@type='REGION_FACTORS']/religion_breakdown")[0].text.split('\n')
        for line in lines[1:-1]:
            religion, population_percentage = line.strip().split('=')
            religion_breakdown[religion] = float(population_percentage)
        return religion_breakdown

    @religion_breakdown.setter
    def religion_breakdown(self, value: ReligiousBreakdown):
        religion_breakdown = {}
        lines = self._tree.xpath("/rec[@type='POPULATION']/rec[@type='REGION_FACTORS']/religion_breakdown")[0].text.split('\n')
        for line in lines[1:-1]:
            religion, population_percentage = line.strip().split('=')
            religion_breakdown[religion] = float(population_percentage)
        religion_breakdown.update(value)
        text = lines[0] + '\n' + '\n'.join([f"   {religion}={population_percentage}" for religion, population_percentage in religion_breakdown.items()]) + '\n' + lines[-1]
        self._tree.xpath("/rec[@type='POPULATION']/rec[@type='REGION_FACTORS']/religion_breakdown")[0].text = text



# startpos/region_slot/

class RegionSlot(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._type = self._soup.find('rec').get('type')
        self._id = self._get_id_tag().string
        self._name = self._get_name_tag().string
        self._commodity_abundance = self._get_commodity_abundance_tag().string
        self._town_prosperity = self._get_town_prosperity_tag().string
        self._emerged = self._get_emerged_tag().name
        self._garrison_faction_id = self._get_garrison_faction_id_tag().string
        self._garrison_building_slot_id = self._get_garrison_building_slot_id_tag().string
        self._garrison_army_id = self._get_garrison_army_id_tag().string
        self._garrison_character_ids = self._get_garrison_character_ids_tag().string
        self._has_building_manager = True if self._get_building_manager_tag() else False
        self._constructed = None
        self._building_health = None
        self._building_name = None
        self._building_faction = None
        self._building_government = None
        self._has_recruitment_manager = True if self._get_recruitment_manager_tag() else False
        self._recruitment_id = None
        if self._get_building_manager_tag():
            self._constructed = self._get_constructed_tag().name
            if self._constructed == 'yes':
                self._building_health = self._get_building_tag().get('health')
                self._building_name = self._get_building_tag().get('name')
                self._building_faction = self._get_building_tag().get('faction')
                self._building_government = self._get_building_tag().get('government')
        if self._get_recruitment_manager_tag():
            self._recruitment_id = self._get_recruitment_id_tag().string

    def __str__(self):
        return '\n'.join([
            f'type                          : {self.get_type()}',
            f'id                            : {self.get_id()}',
            f'name                          : {self.get_name()}',
            f'commodity_abundance           : {self.get_commodity_abundance()}',
            f'town_prosperity               : {self.get_town_prosperity()}',
            f'emerged                       : {self.get_emerged()}',
            f'garrison_faction_id           : {self.get_garrison_faction_id()}',
            f'garrison_building_slot_id     : {self.get_garrison_building_slot_id()}',
            f'garrison_army_id              : {self.get_garrison_army_id()}',
            f'garrison_character_ids        : {self.get_garrison_character_ids()}',
            f'building_health               : {self.get_building_health()}',
            f'building_name                 : {self.get_building_name()}',
            f'building_faction              : {self.get_building_faction()}',
            f'building_government           : {self.get_building_government()}',
            f'recruitment_id                : {self.get_recruitment_id()}'
        ])


    def get_type(self):
        return self._type


    def _get_id_tag(self):
        return self._soup.find('rec', {'type': self._type}).find('rec', {'type': 'REGION_SLOT'}, recursive=False).find('u', recursive=False)

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._get_id_tag().string = id
        self._id = id


    def _get_name_tag(self):
        return self._soup.find('rec', {'type': self._type}).find('rec', {'type': 'REGION_SLOT'}, recursive=False).find('s', recursive=False)

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._get_name_tag().string = name
        self._name = name


    def _get_commodity_abundance_tag(self):
        return self._soup.find('rec', {'type': self._type}).find('rec', {'type': 'REGION_SLOT'}, recursive=False).find_all('i', recursive=False)[2]

    def get_commodity_abundance(self):
        return self._commodity_abundance

    def set_commodity_abundance(self, commodity_abundance):
        self._get_commodity_abundance_tag().string = commodity_abundance
        self._commodity_abundance = commodity_abundance


    def _get_town_prosperity_tag(self):
        return self._soup.find('rec', {'type': self._type}).find('rec', {'type': 'REGION_SLOT'}, recursive=False).find_all('i', recursive=False)[3]

    def get_town_prosperity(self):
        return self._town_prosperity

    def set_town_prosperity(self, town_prosperity):
        self._get_town_prosperity_tag().string = town_prosperity
        self._town_prosperity = town_prosperity


    def _get_emerged_tag(self):
        return self._soup.find('rec', {'type': self._type}).find('rec', {'type': 'REGION_SLOT'}, recursive=False).find(['yes', 'no'], recursive=False)

    def get_emerged(self):
        return self._emerged

    def _set_emerged(self, emerged):
        self._get_emerged_tag().name = emerged
        self._emerged = emerged

    def make_emerged(self):
        self._set_emerged('yes')

    def make_emergent(self):
        self._set_emerged('no')


    def _get_garrison_faction_id_tag(self):
        return self._soup.find('rec', {'type': self._type}).find('rec', {'type': 'REGION_SLOT'}, recursive=False).find('rec', {'type': 'SIEGEABLE_GARRISON_RESIDENCE'}, recursive=False).find('garrison_residence', recursive=False)

    def get_garrison_faction_id(self):
        return self._garrison_faction_id

    def set_garrison_faction_id(self, garrison_faction_id):
        self._get_garrison_faction_id_tag().string = garrison_faction_id
        self._garrison_faction_id = garrison_faction_id


    def _get_garrison_building_slot_id_tag(self):
        return self._soup.find('rec', {'type': self._type}).find('rec', {'type': 'REGION_SLOT'}, recursive=False).find('rec', {'type': 'SIEGEABLE_GARRISON_RESIDENCE'}, recursive=False).find_all('u', recursive=False)[0]

    def get_garrison_building_slot_id(self):
        return self._garrison_building_slot_id

    def set_garrison_building_slot_id(self, garrison_building_slot_id):
        self._get_garrison_building_slot_id_tag().string = garrison_building_slot_id
        self._garrison_building_slot_id = garrison_building_slot_id


    def _get_garrison_army_id_tag(self):
        return self._soup.find('rec', {'type': self._type}).find('rec', {'type': 'REGION_SLOT'}, recursive=False).find('rec', {'type': 'SIEGEABLE_GARRISON_RESIDENCE'}, recursive=False).find_all('u', recursive=False)[5]

    def get_garrison_army_id(self):
        return self._garrison_army_id

    def set_garrison_army_id(self, garrison_army_id):
        self._get_garrison_army_id_tag().string = garrison_army_id
        self._garrison_army_id = garrison_army_id


    def _get_garrison_character_ids_tag(self):
        return self._soup.find('rec', {'type': self._type}).find('rec', {'type': 'REGION_SLOT'}, recursive=False).find('rec', {'type': 'SIEGEABLE_GARRISON_RESIDENCE'}, recursive=False).find_all('u4_ary', recursive=False)[1]

    def get_garrison_character_ids(self):
        return self._garrison_character_ids

    def remove_garrison_character_id(self, garrison_character_id):
        remove_id_from_tag_string(self._get_garrison_character_ids_tag(), garrison_character_id)
        self._garrison_character_ids = self._get_garrison_character_ids_tag().string

    def add_garrison_character_id(self, garrison_character_id):
        append_id_to_tag_string(self._get_garrison_character_ids_tag(), garrison_character_id, sort=False)
        self._garrison_character_ids = self._get_garrison_character_ids_tag().string


    def _get_building_manager_tag(self):
        return self._soup.find('rec', {'type': self._type}).find('rec', {'type': 'REGION_SLOT'}).find('rec', {'type': 'BUILDING_MANAGER'}, recursive=False)

    def has_building_manager(self):
        return self._has_building_manager


    def _get_constructed_tag(self):
        return self._soup.find('rec', {'type': self._type}).find('rec', {'type': 'REGION_SLOT'}).find('rec', {'type': 'BUILDING_MANAGER'}, recursive=False).find_all(['yes', 'no'], recursive=False)[0]

    def get_constructed(self):
        return self._constructed

    def _set_constructed(self, constructed):
        self._get_constructed_tag().name = constructed
        self._constructed = constructed

    def make_constructed(self):
        self._set_constructed('yes')

    def make_non_constructed(self):
        self._set_constructed('no')


    # TODO: Refactor RegionSlot.add_building
    def add_building_manager(self, tag):
        region_slot_soup = self._soup.find('rec', {'type': self._type}).find('rec', {'type': 'REGION_SLOT'}, recursive=False)
        region_slot_soup.insert(3, tag)


    def _get_building_tag(self):
        return self._soup.find('rec', {'type': self._type}).find('rec', {'type': 'REGION_SLOT'}).find('rec', {'type': 'BUILDING_MANAGER'}, recursive=False).find('building', recursive=False)

    def get_building_health(self):
        return self._building_health

    def set_building_health(self, building_health):
        self._get_building_tag()['health'] = building_health
        self._building_health = building_health

    def get_building_name(self):
        return self._building_name

    def set_building_name(self, building_name):
        self._get_building_tag()['name'] = building_name
        self._building_name = building_name

    def get_building_faction(self):
        return self._building_faction

    def set_building_faction(self, building_faction):
        self._get_building_tag()['faction'] = building_faction
        self._building_faction = building_faction

    def get_building_government(self):
        return self._building_government

    def set_building_government(self, building_government):
        self._get_building_tag()['government'] = building_government
        self._building_government = building_government

    def remove_building(self):
        self.make_non_constructed()
        self._get_building_tag().extract()
        self._building_health = None
        self._building_name = None
        self._building_faction = None
        self._building_government = None

    # TODO: Refactor RegionSlot.add_building
    def add_building(self, name, faction_name, government_type, health='100'):
        self.make_constructed()
        building_manager = self._get_building_manager_tag()
        building_manager.insert(2, '\n   ')
        building_manager.insert(3, self._soup.new_tag('building'))
        self.set_building_health(health)
        self.set_building_name(name)
        self.set_building_faction(faction_name)
        self.set_building_government(government_type)


    def _get_recruitment_manager_tag(self):
        return self._soup.find('rec', {'type': self._type}).find('rec', {'type': 'REGION_SLOT'}).find('rec', {'type': 'REGION_RECRUITMENT_MANAGER'}, recursive=False)


    def _get_recruitment_id_tag(self):
        return self._soup.find('rec', {'type': self._type}).find('rec', {'type': 'REGION_SLOT'}).find('rec', {'type': 'REGION_RECRUITMENT_MANAGER'}, recursive=False).find('i', recursive=False)

    def get_recruitment_id(self):
        return self._recruitment_id

    def set_recruitment_id(self, recruitment_id):
        self._get_recruitment_id_tag().string = recruitment_id
        self._recruitment_id = recruitment_id

    # TODO: Refactor RegionSlot.add_building
    def add_recruitment_manager(self, tag):
        region_slot_soup = self._soup.find('rec', {'type': self._type}).find('rec', {'type': 'REGION_SLOT'}, recursive=False)
        region_slot_soup.insert(41, tag)



class Fort(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._type = self._soup.find('rec').get('type')
        self._faction_id = self._get_faction_id_tag().string
        self._fort_level = self._get_fort_level_tag().string
        self._on_screen_name = self._get_on_screen_name_tag().string
        self._name_id = self._get_name_id_tag().string
        self._id = self._get_id_tag().string
        self._fort_faction_id = self._get_fort_faction_id_tag().string
        self._garrison_faction_id = self._get_garrison_faction_id_tag().string
        self._garrison_building_slot_id = self._get_garrison_building_slot_id_tag().string
        self._garrison_army_id = self._get_garrison_army_id_tag().string
        self._garrison_character_ids = self._get_garrison_character_ids_tag().string

    def __str__(self):
        return '\n'.join([
            f'type                          : {self.get_type()}',
            f'faction_id                    : {self.get_faction_id()}',
            f'fort_level                    : {self.get_fort_level()}',
            f'on_screen_name                : {self.get_on_screen_name()}',
            f'name_id                       : {self.get_name_id()}',
            f'id                            : {self.get_id()}',
            f'fort_faction_id               : {self.get_fort_faction_id()}',
            f'garrison_faction_id           : {self.get_garrison_faction_id()}',
            f'garrison_building_slot_id     : {self.get_garrison_building_slot_id()}',
            f'garrison_army_id              : {self.get_garrison_army_id()}',
            f'garrison_character_ids        : {self.get_garrison_character_ids()}'
        ])


    def get_type(self):
        return self._type


    def _get_faction_id_tag(self):
        return self._soup.find('rec', {'type': 'FORT_ARRAY'}).find('i', recursive=False)

    def get_faction_id(self):
        return self._faction_id

    def set_faction_id(self, faction_id):
        self._get_faction_id_tag().string = faction_id
        self._faction_id = faction_id


    def _get_fort_level_tag(self):
        return self._soup.find('rec', {'type': 'FORT_ARRAY'}).find('rec', {'type': 'FORT'}, recursive=False).find_all('i', recursive=False)[0]

    def get_fort_level(self):
        return self._fort_level

    def set_fort_level(self, fort_level):
        self._get_fort_level_tag().string = fort_level
        self._fort_level = fort_level


    def _get_on_screen_name_tag(self):
        return self._soup.find('rec', {'type': 'FORT_ARRAY'}).find('rec', {'type': 'FORT'}, recursive=False).find('loc', recursive=False)

    def get_on_screen_name(self):
        return self._on_screen_name

    def set_on_screen_name(self, on_screen_name):
        self._get_on_screen_name_tag().string = on_screen_name
        self._on_screen_name = on_screen_name


    def _get_name_id_tag(self):
        return self._soup.find('rec', {'type': 'FORT_ARRAY'}).find('rec', {'type': 'FORT'}, recursive=False).find('s', recursive=False)

    def get_name_id(self):
        return self._name_id

    def set_name_id(self, name_id):
        self._get_name_id_tag().string = name_id
        self._name_id = name_id


    def _get_id_tag(self):
        return self._soup.find('rec', {'type': 'FORT_ARRAY'}).find('rec', {'type': 'FORT'}, recursive=False).find_all('i', recursive=False)[1]

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._get_id_tag().string = id
        self._id = id


    def _get_fort_faction_id_tag(self):
        return self._soup.find('rec', {'type': 'FORT_ARRAY'}).find('rec', {'type': 'FORT'}, recursive=False).find_all('i', recursive=False)[2]

    def get_fort_faction_id(self):
        return self._fort_faction_id

    def set_fort_faction_id(self, fort_faction_id):
        self._get_fort_faction_id_tag().string = fort_faction_id
        self._fort_faction_id = fort_faction_id


    def _get_garrison_faction_id_tag(self):
        return self._soup.find('rec', {'type': 'FORT_ARRAY'}).find('rec', {'type': 'SIEGEABLE_GARRISON_RESIDENCE'}, recursive=False).find('garrison_residence', recursive=False)

    def get_garrison_faction_id(self):
        return self._garrison_faction_id

    def set_garrison_faction_id(self, garrison_faction_id):
        self._get_garrison_faction_id_tag().string = garrison_faction_id
        self._garrison_faction_id = garrison_faction_id


    def _get_garrison_building_slot_id_tag(self):
        return self._soup.find('rec', {'type': 'FORT_ARRAY'}).find('rec', {'type': 'SIEGEABLE_GARRISON_RESIDENCE'}, recursive=False).find_all('u', recursive=False)[0]

    def get_garrison_building_slot_id(self):
        return self._garrison_building_slot_id

    def set_garrison_building_slot_id(self, garrison_building_slot_id):
        self._get_garrison_building_slot_id_tag().string = garrison_building_slot_id
        self._garrison_building_slot_id = garrison_building_slot_id


    def _get_garrison_army_id_tag(self):
        return self._soup.find('rec', {'type': 'FORT_ARRAY'}).find('rec', {'type': 'SIEGEABLE_GARRISON_RESIDENCE'}, recursive=False).find_all('u', recursive=False)[5]

    def get_garrison_army_id(self):
        return self._garrison_army_id

    def set_garrison_army_id(self, garrison_army_id):
        self._get_garrison_army_id_tag().string = garrison_army_id
        self._garrison_army_id = garrison_army_id


    def _get_garrison_character_ids_tag(self):
        return self._soup.find('rec', {'type': 'FORT_ARRAY'}).find('rec', {'type': 'SIEGEABLE_GARRISON_RESIDENCE'}, recursive=False).find_all('u4_ary', recursive=False)[1]

    def get_garrison_character_ids(self):
        return self._garrison_character_ids

    def remove_garrison_character_id(self, garrison_character_id):
        remove_id_from_tag_string(self._get_garrison_character_ids_tag(), garrison_character_id)
        self._garrison_character_ids = self._get_garrison_character_ids_tag().string

    def add_garrison_character_id(self, garrison_character_id):
        append_id_to_tag_string(self._get_garrison_character_ids_tag(), garrison_character_id, sort=False)
        self._garrison_character_ids = self._get_garrison_character_ids_tag().string



class Settlement(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._type = self._soup.find('rec').get('type')
        self._id = self._get_id_tag().string
        self._name = self._get_name_tag().string
        self._name_2 = self._get_name_2_tag().string
        self._on_screen_name = self._get_on_screen_name_tag().string
        self._unknown = self._get_unknown_tag().string
        self._garrison_faction_id = self._get_garrison_faction_id_tag().string
        self._garrison_building_slot_id = self._get_garrison_building_slot_id_tag().string
        self._garrison_army_id = self._get_garrison_army_id_tag().string
        self._garrison_character_ids = self._get_garrison_character_ids_tag().string

    def __str__(self):
        return '\n'.join([
            f'type                          : {self.get_type()}',
            f'id                            : {self.get_id()}',
            f'name                          : {self.get_name()}',
            f'name_2                        : {self.get_name_2()}',
            f'on_screen_name                : {self.get_on_screen_name()}',
            f'unknown                       : {self.get_unknown()}',
            f'garrison_faction_id           : {self.get_garrison_faction_id()}',
            f'garrison_building_slot_id     : {self.get_garrison_building_slot_id()}',
            f'garrison_army_id              : {self.get_garrison_army_id()}',
            f'garrison_character_ids        : {self.get_garrison_character_ids()}'
        ])


    def get_type(self):
        return self._type


    def _get_id_tag(self):
        return self._soup.find('rec', {'type': 'SETTLEMENT'}).find_all('i', recursive=False)[1]

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._get_id_tag().string = id
        self._id = id


    def _get_name_tag(self):
        return self._soup.find('rec', {'type': 'SETTLEMENT'}).find_all('s', recursive=False)[0]

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._get_name_tag().string = name
        self._name = name


    def _get_name_2_tag(self):
        return self._soup.find('rec', {'type': 'SETTLEMENT'}).find_all('s', recursive=False)[1]

    def get_name_2(self):
        return self._name_2

    def set_name_2(self, name_2):
        self._get_name_2_tag().string = name_2
        self._name_2 = name_2


    def _get_on_screen_name_tag(self):
        return self._soup.find('rec', {'type': 'SETTLEMENT'}).find('loc', recursive=False)

    def get_on_screen_name(self):
        return self._on_screen_name

    def set_on_screen_name(self, on_screen_name):
        self._get_on_screen_name_tag().string = on_screen_name
        self._on_screen_name = on_screen_name


    # TODO: Check if it is settlement_prosperity
    def _get_unknown_tag(self):
        return self._soup.find('rec', {'type': 'SETTLEMENT'}).find_all('i', recursive=False)[0]

    def get_unknown(self):
        return self._unknown

    def set_unknown(self, unknown):
        self._get_unknown_tag().string = unknown
        self._unknown = unknown


    def _get_garrison_faction_id_tag(self):
        return self._soup.find('rec', {'type': 'SETTLEMENT'}).find('rec', {'type': 'SIEGEABLE_GARRISON_RESIDENCE'}, recursive=False).find('garrison_residence', recursive=False)

    def get_garrison_faction_id(self):
        return self._garrison_faction_id

    def set_garrison_faction_id(self, garrison_faction_id):
        self._get_garrison_faction_id_tag().string = garrison_faction_id
        self._garrison_faction_id = garrison_faction_id


    def _get_garrison_building_slot_id_tag(self):
        return self._soup.find('rec', {'type': 'SETTLEMENT'}).find('rec', {'type': 'SIEGEABLE_GARRISON_RESIDENCE'}, recursive=False).find_all('u', recursive=False)[0]

    def get_garrison_building_slot_id(self):
        return self._garrison_building_slot_id

    def set_garrison_building_slot_id(self, garrison_building_slot_id):
        self._get_garrison_building_slot_id_tag().string = garrison_building_slot_id
        self._garrison_building_slot_id = garrison_building_slot_id


    def _get_garrison_army_id_tag(self):
        return self._soup.find('rec', {'type': 'SETTLEMENT'}).find('rec', {'type': 'SIEGEABLE_GARRISON_RESIDENCE'}, recursive=False).find_all('u', recursive=False)[5]

    def get_garrison_army_id(self):
        return self._garrison_army_id

    def set_garrison_army_id(self, garrison_army_id):
        self._get_garrison_army_id_tag().string = garrison_army_id
        self._garrison_army_id = garrison_army_id


    def _get_garrison_character_ids_tag(self):
        return self._soup.find('rec', {'type': 'SETTLEMENT'}).find('rec', {'type': 'SIEGEABLE_GARRISON_RESIDENCE'}, recursive=False).find_all('u4_ary', recursive=False)[1]

    def get_garrison_character_ids(self):
        return self._garrison_character_ids

    def remove_garrison_character_id(self, garrison_character_id):
        remove_id_from_tag_string(self._get_garrison_character_ids_tag(), garrison_character_id)
        self._garrison_character_ids = self._get_garrison_character_ids_tag().string

    def add_garrison_character_id(self, garrison_character_id):
        append_id_to_tag_string(self._get_garrison_character_ids_tag(), garrison_character_id, sort=False)
        self._garrison_character_ids = self._get_garrison_character_ids_tag().string



# startpos/cai_building_slots/

class CaiBuildingSlot(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._id = self._get_id_tag().string
        self._emerged = self._get_emerged_tag().string
        self._building_slot_id = self._get_building_slot_id_tag().string
        self._type = self._get_type_tag().string
        self._owned_direct = self._get_owned_direct_tag().string

    def __str__(self):
        return '\n'.join([
            f'id                            : {self.get_id()}',
            f'emerged                       : {self.get_emerged()}',
            f'building_slot_id              : {self.get_building_slot_id()}',
            f'type                          : {self.get_type()}',
            f'owned_direct                  : {self.get_owned_direct()}'
        ])


    def _get_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_BUILDING_SLOTS'}).find('u', recursive=False)

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._get_id_tag().string = id
        self._id = id


    def _get_emerged_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_BUILDING_SLOTS'}).find_all('u', recursive=False)[3]

    def get_emerged(self):
        return self._emerged

    def _set_emerged(self, emerged):
        self._get_emerged_tag().string = emerged
        self._emerged = emerged

    def make_emerged(self):
        self._set_emerged('1')

    def make_emergent(self):
        self._set_emerged('0')


    def _get_building_slot_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_BUILDING_SLOTS'}).find('rec', {'type': 'CAI_BUILDING_SLOT'}).find_all('u', recursive=False)[0]

    def get_building_slot_id(self):
        return self._building_slot_id

    def set_building_slot_id(self, building_slot_id):
        self._get_building_slot_id_tag().string = building_slot_id
        self._building_slot_id = building_slot_id


    def _get_type_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_BUILDING_SLOTS'}).find('rec', {'type': 'CAI_BUILDING_SLOT'}).find_all('u', recursive=False)[1]

    def get_type(self):
        return self._type

    def set_type(self, type):
        self._get_type_tag().string = type
        self._type = type


    def _get_owned_direct_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_BUILDING_SLOTS'}).find('rec', {'type': 'CAI_BUILDING_SLOT'}).find_all('u', recursive=False)[2]

    def get_owned_direct(self):
        return self._owned_direct

    def set_owned_direct(self, owned_direct):
        self._get_owned_direct_tag().string = owned_direct
        self._owned_direct = owned_direct


    def _get_bdi_1_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_BUILDING_SLOTS'}).find_all('u4_ary', recursive=False)[1]

    def _get_bdi_3_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_BUILDING_SLOTS'}).find_all('u4_ary', recursive=False)[3]

    def _get_bdi_7_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_BUILDING_SLOTS'}).find_all('u4_ary', recursive=False)[7]

    def clear_bdi(self):
        self._get_bdi_1_tag().string = ''
        self._get_bdi_3_tag().string = ''
        self._get_bdi_7_tag().string = ''



# startpos/cai_settlements/

class CaiSettlement(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._id = self._get_id_tag().string
        self._owned_direct = self._get_owned_direct_tag().string # Faction AI ID
        self._area_id = self._get_cai_situated_tag().get('area_id')
        self._building_slot_ids = self._get_building_slot_ids_tag().string
        self._capital_faction_id = self._get_capital_faction_id_tag().string
        self._settlement_id = self._get_settlement_id_tag().string

    def __str__(self):
        return '\n'.join([
            f'id                            : {self.get_id()}',
            f'owned_direct                  : {self.get_owned_direct()}',
            f'building_slot_ids             : {self.get_building_slot_ids()}',
            f'capital_faction_id            : {self.get_capital_faction_id()}',
            f'settlement_id                 : {self.get_settlement_id()}'
        ])


    def _get_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_SETTLEMENTS'}).find('u', recursive=False)

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._get_id_tag().string = id
        self._id = id


    def _get_owned_direct_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_SETTLEMENTS'}).find('owned_direct', recursive=False)

    def get_owned_direct(self):
        return self._owned_direct

    def set_owned_direct(self, owned_direct):
        self._get_owned_direct_tag().string = owned_direct
        self._owned_direct = owned_direct


    def _get_cai_situated_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_SETTLEMENTS'}).find('cai_situated', recursive=False)

    def get_area_id(self):
        return self._area_id


    def _get_building_slot_ids_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_SETTLEMENTS'}).find('rec', {'type': 'CAI_SETTLEMENT'}, recursive=False).find('u4_ary', recursive=False)

    def get_building_slot_ids(self):
        return self._building_slot_ids

    def remove_building_slot_id(self, building_slot_id):
        remove_id_from_tag_string(self._get_building_slot_ids_tag(), building_slot_id)
        self._building_slot_ids = self._get_building_slot_ids_tag().string

    def add_building_slot_id(self, building_slot_id):
        append_id_to_tag_string(self._get_building_slot_ids_tag(), building_slot_id, sort=False)
        self._building_slot_ids = self._get_building_slot_ids_tag().string


    def _get_capital_faction_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_SETTLEMENTS'}).find('rec', {'type': 'CAI_SETTLEMENT'}, recursive=False).find_all('u', recursive=False)[0]

    def get_capital_faction_id(self):
        return self._capital_faction_id

    def set_capital_faction_id(self, capital_faction_id):
        self._get_capital_faction_id_tag().string = capital_faction_id
        self._capital_faction_id = capital_faction_id


    def _get_settlement_id_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_SETTLEMENTS'}).find('rec', {'type': 'CAI_SETTLEMENT'}, recursive=False).find_all('u', recursive=False)[1]

    def get_settlement_id(self):
        return self._settlement_id

    def set_settlement_settlement_id(self, settlement_id):
        self._get_settlement_id_tag().string = settlement_id
        self._settlement_id = settlement_id


    def _get_bdi_1_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_SETTLEMENTS'}).find_all('u4_ary', recursive=False)[1]

    def _get_bdi_3_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_SETTLEMENTS'}).find_all('u4_ary', recursive=False)[3]

    def _get_bdi_7_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD_SETTLEMENTS'}).find_all('u4_ary', recursive=False)[7]

    def clear_bdi(self):
        self._get_bdi_1_tag().string = ''
        self._get_bdi_3_tag().string = ''
        self._get_bdi_7_tag().string = ''



# startpos/domestic_trade_routes/

class DomesticTradeRoute(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._faction_name = self._get_faction_name_tag().string

    def __str__(self):
        return '\n'.join([
            f'faction_name                  : {self.get_faction_name()}'
        ])


    def _get_faction_name_tag(self):
        return self._soup.find('rec', {'type': 'DOMESTIC_TRADE_ROUTES'}).find('s', recursive=False)

    def get_faction_name(self):
        return self._faction_name

    def set_faction_name(self, faction_name):
        self._get_faction_name_tag().string = faction_name
        self._faction_name = faction_name


    def _get_routes_soups(self):
        return self._soup.find('rec', {'type': 'DOMESTIC_TRADE_ROUTES'}) \
            .find('ary', {'type': 'FACTION_DOMESTIC_TRADE_ROUTES_ARRAY'}, recursive=False) \
            .find_all('rec', {'type': 'FACTION_DOMESTIC_TRADE_ROUTES_ARRAY'}, recursive=False)



# startpos/international_trade_routes/

class InternationalTradeRoute(EsfXmlSoup):
    def __init__(self, soup: BeautifulSoup):
        self._soup = soup
        self._start_region_id = self._get_start_region_id_tag().string
        self._destination_region_id = self._get_destination_region_id_tag().string
        self._route_id = self._get_route_id_tag().string
        self._id = self._get_id_tag().string

    def __str__(self):
        return '\n'.join([
            f'start_region_id               : {self.get_start_region_id()}',
            f'destination_region_id         : {self.get_destination_region_id()}',
            f'route_id                      : {self.get_route_id()}',
            f'id                            : {self.get_id()}'
        ])

    def print(self):
        print(str(self))


    def _get_start_region_id_tag(self):
        return self._soup.find('rec', {'type': 'INTERNATIONAL_TRADE_ROUTE'}, recursive=False).find('i', recursive=False)

    def get_start_region_id(self):
        return self._start_region_id

    def set_start_region_id(self, start_region_id):
        self._get_start_region_id_tag().string = start_region_id
        self._start_region_id = start_region_id


    def _get_destination_region_id_tag(self):
        return self._soup.find('rec', {'type': 'INTERNATIONAL_TRADE_ROUTE'}, recursive=False).find_all('i', recursive=False)[-2]

    def get_destination_region_id(self):
        return self._destination_region_id

    def set_destination_region_id(self, destination_region_id):
        self._get_destination_region_id_tag().string = destination_region_id
        self._destination_region_id = destination_region_id


    def _get_route_id_tag(self):
        return self._soup.find('rec', {'type': 'INTERNATIONAL_TRADE_ROUTE'}, recursive=False).find_all('i', recursive=False)[-1]

    def get_route_id(self):
        return self._route_id

    def set_route_id(self, route_id):
        self._get_route_id_tag().string = route_id
        self._route_id = route_id


    def _get_id_tag(self):
        return self._soup.find('u', recursive=False)

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._get_id_tag().string = id
        self._id = id



class InternationalTradeRoutes(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._faction_name = self._get_faction_name_tag().string
        self._routes = {}
        for route_soup in self._get_route_soups():
            route = InternationalTradeRoute(route_soup)
            self._routes[route.get_destination_region_id()] = route

    def __str__(self):
        return '\n'.join([
            f'faction_name                  : {self.get_faction_name()}'
        ])


    def _get_faction_name_tag(self):
        return self._soup.find('rec', {'type': 'INTERNATIONAL_TRADE_ROUTES'}).find('s', recursive=False)

    def get_faction_name(self):
        return self._faction_name

    def set_faction_name(self, faction_name):
        self._get_faction_name_tag().string = faction_name
        self._faction_name = faction_name


    def _get_route_soups(self):
        return self._soup.find('rec', {'type': 'INTERNATIONAL_TRADE_ROUTES'}) \
            .find('ary', {'type': 'FACTION_INTERNATIONAL_TRADE_ROUTES_ARRAY'}, recursive=False) \
            .find_all('rec', {'type': 'FACTION_INTERNATIONAL_TRADE_ROUTES_ARRAY'}, recursive=False)


    def get_routes(self) -> Dict[str, InternationalTradeRoute]:
        return self._routes

    def clear_routes(self):
        self._soup.find('rec', {'type': 'INTERNATIONAL_TRADE_ROUTES'}).find('ary', {'type': 'FACTION_INTERNATIONAL_TRADE_ROUTES_ARRAY'}, recursive=False).string = ''
        self._routes.clear()

    def get_route(self, destination_region_id) -> InternationalTradeRoute:
        return self._routes[destination_region_id]

    def remove_route(self, destination_region_id):
        for route_soup in self._get_route_soups():
            current_region_id = route_soup.find('rec', {'type': 'INTERNATIONAL_TRADE_ROUTE'}, recursive=False).find_all('i', recursive=False)[-2].string
            if current_region_id == destination_region_id:
                route_soup.decompose()
        del self._routes[destination_region_id]



# startpos/victory_conditions/

class VictoryConditionsBlock:
    _supported_campaign_types = Literal['0 (Short)', '1 (Long)', '2 (Prestige)', '3 (Global Domination)']

    def __init__(self, element: etree._Element):
        self._element = element

    @cached_property
    def victory_conditions_tag(self):
        return self._element.find('victory_conditions')

    @property
    def year(self) -> int:
        return int(self.victory_conditions_tag.attrib['year'])

    @year.setter
    def year(self, year: int):
        self.victory_conditions_tag.attrib['year'] = str(year)

    def add_years(self, value: int):
        self.year = self.year + value

    @property
    def region_count(self) -> int:
        return int(self.victory_conditions_tag.attrib['region_count'])

    @region_count.setter
    def region_count(self, value: int):
        self.victory_conditions_tag.attrib['region_count'] = str(value)

    @property
    def prestige_victory(self) -> Literal['yes', 'no']:
        return self.victory_conditions_tag.attrib['prestige_victory']

    @prestige_victory.setter
    def prestige_victory(self, value: Literal['yes', 'no']):
        self.victory_conditions_tag.attrib['prestige_victory'] = value

    def make_prestiege_victory(self):
        self.prestige_victory = 'yes'

    def make_non_prestiege_victory(self):
        self.prestige_victory = 'no'

    @property
    def campaign_type(self) -> _supported_campaign_types:
        return self.victory_conditions_tag.attrib['campaign_type']

    @campaign_type.setter
    def campaign_type(self, campaign_type: _supported_campaign_types):
        assert campaign_type in get_args(self._supported_campaign_types), f"'{campaign_type}' campaign type is not supported."
        self.victory_conditions_tag.attrib['campaign_type'] = campaign_type
        self._campaign_type = campaign_type

    @property
    def regions(self) -> List[VANILLA_REGION_KEY_HINTS]:
        return self.victory_conditions_tag.text.split('\n')[1:-1]



class VictoryCondition(EsfXmlEtree):
    def __init__(self, read_xml_path: os.PathLike, write_xml_path: os.PathLike = None, create_new: bool = False):
        super().__init__(read_xml_path, write_xml_path, sub_dir='victory_conditions', create_new=create_new)

    @property
    def faction_name(self):
        return self._tree.xpath("/rec[@type='VICTORY_CONDITION_OPTIONS']/s")[0].text

    @faction_name.setter
    def faction_name(self, value):
        self._tree.xpath("/rec[@type='VICTORY_CONDITION_OPTIONS']/s")[0].text = value

    @cached_property
    def victory_conditions_block_elements(self):
        return self._tree.xpath("/rec[@type='VICTORY_CONDITION_OPTIONS']/ary[@type='VICTORY_CONDITIONS_BLOCK']/rec[@type='VICTORY_CONDITIONS_BLOCK']")

    @cached_property
    def victory_conditions_blocks(self) -> Dict[VictoryConditionsBlock._supported_campaign_types, VictoryConditionsBlock]:
        victory_conditions_blocks = {}
        for victory_conditions_block_tree in self.victory_conditions_block_elements:
            victory_conditions_block = VictoryConditionsBlock(victory_conditions_block_tree)
            victory_conditions_blocks[victory_conditions_block.campaign_type] = victory_conditions_block
        return victory_conditions_blocks

    def get_victory_conditions_blocks(self) -> List[VictoryConditionsBlock]:
        return list(self.victory_conditions_blocks.values())



# startpos/preopen_map_info/ and startpos/campaign_env/

class PlayerSetup:
    def __init__(self, soup: BeautifulSoup):
        self._soup = soup
        self._name = self._get_name_tag().string
        self._playable = self._get_playable_tag().name

    def __str__(self):
        return '\n'.join([
            f'name                          : {self.get_name()}',
            f'playable                      : {self.get_playable()}'
        ])

    def print(self):
        print(str(self))


    def _get_name_tag(self):
        return self._soup.find('rec', {'type': 'CAMPAIGN_PLAYER_SETUP'}).find('s', recursive=False)

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._get_name_tag().string = name
        self._name = name


    def _get_playable_tag(self):
        return self._soup.find('rec', {'type': 'CAMPAIGN_PLAYER_SETUP'}).find_all(['yes', 'no'], recursive=False)[1]

    def get_playable(self):
        return self._playable

    def _set_playable(self, playable):
        self._get_playable_tag().name = playable
        self._playable = playable

    def make_playable(self):
        self._set_playable('yes')

    def make_non_playable(self):
        self._set_playable('no')



# startpos/campaign_env/

class Env(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._campaign_setup = get_base_name_from_path(self._get_campaign_setup_tag().get('path'))

    def __str__(self):
        return '\n'.join([
            f'campaign_setup              : {self.get_campaign_setup()}'
            f'preopen_map_info              : {self.get_preopen_map_info()}'
        ])


    def _get_campaign_setup_tag(self):
        return self._soup.find('rec', {'type': 'CAMPAIGN_ENV'}).find('xml_include', recursive=False)

    def get_campaign_setup(self):
        return self._campaign_setup

    def set_campaign_setup(self, campaign_setup):
        self._get_campaign_setup_tag()['path'] = 'campaign_env/' + campaign_setup
        self._campaign_setup = campaign_setup



class CampaignSetup(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._campaign_name = self._get_campaign_name_tag().string
        self._player_setups = {}
        for player_setup_soup in self._get_player_setup_soups():
            player_setup = PlayerSetup(player_setup_soup)
            self._player_setups[player_setup.get_name()] = player_setup

    def __str__(self):
        return '\n'.join([
            f'campaign_name                 : {self.get_campaign_name()}'
        ])


    def _get_campaign_name_tag(self):
        return self._soup.find('rec', {'type': 'CAMPAIGN_SETUP'}).find('s', recursive=False)

    def get_campaign_name(self):
        return self._campaign_name

    def set_campaign_name(self, campaign_name):
        self._get_campaign_name_tag().string = campaign_name
        self._campaign_name = campaign_name


    def _get_player_setup_soups(self):
        return self._soup.find('rec', {'type': 'CAMPAIGN_SETUP'}) \
            .find('rec', {'type': 'CAMPAIGN_PLAYERS_SETUP'}, recursive=False) \
            .find('ary', {'type': 'PLAYERS_ARRAY'}, recursive=False) \
            .find_all('rec', {'type': 'PLAYERS_ARRAY'}, recursive=False)


    def get_player_setup(self, name) -> PlayerSetup:
        return self._player_setups.get(name)



class SpyingArray:
    def __init__(self, soup: BeautifulSoup):
        self._soup = soup
        self._faction_name = self._get_faction_name_tag().string

    def __str__(self):
        return '\n'.join([
            f'faction_name                  : {self.get_faction_name()}',
            f'playable                      : {self.get_playable()}'
        ])

    def print(self):
        print(str(self))


    def _get_faction_name_tag(self):
        return self._soup.find('s', recursive=False)

    def get_faction_name(self):
        return self._faction_name

    def set_faction_name(self, faction_name):
        self._get_faction_name_tag().string = faction_name
        self._faction_name = faction_name



class World(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._unknown_1 = self._get_unknown_1_tag().string
        self._unknown_2 = self._get_unknown_2_tag().string
        self._spying_arrays = {}
        for spying_array_soup in self._get_spying_array_soups():
            spying_array = SpyingArray(spying_array_soup)
            self._spying_arrays[spying_array.get_faction_name()] = spying_array

    def __str__(self):
        return '\n'.join([
            f'unknown_1                     : {self.get_unknown_1()}',
            f'unknown_2                     : {self.get_unknown_2()}'
        ])


    def _get_unknown_1_tag(self):
        return self._soup.find('rec', {'type': 'WORLD'}).find_all('u', recursive=False)[0]

    def get_unknown_1(self):
        return self._unknown_1

    def set_unknown_1(self, unknown_1):
        self._get_unknown_1_tag().string = unknown_1
        self._unknown_1 = unknown_1


    def _get_unknown_2_tag(self):
        return self._soup.find('rec', {'type': 'WORLD'}).find_all('u', recursive=False)[1]

    def get_unknown_2(self):
        return self._unknown_2

    def set_unknown_2(self, unknown_2):
        self._get_unknown_2_tag().string = unknown_2
        self._unknown_2 = unknown_2


    def _get_spying_array_soups(self):
        return self._soup.find('rec', {'type': 'WORLD'}) \
            .find('ary', {'type': 'SPYING_ARRAY'}, recursive=False) \
            .find_all('rec', {'type': 'SPYING_ARRAY'}, recursive=False)


    def get_spying_array(self, faction_name) -> SpyingArray:
        return self._spying_arrays.get(faction_name)



class CampaignModel(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._map_location = self._get_map_location_tag().string
        self._map_name = self._get_map_name_tag().string
        self._turns_per_year = self._get_turns_per_year_tag().string
        self._date = self._get_date_tag().string

    def __str__(self):
        return '\n'.join([
            f'map_location                  : {self.get_map_location()}',
            f'map_name                      : {self.get_map_name()}',
            f'turns_per_year                : {self.get_turns_per_year()}',
            f'date                          : {self.get_date()}'
        ])


    def _get_map_location_tag(self):
        return self._soup.find('rec', {'type': 'CAMPAIGN_MODEL'}).find('rec', {'type': 'CAMPAIGN_MAP_DATA'}).find_all('s', recursive=False)[0]

    def get_map_location(self):
        return self._map_location

    def set_map_location(self, map_location):
        self._get_map_location_tag().string = map_location
        self._map_location = map_location


    def _get_map_name_tag(self):
        return self._soup.find('rec', {'type': 'CAMPAIGN_MODEL'}).find('rec', {'type': 'CAMPAIGN_MAP_DATA'}).find_all('s', recursive=False)[2]

    def get_map_name(self):
        return self._map_name

    def set_map_name(self, map_name):
        self._get_map_name_tag().string = map_name
        self._map_name = map_name


    def _get_turns_per_year_tag(self):
        return self._soup.find('rec', {'type': 'CAMPAIGN_MODEL'}).find('rec', {'type': 'CAMPAIGN_CALENDAR'}).find_all('u', recursive=False)[0]

    def get_turns_per_year(self):
        return self._turns_per_year

    def set_turns_per_year(self, turns_per_year):
        self._get_turns_per_year_tag().string = turns_per_year
        self._turns_per_year = turns_per_year


    def _get_date_tag(self):
        return self._soup.find('rec', {'type': 'CAMPAIGN_MODEL'}).find('rec', {'type': 'CAMPAIGN_CALENDAR'}).find('date', recursive=False)

    def get_date(self):
        return self._date

    def set_date(self, date):
        self._get_date_tag().string = date
        self._date = date

    def get_year(self):
        return get_year_from_date(self.get_date())



# startpos/esf.xml

class Esf(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._save_game_header = get_base_name_from_path(self._get_save_game_header_tag().get('path'))
        self._preopen_map_info = get_base_name_from_path(self._get_preopen_map_info_tag().get('path'))

    def __str__(self):
        return '\n'.join([
            f'save_game_header              : {self.get_save_game_header()}'
            f'preopen_map_info              : {self.get_preopen_map_info()}'
        ])


    def _get_save_game_header_tag(self):
        return self._soup.find('esf').find('rec', {'type': 'CAMPAIGN_STARTPOS'}, recursive=False).find_all('xml_include', recursive=False)[0]

    def get_save_game_header(self) -> str:
        return self._save_game_header

    def set_save_game_header(self, save_game_header):
        self._get_save_game_header_tag()['path'] = 'save_game_header/' + save_game_header
        self._save_game_header = save_game_header


    def _get_preopen_map_info_tag(self):
        return self._soup.find('esf').find('rec', {'type': 'CAMPAIGN_STARTPOS'}, recursive=False).find_all('xml_include', recursive=False)[1]

    def get_preopen_map_info(self) -> str:
        return self._preopen_map_info

    def set_preopen_map_info(self, preopen_map_info):
        self._get_preopen_map_info_tag()['path'] = 'preopen_map_info/' + preopen_map_info
        self._preopen_map_info = preopen_map_info



# startpos/preopen_map_info/

class FactionInfo:
    def __init__(self, soup: BeautifulSoup):
        self._soup = soup
        self._name = self._get_name_tag().string
        self._leader_portrait = self._get_leader_portrait_tag().string
        self._majority = self._get_majority_tag().name
        self._playable = self._get_playable_tag().name
        self._order = self._get_order_tag().string
        self._description = self._get_description_tag().string
        self._flag = self._get_flag_tag().string
        self._n_provinces = self._get_n_provinces_tag().string

    def __str__(self):
        return '\n'.join([
            f'name                          : {self.get_name()}',
            f'leader_portrait               : {self.get_leader_portrait()}',
            f'majority                      : {self.get_majority()}',
            f'playable                      : {self.get_playable()}',
            f'order                         : {self.get_order()}',
            f'description                   : {self.get_description()}',
            f'flag                          : {self.get_flag()}',
            f'n_provinces                   : {self.get_n_provinces()}'
        ])

    def print(self):
        print(str(self))


    def _get_name_tag(self):
        return self._soup.find_all('s', recursive=False)[0]

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._get_name_tag().string = name
        self._name = name


    def _get_leader_portrait_tag(self):
        return self._soup.find_all('s', recursive=False)[1]

    def get_leader_portrait(self):
        return self._leader_portrait

    def set_leader_portrait(self, leader_portrait):
        self._get_leader_portrait_tag().string = leader_portrait
        self._leader_portrait = leader_portrait


    def _get_majority_tag(self):
        return self._soup.find_all(['yes', 'no'], recursive=False)[0]

    def get_majority(self):
        return self._majority

    def _set_majority(self, majority):
        self._get_majority_tag().name = majority
        self._majority = majority

    def make_major(self):
        self._set_majority('yes')

    def make_minor(self):
        self._set_majority('no')


    def _get_playable_tag(self):
        return self._soup.find_all(['yes', 'no'], recursive=False)[1]

    def get_playable(self):
        return self._playable

    def _set_playable(self, playable):
        self._get_playable_tag().name = playable
        self._playable = playable

    def make_playable(self):
        self._set_playable('yes')

    def make_non_playable(self):
        self._set_playable('no')


    def _get_order_tag(self):
        return self._soup.find_all('i', recursive=False)[0]

    def get_order(self):
        return self._order

    def set_order(self, order):
        self._get_order_tag().string = order
        self._order = order


    def _get_description_tag(self):
        return self._soup.find_all('s', recursive=False)[2]

    def get_description(self):
        return self._description

    def set_description(self, description):
        self._get_description_tag().string = description
        self._description = description


    def _get_flag_tag(self):
        return self._soup.find_all('s', recursive=False)[3]

    def get_flag(self):
        return self._flag

    def set_flag(self, flag):
        self._get_flag_tag().string = flag
        self._flag = flag


    def _get_n_provinces_tag(self):
        return self._soup.find_all('i', recursive=False)[1]

    def get_n_provinces(self):
        return self._n_provinces

    def set_n_provinces(self, n_provinces):
        self._get_n_provinces_tag().string = n_provinces
        self._n_provinces = n_provinces

    def increment_n_provinces(self):
        n_provinces = str(int(self.get_n_provinces()) + 1)
        self._get_n_provinces_tag().string = n_provinces
        self._n_provinces = n_provinces

    def decrement_n_provinces(self):
        n_provinces = str(int(self.get_n_provinces()) - 1)
        self._get_n_provinces_tag().string = n_provinces
        self._n_provinces = n_provinces



class PreopenMapInfo(EsfXmlSoup):
    _supported_theaters = Literal['america', 'europe', 'india']

    class PreopenRegionOwnership(TypedDict):
        theatre: Literal['america', 'europe', 'india']
        region: str
        faction: str

    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._date = self._get_date_tag().string
        self._campaign_name = self._get_campaign_name_tag().string
        self._campaign_map = self._get_campaign_map_tag().string
        self._player_setups = {}
        self._faction_infos = {}
        for player_setup_soup in self._get_player_setup_soups():
            player_setup = PlayerSetup(player_setup_soup)
            self._player_setups[player_setup.get_name()] = player_setup
        for faction_info_soup in self._get_faction_info_soups():
            faction_info = FactionInfo(faction_info_soup)
            self._faction_infos[faction_info.get_name()] = faction_info

    def __str__(self):
        return '\n'.join([
            f'date                          : {self.get_date()}',
            f'campaign_name                 : {self.get_campaign_name()}',
            f'campaign_map                  : {self.get_campaign_map()}'
        ])


    def _get_date_tag(self):
        return self._soup.find('rec', {'type': 'CAMPAIGN_PREOPEN_MAP_INFO'}).find('date', recursive=False)

    def get_date(self):
        return self._date

    def set_date(self, date):
        self._get_date_tag().string = date
        self._date = date


    def _get_campaign_name_tag(self):
        return self._soup.find('rec', {'type': 'CAMPAIGN_PREOPEN_MAP_INFO'}).find_all('s', recursive=False)[0]

    def get_campaign_name(self):
        return self._campaign_name

    def set_campaign_name(self, campaign_name):
        self._get_campaign_name_tag().string = campaign_name
        self._campaign_name = campaign_name


    def _get_campaign_map_tag(self):
        return self._soup.find('rec', {'type': 'CAMPAIGN_PREOPEN_MAP_INFO'}).find_all('s', recursive=False)[1]

    def get_campaign_map(self):
        return self._campaign_map

    def set_campaign_map(self, campaign_map):
        self._get_campaign_map_tag().string = campaign_map
        self._campaign_map = campaign_map


    def _get_region_ownerships_tag(self, theatre: _supported_theaters):
        assert theatre in get_args(self._supported_theaters), f"'{theatre}' theatre is not supported."
        return self._soup.find('rec', {'type': 'CAMPAIGN_PREOPEN_MAP_INFO'}).find('ary', {'type': 'REGION_OWNERSHIPS_BY_THEATRE'}, recursive=False).find('region_ownerships_by_theatre', {'theatre': theatre}, recursive=False)

    def get_region_ownerships(self) -> List[PreopenRegionOwnership]:
        region_ownerships = []
        for theatre in get_args(self._supported_theaters):
            for string in self._get_region_ownerships_tag(theatre).string.split('\n'):
                string = string.strip()
                if not string == '':
                    region, faction = string.split('=')
                    region_ownerships.append({'theatre': theatre, 'region': region, 'faction': faction})
        return region_ownerships

    def get_faction_regions(self, faction):
        return [region_ownership for region_ownership in self.get_region_ownerships() if region_ownership['faction'] == faction]

    def set_region_ownership(self, theatre: _supported_theaters, region, faction):
        region_ownerships = self._get_region_ownerships_tag(theatre).string
        region_ownerships = re.sub(f"{region}=.*", f"{region}={faction}", region_ownerships)
        self._get_region_ownerships_tag(theatre).string = region_ownerships


    def _get_player_setup_soups(self):
        return self._soup.find('rec', {'type': 'CAMPAIGN_PREOPEN_MAP_INFO'}) \
            .find('rec', {'type': 'CAMPAIGN_PLAYERS_SETUP'}, recursive=False) \
            .find('ary', {'type': 'PLAYERS_ARRAY'}, recursive=False) \
            .find_all('rec', {'type': 'PLAYERS_ARRAY'}, recursive=False)


    def _get_faction_info_soups(self):
        return self._soup.find('rec', {'type': 'CAMPAIGN_PREOPEN_MAP_INFO'}) \
            .find('ary', {'type': 'FACTION_INFOS'}, recursive=False) \
            .find_all('rec', {'type': 'FACTION_INFOS'}, recursive=False)


    def get_player_setup(self, name) -> PlayerSetup:
        return self._player_setups.get(name)


    def get_faction_info(self, name) -> FactionInfo:
        return self._faction_infos.get(name)



# startpos/cai_interface

class HistoryEvent:
    def __init__(self, soup: BeautifulSoup):
        self._soup = soup
        self._type = self._get_class_tag().string.split('\n')[1].split('_', 1)[1]
        self._round = self._get_class_tag().string.split('\n')[2].split('_', 1)[1]
        self._faction_name = self._get_class_tag().string.split('\n')[3].split('_', 1)[1]
        self._event_faction_name = None
        if self._type in ['new_manager_for_faction', 'invasion_requested']:
            self._event_faction_name = self._get_event_faction_name_tag().string

    def __str__(self):
        return '\n'.join([
            f'type                          : {self.get_type()}',
            f'round                         : {self.get_round()}',
            f'faction_name                  : {self.get_faction_name()}',
            f'event_faction_name            : {self.get_event_faction_name()}'
        ])

    def print(self):
        print(str(self))


    def _get_class_tag(self):
        return self._soup.find('rec', {'type': 'CAI_HISTORY_EVENT'}).find('cai_event_classes', recursive=False)

    def get_type(self):
        return self._type

    def set_type(self, type):
        lines = self._get_class_tag().string.split('\n')
        lines[1] = f"{lines[1].split('_', 1)[0]}_{type}"
        self._get_class_tag().string = '\n'.join(lines)
        self._type = type

    def get_round(self):
        return self._round

    def set_round(self, round):
        lines = self._get_class_tag().string.split('\n')
        lines[2] = f"{lines[2].split('_', 1)[0]}_{round}"
        self._get_class_tag().string = '\n'.join(lines)
        self._round = round

    def get_faction_name(self):
        return self._faction_name

    def set_faction_name(self, faction_name):
        lines = self._get_class_tag().string.split('\n')
        lines[3] = f"{lines[3].split('_', 1)[0]}_{faction_name}"
        self._get_class_tag().string = '\n'.join(lines)
        self._faction_name = faction_name


    def _get_event_faction_name_tag(self):
        return self._soup.find('rec', {'type': ['CAI_HISTORY_EVENT_NEW_MANAGER_FOR_FACTION', 'CAI_HISTORY_EVENT_INVASION_REQUESTED']}).find('asc', recursive=False)

    def get_event_faction_name(self):
        return self._event_faction_name

    def set_event_faction_name(self, event_faction_name):
        self._get_event_faction_name_tag().string = event_faction_name
        self._event_faction_name = event_faction_name



class CaiHistory(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._unknown_1 = self._get_unknown_1_tag().string
        self._unknown_2 = self._get_unknown_2_tag().string
        self._events = {}
        for event_soup in self._get_event_soups():
            event = HistoryEvent(event_soup)
            if event.get_faction_name() not in self._events:
                self._events[event.get_faction_name()] = []
            self._events[event.get_faction_name()].append(event)

    def __str__(self):
        return '\n'.join([
            f'unknown_1                     : {self.get_unknown_1()}',
            f'unknown_2                     : {self.get_unknown_2()}'
        ])


    def _get_unknown_1_tag(self):
        return self._soup.find('rec', {'type': 'CAI_HISTORY'}).find_all('u', recursive=False)[0]

    def get_unknown_1(self):
        return self._unknown_1

    def set_unknown_1(self, unknown_1):
        self._get_unknown_1_tag().string = unknown_1
        self._unknown_1 = unknown_1


    def _get_unknown_2_tag(self):
        return self._soup.find('rec', {'type': 'CAI_HISTORY'}).find_all('u', recursive=False)[1]

    def get_unknown_2(self):
        return self._unknown_2

    def set_unknown_2(self, unknown_2):
        self._get_unknown_2_tag().string = unknown_2
        self._unknown_2 = unknown_2


    def _get_event_soups(self):
        return self._soup.find('rec', {'type': 'CAI_HISTORY'}) \
            .find('ary', {'type': 'CAI_HISTORY_EVENTS'}, recursive=False) \
            .find_all('rec', {'type': 'CAI_HISTORY_EVENTS'}, recursive=False)


    def get_events(self, faction_name) -> List[HistoryEvent]:
        return self._events.get(faction_name)



class CaiWorld(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._characters_paths = [get_base_name_from_path(characters_array_soup.get('path')) for characters_array_soup in self._get_characters_array_soups()]
        self._governorships_paths = [get_base_name_from_path(governorships_array_soup.get('path')) for governorships_array_soup in self._get_governorships_array_soups()]
        self._units_paths = [get_base_name_from_path(units_array_soup.get('path')) for units_array_soup in self._get_units_array_soups()]
        self._mobiles_paths = [get_base_name_from_path(mobiles_array_soup.get('path')) for mobiles_array_soup in self._get_mobiles_array_soups()]


    def _get_characters_array_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD'}).find('ary', {'type': 'CAI_WORLD_CHARACTERS'}, recursive=False)

    def _get_characters_array_soups(self):
        return self._get_characters_array_tag().find_all('xml_include', recursive=False)

    def get_characters_paths(self):
        return self._characters_paths

    def remove_characters_path(self, path):
        self._get_characters_array_tag().find('xml_include', {'path': 'cai_characters/' + path}, recursive=False).decompose()
        self._characters_paths.remove(path)

    def add_characters_path(self, path):
        insert_tag(self._get_characters_array_tag(), 'xml_include', self._soup.new_tag('xml_include', attrs={'path': 'cai_characters/' + path}), 2)
        self._characters_paths.append(path)


    def _get_governorships_array_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD'}).find('ary', {'type': 'CAI_WORLD_GOVERNORSHIPS'}, recursive=False)

    def _get_governorships_array_soups(self):
        return self._get_governorships_array_tag().find_all('xml_include', recursive=False)

    def get_governorships_paths(self):
        return self._governorships_paths

    def remove_governorships_path(self, path):
        self._get_governorships_array_tag().find('xml_include', {'path': 'cai_governorships/' + path}, recursive=False).decompose()
        self._governorships_paths.remove(path)

    def add_governorships_path(self, path):
        insert_tag(self._get_governorships_array_tag(), 'xml_include', self._soup.new_tag('xml_include', attrs={'path': 'cai_governorships/' + path}), 2)
        self._governorships_paths.append(path)


    def _get_units_array_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD'}).find('ary', {'type': 'CAI_WORLD_UNITS'}, recursive=False)

    def _get_units_array_soups(self):
        return self._get_units_array_tag().find_all('xml_include', recursive=False)

    def get_units_paths(self):
        return self._units_paths

    def remove_units_path(self, path):
        self._get_units_array_tag().find('xml_include', {'path': 'cai_units/' + path}, recursive=False).decompose()
        self._units_paths.remove(path)

    def add_units_path(self, path):
        insert_tag(self._get_units_array_tag(), 'xml_include', self._soup.new_tag('xml_include', attrs={'path': 'cai_units/' + path}), 2)
        self._units_paths.append(path)


    def _get_mobiles_array_tag(self):
        return self._soup.find('rec', {'type': 'CAI_WORLD'}).find('ary', {'type': 'CAI_WORLD_RESOURCE_MOBILES'}, recursive=False)

    def _get_mobiles_array_soups(self):
        return self._get_mobiles_array_tag().find_all('xml_include', recursive=False)

    def get_mobiles_paths(self):
        return self._mobiles_paths

    def remove_mobiles_path(self, path):
        self._get_mobiles_array_tag().find('xml_include', {'path': 'cai_mobiles/' + path}, recursive=False).decompose()
        self._mobiles_paths.remove(path)

    def add_mobiles_path(self, path):
        insert_tag(self._get_mobiles_array_tag(), 'xml_include', self._soup.new_tag('xml_include', attrs={'path': 'cai_mobiles/' + path}), 2)
        self._mobiles_paths.append(path)



# startpos/bdi_pool

class UnitAvailability:
    def __init__(self, element: etree._Element):
        self._element = element

    @cached_property
    def land_recruitment_ids_tag(self):
        return self._element.xpath("./rec[@type='CAI_UNIT_AVAILABILITY_ANALYSIS_BASE']/rec[@type='CAI_UNIT_AVAILABILITY_ANALYSIS_BASE_INFO']/u4_ary")[0]

    @property
    def land_recruitment_ids(self):
        return self.land_recruitment_ids_tag.text

    @land_recruitment_ids.setter
    def land_recruitment_ids(self, value):
        self.land_recruitment_ids_tag.text = value

    def remove_land_recruitment_id(self, land_recruitment_id):
        remove_id_from_tag_text(self.land_recruitment_ids_tag, land_recruitment_id)

    def add_land_recruitment_id(self, land_recruitment_id):
        append_id_to_tag_text(self.land_recruitment_ids_tag, land_recruitment_id, sort=False)

    @cached_property
    def naval_recruitment_ids_tag(self):
        return self._element.xpath("./rec[@type='CAI_UNIT_AVAILABILITY_ANALYSIS_BASE']/rec[@type='CAI_UNIT_AVAILABILITY_ANALYSIS_BASE_INFO']/u4_ary")[1]

    @property
    def naval_recruitment_ids(self):
        return self.naval_recruitment_ids_tag.text

    @naval_recruitment_ids.setter
    def naval_recruitment_ids(self, naval_recruitment_ids):
        self.naval_recruitment_ids_tag.text = naval_recruitment_ids

    def remove_naval_recruitment_id(self, naval_recruitment_id):
        remove_id_from_tag_text(self.naval_recruitment_ids_tag, naval_recruitment_id)

    def add_naval_recruitment_id(self, naval_recruitment_id):
        append_id_to_tag_text(self.naval_recruitment_ids_tag, naval_recruitment_id, sort=False)



class BdiPool(EsfXmlEtree):
    def __init__(self, read_xml_path: os.PathLike, write_xml_path: os.PathLike = None, create_new: bool = False):
        super().__init__(read_xml_path, write_xml_path, sub_dir='bdi_pool', create_new=create_new)
        self._unit_availabilities_region_group = []
        self._unit_availabilities_faction = []
        for unit_availability_element in self.belief_unit_availability_elements:
            if unit_availability_element.find("./rec[@type='CAI_UNIT_AVAILABILITY_ANALYSIS_REGION_GROUP']") is not None:
                unit_availability = UnitAvailability(unit_availability_element)
                self._unit_availabilities_region_group.append(unit_availability)
            if unit_availability_element.find("./rec[@type='CAI_UNIT_AVAILABILITY_ANALYSIS_FACTION']") is not None:
                unit_availability = UnitAvailability(unit_availability_element)
                self._unit_availabilities_faction.append(unit_availability)

    @cached_property
    def belief_unit_availability_elements(self) -> List[etree._Element]:
        return self._tree.xpath("/rec[@type='CAI_BDI_POOL']/ary[@type='CAI_BDI_POOL_BELIEFS']/rec[@type='CAI_BDI_POOL_BELIEFS']")

    def get_unit_availabilities_region_group(self) -> List[UnitAvailability]:
        return self._unit_availabilities_region_group

    def get_unit_availabilities_faction(self) -> List[UnitAvailability]:
        return self._unit_availabilities_faction



# startpos/save_game_header/

class SaveGameHeader(EsfXmlSoup):
    def __init__(self, read_xml_path, write_xml_path=None):
        super().__init__(read_xml_path, write_xml_path)
        self._name = self._get_name_tag().string
        self._leader_portrait = self._get_leader_portrait_tag().string
        self._n_turns = self._get_n_turns_tag().string
        self._year = self._get_year_tag().string
        self._season = self._get_season_tag().string
        self._flag = self._get_flag_tag().string

    def __str__(self):
        return '\n'.join([
            f'name                          : {self.get_name()}',
            f'leader_portrait               : {self.get_leader_portrait()}',
            f'n_turns                       : {self.get_n_turns()}',
            f'year                          : {self.get_year()}',
            f'season                        : {self.get_season()}',
            f'flag                          : {self.get_flag()}'
        ])


    def _get_name_tag(self):
        return self._soup.find('rec', {'type': 'SAVE_GAME_HEADER'}).find_all('s', recursive=False)[0]

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._get_name_tag().string = name
        self._name = name


    def _get_leader_portrait_tag(self):
        return self._soup.find('rec', {'type': 'SAVE_GAME_HEADER'}).find_all('s', recursive=False)[1]

    def get_leader_portrait(self):
        return self._leader_portrait

    def set_leader_portrait(self, leader_portrait):
        self._get_leader_portrait_tag().string = leader_portrait
        self._leader_portrait = leader_portrait


    def _get_n_turns_tag(self):
        return self._soup.find('rec', {'type': 'SAVE_GAME_HEADER'}).find_all('u', recursive=False)[0]

    def get_n_turns(self):
        return self._n_turns

    def set_n_turns(self, n_turns):
        self._get_n_turns_tag().string = n_turns
        self._n_turns = n_turns


    def _get_year_tag(self):
        return self._soup.find('rec', {'type': 'SAVE_GAME_HEADER'}).find_all('u', recursive=False)[1]

    def get_year(self):
        return self._year

    def set_year(self, year):
        self._get_year_tag().string = year
        self._year = year


    def _get_season_tag(self):
        return self._soup.find('rec', {'type': 'SAVE_GAME_HEADER'}).find_all('s', recursive=False)[2]

    def get_season(self):
        return self._season

    def set_season(self, season):
        self._get_season_tag().string = season
        self._season = season


    def _get_flag_tag(self):
        return self._soup.find('rec', {'type': 'SAVE_GAME_HEADER'}).find_all('s', recursive=False)[3]

    def get_flag(self):
        return self._flag

    def set_flag(self, flag):
        self._get_flag_tag().string = flag
        self._flag = flag



# Old model

# TODO: Remake using the new OOP model

def get_cai_fort(xml_path):
    soup = read_xml(xml_path)

    id = soup.find('rec', {'type': 'CAI_WORLD_FORTS'}).find('rec', {'type': 'CAI_FORT'}, recursive=False).find('u', recursive=False).string
    cai_id = soup.find('rec', {'type': 'CAI_WORLD_FORTS'}).find('u', recursive=False).string

    return {'id': id, 'cai_id': cai_id}

def get_cai_region_slot(xml_path):
    soup = read_xml(xml_path)

    id = soup.find('rec', {'type': 'CAI_WORLD_REGION_SLOTS'}).find('rec', {'type': 'CAI_REGION_SLOT'}, recursive=False).find('u', recursive=False).string
    cai_id = soup.find('rec', {'type': 'CAI_WORLD_REGION_SLOTS'}).find('u', recursive=False).string

    return {'id': id, 'cai_id': cai_id}
