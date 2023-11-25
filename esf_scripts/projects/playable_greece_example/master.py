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






    # User-defined flow start (insert your code here) #########################################################################


    # 'print' and 'print_block' are simply printing strings to the console.
    # These functions don't make any changes.
    print_block('Changing start date.')

    print('Changing start date to Summer 1830.')
    # This function automatically changes:
    # - calendar date in campaign
    # - all unit creation dates
    # - birth dates of all characters (to preserve their age)
    # - victory condition end dates (to preserver the same number of years)
    # - starting date in all BDI records
    # Last point is essential: otherwise earlier than vanilla start dates
    # would lead to the AI being passive until the vanilla start date is reached.
    change_starting_date('summer', 1830)

    print('Changing victory conditions dates.')
    # The previous function automatically added 130 years to all victory conditions end dates.
    # Which preserved the vanilla campaign length (100 years), but made long victory end in 1930,
    # which is probably a bit too much... Let's pick some more reasonable end dates.
    change_victory_conditions_date('0 (Short)', 1860)
    change_victory_conditions_date('1 (Long)', 1899)
    change_victory_conditions_date('2 (Prestige)', 1899)
    change_victory_conditions_date('3 (Global Domination)', 1899)

    print('Setting turns per year to 4.')
    # Setting earlier end dates made the campaign shorter in terms of the number of turns it takes.
    # Let's increase the number of turns per year from 2 to 4, making the campaign even longer than previously.
    change_number_of_turns_per_year(4)


    print_block('Swapping faction keys.')

    print('Exchanging faction keys between Greece and Venice.')
    # This way we're 'emerging' Greece while making Venice emergent, preserving correct troop trees and cultures for both factions.
    # 'portugese_rebels' is not present in the startpos and is used to provide space for swapping operations,
    # otherwise we would have 2 factions with the same name, causing confusion.
    change_faction_key('greece', 'portugese_rebels')
    change_faction_key('venice', 'greece')
    change_faction_key('portugese_rebels', 'venice')


    print_block('Tweaking faction specifics.')

    print('Exchanging Greek and Venetian victory conditions.')
    # Let's immediately exchange faction's victory conditions as well.
    exchange_faction_victory_conditions('greece', 'venice')

    print('Setting Greek and Venetian campaign AI.')
    # Since we exchanged the keys, we need to re-assign the AI profiles.
    # Here we're also making Greece FULL, to make it a bit more active in campaign.
    change_faction_campaign_ai('greece', new_manager='FULL', new_personality='mixed_repressive')
    change_faction_campaign_ai('venice', new_personality='trader')

    print('Fixing Greek capital.')
    # Greece inherited capital in Venice from Venetian faction. Here we're moving it's capital to Greece.
    # A faction must own it's capital - otherwise bugs are expected. We will hand over Greece to Greek faction later.
    # Venice is now inherited from Greece which is an emergent faction - emergent factions don't have assigned capitals
    change_faction_capital('greece', 'greece')

    print('Setting Greek and Venetian government types.')
    # Let's assume, a hypothetical 1830 Venetian state would be a constitutional monarchy
    # change_faction_government_type('greece', 'gov_republic')
    change_faction_government_type('greece', 'gov_absolute_monarchy') # since 1832
    change_faction_government_type('venice', 'gov_constitutional_monarchy')

    print('Randomising Greek and Venetian character names.')
    # This is needed to update the names of characters belonging to the factions with changed keys.
    # If Greece have 'names_group' = 'names_greek', this script will automatically pick random Greek names and apply them
    # to all Greek characters, inherited from Venice and originally having Italian names.
    # The function will not only change names of all ministers, agents, generals and colonels,
    # but will also change names of each individual unit commander.
    change_faction_randomise_all_character_names('greece')
    change_faction_randomise_all_character_names('venice')

    print('Setting Greek faction leader\'s name.')
    # Here we're chosing the right name for the monarch.
    # Remember that Greece inherited all it's characters from Venice, so we need to take a Venetian minister character path.
    # change_faction_key function only changes the faction keys in all files, but it doesn't change the names of the files.
    # This was done for 2 reasons: it simplifies execution logic and it allows to more easily track the scripted changes in git.
    # https://en.wikipedia.org/wiki/Ioannis_Kapodistrias
    # change_character_name('venice-minister-0001.xml', names_group='names_german_catholic', gender='m', forename='Ioannis', surname='Kapodistrias')
    # change_character_birth_date('venice-minister-0001.xml', 'winter', 1776)
    # change_character_portrait('venice-minister-0001.xml', faction_leader=True, portrait_age='old', portrait_number=88)
    # https://en.wikipedia.org/wiki/Otto_of_Greece (since 1832)
    change_character_name('venice-minister-0001.xml', names_group='names_german_catholic', gender='m', forename='Otto', regnal_number='I')
    change_character_birth_date('venice-minister-0001.xml', 'summer', 1815)
    change_character_portrait('venice-minister-0001.xml', faction_leader=True, king=True, portrait_age='young', portrait_number=24)

    print('Making Greece major.')
    # Let's buff up the Grand Kingdom of Greece's importance.
    change_faction_majority('greece', 'yes')

    print('Setting Greek and Venetian religions.')
    # Catholic Greece? Not diring my lifetime.
    change_faction_religion('greece', 'rel_orthodox')
    change_faction_religion('venice', 'rel_catholic')

    print('Making Greece playable.')
    # Because why are we bothering at all?
    change_faction_playability('greece', 'yes')


    print_block('Tweaking regions.')

    print('Setting generic rebels in Morea.')
    # In vanilla, both Greece and Morea produce Greek faction rebel stacks.
    # Here we leave Greece to 'greece' faction rebels, so that the rebellion in Greece leads to a revolution.
    # However, we're changing Morean rebels to generic 'greek_rebels',
    # so that the region rebels against Greece if the population is unsatisfied.
    change_region_rebels('morea', 'greek_rebels')

    print('Building a cannon foundry in Greece.')
    # Finally, let's give Greece some firepower rightaway.
    change_region_slot_building('settlement:greece:athens:settlement_ordnance', 'cannon_foundry', 'greece', 'gov_absolute_monarchy')


    print_block('Swapping regions and characters ownerships.')

    print('Giving Greece to Greece.')
    # Remember we remade Venice into Greece? Now we're handing Greece over to them.
    # Aside from the region itself, we're handing all the armies in Greece to the new owner as well,
    # otherwise the Ottomans would still control these armies,
    # while not having a war or passage agreement with Greece, which would cause bugs.
    hand_over_region('greece', 'greece')
    hand_over_character('ottomans-colonel-0003.xml', 'greece')
    # If you don't specify 'names_group' as the second argument, the function will deduce it from faction name found in character file,
    # which might be inaccurate, if some person experimented with the startpos previously, trying to change a character ownership,
    # but should not be a problem, if you're building a new startpos from vanilla.
    # Like previously, the function will not only change the name of the colonel, but also the names of each individual unit commander.
    change_character_name('ottomans-colonel-0003.xml')
    # And now, let's change the army troop types from isarelys and bashi-bazouks to some proper European units.
    # When changing the unit types, you need to specify types of each unit in the army:
    # changing the type of only some of the units is not implemented yet.
    change_army_unit_type('ottomans-colonel-0003.xml', ['euro_militia_infantry', 'euro_militia_infantry', 'euro_pikemen'])
    # And how about giving Greece some starting cavalry?
    add_army_unit('ottomans-colonel-0003.xml', 'euro_provincial_cavalry', 600000000, 660000000)

    print('Giving Venice to Austria.')
    # Now we're also giving away Venice to Austria, together with the armies. Historically, Venice belonged to Austria in 1830
    hand_over_region('venice', 'austria')
    hand_over_character('venice-General-0001.xml', 'austria')
    change_character_name('venice-General-0001.xml')

    print('Removing Greek trade routes.')
    # Greece inherited Venetian trade routes leading to Venice. We should remove them.
    delete_faction_all_trade_routes('greece')
    delete_faction_trade_route('ottomans', 'venice')
    delete_faction_trade_route('austria', 'venice')
    break_trade('greece', 'ottomans')
    break_trade('greece', 'austria')
    break_trade('ottomans', 'greece')
    break_trade('austria', 'greece')

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
