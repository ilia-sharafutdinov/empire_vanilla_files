import os
import shutil
import builtins
import warnings
from tqdm import tqdm

from dotenv import load_dotenv
load_dotenv()

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from scripts.lib import *

from scripts.aggregators import *
from scripts.characters import *
from scripts.diplomacy import *
from scripts.factions import *
from scripts.governments import *
from scripts.miscellaneous import *
from scripts.regions import *



try:

    # Initiating

    print_block('Initiating.')

    if OUTPUT_DIR != STARTPOS_DIR:
        print('Copying startpos.')
        if os.path.exists(OUTPUT_DIR):
            shutil.rmtree(OUTPUT_DIR)
        shutil.copytree(STARTPOS_DIR, OUTPUT_DIR)

    print('Initialising global variables.')

    # https://stackoverflow.com/questions/15959534/visibility-of-global-variables-in-imported-modules
    builtins.CHARACTER_IDS = get_character_ids()
    builtins.FACTION_IDS = get_faction_ids()
    builtins.GOVERNORSHIP_IDS = get_governorship_ids()
    builtins.REGION_IDS = get_region_ids()
    builtins.REGION_SLOT_IDS = get_region_slot_ids()






    # User-defined flow start ('insert', your code here) #########################################################################

    # Factions left emergent:
    # - mughal
    # - genoa (to confederate_states?)
    # - hessen (to haiti?)
    # - hungary
    # - ireland
    # - norway (emerge them?)
    # - quebec
    # - scotland
    #
    # Factions sacrificed:
    # - crimean_khanate -> romania
    # - huron -> rajput_states
    # - inuit -> hyderabad
    # - knights_stjohn -> serbia
    # - louisiana -> british_company
    # - new_spain -> venezuela
    # - pueblo -> texas
    # - thirteen_colonies -> canada
    # - westphalia -> belgium
    #
    # Intentional brain swaps:
    # - ...genoa -> denmark -> naples_sicily ->...
    # - piedmont_savoy -> sweden -> sardinia
    # - maratha <-> punjab
    # - poland_lithuania <-> mamelukes
    # - persia <-> spain
    # - louisiana -> united_states -> mughal -> british_company



    print_block('Tweaking campaign model.')

    print('Setting starting date to 1830.')
    change_starting_date('summer', '1830')

    print('Changing victory conditions dates.')
    change_victory_conditions_date('0 (Short)', 1860)
    change_victory_conditions_date('1 (Long)', 1899)
    change_victory_conditions_date('2 (Prestige)', 1899)
    change_victory_conditions_date('3 (Global Domination)', 1899)

    print('Setting turns per year to 4.')
    change_number_of_turns_per_year(4)



    print_block('Remaking factions.')

    print('Remaking Westphalia into Belgium.')
    change_faction_key('westphalia', 'belgium')
    change_faction_capital('belgium', 'flanders')
    delete_faction_all_trade_routes('belgium')
    delete_faction_trade_route('wurttemberg', 'rhineland')
    break_trade('belgium', 'wurttemberg')
    break_trade('wurttemberg', 'belgium')

    print('Remaking Denmark into Naples & Sicily.')
    change_faction_key('naples_sicily', 'portugese_rebels')
    change_faction_key('denmark', 'naples_sicily')
    exchange_faction_victory_conditions('portugese_rebels', 'naples_sicily')
    change_faction_capital('naples_sicily', 'naples')

    print('Remaking Genoa into Denmark.')
    change_faction_key('genoa', 'denmark')
    change_faction_capital('denmark', 'denmark')
    exchange_faction_victory_conditions('portugese_rebels', 'denmark')

    print('Remaking Naples & Sicily into Genoa.')
    change_faction_key('portugese_rebels', 'genoa')

    print('Exchanging Danish and Sicilian diplomacy and international trading routes.')
    exchange_faction_diplomacy('denmark', 'naples_sicily')
    delete_faction_all_trade_routes('naples_sicily')
    delete_faction_trade_route('ottomans', 'genoa')
    delete_faction_trade_route('spain', 'genoa')
    delete_faction_trade_route('papal_states', 'genoa')
    break_trade('naples_sicily', 'ottomans')
    break_trade('naples_sicily', 'spain')
    break_trade('naples_sicily', 'papal_states')
    break_trade('ottomans', 'naples_sicily')
    break_trade('spain', 'naples_sicily')
    break_trade('papal_states', 'naples_sicily')

    print('Remaking Savoy into Sweden.')
    change_faction_key('sweden', 'portugese_rebels')
    change_faction_key('piedmont_savoy', 'sweden')
    change_faction_capital('sweden', 'sweden')

    print('Remaking Sweden into Sardinia.')
    change_faction_key('portugese_rebels', 'sardinia')
    change_faction_capital('sardinia', 'savoy', retake_region_name='the_papal_states')

    print('Exchanging Swedish and Sardinian diplomacy and international trading routes.')
    exchange_faction_victory_conditions('sweden', 'sardinia')
    exchange_faction_diplomacy('sweden', 'sardinia')

    print('Remaking Venice into Greece.')
    change_faction_key('greece', 'portugese_rebels')
    change_faction_key('venice', 'greece')
    change_faction_capital('greece', 'greece')
    delete_faction_all_trade_routes('greece')
    delete_faction_trade_route('ottomans', 'venice')
    delete_faction_trade_route('austria', 'venice')
    break_trade('greece', 'ottomans')
    break_trade('greece', 'austria')
    break_trade('ottomans', 'greece')
    break_trade('austria', 'greece')

    print('Remaking Greece into Venice.')
    change_faction_key('portugese_rebels', 'venice')

    print('Exchanging Greek and Venetian victory conditions.')
    exchange_faction_victory_conditions('greece', 'venice')

    print('Remaking Serbia into Serbia.')
    change_faction_key('knights_stjohn', 'serbia')
    change_faction_capital('serbia', 'serbia')

    print('Remaking Courland into Finland.')
    change_faction_key('courland', 'finland')
    change_faction_capital('finland', 'finland')
    delete_faction_all_trade_routes('finland')
    delete_faction_trade_route('poland_lithuania', 'courland')
    break_trade('finland', 'poland_lithuania')
    break_trade('poland_lithuania', 'finland')

    print('Remaking Crimean Khanate into Romania.')
    change_faction_key('crimean_khanate', 'romania')
    change_faction_capital('romania', 'moldavia')
    delete_faction_all_trade_routes('romania')
    delete_faction_trade_route('ottomans', 'crimea')
    break_trade('romania', 'ottomans')
    break_trade('ottomans', 'romania')
    change_character_type('crimean_khanate-assassin-0001.xml', 'rake')

    print('Remaking Huron-Wyandont into Rajput States.')
    change_faction_key('huron', 'rajput_states')
    change_faction_capital('rajput_states', 'rajpootana')

    print('Updating Russia.')
    change_faction_capital('russia', 'ingria')

    print('Emerging Punjab.')
    change_faction_playability('punjab', 'yes')
    change_faction_emergency('punjab', 'no')
    change_faction_capital('punjab', 'punjab')
    create_governorship('punjab', 'governor_india', 900001000, 800001000, 700001000, 990001000, 880001000)
    # https://en.wikipedia.org/wiki/Ranjit_Singh
    create_minister('punjab', 900001010, 990001010, government_post='faction_leader', king=True,
                    regnal_number='I', birth_season='winter', birth_year=1780, portrait_number=11, portrait_age='old')
    create_minister('punjab', 900001020, 990001020, government_post='head_of_government')
    create_minister('punjab', 900001030, 990001030, government_post='finance')
    create_minister('punjab', 900001040, 990001040, government_post='justice')
    create_minister('punjab', 900001050, 990001050, government_post='army')
    create_minister('punjab', 900001060, 990001060, government_post='navy')
    create_minister('punjab', 900001070, 990001070, government_post='accident')
    create_minister('punjab', 900001080, 990001080)
    create_minister('punjab', 900001090, 990001090)
    create_minister('punjab', 900001100, 990001100)
    create_minister('punjab', 900001110, 990001110)
    create_minister('punjab', 900001120, 990001120)

    print('Remaking Punjab into Maratha Confederacy.')
    change_faction_key('maratha', 'portugese_rebels')
    change_faction_key('punjab', 'maratha')
    change_faction_capital('maratha', 'bijapur')

    print('Remaking Maratha Confederacy into Punjab.')
    change_faction_key('portugese_rebels', 'punjab')
    change_faction_capital('punjab', 'punjab')

    print('Exchanging Marathan and Punjabi diplomacy and international trading routes.')
    exchange_faction_victory_conditions('maratha', 'punjab')
    exchange_faction_diplomacy('maratha', 'punjab')

    print('Emerging Afghanistan.')
    change_faction_playability('afghanistan', 'yes')
    change_faction_emergency('afghanistan', 'no')
    change_faction_capital('afghanistan', 'sindh', retake_region_name='afghanistan')
    create_governorship('afghanistan', 'governor_india', 900002000, 800002000, 700002000, 990002000, 880002000)
    # https://en.wikipedia.org/wiki/Dost_Mohammad_Khan
    create_minister('afghanistan', 900002010, 990002010, government_post='faction_leader', king=True,
                    forename='Mohammad', regnal_number='I', birth_season='winter', birth_year=1792, portrait_age='old', portrait_number=93)
    create_minister('afghanistan', 900002020, 990002020, government_post='head_of_government')
    create_minister('afghanistan', 900002030, 990002030, government_post='finance')
    create_minister('afghanistan', 900002040, 990002040, government_post='justice')
    create_minister('afghanistan', 900002050, 990002050, government_post='army')
    create_minister('afghanistan', 900002060, 990002060, government_post='navy')
    create_minister('afghanistan', 900002070, 990002070, government_post='accident')
    create_minister('afghanistan', 900002080, 990002080)
    create_minister('afghanistan', 900002090, 990002090)
    create_minister('afghanistan', 900002100, 990002100)
    create_minister('afghanistan', 900002110, 990002110)
    create_minister('afghanistan', 900002120, 990002120)

    print('Emerging Mamelukes.')
    change_faction_playability('mamelukes', 'yes')
    change_faction_emergency('mamelukes', 'no')
    change_faction_capital('mamelukes', 'egypt')
    delete_faction_trade_route('barbary_states', 'rumelia')
    delete_faction_trade_route('ottomans', 'tripoli')
    break_trade('barbary_states', 'ottomans')
    break_trade('ottomans', 'barbary_states')
    create_governorship('mamelukes', 'governor_europe', 900003000, 800003000, 700003000, 990003000, 880003000)
    # https://en.wikipedia.org/wiki/Muhammad_Ali_of_Egypt
    create_minister('mamelukes', 900003010, 990003010, government_post='faction_leader', king=True,
                    names_group='names_ottoman', forename='Muhammad', surname='Ali', regnal_number='I',
                    birth_season='winter', birth_year=1769, portrait_age='old')
    create_minister('mamelukes', 900003020, 990003020, government_post='head_of_government')
    create_minister('mamelukes', 900003030, 990003030, government_post='finance')
    create_minister('mamelukes', 900003040, 990003040, government_post='justice')
    create_minister('mamelukes', 900003050, 990003050, government_post='army')
    create_minister('mamelukes', 900003060, 990003060, government_post='navy')
    create_minister('mamelukes', 900003070, 990003070, government_post='accident')
    create_minister('mamelukes', 900003080, 990003080)
    create_minister('mamelukes', 900003090, 990003090)
    create_minister('mamelukes', 900003100, 990003100)
    create_minister('mamelukes', 900003110, 990003110)
    create_minister('mamelukes', 900003120, 990003120)

    print('Remaking Mamelukes into Poland-Lithuania.')
    change_faction_key('poland_lithuania', 'portugese_rebels')
    change_faction_key('mamelukes', 'poland_lithuania')
    change_faction_capital('poland_lithuania', 'poland')

    print('Remaking Poland-Lithuania into Mamelukes.')
    change_faction_key('portugese_rebels', 'mamelukes')
    change_faction_capital('mamelukes', 'egypt')

    print('Exchanging Polish and Mameluke diplomacy and international trading routes.')
    exchange_faction_victory_conditions('poland_lithuania', 'mamelukes')
    exchange_faction_diplomacy('poland_lithuania', 'mamelukes')
    delete_faction_all_trade_routes('poland_lithuania')
    delete_faction_trade_route('prussia', 'poland')
    delete_faction_trade_route('russia', 'poland')
    break_trade('poland_lithuania', 'prussia')
    break_trade('poland_lithuania', 'russia')
    break_trade('prussia', 'poland_lithuania')
    break_trade('russia', 'poland_lithuania')

    print('Remaking Inuit into Hyderabad.')
    change_faction_key('inuit', 'hyderabad')
    change_faction_capital('hyderabad', 'hyderabad')

    print('Remaking Mughal Empire into British East India Company.')
    change_faction_key('mughal', 'british_company')
    change_faction_capital('british_company', 'bengal')
    delete_faction_all_trade_routes('british_company')
    delete_faction_trade_route('safavids', 'hindustan')
    delete_faction_trade_route('netherlands', 'hindustan')
    delete_faction_trade_route('ottomans', 'hindustan')
    delete_faction_trade_route('mysore', 'hindustan')
    delete_faction_trade_route('portugal', 'hindustan')
    break_trade('british_company', 'safavids')
    break_trade('british_company', 'netherlands')
    break_trade('british_company', 'ottomans')
    break_trade('british_company', 'mysore')
    break_trade('british_company', 'portugal')
    break_trade('safavids', 'british_company')
    break_trade('netherlands', 'british_company')
    break_trade('ottomans', 'british_company')
    break_trade('mysore', 'british_company')
    break_trade('portugal', 'british_company')
    change_character_type('mughal-assassin-0002.xml', 'rake')
    change_character_type('mughal-Eastern_Scholar-0001.xml', 'gentleman')
    change_character_type('mughal-Eastern_Scholar-0002.xml', 'gentleman')
    change_character_type('mughal-middle_east_missionary-0001.xml', 'Protestant_Missionary')

    print('Remaking United States into Mughal Empire.')
    change_faction_key('united_states', 'mughal')

    print('Remaking France into Revolutionary France')
    change_faction_key('france', 'revolutionary_france')

    print('Remaking Louisiana into United States.')
    change_faction_key('louisiana', 'united_states')
    change_faction_capital('united_states', 'pennsylvania')
    delete_faction_all_trade_routes('united_states')
    delete_faction_trade_route('cherokee', 'lower_louisiana')
    delete_faction_trade_route('revolutionary_france', 'lower_louisiana')
    break_trade('united_states', 'cherokee')
    break_trade('united_states', 'revolutionary_france')
    break_trade('cherokee', 'united_states')
    break_trade('revolutionary_france', 'united_states')
    change_character_type('louisiana-catholic_missionary-0001.xml', 'Protestant_Missionary')

    print('Remaking Thirteen Colonies into Canada.')
    change_faction_key('thirteen_colonies', 'canada')
    change_faction_capital('canada', 'new_france')
    delete_faction_all_trade_routes('canada')
    delete_faction_trade_route('cherokee', 'pennsylvania')
    delete_faction_trade_route('britain', 'pennsylvania')
    break_trade('canada', 'cherokee')
    break_trade('canada', 'britain')
    break_trade('cherokee', 'canada')
    break_trade('britain', 'canada')

    print('Remaking New Spain into Venezuela.')
    change_faction_key('new_spain', 'venezuela')

    print('Emerging México.')
    change_faction_playability('mexico', 'yes')
    change_faction_emergency('mexico', 'no')
    change_faction_capital('mexico', 'new_spain')
    delete_faction_all_trade_routes('venezuela')
    delete_faction_trade_route('spain', 'new_spain')
    break_trade('venezuela', 'spain')
    break_trade('spain', 'venezuela')
    create_governorship('mexico', 'governor_america', 900004000, 800004000, 700004000, 990004000, 880004000)
    # https://en.wikipedia.org/wiki/Anastasio_Bustamante
    create_minister('mexico', 900004010, 990004010, government_post='faction_leader', birth_season='summer', birth_year=1780, portrait_age='old')
    create_minister('mexico', 900004020, 990004020, government_post='head_of_government')
    create_minister('mexico', 900004030, 990004030, government_post='finance')
    create_minister('mexico', 900004040, 990004040, government_post='justice')
    create_minister('mexico', 900004050, 990004050, government_post='army')
    create_minister('mexico', 900004060, 990004060, government_post='navy')
    create_minister('mexico', 900004070, 990004070, government_post='accident')
    create_minister('mexico', 900004080, 990004080)
    create_minister('mexico', 900004090, 990004090)
    create_minister('mexico', 900004100, 990004100)
    create_minister('mexico', 900004110, 990004110)
    create_minister('mexico', 900004120, 990004120)

    print('Emerging Gran Colombia.')
    change_faction_playability('colombia', 'yes')
    change_faction_emergency('colombia', 'no')
    change_faction_capital('colombia', 'new_grenada')
    create_governorship('colombia', 'governor_america', 900005000, 800005000, 700005000, 990005000, 880005000)
    # https://en.wikipedia.org/wiki/Francisco_de_Paula_Santander (since 1832)
    create_minister('colombia', 900005010, 990005010, government_post='faction_leader', birth_season='winter', birth_year=1792, portrait_age='young')
    create_minister('colombia', 900005020, 990005020, government_post='head_of_government')
    create_minister('colombia', 900005030, 990005030, government_post='finance')
    create_minister('colombia', 900005040, 990005040, government_post='justice')
    create_minister('colombia', 900005050, 990005050, government_post='army')
    create_minister('colombia', 900005060, 990005060, government_post='navy')
    create_minister('colombia', 900005070, 990005070, government_post='accident')
    create_minister('colombia', 900005080, 990005080)
    create_minister('colombia', 900005090, 990005090)
    create_minister('colombia', 900005100, 990005100)
    create_minister('colombia', 900005110, 990005110)
    create_minister('colombia', 900005120, 990005120)

    print('Remaking Pueblo into Texas.')
    change_faction_key('pueblo', 'texas')
    change_faction_capital('texas', 'tejas')

    # EXPERIMENTAL PART START

    # print('Remaking Spain into Persia.')
    # change_faction_key('safavids', 'portugese_rebels')
    # change_faction_key('spain', 'safavids')
    # change_faction_capital('safavids', 'persia')

    # print('Remaking Persia into Spain.')
    # change_faction_key('portugese_rebels', 'spain')
    # change_faction_capital('spain', 'spain')

    # print('Exchanging Spanish and Persian diplomacy and international trading routes.')
    # exchange_faction_victory_conditions('spain', 'safavids')
    # exchange_faction_diplomacy('spain', 'safavids')

    # EXPERIMENTAL PART END

    print('Remaking Pirates into Jihadists.')
    change_faction_key('pirates', 'jihadists')



    print_block('Updating factions.')

    print('Changing faction government types.')
    pbar = tqdm(total=27)
    change_faction_government_type('bavaria', 'gov_constitutional_monarchy'); pbar.update() # since 1808
    change_faction_government_type('colombia', 'gov_republic'); pbar.update()
    change_faction_government_type('denmark', 'gov_absolute_monarchy'); pbar.update()
    change_faction_government_type('revolutionary_france', 'gov_constitutional_monarchy'); pbar.update() # since 1815
    change_faction_government_type('genoa', 'gov_constitutional_monarchy'); pbar.update()
    change_faction_government_type('hannover', 'gov_constitutional_monarchy'); pbar.update() # since 1819
    change_faction_government_type('hessen', 'gov_constitutional_monarchy'); pbar.update() # since 1820
    change_faction_government_type('texas', 'gov_republic'); pbar.update()
    change_faction_government_type('hungary', 'gov_constitutional_monarchy'); pbar.update()
    change_faction_government_type('ireland', 'gov_constitutional_monarchy'); pbar.update()
    change_faction_government_type('mexico', 'gov_republic'); pbar.update()
    change_faction_government_type('mughal', 'gov_absolute_monarchy'); pbar.update()
    change_faction_government_type('naples_sicily', 'gov_absolute_monarchy'); pbar.update()
    change_faction_government_type('netherlands', 'gov_constitutional_monarchy'); pbar.update() # since 1815
    change_faction_government_type('venezuela', 'gov_republic'); pbar.update()
    change_faction_government_type('poland_lithuania', 'gov_republic'); pbar.update()
    change_faction_government_type('portugal', 'gov_constitutional_monarchy'); pbar.update() # since 1834
    change_faction_government_type('quebec', 'gov_republic'); pbar.update()
    change_faction_government_type('saxony', 'gov_constitutional_monarchy'); pbar.update() # since 1831
    change_faction_government_type('scotland', 'gov_constitutional_monarchy'); pbar.update()
    change_faction_government_type('spain', 'gov_constitutional_monarchy'); pbar.update() # since 1837
    change_faction_government_type('sweden', 'gov_constitutional_monarchy'); pbar.update() # since 1809
    change_faction_government_type('british_company', 'gov_republic'); pbar.update()
    change_faction_government_type('united_states', 'gov_republic'); pbar.update()
    change_faction_government_type('venice', 'gov_constitutional_monarchy'); pbar.update()
    change_faction_government_type('belgium', 'gov_constitutional_monarchy'); pbar.update()
    change_faction_government_type('wurttemberg', 'gov_constitutional_monarchy'); pbar.update() # since 1819
    pbar.close()

    print('Changing faction religions.')
    pbar = tqdm(total=21)
    change_faction_religion('rajput_states', 'rel_hindu'); pbar.update()
    change_faction_religion('denmark', 'rel_protestant'); pbar.update()
    change_faction_religion('greece', 'rel_orthodox'); pbar.update()
    change_faction_religion('texas', 'rel_protestant'); pbar.update()
    change_faction_religion('hyderabad', 'rel_islamic'); pbar.update()
    change_faction_religion('serbia', 'rel_orthodox'); pbar.update()
    change_faction_religion('maratha', 'rel_hindu'); pbar.update()
    change_faction_religion('romania', 'rel_orthodox'); pbar.update()
    change_faction_religion('mughal', 'rel_islamic'); pbar.update()
    change_faction_religion('mamelukes', 'rel_islamic'); pbar.update()
    change_faction_religion('naples_sicily', 'rel_catholic'); pbar.update()
    change_faction_religion('sardinia', 'rel_catholic'); pbar.update()
    change_faction_religion('jihadists', 'rel_islamic'); pbar.update()
    change_faction_religion('poland_lithuania', 'rel_catholic'); pbar.update()
    change_faction_religion('punjab', 'rel_sikh'); pbar.update()
    change_faction_religion('safavids', 'rel_islamic'); pbar.update()
    change_faction_religion('spain', 'rel_catholic'); pbar.update()
    change_faction_religion('sweden', 'rel_protestant'); pbar.update()
    change_faction_religion('british_company', 'rel_protestant'); pbar.update()
    change_faction_religion('united_states', 'rel_protestant'); pbar.update()
    change_faction_religion('venice', 'rel_catholic'); pbar.update()
    pbar.close()

    print('Changing faction campaign AIs.')
    change_faction_campaign_ai('afghanistan', new_manager='FULL', new_personality='non_euro')
    change_faction_campaign_ai('austria', new_manager='FULL', new_personality='continental_progressive')
    change_faction_campaign_ai('barbary_states', new_manager='FULL', new_personality='non_euro')
    change_faction_campaign_ai('bavaria', new_manager='FULL', new_personality='continental_repressive')
    change_faction_campaign_ai('britain', new_manager='FULL', new_personality='maritime_progressive')
    change_faction_campaign_ai('chechenya_dagestan', new_manager='FULL', new_personality='non_euro')
    change_faction_campaign_ai('cherokee', new_manager='FULL', new_personality='new_age')
    change_faction_campaign_ai('colombia', new_manager='FULL', new_personality='continental_progressive')
    change_faction_campaign_ai('finland', new_manager='FULL', new_personality='default')
    change_faction_campaign_ai('rajput_states', new_manager='FULL', new_personality='non_euro')
    change_faction_campaign_ai('denmark', new_manager='FULL', new_personality='maritime_progressive')
    change_faction_campaign_ai('revolutionary_france', new_manager='FULL', new_personality='mixed_progressive')
    change_faction_campaign_ai('genoa', new_manager='FULL', new_personality='trader')
    change_faction_campaign_ai('georgia', new_manager='FULL', new_personality='non_euro')
    change_faction_campaign_ai('greece', new_manager='FULL', new_personality='mixed_repressive')
    change_faction_campaign_ai('hannover', new_manager='FULL', new_personality='trader')
    change_faction_campaign_ai('hessen', new_manager='FULL', new_personality='continental_progressive')
    change_faction_campaign_ai('texas', new_manager='FULL', new_personality='continental_repressive')
    change_faction_campaign_ai('hungary', new_manager='FULL', new_personality='continental_repressive')
    change_faction_campaign_ai('ireland', new_manager='FULL', new_personality='default')
    change_faction_campaign_ai('iroquoi', new_manager='FULL', new_personality='new_age')
    change_faction_campaign_ai('hyderabad', new_manager='FULL', new_personality='non_euro')
    change_faction_campaign_ai('serbia', new_manager='FULL', new_personality='continental_repressive')
    change_faction_campaign_ai('mamelukes', new_manager='FULL', new_personality='continental_repressive')
    change_faction_campaign_ai('maratha', new_manager='FULL', new_personality='continental_progressive')
    change_faction_campaign_ai('romania', new_manager='FULL', new_personality='continental_repressive')
    change_faction_campaign_ai('mexico', new_manager='FULL', new_personality='continental_repressive')
    change_faction_campaign_ai('morocco', new_manager='FULL', new_personality='non_euro')
    change_faction_campaign_ai('mughal', new_manager='FULL', new_personality='continental_repressive')
    change_faction_campaign_ai('mysore', new_manager='FULL', new_personality='non_euro')
    change_faction_campaign_ai('naples_sicily', new_manager='FULL', new_personality='mixed_repressive')
    change_faction_campaign_ai('netherlands', new_manager='FULL', new_personality='trader')
    change_faction_campaign_ai('venezuela', new_manager='FULL', new_personality='continental_repressive')
    change_faction_campaign_ai('norway', new_manager='FULL', new_personality='default')
    change_faction_campaign_ai('ottomans', new_manager='FULL', new_personality='continental_repressive')
    change_faction_campaign_ai('papal_states', new_manager='FULL', new_personality='mixed_repressive')
    change_faction_campaign_ai('sardinia', new_manager='FULL', new_personality='mixed_progressive')
    change_faction_campaign_ai('jihadists', new_manager='FULL', new_personality='pirates')
    change_faction_campaign_ai('plains', new_manager='FULL', new_personality='new_age')
    change_faction_campaign_ai('poland_lithuania', new_manager='FULL', new_personality='continental_progressive')
    change_faction_campaign_ai('portugal', new_manager='FULL', new_personality='maritime_repressive')
    change_faction_campaign_ai('prussia', new_manager='FULL', new_personality='industrialist')
    change_faction_campaign_ai('punjab', new_manager='FULL', new_personality='continental_progressive')
    change_faction_campaign_ai('quebec', new_manager='FULL', new_personality='continental_progressive')
    change_faction_campaign_ai('russia', new_manager='FULL', new_personality='continental_repressive')
    change_faction_campaign_ai('safavids', new_manager='FULL', new_personality='continental_repressive')
    change_faction_campaign_ai('saxony', new_manager='FULL', new_personality='continental_repressive')
    change_faction_campaign_ai('scotland', new_manager='FULL', new_personality='default')
    change_faction_campaign_ai('spain', new_manager='FULL', new_personality='maritime_repressive')
    change_faction_campaign_ai('sweden', new_manager='FULL', new_personality='industrialist')
    change_faction_campaign_ai('british_company', new_manager='FULL', new_personality='continental_repressive')
    change_faction_campaign_ai('canada', new_manager='FULL', new_personality='continental_repressive')
    change_faction_campaign_ai('united_states', new_manager='FULL', new_personality='industrialist')
    change_faction_campaign_ai('venice', new_manager='FULL', new_personality='trader')
    change_faction_campaign_ai('belgium', new_manager='FULL', new_personality='trader')
    change_faction_campaign_ai('wurttemberg', new_manager='FULL', new_personality='industrialist')



    print_block('Changing ownerships.')

    print('Giving Flanders to Belgium.')
    hand_over_region('flanders', 'belgium')
    hand_over_character('spain-General-0002.xml', 'belgium')
    change_character_name('spain-General-0002.xml')

    print('Giving Rhineland to Prussia.')
    hand_over_region('rhineland', 'prussia')
    hand_over_character('westphalia-General-0001.xml', 'prussia')
    change_character_name('westphalia-General-0001.xml')

    print('Giving Silesia to Prussia.')
    hand_over_region('silesia', 'prussia')
    hand_over_character('austria-General-0003.xml', 'prussia')
    change_character_name('austria-General-0003.xml')

    print('Giving West Prussia to Prussia.')
    hand_over_region('west_prussia', 'prussia')

    print('Giving Greece to Greece.')
    hand_over_region('greece', 'greece')
    hand_over_character('ottomans-colonel-0003.xml', 'greece')
    change_character_name('ottomans-colonel-0003.xml')
    change_army_unit_type('ottomans-colonel-0003.xml', ['euro_militia_infantry', 'euro_militia_infantry', 'euro_pikemen'])

    print('Giving Venice to Austria.')
    hand_over_region('venice', 'austria')
    hand_over_character('venice-General-0001.xml', 'austria')
    change_character_name('venice-General-0001.xml')

    print('Giving Milan to Austria.')
    hand_over_region('milan', 'austria')
    hand_over_character('spain-General-0003.xml', 'austria')
    change_character_name('spain-General-0003.xml')

    print('Giving Galicia to Austria.')
    hand_over_region('galicia', 'austria')
    hand_over_character('poland_lithuania-colonel-0001.xml', 'austria')
    hand_over_character('poland_lithuania-General-0001.xml', 'austria')
    change_character_name('poland_lithuania-colonel-0001.xml')
    change_character_name('poland_lithuania-General-0001.xml')

    print('Giving Finland to Finland')
    hand_over_region('finland', 'finland')
    hand_over_character('sweden-colonel-0003.xml', 'finland')
    hand_over_character('sweden-Protestant_Missionary-0001.xml', 'finland')
    hand_over_character('sweden-rake-0001.xml', 'finland')
    change_character_name('sweden-colonel-0003.xml')
    change_character_name('sweden-Protestant_Missionary-0001.xml')
    change_character_name('sweden-rake-0001.xml')

    print('Giving Courland to Russia.')
    hand_over_region('courland', 'russia')
    hand_over_character('courland-General-0001.xml', 'russia')
    change_character_name('courland-General-0001.xml')

    print('Giving Estonia and Livonia to Russia.')
    hand_over_region('estonia_and_livonia', 'russia')
    hand_over_character('sweden-General-0001.xml', 'russia')
    change_character_name('sweden-General-0001.xml')

    print('Giving Ingria to Russia.')
    hand_over_region('ingria', 'russia')
    hand_over_character('sweden-colonel-0001.xml', 'russia')
    hand_over_character('sweden-General-0002.xml', 'russia')
    change_character_name('sweden-colonel-0001.xml')
    change_character_name('sweden-General-0002.xml')

    print('Giving Lithuania to Russia.')
    hand_over_region('lithuania', 'russia')
    hand_over_character('poland_lithuania-colonel-0002.xml', 'russia')
    hand_over_character('poland_lithuania-General-0003.xml', 'russia')
    change_character_name('poland_lithuania-colonel-0002.xml')
    change_character_name('poland_lithuania-General-0003.xml')

    print('Giving Belarus to Russia.')
    hand_over_region('belarus', 'russia')

    print('Giving Moldavia to Romania.')
    hand_over_region('moldavia', 'romania')
    hand_over_character('ottomans-General-0002.xml', 'romania')
    change_character_name('ottomans-General-0002.xml')
    change_character_portrait('ottomans-General-0002.xml')
    change_army_unit_type('ottomans-General-0002.xml', ['euro_generals_bodyguard', 'euro_dragoons',
                                                        'pandours', 'euro_pikemen', 'euro_militia_infantry'])

    print('Giving Crimea to Russia.')
    hand_over_region('crimea', 'russia')
    hand_over_character('crimean_khanate-General-0001.xml', 'russia')
    change_character_name('crimean_khanate-General-0001.xml')
    change_character_portrait('crimean_khanate-General-0001.xml')
    change_army_unit_type('crimean_khanate-General-0001.xml', ['euro_generals_bodyguard', 'cossack_cavalry',
                                                               'cossack_infantry', 'cossack_infantry'])

    print('Giving Don Voisko to Dagestan.')
    hand_over_region('don_voisko', 'chechenya_dagestan')

    print('Giving Egypt to Mamelukes.')
    hand_over_region('egypt', 'mamelukes')

    print('Giving Palestine to Mamelukes.')
    hand_over_region('palestine', 'mamelukes')

    print('Giving Poland to Poland-Lithuania')
    hand_over_region('poland', 'poland_lithuania')
    hand_over_character('poland_lithuania-catholic_missionary-0001.xml', 'poland_lithuania')
    hand_over_character('poland_lithuania-General-0002.xml', 'poland_lithuania')
    hand_over_character('poland_lithuania-gentleman-0001.xml', 'poland_lithuania')
    hand_over_character('poland_lithuania-rake-0001.xml', 'poland_lithuania')
    change_character_name('poland_lithuania-catholic_missionary-0001.xml')
    change_character_name('poland_lithuania-General-0002.xml')
    change_character_name('poland_lithuania-gentleman-0001.xml')
    change_character_name('poland_lithuania-rake-0001.xml')

    print('Giving Serbia to Serbia.')
    hand_over_region('serbia', 'serbia')
    hand_over_character('ottomans-colonel-0001.xml', 'serbia')
    hand_over_character('ottomans-colonel-0006.xml', 'serbia')
    change_character_name('ottomans-colonel-0001.xml')
    change_character_name('ottomans-colonel-0006.xml')
    change_army_unit_type('ottomans-colonel-0001.xml', ['euro_pikemen'])
    change_army_unit_type('ottomans-colonel-0006.xml', ['euro_militia_infantry'])
    add_army_unit('ottomans-colonel-0001.xml', 'euro_provincial_cavalry', 600000000, 660000000)
    add_army_unit('ottomans-colonel-0001.xml', 'euro_militia_infantry', 600000005, 660000005)

    print('Giving Malta to Great Britain.')
    hand_over_region('malta', 'britain')
    hand_over_character('knights_stjohn-admiral-0001.xml', 'britain')
    hand_over_character('knights_stjohn-General-0001.xml', 'britain')
    change_character_name('knights_stjohn-admiral-0001.xml')
    change_character_name('knights_stjohn-General-0001.xml')

    print('Giving Gibraltar to Great Britain.')
    hand_over_region('gibraltar', 'britain')

    print('Creating a British Indian governorship.')
    # https://en.wikipedia.org/wiki/Neil_B._Edmonstone
    create_governorship('britain', 'governor_india', 900000000, 800000000, 700000000, 990000000, 880000000,
                        birth_season='winter', birth_year=1765, portrait_age='old')

    print('Giving Gujarat to Great Britain.')
    hand_over_region('gujarat', 'britain')
    hand_over_character('mughal-colonel-0003.xml', 'britain')
    change_character_name('mughal-colonel-0003.xml')
    change_army_unit_type('mughal-colonel-0003.xml', ['euro_company_infantry_e_india_co', 'euro_pikemen'])

    print('Giving Punjab to Punjab.')
    hand_over_region('punjab', 'punjab')

    print('Giving Kashmir to Punjab.')
    hand_over_region('kashmir', 'punjab')

    print('Giving Afghanistan to Afghanistan.')
    hand_over_region('afghanistan', 'afghanistan')
    hand_over_character('mughal-assassin-0001.xml', 'afghanistan')
    hand_over_character('safavids-colonel-0001.xml', 'afghanistan')
    hand_over_character('safavids-colonel-0002.xml', 'afghanistan')
    hand_over_character('safavids-Eastern_Scholar-0002.xml', 'afghanistan')
    change_character_name('mughal-assassin-0001.xml')
    change_character_name('safavids-colonel-0001.xml')
    change_character_name('safavids-colonel-0002.xml')
    change_character_name('safavids-Eastern_Scholar-0002.xml')

    print('Giving Sindh to Afghanistan.')
    hand_over_region('sindh', 'afghanistan')
    hand_over_character('mughal-assassin-0001.xml', 'safavids')
    change_character_name('mughal-assassin-0001.xml')

    # EXPERIMENTAL PART START

    # print('Giving Balochistan to Afghanistan.')
    # hand_over_region('baluchistan', 'afghanistan')

    # print('Changing Spanish Indian governorship to American.')
    # change_governorship_theatre('spain', 'governor_india', 'governor_america')

    # print('Giving Cuba to Spain.')
    # hand_over_region('cuba', 'spain')
    # hand_over_character('spain-admiral-0001.xml', 'spain')
    # hand_over_character('spain-colonel-0003.xml', 'spain')
    # change_character_name('spain-admiral-0001.xml')
    # change_character_name('spain-colonel-0003.xml')

    # print('Giving Hispaniola to Spain.')
    # hand_over_region('hispaniola', 'spain')
    # hand_over_character('spain-colonel-0002.xml', 'spain')
    # change_character_name('spain-colonel-0002.xml')

    # print('Giving Florida to Spain.')
    # hand_over_region('florida', 'spain', ignore_not_enough_regions=True)
    # hand_over_character('spain-catholic_missionary-0001.xml', 'spain')
    # hand_over_character('spain-colonel-0004.xml', 'spain')
    # change_character_name('spain-catholic_missionary-0001.xml')
    # change_character_name('spain-colonel-0004.xml')

    # print('Changing Persian American governorship to Indian.')
    # change_governorship_theatre('safavids', 'governor_america', 'governor_india')

    # print('Changing Spanish American governorship to Indian.')
    # change_governorship_theatre('spain', 'governor_america', 'governor_india')

    # print('Giving Balochistan to Persia.')
    # hand_over_region('baluchistan', 'safavids')

    # print('Giving Afghanistan to Persia.')
    # hand_over_region('afghanistan', 'safavids')
    # hand_over_character('safavids-colonel-0001.xml', 'safavids')
    # hand_over_character('safavids-colonel-0002.xml', 'safavids')
    # hand_over_character('safavids-Eastern_Scholar-0002.xml', 'safavids')
    # change_character_name('safavids-colonel-0001.xml')
    # change_character_name('safavids-colonel-0002.xml')
    # change_character_name('safavids-Eastern_Scholar-0002.xml')

    # print('Changing Spanish Indian governorship to American.')
    # change_governorship_theatre('spain', 'governor_india', 'governor_america')

    # print('Disabling Persian Indian governorship.')
    # disable_governorship('safavids', 'governor_india')
    # change_character_birth_date('spain-minister-0009.xml', 'summer', 1730)

    # print('Giving Spain to Spain.')
    # hand_over_region('spain', 'spain', ignore_not_enough_regions=True)
    # hand_over_character('spain-admiral-0002.xml', 'spain')
    # hand_over_character('spain-catholic_missionary-0002.xml', 'spain')
    # hand_over_character('spain-colonel-0001.xml', 'spain')
    # hand_over_character('spain-General-0001.xml', 'spain')
    # hand_over_character('spain-gentleman-0001.xml', 'spain')
    # hand_over_character('spain-rake-0001.xml', 'spain')
    # change_character_name('spain-admiral-0002.xml')
    # change_character_name('spain-catholic_missionary-0002.xml')
    # change_character_name('spain-colonel-0001.xml')
    # change_character_name('spain-General-0001.xml')
    # change_character_name('spain-gentleman-0001.xml')
    # change_character_name('spain-rake-0001.xml')

    # print('Giving Persia to Persia.')
    # hand_over_region('persia', 'safavids')
    # hand_over_character('safavids-admiral-0001.xml', 'safavids')
    # hand_over_character('safavids-assassin-0001.xml', 'safavids')
    # hand_over_character('safavids-Eastern_Scholar-0001.xml', 'safavids')
    # hand_over_character('safavids-General-0001.xml', 'safavids')
    # change_character_name('safavids-admiral-0001.xml')
    # change_character_name('safavids-assassin-0001.xml')
    # change_character_name('safavids-Eastern_Scholar-0001.xml')
    # change_character_name('safavids-General-0001.xml')

    # print('Giving Azerbaijan to Persia.')
    # hand_over_region('azerbaijan', 'safavids')
    # hand_over_character('safavids-General-0002.xml', 'safavids')
    # change_character_name('safavids-General-0002.xml')

    # EXPERIMENTAL PART END

    print('Giving Sweden to Sweden.')
    hand_over_region('sweden', 'sweden', ignore_not_enough_regions=True)
    hand_over_character('sweden-admiral-0001.xml', 'sweden')
    hand_over_character('sweden-colonel-0002.xml', 'sweden')
    hand_over_character('sweden-General-0003.xml', 'sweden')
    hand_over_character('sweden-gentleman-0001.xml', 'sweden')
    change_character_name('sweden-admiral-0001.xml')
    change_character_name('sweden-colonel-0002.xml')
    change_character_name('sweden-General-0003.xml')
    change_character_name('sweden-gentleman-0001.xml')

    print('Giving Norway to Sweden.')
    hand_over_region('norway', 'sweden')
    hand_over_character('denmark-colonel-0001.xml', 'sweden')
    change_character_name('denmark-colonel-0001.xml')

    print('Giving Savoy to Sardinia.')
    hand_over_region('savoy', 'sardinia')
    hand_over_character('piedmont_savoy-General-0001.xml', 'sardinia')
    hand_over_character('piedmont_savoy-gentleman-0001.xml', 'sardinia')
    hand_over_character('piedmont_savoy-rake-0001.xml', 'sardinia')
    change_character_name('piedmont_savoy-General-0001.xml')
    change_character_name('piedmont_savoy-gentleman-0001.xml')
    change_character_name('piedmont_savoy-rake-0001.xml')

    print('Giving Sardinia to Sardinia.')
    hand_over_region('sardinia', 'sardinia')

    print('Giving Genoa to Sardinia.')
    hand_over_region('genoa', 'sardinia')
    hand_over_character('genoa-admiral-0001.xml', 'sardinia')
    hand_over_character('genoa-General-0001.xml', 'sardinia')
    change_character_name('genoa-admiral-0001.xml')
    change_character_name('genoa-General-0001.xml')

    print('Giving Corsica to France.')
    hand_over_region('corsica', 'revolutionary_france', ignore_not_enough_regions=True)

    print('Giving Denmark to Denmark.')
    hand_over_region('denmark', 'denmark')
    hand_over_character('denmark-admiral-0001.xml', 'denmark')
    hand_over_character('denmark-General-0001.xml', 'denmark')
    hand_over_character('denmark-gentleman-0001.xml', 'denmark')
    change_character_name('denmark-admiral-0001.xml')
    change_character_name('denmark-General-0001.xml')
    change_character_name('denmark-gentleman-0001.xml')

    print('Giving Iceland to Denmark.')
    hand_over_region('iceland', 'denmark', ignore_not_enough_regions=True)

    print('Giving Naples to Naples & Sicily.')
    hand_over_region('naples', 'naples_sicily')
    hand_over_character('genoa-gentleman-0001.xml', 'naples_sicily')
    hand_over_character('genoa-rake-0001.xml', 'naples_sicily')
    change_character_name('genoa-gentleman-0001.xml')
    change_character_name('genoa-rake-0001.xml')

    print('Giving New Spain to Mexico.')
    hand_over_region('new_spain', 'mexico')
    hand_over_character('new_spain-catholic_missionary-0001.xml', 'mexico')
    hand_over_character('new_spain-General-0001.xml', 'mexico')
    hand_over_character('new_spain-rake-0001.xml', 'mexico')
    change_character_name('new_spain-catholic_missionary-0001.xml')
    change_character_name('new_spain-General-0001.xml')
    change_character_name('new_spain-rake-0001.xml')

    print('Giving New Mexico to Mexico.')
    hand_over_region('new_mexico', 'mexico')

    print('Creating a Belgian American governorship.')
    # https://en.wikipedia.org/wiki/Belgian_colonial_empire#Santo_Tom%C3%A1s,_Guatemala_(1843%E2%80%931854) (since 1843)
    create_governorship('belgium', 'governor_america', 901000000, 801000000, 701000000, 991000000, 881000000)

    print('Giving Guatemala to Belgium.')
    hand_over_region('guatemala', 'belgium')

    print('Giving New Grenada to Gran Colombia.')
    hand_over_region('new_grenada', 'colombia')
    hand_over_character('new_spain-colonel-0002.xml', 'colombia')
    hand_over_character('new_spain-General-0002.xml', 'colombia')
    change_character_name('new_spain-colonel-0002.xml')
    change_character_name('new_spain-General-0002.xml')

    print('Giving Panama to Gran Colombia.')
    hand_over_region('panama', 'colombia')

    print('Giving Labrador to Canada.')
    hand_over_region('labrador', 'canada', ignore_not_enough_regions=True)

    print('Changing Texas minor governor building.')
    change_region_slot_building('settlement:tejas:villa_de_bexar:settlement_minor', 'minor_magistrate', 'texas', 'gov_republic')

    print('Changing troop types in Texan army.')
    change_army_unit_type('pueblo-General-0001.xml', ['euro_generals_bodyguard', 'euro_provincial_cavalry', 'euro_pikemen', 'euro_pikemen',
                                                      'euro_militia_infantry_colonial_militia', 'euro_militia_infantry_colonial_militia'])

    print('Changing Hyderabad American governorship into Indian.')
    change_governorship_theatre('hyderabad', 'governor_america', 'governor_india')

    print('Giving Hyderabad to Hyderabad.')
    hand_over_region('hyderabad', 'hyderabad')
    hand_over_character('mughal-colonel-0004.xml', 'hyderabad')
    change_character_name('mughal-colonel-0004.xml')

    print('Handing a Marathan general to British East India Company.')
    hand_over_character('maratha-General-0001.xml', 'british_company')
    change_character_name('maratha-General-0001.xml')
    change_character_portrait('maratha-General-0001.xml')
    change_character_location('maratha-General-0001.xml', 'bengal', 619.239990234375, 172.52999877929688)
    change_army_unit_type(
        'maratha-General-0001.xml',
        ['euro_generals_bodyguard', 'euro_lancers_east_india_company_lancers', 'euro_sepoys',
         'euro_sepoys', 'euro_pikemen', 'euro_militia_infantry_colonial_militia'])

    print('Giving Huron Territory to Canada.')
    hand_over_region('huron_territory', 'canada')
    change_region_slot_building('settlement:huron_territory:fort_sault_ste-marie:settlement_minor', 'minor_magistrate', 'canada', 'gov_constitutional_monarchy')
    hand_over_character('huron-General-0001.xml', 'canada')
    change_character_name('huron-General-0001.xml')
    change_character_portrait('huron-General-0001.xml')
    change_army_unit_type('huron-General-0001.xml', ['euro_generals_bodyguard', 'euro_militia_infantry_colonial_militia',
                                                     'euro_militia_infantry_colonial_militia', 'euro_provincial_cavalry', 'euro_militia_infantry_colonial_militia',
                                                     'euro_pikemen', 'euro_pikemen'])

    print('Giving Northwest Territories to Canada.')
    hand_over_region('northwest_territories', 'canada', ignore_not_enough_regions=True)
    change_region_slot_building('settlement:northwest_territories:york_factory:settlement_minor', 'minor_magistrate', 'canada', 'gov_constitutional_monarchy')

    print('Giving Newfoundland to Canada.')
    hand_over_region('newfoundland', 'canada')

    print('Giving Acadia to Canada.')
    hand_over_region('acadia', 'canada')

    print('Giving New France to Canada.')
    hand_over_region('new_france', 'canada')
    hand_over_character('france-admiral-0001.xml', 'canada')
    change_character_name('france-admiral-0001.xml')

    print('Giving Upper Canada to Canada.')
    hand_over_region('ontario', 'canada')
    hand_over_character('france-catholic_missionary-0002.xml', 'canada')
    hand_over_character('france-General-0002.xml', 'canada')
    change_character_type('france-catholic_missionary-0002.xml', 'Protestant_Missionary')
    change_character_name('france-catholic_missionary-0002.xml')
    change_character_name('france-General-0002.xml')
    change_character_portrait('france-catholic_missionary-0002.xml')

    print('Giving Rupert\'s Land to Canada.')
    hand_over_region('ruperts_land', 'canada')
    hand_over_character('britain-colonel-0002.xml', 'canada')
    hand_over_character('britain-Protestant_Missionary-0001.xml', 'canada')
    change_character_name('britain-colonel-0002.xml')
    change_character_name('britain-Protestant_Missionary-0001.xml')

    print('Giving Maine to United States.')
    hand_over_region('maine', 'united_states')

    print('Giving Confederation of New England to United States.')
    hand_over_region('new_england', 'united_states')
    hand_over_character('thirteen_colonies-colonel-0001.xml', 'united_states')
    change_character_name('thirteen_colonies-colonel-0001.xml')

    print('Giving New York to United States.')
    hand_over_region('new_york', 'united_states')

    print('Giving Pennsylvania to United States.')
    hand_over_region('pennsylvania', 'united_states')
    hand_over_character('thirteen_colonies-colonel-0002.xml', 'united_states')
    hand_over_character('thirteen_colonies-Protestant_Missionary-0002.xml', 'united_states')
    change_character_name('thirteen_colonies-colonel-0002.xml')
    change_character_name('thirteen_colonies-Protestant_Missionary-0002.xml')

    print('Giving Maryland to United States.')
    hand_over_region('maryland', 'united_states')

    print('Giving Virginia to United States.')
    hand_over_region('virginia', 'united_states')

    print('Giving Carolinas to United States.')
    hand_over_region('carolinas', 'united_states')
    hand_over_character('thirteen_colonies-General-0001.xml', 'united_states')
    hand_over_character('thirteen_colonies-Protestant_Missionary-0001.xml', 'united_states')
    change_character_name('thirteen_colonies-General-0001.xml')
    change_character_name('thirteen_colonies-Protestant_Missionary-0001.xml')

    print('Giving Georgia to United States.')
    hand_over_region('georgia_usa', 'united_states')
    change_region_slot_building('settlement:georgia_usa:savannah:settlement_minor', 'minor_magistrate', 'united_states', 'gov_republic')
    hand_over_character('cherokee-colonel-0001.xml', 'united_states')
    change_character_name('cherokee-colonel-0001.xml')
    change_army_unit_type('cherokee-colonel-0001.xml', ['euro_rangers', 'euro_militia_infantry_colonial_militia', 'euro_pikemen', 'euro_pikemen'])

    print('Changing Rajput American governorship into Indian.')
    change_governorship_theatre('rajput_states', 'governor_america', 'governor_india')

    print('Giving Rajputana to Rajput States.')
    hand_over_region('rajpootana', 'rajput_states')
    hand_over_character('mughal-colonel-0005.xml', 'rajput_states')
    change_character_name('mughal-colonel-0005.xml')
    hand_over_character('mughal-middle_east_missionary-0002.xml', 'afghanistan')
    change_character_name('mughal-middle_east_missionary-0002.xml')

    print('Giving Malwa to Rajput States.')
    hand_over_region('malwa', 'rajput_states')
    hand_over_character('mughal-colonel-0001.xml', 'rajput_states')
    change_character_name('mughal-colonel-0001.xml')

    print('Giving Ahmadnagar to Maratha Confederacy.')
    hand_over_region('ahmadnagar', 'maratha')
    hand_over_character('maratha-General-0003.xml', 'maratha')
    hand_over_character('mughal-colonel-0002.xml', 'maratha')
    hand_over_character('mughal-General-0001.xml', 'afghanistan')
    hand_over_character('mughal-General-0002.xml', 'punjab')
    change_character_name('maratha-General-0003.xml')
    change_character_name('mughal-colonel-0002.xml')
    change_character_name('mughal-General-0001.xml')
    change_character_name('mughal-General-0002.xml')
    change_character_portrait('maratha-General-0003.xml')
    change_character_portrait('mughal-General-0001.xml')
    change_character_portrait('mughal-General-0002.xml')
    change_army_unit_type('mughal-colonel-0002.xml', ['east_irregular_cavalry_pindari', 'east_ethnic_musketeers_bargir'])
    change_army_unit_type('mughal-General-0002.xml', ['indian_generals_bodyguard', 'east_sikh_warriors',
                                                      'east_sikh_infantry_musketeers', 'east_sikh_infantry_musketeers'])
    add_army_unit('mughal-General-0002.xml', '24_lber_land_cannon_(demi_cannon)_indian', 600000010, 660000010)
    add_army_unit('mughal-General-0002.xml', 'east_lancers_silladar', 600000015, 660000015)
    add_army_unit('mughal-General-0002.xml', 'east_irregular_cavalry_pindari', 600000020, 660000020)
    add_army_unit('mughal-General-0002.xml', 'east_ethnic_musketmen_hindu_musketeers', 600000025, 660000025)
    add_army_unit('mughal-General-0001.xml', 'east_lancers', 600000030, 660000030)
    add_army_unit('mughal-General-0001.xml', 'east_ethnic_hillmen_musketeers_afghan', 600000035, 660000035)
    add_army_unit('mughal-General-0001.xml', 'east_ethnic_hillmen_musketeers_afghan', 600000040, 660000040)
    add_army_unit('mughal-General-0001.xml', 'east_ethnic_swordsmen_islamic_swordsmen', 600000045, 660000045)
    change_character_location('mughal-General-0001.xml', 'sindh', 490.6145191192627, 174.39988231658936)
    change_character_location('mughal-General-0002.xml', 'punjab', 533.4486083984375, 214.8444061279297)

    print('Giving Bijapur to Maratha Confederacy.')
    hand_over_region('bijapur', 'maratha')
    hand_over_character('maratha-assassin-0001.xml', 'maratha')
    hand_over_character('maratha-indian_missionary-0001.xml', 'maratha')
    hand_over_character('maratha-colonel-0002.xml', 'maratha')
    hand_over_character('maratha-Eastern_Scholar-0001.xml', 'maratha')
    hand_over_character('maratha-General-0002.xml', 'maratha')
    change_character_name('maratha-assassin-0001.xml')
    change_character_name('maratha-indian_missionary-0001.xml')
    change_character_name('maratha-colonel-0002.xml')
    change_character_name('maratha-Eastern_Scholar-0001.xml')
    change_character_name('maratha-General-0002.xml')

    print('Giving Leeward Islands to Great Britain.')
    hand_over_region('leeward_islands', 'britain')

    print('Giving Trinidad & Tobago to Great Britain.')
    hand_over_region('trinidad_tobago', 'britain', ignore_not_enough_regions=True)

    print('Changing Jihadist American governorship into Indian.')
    change_governorship_theatre('jihadists', 'governor_america', 'governor_india')

    print('Giving Carnatica to Netherlands.')
    hand_over_region('carnatica', 'netherlands')
    hand_over_character('maratha-colonel-0001.xml', 'netherlands')
    change_character_name('maratha-colonel-0001.xml')
    change_army_unit_type('maratha-colonel-0001.xml', ['euro_company_infantry_voc_infantry'])

    print('Giving Ceylon to Jihadists.')
    hand_over_region('ceylon', 'jihadists')
    change_faction_capital('jihadists', 'ceylon')
    change_character_type('netherlands-Protestant_Missionary-0001.xml', 'middle_east_missionary')
    hand_over_character('netherlands-captain-0001.xml', 'jihadists')
    hand_over_character('netherlands-General-0002.xml', 'jihadists')
    hand_over_character('netherlands-Protestant_Missionary-0001.xml', 'jihadists')
    change_character_name('netherlands-captain-0001.xml')
    change_character_name('netherlands-General-0002.xml')
    change_character_name('netherlands-Protestant_Missionary-0001.xml')
    change_character_portrait('netherlands-General-0002.xml')
    change_character_portrait('netherlands-Protestant_Missionary-0001.xml')
    change_army_unit_type('netherlands-General-0002.xml', ['east_generals_bodyguard', 'east_ethnic_warriors_barbary_pirates'])

    # print('Moving a French general to Algeria.')
    # change_character_location('france-General-0003.xml', 'algiers', 10.778590202331543, 255.64031600952148)
    # change_army_unit_type('france-General-0003.xml', ['euro_generals_bodyguard', 'euro_provincial_cavalry_gendarmerie', '24_lber_land_cannon_(demi_cannon)', 'euro_pikemen', 'euro_militia_infantry_colonial_militia'])
    # add_army_unit('france-General-0003.xml', 'euro_company_infantry_french_eic', 600000050, 660000050)
    # add_army_unit('france-General-0003.xml', 'euro_pikemen', 600000055, 660000055)
    # add_army_unit('france-General-0003.xml', 'euro_african_infantry', 600000060, 660000060)
    # add_army_unit('france-General-0003.xml', 'euro_company_cavalry_french_eic', 600000065, 660000065)



    print_block('Customising characters.')

    print('Customising characters of Persia.')
    change_faction_randomise_all_character_names('safavids')
    change_faction_randomise_all_character_portraits('safavids')
    # https://en.wikipedia.org/wiki/Fath-Ali_Shah_Qajar (till 1834)
    change_character_birth_date('safavids-minister-0003.xml', 'summer', 1769)

    print('Customising characters of Spain.')
    change_faction_randomise_all_character_names('spain')
    change_faction_randomise_all_character_portraits('spain')
    # https://en.wikipedia.org/wiki/Ferdinand_VII_of_Spain (till 1833)
    change_character_name('spain-minister-0001.xml', names_group='names_spanish', forename='Ferdinand', regnal_number='VII')
    change_character_birth_date('spain-minister-0001.xml', 'winter', 1784)

    print('Customising characters of Poland-Lithuania.')
    change_faction_randomise_all_character_names('poland_lithuania')
    change_faction_randomise_all_character_portraits('poland_lithuania')
    # https://en.wikipedia.org/wiki/Adam_Jerzy_Czartoryski
    change_character_name('mamelukes-minister-0002.xml', names_group='names_polish', forename='Adam', surname='Czartoryski', regnal_number='')
    change_character_birth_date('mamelukes-minister-0002.xml', 'winter', 1770)
    change_character_portrait('mamelukes-minister-0002.xml', faction_leader=True, portrait_age='old')

    print('Customising characters of Mamelukes.')
    change_faction_randomise_all_character_names('mamelukes')
    change_faction_randomise_all_character_portraits('mamelukes')
    # https://en.wikipedia.org/wiki/Muhammad_Ali_of_Egypt
    change_character_name('poland_lithuania-minister-0004.xml', names_group='names_ottoman', forename='Muhammad', surname='Ali', regnal_number='I')
    change_character_birth_date('poland_lithuania-minister-0004.xml', 'winter', 1769)
    change_character_portrait('poland_lithuania-minister-0004.xml', faction_leader=True, king=True, portrait_age='old')

    print('Customising characters of Maratha Confederacy.')
    change_faction_randomise_all_character_names('maratha')
    change_faction_randomise_all_character_portraits('maratha')

    print('Customising characters of Punjab.')
    change_faction_randomise_all_character_names('punjab')
    change_faction_randomise_all_character_portraits('punjab')
    # https://en.wikipedia.org/wiki/Ranjit_Singh
    change_character_portrait('maratha-minister-0001.xml', faction_leader=True, king=True, portrait_age='old', portrait_number=11)
    change_character_birth_date('maratha-minister-0001.xml', 'winter', 1780)

    print('Customising characters of Hyderabad.')
    change_faction_randomise_all_character_names('hyderabad')
    change_faction_randomise_all_character_portraits('hyderabad')
    # https://en.wikipedia.org/wiki/Nasir-ud-Daulah
    change_character_name('inuit-minister-0001.xml', names_group='names_persian', forename='Naser', regnal_number='I')
    change_character_birth_date('inuit-minister-0001.xml', 'summer', 1794)
    change_character_portrait('inuit-minister-0001.xml', faction_leader=True, king=True, portrait_age='young', portrait_number=15)

    print('Customising characters of Rajput States.')
    change_faction_randomise_all_character_names('rajput_states')
    change_faction_randomise_all_character_portraits('rajput_states')
    # https://en.wikipedia.org/wiki/Man_Singh_of_Marwar https://en.wikipedia.org/wiki/Kingdom_of_Marwar
    # https://en.wikipedia.org/wiki/Jawan_Singh https://en.wikipedia.org/wiki/Kingdom_of_Mewar
    change_character_name('huron-minister-0001.xml', surname='', regnal_number='I')
    change_character_birth_date('huron-minister-0001.xml')

    print('Customising characters of British East India Company.')
    change_faction_randomise_all_character_names('british_company')
    change_faction_randomise_all_character_portraits('british_company')
    # https://en.wikipedia.org/wiki/Neil_B._Edmonstone
    change_character_name('mughal-minister-0001.xml')
    change_character_birth_date('mughal-minister-0001.xml', 'winter', 1765)
    change_character_portrait('mughal-minister-0001.xml', faction_leader=True, portrait_age='old')

    print('Customising characters of Canada.')
    change_faction_randomise_all_character_names('canada')
    change_faction_randomise_all_character_portraits('canada')

    print('Customising characters of United States.')
    change_faction_randomise_all_character_names('united_states')
    change_faction_randomise_all_character_portraits('united_states')

    print('Customising characters of Texas.')
    change_faction_randomise_all_character_names('texas')
    change_faction_randomise_all_character_portraits('texas')
    # https://en.wikipedia.org/wiki/Sam_Houston
    change_character_name('pueblo-minister-0001.xml', names_group='names_english', forename='Samuel')
    change_character_birth_date('pueblo-minister-0001.xml', 'summer', 1793)
    change_character_portrait('pueblo-minister-0001.xml', faction_leader=True, portrait_age='young')

    print('Customising characters of Russia.')
    change_faction_randomise_all_character_names('russia')
    # https://en.wikipedia.org/wiki/Nicholas_I_of_Russia
    change_character_name('russia-minister-0004.xml', names_group='names_english', forename='Nicholas', regnal_number='I')
    change_character_birth_date('russia-minister-0004.xml', 'summer', 1796)

    print('Customising characters of Finland.')
    change_faction_randomise_all_character_names('finland')
    # https://en.wikipedia.org/wiki/Alexander_Sergeyevich_Menshikov
    change_character_name('courland-minister-0001.xml', names_group='names_slavonic_general', forename='Alexander', surname='Menshikov')
    change_character_birth_date('courland-minister-0001.xml', 'summer', 1787)

    print('Customising characters of Sweden.')
    change_faction_randomise_all_character_names('sweden')
    # https://en.wikipedia.org/wiki/Charles_XIV_John
    change_character_name('piedmont_savoy-minister-0001.xml', names_group='names_swedish', forename='Charles', regnal_number='XIV')
    change_character_birth_date('piedmont_savoy-minister-0001.xml', 'winter', 1763)

    print('Customising characters of Denmark.')
    change_faction_randomise_all_character_names('denmark')
    # https://en.wikipedia.org/wiki/Frederick_VI_of_Denmark
    change_character_name('genoa-minister-0001.xml', names_group='names_swedish', forename='Frederick', regnal_number='VI')
    change_character_birth_date('genoa-minister-0001.xml', 'winter', 1768)

    print('Customising characters of Romania.')
    change_faction_randomise_all_character_names('romania')
    change_faction_randomise_all_character_portraits('romania')
    # https://en.wikipedia.org/wiki/Alexandru_II_Ghica
    change_character_name('crimean_khanate-minister-0001.xml', regnal_number='I')
    change_character_birth_date('crimean_khanate-minister-0001.xml', 'winter', 1796)

    print('Customising characters of Serbia.')
    change_faction_randomise_all_character_names('serbia')
    # https://en.wikipedia.org/wiki/Milo%C5%A1_Obrenovi%C4%87,_Prince_of_Serbia
    change_character_name('knights_stjohn-minister-0001.xml', names_group='names_polish')
    change_character_birth_date('knights_stjohn-minister-0001.xml', 'winter', 1780)

    print('Customising characters of Greece.')
    change_faction_randomise_all_character_names('greece')
    # https://en.wikipedia.org/wiki/Ioannis_Kapodistrias
    # change_character_name('venice-minister-0001.xml', names_group='names_german_catholic', forename='Ioannis', surname='Kapodistrias')
    # change_character_birth_date('venice-minister-0001.xml', 'winter', 1776)
    # change_character_portrait('venice-minister-0001.xml', portrait_age='old', portrait_number=88)
    # https://en.wikipedia.org/wiki/Otto_of_Greece (since 1832)
    change_character_name('venice-minister-0001.xml', names_group='names_german_catholic', forename='Otto', regnal_number='I')
    change_character_birth_date('venice-minister-0001.xml', 'summer', 1815)
    change_character_portrait('venice-minister-0001.xml', faction_leader=True, king=True, portrait_age='young', portrait_number=24)

    print('Customising characters of Sardinia.')
    change_faction_randomise_all_character_names('sardinia')
    # https://en.wikipedia.org/wiki/Charles_Felix_of_Sardinia
    change_character_name('sweden-minister-0001.xml', names_group='names_english', forename='Charles', regnal_number='I')
    change_character_birth_date('sweden-minister-0001.xml', 'winter', 1765)

    print('Customising characters of Naples & Sicily.')
    change_faction_randomise_all_character_names('naples_sicily')
    # https://en.wikipedia.org/wiki/Ferdinand_II_of_the_Two_Sicilies
    change_character_name('denmark-minister-0001.xml', names_group='names_italian', forename='Ferdinand', regnal_number='II')
    change_character_birth_date('denmark-minister-0001.xml', 'winter', 1810)

    print('Customising characters of Belgium.')
    change_faction_randomise_all_character_names('belgium')
    # https://en.wikipedia.org/wiki/Leopold_I_of_Belgium
    change_character_name('westphalia-minister-0001.xml', names_group='names_german_catholic', forename='Leopold', regnal_number='I')
    change_character_birth_date('westphalia-minister-0001.xml', 'winter', 1790)
    change_character_portrait('westphalia-minister-0001.xml', faction_leader=True, king=True, portrait_age='old', portrait_number=3)

    print('Customising characters of Jihadists.')
    change_faction_randomise_all_character_names('jihadists')
    change_faction_randomise_all_character_portraits('jihadists')



    print_block('Changing construction.')

    print('Replacing school in Rhineland with metal workshops.')
    change_region_slot_building('town:rhineland:marburg', 'craft_workshops_metal', 'prussia', 'gov_absolute_monarchy')

    print('Constructing a shipyard in Denmark.')
    emerge_port('port:denmark:lubeck', 1, 500000000)
    change_region_slot_building('port:denmark:lubeck', 'shipyard', 'denmark', 'gov_absolute_monarchy')

    print('Constructing a school in Savoy.')
    emerge_town('town:savoy:chieri', 1)
    change_region_slot_building('town:savoy:chieri', 'school', 'sardinia', 'gov_absolute_monarchy')

    # print('Replacing church in Italian States with a school.')
    # change_region_slot_building('town:the_papal_states:bologna', 'school', 'papal_states', 'gov_absolute_monarchy')

    print('Replacing school in Poland with a coaching inn.')
    change_region_slot_building('town:poland:cracow', 'coaching_inn', 'poland_lithuania', 'gov_republic')

    print('Replacing school in Georgia with a church.')
    change_region_slot_building('town:georgia:suhumkale', 'rel_orthodox_0', 'georgia', 'gov_absolute_monarchy')

    print('Replacing mosque in Punjab with textiles workshop.')
    change_region_slot_building('town:punjab:kasur', 'craft_workshops_textiles', 'punjab', 'gov_absolute_monarchy')

    print('Replacing minor magistrate in Afghanistan with a minor governor\'s encampment.')
    change_region_slot_building('settlement:afghanistan:kabul:settlement_minor', 'minor_governors_encampment', 'afghanistan', 'gov_absolute_monarchy')

    print('Replacing minor magistrate in Balochistan with a minor governor\'s encampment.')
    change_region_slot_building('settlement:baluchistan:zahedan:settlement_minor', 'minor_governors_encampment', 'safavids', 'gov_absolute_monarchy')

    print('Replacing minor magistrate in Sindh with a minor governor\'s encampment.')
    change_region_slot_building('settlement:sindh:neroon_kot:settlement_minor', 'minor_governors_encampment', 'afghanistan', 'gov_absolute_monarchy')

    print('Replacing minor magistrate in Rajputana with a minor governor\'s encampment.')
    change_region_slot_building('settlement:rajpootana:udaipur:settlement_minor', 'minor_governors_encampment', 'rajput_states', 'gov_absolute_monarchy')

    print('Constructing an army barracks in Punjab.')
    change_region_slot_building('settlement:punjab:lahore:settlement_army-admin', 'army_barracks', 'punjab', 'gov_absolute_monarchy')

    print('Constructing a cannon foundry in Punjab.')
    change_region_slot_building('settlement:punjab:lahore:settlement_ordnance', 'cannon_foundry', 'punjab', 'gov_absolute_monarchy')

    print('Constructing an army barracks in Bengal.')
    change_region_slot_building('settlement:bengal:calcutta:settlement_army-admin', 'army_barracks', 'british_company', 'gov_republic')

    print('Constructing a cannon foundry in Bengal.')
    change_region_slot_building('settlement:bengal:calcutta:settlement_ordnance', 'cannon_foundry', 'british_company', 'gov_republic')

    print('Constructing a shool in Persia.')
    emerge_town('town:persia:qom', 1)
    change_region_slot_building('town:persia:qom', 'school', 'safavids', 'gov_absolute_monarchy')

    print('Replacing minor magistrate in Goa with a minor governor\'s encampment.')
    change_region_slot_building('settlement:malabar:goa:settlement_minor', 'minor_governors_encampment', 'portugal', 'gov_constitutional_monarchy')

    print('Constructing a trading port in Mysore.')
    emerge_port('port:mysore:mangalore', 4, 500000005)
    change_region_slot_building('port:mysore:mangalore', 'trading_port', 'mysore', 'gov_absolute_monarchy')

    print('Constructing an army barracks in Egypt.')
    change_region_slot_building('settlement:egypt:cairo:settlement_army-admin', 'army_barracks', 'mamelukes', 'gov_absolute_monarchy')

    print('Increasing prosperity of Asyut in Egypt.')
    change_town_prosperity('town:egypt:asyut', 5)

    print('Replacing coaching inn in Egypt with a school.')
    change_region_slot_building('town:egypt:luxor', 'school', 'mamelukes', 'gov_absolute_monarchy')

    print('Constructing a trading port in Egypt.')
    emerge_port('port:egypt:alexandria', 5, 500000010)
    change_region_slot_building('port:egypt:alexandria', 'trading_port', 'mamelukes', 'gov_absolute_monarchy')

    print('Replacing minor governor\'s encampment in Leeward Islands with a minor magistrate.')
    change_region_slot_building('settlement:leeward_islands:antigua:settlement_minor', 'minor_magistrate', 'britain', 'gov_constitutional_monarchy')

    print('Replacing shipyard in Leeward Islands with a trading port.')
    change_region_slot_building('port:leeward_islands:guadeloupe', 'trading_port', 'pirates', 'gov_absolute_monarchy')

    print('Replacing shipyard in Trinidad & Tobago with a trading port.')
    change_region_slot_building('port:trinidad_tobago:puerto_de_espana', 'trading_port', 'pirates', 'gov_absolute_monarchy')

    print('Replacing trading port in Ceylon with a shipyard.')
    change_region_slot_building('port:ceylon:colombo', 'shipyard', 'jihadists', 'gov_absolute_monarchy')



    print_block('Updating region rebels.')

    print('Changing regions\' rebelling factions.')
    change_region_rebels('bahamas', 'amerind_rebels')
    change_region_rebels('baluchistan', 'persian_rebels')
    change_region_rebels('bengal', 'mughal')
    change_region_rebels('berar', 'mughal')
    change_region_rebels('carolinas', 'american_rebels')
    change_region_rebels('ceylon', 'jihadists')
    change_region_rebels('courland', 'prussian_rebels')
    change_region_rebels('crimea', 'slavic_rebels')
    change_region_rebels('cuba', 'amerind_rebels')
    change_region_rebels('curacao', 'amerind_rebels')
    change_region_rebels('finland', 'finland')
    change_region_rebels('flanders', 'belgium')
    change_region_rebels('hindustan', 'mughal')
    change_region_rebels('hispaniola', 'amerind_rebels')
    change_region_rebels('huron_territory', 'amerind_rebels')
    change_region_rebels('hyderabad', 'hyderabad')
    change_region_rebels('ingria', 'russia')
    change_region_rebels('jamaica', 'amerind_rebels')
    change_region_rebels('kashmir', 'afghanistan')
    change_region_rebels('labrador', 'amerind_rebels')
    change_region_rebels('leeward_islands', 'amerind_rebels')
    change_region_rebels('maine', 'american_rebels')
    change_region_rebels('malta', 'italian_rebels')
    change_region_rebels('malwa', 'mughal')
    change_region_rebels('maryland', 'american_rebels')
    change_region_rebels('mesopotamia', 'ottoman_rebels')
    change_region_rebels('moldavia', 'romania')
    change_region_rebels('morea', 'greek_rebels')
    change_region_rebels('muscovy', 'slavic_rebels')
    change_region_rebels('new_andalusia', 'venezuela')
    change_region_rebels('new_england', 'american_rebels')
    change_region_rebels('new_mexico', 'amerind_rebels')
    change_region_rebels('new_york', 'american_rebels')
    change_region_rebels('northwest_territories', 'amerind_rebels')
    change_region_rebels('orissa', 'mughal')
    change_region_rebels('pennsylvania', 'american_rebels')
    change_region_rebels('rajpootana', 'rajput_states')
    change_region_rebels('serbia', 'serbia')
    change_region_rebels('sindh', 'afghanistan')
    change_region_rebels('tejas', 'texas')
    change_region_rebels('the_papal_states', 'sardinia')
    change_region_rebels('trinidad_tobago', 'amerind_rebels')
    change_region_rebels('virginia', 'american_rebels')
    change_region_rebels('west_prussia', 'prussian_rebels')
    change_region_rebels('windward_islands', 'amerind_rebels')

    print('Adding unit resources to Ceylon.')
    add_region_unit_resource('ceylon', 'camels')
    add_region_unit_resource('ceylon', 'desert')
    add_region_unit_resource('ceylon', 'med_coast')
    add_region_unit_resource('ceylon', 'galleys')



    print_block('Tweaking diplomacy.')

    print('Breaking old protectorates.')
    break_protectorate('united_states')
    break_protectorate('venezuela')
    break_protectorate('barbary_states')
    break_protectorate('finland')
    break_protectorate('saxony')
    break_protectorate('romania')

    print('Making new protectorates.')
    make_protectorate('britain', 'british_company')
    make_protectorate('revolutionary_france', 'belgium')
    make_protectorate('russia', 'finland')
    make_protectorate('russia', 'georgia')
    make_protectorate('mexico', 'texas')
    make_protectorate('austria', 'naples_sicily')

    print('Enabling new protectorates diplomacy.')
    enable_protectorate_diplomacy('british_company')
    enable_protectorate_diplomacy('canada')
    enable_protectorate_diplomacy('belgium')
    enable_protectorate_diplomacy('finland')
    enable_protectorate_diplomacy('georgia')
    enable_protectorate_diplomacy('texas')
    enable_protectorate_diplomacy('naples_sicily')

    print('Breaking old alliances.')
    make_neutral('britain', 'austria')
    make_neutral('sardinia', 'austria')
    make_neutral('bavaria', 'austria')
    make_neutral('wurttemberg', 'austria')
    make_neutral('spain', 'bavaria')
    make_neutral('denmark', 'russia')
    make_neutral('poland_lithuania', 'russia')
    make_neutral('poland_lithuania', 'denmark')
    make_neutral('belgium', 'wurttemberg')
    make_neutral('hannover', 'belgium')
    make_neutral('britain', 'netherlands')

    print('Stopping old wars.')
    make_neutral('russia', 'ottomans')
    make_neutral('russia', 'romania')
    make_neutral('plains', 'spain')
    make_neutral('cherokee', 'venezuela')
    make_neutral('maratha', 'british_company')

    print('Making new alliances')
    make_alliance('russia', 'serbia')
    # make_alliance('russia', 'prussia')
    # make_alliance('russia', 'austria')
    make_alliance('prussia', 'austria')
    make_alliance('romania', 'ottomans')
    make_alliance('romania', 'britain')
    make_alliance('romania', 'revolutionary_france')
    make_alliance('romania', 'sardinia')
    make_alliance('bavaria', 'wurttemberg')
    make_alliance('wurttemberg', 'revolutionary_france')
    make_alliance('britain', 'revolutionary_france')
    # make_alliance('ottomans', 'britain')
    # make_alliance('ottomans', 'revolutionary_france')
    make_alliance('sardinia', 'revolutionary_france')
    make_alliance('maratha', 'mysore')
    make_alliance('maratha', 'rajput_states')
    make_alliance('maratha', 'netherlands')
    make_alliance('hyderabad', 'mysore')
    make_alliance('hyderabad', 'rajput_states')
    make_alliance('hyderabad', 'afghanistan')
    make_alliance('punjab', 'rajput_states')
    make_alliance('punjab', 'mysore')
    make_alliance('mamelukes', 'safavids')
    make_alliance('mamelukes', 'morocco')
    make_alliance('safavids', 'chechenya_dagestan')

    print('Making new wars.')
    make_war('russia', 'chechenya_dagestan')
    make_war('russia', 'safavids')
    make_war('russia', 'poland_lithuania')
    make_war('georgia', 'safavids')
    make_war('punjab', 'british_company')
    make_war('britain', 'afghanistan')
    make_war('mexico', 'barbary_states')
    make_war('colombia', 'barbary_states')
    make_war('romania', 'barbary_states')
    make_war('texas', 'barbary_states')
    make_war('british_company', 'barbary_states')
    make_war('britain', 'mamelukes')
    make_war('revolutionary_france', 'mamelukes')

    print('Setting military access.')

    set_military_access('united_states', 'revolutionary_france', 0)
    set_military_access('canada', 'britain', 0)
    set_military_access('venezuela', 'spain', 0)
    set_military_access('saxony', 'poland_lithuania', 0)
    set_military_access('finland', 'poland_lithuania', 0)
    set_military_access('romania', 'ottomans', 0)
    set_military_access('barbary_states', 'ottomans', 0)
    set_military_access('belgium', 'austria', 0)
    set_military_access('wurttemberg', 'austria', 0)
    set_military_access('greece', 'austria', 0)
    set_military_access('naples_sicily', 'spain', 0)
    set_military_access('papal_states', 'spain', 0)

    print('Setting attitudes.')

    set_total_attitude('russia', 'romania', -85)
    set_total_attitude('russia', 'ottomans', -85)
    set_total_attitude('russia', 'britain', -85)
    set_total_attitude('russia', 'revolutionary_france', -45)
    set_total_attitude('russia', 'sardinia', -45)
    set_total_attitude('russia', 'finland', -45)
    set_total_attitude('russia', 'sweden', -45)
    set_total_attitude('russia', 'prussia', 0)
    set_total_attitude('russia', 'austria', 45)
    set_total_attitude('russia', 'georgia', -45)
    set_historical_attitude('russia', 'safavids', 0)
    set_historical_attitude('russia', 'chechenya_dagestan', 0)
    set_historical_attitude('russia', 'poland_lithuania', 0)

    set_total_attitude('romania', 'russia', -85)

    set_total_attitude('safavids', 'ottomans', -85)
    set_total_attitude('safavids', 'afghanistan', -45)
    set_total_attitude('safavids', 'punjab', -45)
    set_total_attitude('safavids', 'hyderabad', 45)
    set_total_attitude('safavids', 'mysore', 45)
    set_total_attitude('safavids', 'mamelukes', 45)
    set_total_attitude('safavids', 'maratha', 0)
    set_total_attitude('safavids', 'rajput_states', -45)
    set_historical_attitude('safavids', 'russia', 0)
    set_historical_attitude('safavids', 'georgia', 0)

    set_total_attitude('ottomans', 'russia', -85)
    set_total_attitude('ottomans', 'mamelukes', -85)
    set_total_attitude('ottomans', 'safavids', -45)
    set_total_attitude('ottomans', 'georgia', -85)
    set_total_attitude('ottomans', 'chechenya_dagestan', -45)
    set_total_attitude('ottomans', 'romania', 0)
    set_total_attitude('ottomans', 'serbia', -85)
    set_total_attitude('ottomans', 'britain', 85)
    set_total_attitude('ottomans', 'revolutionary_france', 45)
    set_total_attitude('ottomans', 'sardinia', -85)
    set_total_attitude('ottomans', 'austria', -85)
    set_total_attitude('ottomans', 'papal_states', -85)
    set_total_attitude('ottomans', 'naples_sicily', 0)
    set_total_attitude('ottomans', 'barbary_states', 0)
    set_total_attitude('ottomans', 'morocco', -85)
    set_total_attitude('ottomans', 'mysore', 45)
    set_total_attitude('ottomans', 'hyderabad', 45)

    set_total_attitude('mamelukes', 'ottomans', -85)
    set_total_attitude('mamelukes', 'safavids', 0)
    set_total_attitude('mamelukes', 'barbary_states', -85)
    set_total_attitude('mamelukes', 'morocco', 45)
    set_total_attitude('mamelukes', 'hyderabad', 45)
    set_total_attitude('mamelukes', 'mysore', 45)
    set_total_attitude('mamelukes', 'britain', -45)
    set_total_attitude('mamelukes', 'revolutionary_france', -45)
    set_total_attitude('mamelukes', 'afghanistan', -45)

    set_total_attitude('barbary_states', 'mamelukes', -85)
    set_total_attitude('barbary_states', 'morocco', 0)

    set_total_attitude('morocco', 'barbary_states', 0)
    set_total_attitude('morocco', 'mamelukes', 45)
    set_total_attitude('morocco', 'revolutionary_france', -85)
    set_total_attitude('morocco', 'prussia', 85)

    set_total_attitude('afghanistan', 'british_company', -85)
    set_total_attitude('afghanistan', 'punjab', 45)
    set_total_attitude('afghanistan', 'rajput_states', -85)
    set_total_attitude('afghanistan', 'hyderabad', 85)
    set_total_attitude('afghanistan', 'mysore', 45)
    set_total_attitude('afghanistan', 'ottomans', 0)
    set_total_attitude('afghanistan', 'safavids', -85)
    set_total_attitude('afghanistan', 'maratha', -85)
    set_total_attitude('afghanistan', 'mamelukes', 0)
    set_historical_attitude('afghanistan', 'britain', 0)

    set_total_attitude('punjab', 'afghanistan', 45)
    set_total_attitude('punjab', 'britain', -45)
    set_total_attitude('punjab', 'rajput_states', 85)
    set_total_attitude('punjab', 'maratha', 45)
    set_total_attitude('punjab', 'hyderabad', 0)
    set_total_attitude('punjab', 'mysore', 0)
    set_total_attitude('punjab', 'ottomans', -45)
    set_historical_attitude('punjab', 'british_company', 0)

    set_total_attitude('revolutionary_france', 'russia', -85)
    set_total_attitude('revolutionary_france', 'britain', -45)
    set_total_attitude('revolutionary_france', 'prussia', -85)
    set_total_attitude('revolutionary_france', 'austria', -85)
    set_total_attitude('revolutionary_france', 'sardinia', 85)
    set_total_attitude('revolutionary_france', 'belgium', 85)
    set_total_attitude('revolutionary_france', 'mexico', -85)
    set_total_attitude('revolutionary_france', 'ottomans', 0)
    set_total_attitude('revolutionary_france', 'morocco', -85)
    set_total_attitude('revolutionary_france', 'netherlands', -45)
    set_historical_attitude('revolutionary_france', 'mamelukes', 0)

    set_total_attitude('britain', 'russia', -85)
    set_total_attitude('britain', 'revolutionary_france', 0)
    set_total_attitude('britain', 'denmark', 45)
    set_total_attitude('britain', 'sardinia', 0)
    set_total_attitude('britain', 'prussia', -85)
    set_total_attitude('britain', 'austria', -45)
    set_total_attitude('britain', 'ottomans', -85)
    set_total_attitude('britain', 'punjab', -85)
    set_total_attitude('britain', 'maratha', 45)
    set_total_attitude('britain', 'mysore', 0)
    set_total_attitude('britain', 'hyderabad', 0)
    set_total_attitude('britain', 'canada', 0)
    set_total_attitude('britain', 'united_states', -85)
    set_total_attitude('britain', 'greece', 45)
    set_total_attitude('britain', 'netherlands', 0)
    set_historical_attitude('britain', 'afghanistan', 0)
    set_historical_attitude('britain', 'mamelukes', 0)

    set_total_attitude('prussia', 'russia', -45)
    set_total_attitude('prussia', 'austria', 0)
    set_total_attitude('prussia', 'revolutionary_france', -85)
    set_total_attitude('prussia', 'britain', -85)
    set_total_attitude('prussia', 'sweden', 0)
    set_total_attitude('prussia', 'denmark', 0)
    set_total_attitude('prussia', 'saxony', -85)
    set_total_attitude('prussia', 'wurttemberg', -85)
    set_total_attitude('prussia', 'hannover', -85)
    set_total_attitude('prussia', 'bavaria', -85)
    set_total_attitude('prussia', 'morocco', 85)
    set_total_attitude('prussia', 'sardinia', 45)

    set_total_attitude('austria', 'sardinia', -85)
    set_total_attitude('austria', 'russia', 0)
    set_total_attitude('austria', 'britain', -45)
    set_total_attitude('austria', 'revolutionary_france', -45)
    set_total_attitude('austria', 'serbia', -85)
    set_total_attitude('austria', 'greece', 0)
    set_total_attitude('austria', 'romania', 0)
    set_total_attitude('austria', 'ottomans', -45)
    set_total_attitude('austria', 'papal_states', -45)
    set_total_attitude('austria', 'naples_sicily', 0)
    set_total_attitude('austria', 'netherlands', -45)

    set_total_attitude('sardinia', 'austria', -85)
    set_total_attitude('sardinia', 'russia', -85)
    set_total_attitude('sardinia', 'prussia', 85)
    set_total_attitude('sardinia', 'britain', -45)
    set_total_attitude('sardinia', 'revolutionary_france', 85)
    set_total_attitude('sardinia', 'papal_states', -85)
    set_total_attitude('sardinia', 'naples_sicily', -85)
    set_total_attitude('sardinia', 'ottomans', -85)
    set_total_attitude('sardinia', 'greece', 85)
    set_total_attitude('sardinia', 'serbia', 45)
    set_total_attitude('sardinia', 'mamelukes', 0)
    set_total_attitude('sardinia', 'morocco', -85)

    set_total_attitude('papal_states', 'sardinia', -85)
    set_total_attitude('papal_states', 'greece', -45)

    set_total_attitude('greece', 'papal_states', -45)
    set_total_attitude('greece', 'britain', 45)

    set_total_attitude('british_company', 'maratha', -85)
    set_total_attitude('british_company', 'britain', -45)
    set_total_attitude('british_company', 'rajput_states', -45)
    set_total_attitude('british_company', 'mysore', 45)
    set_total_attitude('british_company', 'hyderabad', -85)
    set_total_attitude('british_company', 'afghanistan', 45)
    set_total_attitude('british_company', 'safavids', 0)
    set_total_attitude('british_company', 'ottomans', 0)
    set_total_attitude('british_company', 'netherlands', -85)
    set_historical_attitude('british_company', 'punjab', 0)

    set_total_attitude('netherlands', 'british_company', -85)
    set_total_attitude('netherlands', 'britain', 0)

    # User-defined flow end ###################################################################################################






except Exception as exception:

    # Rethrowing exception

    warnings.warn('A critical error happened during execution.')

    raise exception

finally:

    # Finalising

    print_block('Finalising.')

    print('Clearing recruitment manager IDs from bdi_pool.')
    remove_recruitment_ids()

    print('Writing tables.')
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    if hasattr(builtins, 'CHARACTER_IDS'):
        builtins.CHARACTER_IDS.to_csv(CHARACTER_IDS_PATH, sep='\t', index=False)
    if hasattr(builtins, 'FACTION_IDS'):
        builtins.FACTION_IDS.to_csv(FACTION_IDS_PATH, sep='\t', index=False)
    if hasattr(builtins, 'GOVERNORSHIP_IDS'):
        builtins.GOVERNORSHIP_IDS.to_csv(GOVERNORSHIP_IDS_PATH, sep='\t', index=False)
    if hasattr(builtins, 'REGION_IDS'):
        builtins.REGION_IDS.to_csv(REGION_IDS_PATH, sep='\t', index=False)
    if hasattr(builtins, 'REGION_SLOT_IDS'):
        builtins.REGION_SLOT_IDS.to_csv(REGION_SLOT_IDS_PATH, sep='\t', index=False)

    print_block('Done.')
