# How to add a completely new faction to a startpos, increasing the overall number of factions in campaign

## Preface

The method described below was invented a long time ago by Lom, a modder of tremendous talent. Many of the techniques he came up with have not been shared previously, and their preservation is of utmost importance for the community. I'm posting this guide with Lom's authorisation, for free, but since he kindly asked, I'm attaching his DonationAlerts. If you successfully implement his methods, I ask you to demonstrate solidarity with Lom and donate him any symbolic amount you see fit, so that he knows his work is important for the community.



## Intro

Vanilla early campaign startpos features exactly 56 factions and a special rebel faction.

Previously nobody was capable of increase that number. You could introduce new factions to the startpos by sacrificing the existing ones, but you couldn't add entirely new ones. With Lom's techniques, that became possible, and now you can add as many new factions as you want, taken you also add the DB keys for them.

In this guide we will be adding Mecklenburg, since it already has all the needed records in DB.



# Unpacking the startpos

In order to follow this guide, you are required to learn using [taw's esf2xml](https://github.com/taw/etwng). If you don't have any experience with taw's tools, I advise you to pass the following [tutorial](../../../esf_scripts/README.md#how-to-use-taws-esf2xml) before proceeding.



## IDs

Each faction needs 13 IDs: 10 base IDs and 3 campaign AI (**CAI**) IDs.

For Mecklenburg, let's agree to use the following ones:
- Main faction ID: `900000000`
- Technology tree ID: `910000000`
- Government ID: `920000000`

Government post IDs:
- finance: `921000000`
- faction_leader: `922000000`
- navy: `923000000`
- accident: `924000000`
- justice: `925000000`
- army: `926000000`
- head_of_government: `927000000`

CAI IDs:
- Main CAI faction ID: `80000000`
- CAI technology tree ID: `81000000`
- Unknown CAI ID `82000000`

The base IDs should have length of 9 digits, and CAI IDs should have length of no less than 8 digits: otherwise the new IDs created during gameplay could eventually collide with the new ones. It is also very important that the new IDs don't duplicate any IDs already existing in the startpos.

To make visual identification more clear, let's agree to use base IDs starting with 9 and having 9 digits, and CAI IDs starting with 8 and having 8 digits.

When addging a second faction, you could simply increment all IDs by 1, when adding a third one, increment all IDs by 2 - and so on.



## Adding diplomacy to BDI pool

Unpack the startpos to `unpacked_startpos_dir` and open `unpacked_startpos_dir\bdi_pool\0001.xml`. The file may be huge, weighting 15 MB, so it may take time to load.

Search for the following string:
`<ary type="CAI_DIPLOMATIC_ANALYSIS_FACTIONINFO">`

You should find 57 such strings - 1 per each faction. These are BDI records, responsible for initial diplomatic outlook of each faction towards each other one.

We need to update each of the 57 arrays.

Under the first array, search for the following block:
```xml
     <rec type="CAI_DIPLOMATIC_ANALYSIS_FACTIONINFO">
      <u>1415</u>
      <flt>0.1666666567325592</flt>
      <flt>0.23139679431915283</flt>
      <u>0</u>
     </rec>
```

These are the CAI attitudes of faction with CAI ID = 1265 (Great Britain) towards the faction with CAI ID = 1415 (Hessen).

Let's agree, that we're copying all the info needed for Mecklenburg creation from Hessen - because Hessen is an emergent nation, which is similar to the one we'd like to create.

Copy the entire block and paste it right under `<ary type="CAI_DIPLOMATIC_ANALYSIS_FACTIONINFO">` line, replacing Hessen's CAI ID (`1415`) with our new one (`80000000`), so that the result looks like this:
```xml
   <rec type="CAI_DIPLOMATIC_ANALYSIS">
    <u>1265</u> <!-- CAI ID of Great Britain -->
    <ary type="CAI_DIPLOMATIC_ANALYSIS_FACTIONINFO">
     <rec type="CAI_DIPLOMATIC_ANALYSIS_FACTIONINFO">
      <u>80000000</u> <!-- CAI ID of Mecklenburg -->
      <flt>0.1666666567325592</flt>
      <flt>0.23139679431915283</flt>
      <u>0</u>
     </rec>
     <rec type="CAI_DIPLOMATIC_ANALYSIS_FACTIONINFO">
      <u>1268</u> <!-- CAI ID of France -->
      <flt>0.3343749940395355</flt>
      <flt>0.351079523563385</flt>
      <u>0</u>
     </rec>
```

And so on. Repeat this process for each of the 57 arrays.

**TIP**: You don't necessarily have to copy Hessen's block. To simplify the task, you can even paste one similar block into each of the factions' arrays. Although, ideally, you'd like to choose to copy blocks of a faction which is most similar to the one you are creating, searching for it under *each* of the arrays, because relationship of each of the 57 factions with each of the other one is unique, producing a huge number of possible combinations.



## Adding main section diplomacy

Navigate to `unpacked_startpos_dir\diplomacy` folder.

In every `.xml`-file inside, you need to search for the following line:
`<ary type="DIPLOMACY_RELATIONSHIPS_ARRAY">`

Open `unpacked_startpos_dir\diplomacy\britain.xml` and search for that line. Under that line, search for Hessen's block:
```xml
  <rec type="DIPLOMACY_RELATIONSHIPS_ARRAY">
   <rec type="DIPLOMACY_RELATIONSHIP">
    <i>583887784</i><!-- hessen -->
    <ary type="DIPLOMACY_RELATIONSHIP_ATTITUDES_ARRAY">
     <draa/><!-- State Gift Received -->
     <draa/><!-- Military Alliance +1 If Broken -2 -->
     <draa/><!-- Alliance Broken -->
     <draa/><!-- Alliances Not Honoured -->
     <draa extra="15" active2="yes"/><!-- War Against Enemy And Enemy Of My Enemy (If No War Then Enemy Of My Enemy) -->
     <draa/><!-- Trade Agreement -->
     <draa/><!-- Trade Agreement Broken -->
     <draa/><!-- War Dragged By Ally (-70) And/Or Declare War (-140) -->
     <draa/><!-- Peace Treaty -->
     <draa/><!-- Allied With Enemy -->
     <draa extra="-15" active2="yes"/><!-- War Declared On Friend -->
     <draa/><!-- Unreliable Ally -->
     <draa/><!-- Territorial Expansion -->
     <draa/><!-- Backstabber -->
     <draa/><!-- Assassination Attempts -->
     <draa drift="0" current="10" limit="0" active1="no"/><!-- Religion -->
     <draa drift="0" current="-10" limit="0" active1="no"/><!-- Government Type -->
     <draa/><!-- Historical Friendship/Grievance -->
     <draa/><!-- Acts Of Sabotage -->
     <draa/><!-- Acts Of Espionage -->
     <draa/><!-- Threats Of Attack -->
     <draa/><!-- Respect Given To National Leader -->
    </ary>
    <no/><!-- Trade Agreement -->
    <i>0</i><!-- Military Access (-1 = Infinite) -->
    <s>neutral</s><!-- Relationship -->
    <i>0</i><!-- Supporting Faction ID -->
    <u>0</u><!-- 20 If Allied Then Countdown To 0 -->
    <i>0</i><!-- Declare war -?. Victim of war +? -->
    <i>0</i><!-- Payment To Patron -->
    <i>0</i><!-- Income From Protectorate -->
    <i>0</i><!-- War - Opposition Has Opposite Value -->
    <i>0</i><!-- Declare War -?. Victim Of War +? -->
    <u>0</u><!-- Number Of Turns At War -->
    <u>0</u><!-- Number Of Turns At War Without Battle -->
    <ary type="REGULAR_PAYMENTS"/>
    <u>0</u><!-- 10 If Allied Then Countdown To 0 When No Longer Allied -->
    <u>0</u>
    <ary type="ALLIED_IN_WAR_AGAINST"/>
    <u4_ary>0 0 0 0 0 0 0 0 0 0 0</u4_ary>
    <u>0</u>
    <s>neutral</s><!-- Current Relationship With Protectorate ?? -->
    <no/>
    <no/>
    <i>0</i>
   </rec>
  </rec>
```

Copy the entire block and paste it right under `<ary type="DIPLOMACY_RELATIONSHIPS_ARRAY">` line, replacing Hessen's faction ID (`583887784`) with our new one (`900000000`), so that the result looks like this:
```xml
 <ary type="DIPLOMACY_RELATIONSHIPS_ARRAY">
  <rec type="DIPLOMACY_RELATIONSHIPS_ARRAY">
   <rec type="DIPLOMACY_RELATIONSHIP">
    <i>900000000</i><!-- mecklenburg -->
    <ary type="DIPLOMACY_RELATIONSHIP_ATTITUDES_ARRAY">
     <draa/><!-- State Gift Received -->
     <draa/><!-- Military Alliance +1 If Broken -2 -->
     <draa/><!-- Alliance Broken -->
     <draa/><!-- Alliances Not Honoured -->
     <draa extra="15" active2="yes"/><!-- War Against Enemy And Enemy Of My Enemy (If No War Then Enemy Of My Enemy) -->
     <draa/><!-- Trade Agreement -->
     <draa/><!-- Trade Agreement Broken -->
     <draa/><!-- War Dragged By Ally (-70) And/Or Declare War (-140) -->
     <draa/><!-- Peace Treaty -->
     <draa/><!-- Allied With Enemy -->
     <draa extra="-15" active2="yes"/><!-- War Declared On Friend -->
     <draa/><!-- Unreliable Ally -->
     <draa/><!-- Territorial Expansion -->
     <draa/><!-- Backstabber -->
     <draa/><!-- Assassination Attempts -->
     <draa drift="0" current="10" limit="0" active1="no"/><!-- Religion -->
     <draa drift="0" current="-10" limit="0" active1="no"/><!-- Government Type -->
     <draa/><!-- Historical Friendship/Grievance -->
     <draa/><!-- Acts Of Sabotage -->
     <draa/><!-- Acts Of Espionage -->
     <draa/><!-- Threats Of Attack -->
     <draa/><!-- Respect Given To National Leader -->
    </ary>
    <no/><!-- Trade Agreement -->
    <i>0</i><!-- Military Access (-1 = Infinite) -->
    <s>neutral</s><!-- Relationship -->
    <i>0</i><!-- Supporting Faction ID -->
    <u>0</u><!-- 20 If Allied Then Countdown To 0 -->
    <i>0</i><!-- Declare war -?. Victim of war +? -->
    <i>0</i><!-- Payment To Patron -->
    <i>0</i><!-- Income From Protectorate -->
    <i>0</i><!-- War - Opposition Has Opposite Value -->
    <i>0</i><!-- Declare War -?. Victim Of War +? -->
    <u>0</u><!-- Number Of Turns At War -->
    <u>0</u><!-- Number Of Turns At War Without Battle -->
    <ary type="REGULAR_PAYMENTS"/>
    <u>0</u><!-- 10 If Allied Then Countdown To 0 When No Longer Allied -->
    <u>0</u>
    <ary type="ALLIED_IN_WAR_AGAINST"/>
    <u4_ary>0 0 0 0 0 0 0 0 0 0 0</u4_ary>
    <u>0</u>
    <s>neutral</s><!-- Current Relationship With Protectorate ?? -->
    <no/>
    <no/>
    <i>0</i>
   </rec>
  </rec>
```

Proceed to repeat that process for all the other factions' `.xml`'s in the folder.

**TIP**: As previously mentioned, you don't necessarily have to copy Hessen's block. As an option you can even use a generic block, fitting all factions. However, the following block doesn't feature any initial diplomatic attitudes, so you should expect these to be missing from the startpos.
```xml
  <rec type="DIPLOMACY_RELATIONSHIPS_ARRAY">
   <rec type="DIPLOMACY_RELATIONSHIP">
    <i>900000000</i>
    <ary type="DIPLOMACY_RELATIONSHIP_ATTITUDES_ARRAY">
     <draa/>
     <draa/>
     <draa/>
     <draa/>
     <draa extra="15" active2="yes"/>
     <draa/>
     <draa/>
     <draa/>
     <draa/>
     <draa/>
     <draa extra="-15" active2="yes"/>
     <draa/>
     <draa/>
     <draa/>
     <draa/>
     <draa/>
     <draa drift="0" current="15" limit="0" active1="no"/>
     <draa/>
     <draa/>
     <draa/>
     <draa/>
     <draa/>
    </ary>
    <no/>
    <i>0</i>
    <s>neutral</s>
    <i>0</i>
    <u>0</u>
    <i>0</i>
    <i>0</i>
    <i>0</i>
    <i>0</i>
    <i>0</i>
    <u>0</u>
    <u>0</u>
    <ary type="REGULAR_PAYMENTS"/>
    <u>0</u>
    <u>0</u>
    <ary type="ALLIED_IN_WAR_AGAINST"/>
    <u4_ary>0 0 0 0 0 0 0 0 0 0 0</u4_ary>
    <u>0</u>
    <s>neutral</s>
    <no/>
    <no/>
    <i>0</i>
   </rec>
  </rec>
```

Now we need to add Mecklenburg's own diplomacy. Copy `hessen.xml` and paste it, renaming it to `mecklenburg.xml`. Then search for Mecklenburg's ID (`900000000`) and replace it with Hessen's (`583887784`).



## Adding main faction records

Now we need to create the main faction records. In order to do this, you'll need some additional information. Open `patch2.pack` using Rusted Pack File Manager, go to `db/factions_tables` and open `factions`.

Inside the table, search for Mecklenburg. Search and record the values from the following columns:
- Key: `mecklenburg`
- Screen name: `Mecklenburg`
- Flag path and republican flag pah: in our case, both are `data\ui\flags\mecklenburg`
- *Optionally, record primary, secondary and uniform colours' RGBs - 9 columns in total.

### Main faction record

Navigate to `unpacked_startpos_dir\factions` and copy `hessen.xml` renaming it to `mecklenburg.xml`.

First, we should replace all ID and faction key entries:
- In line 12, replace Hessen's faction key `hessen` with Mecklenburg's `mecklenburg`
- In line 41, replace Hessen's ID `583887784` with Mecklenburg's `900000000`
- In line 42, replace Hessen's faction key `hessen` with Mecklenburg's `mecklenburg`
- In line 43, replace Hessen's screen name `Hessen` with Mecklenburg's `Mecklenburg`.
- *Optionally, search for `flag_and_colours` and in lines 162 and 163 replace the flag paths and colours. You can generate correct colour hex values by copying the faction's RGB colours from `factions_tables` and transforming them into hex values using [rgbtohex](https://www.rgbtohex.net/).

Now, we also need to replace links to all faction-related files:
- Replace `diplomacy/hessen.xml` with `diplomacy/mecklenburg.xml`.
- Replace `government/hessen-gov_absolute_monarchy.xml` with `government/mecklenburg-gov_absolute_monarchy.xml`.
- Replace `family/hessen.xml` with `family/mecklenburg.xml`.
- Replace `technology/hessen-hessen.xml` with `technology/mecklenburg-mecklenburg.xml`.
- Replace `unit_name_alloc/hessen-naval-0001.xml` with `unit_name_alloc/mecklenburg-naval-0001.xml`.
- Replace all `unit_name_alloc/hessen-land-` ... `.xml`'s with `unit_name_alloc/mecklenburg-land-`.

All these linked files now have to be created and edited (except `diplomacy/hessen.xml` which we already added [in the previous section](#adding-main-section-diplomacy)).

### Government record

Navigate to `unpacked_startpos_dir\government` and copy `hessen-gov_absolute_monarchy.xml` renaming it to `mecklenburg-gov_absolute_monarchy.xml`.

Start replacing the IDs:
- For each of the 7 government ID lines, replace Hessen's government ID `585057944` with Mecklenburg's `920000000`.
- For each of the government posts, consult the table in [IDs section](#ids) to replace Hessen's government post ID with the corresponding Mecklenburg's ID.
  + `585069216` -> `921000000` (finance)
  + `585069312` -> `922000000` (faction_leader)
  + `585069408` -> `923000000` (navy)
  + `585069592` -> `924000000` (accident)
  + `585069688` -> `925000000` (justice)
  + `585069888` -> `926000000` (army)
  + `585069984` -> `927000000` (head_of_government)

**TIP**: If you wish to have a government type different from absolute monarchy, you can copy a different government. However, it is important that you copy an **emergent** faction. If you want a republic, it is advised to copy USA. If you want a constitutional monarchy, it is advised to copy Norway.

### Family record

Navigate to `unpacked_startpos_dir\family` and copy `hessen.xml` renaming it to `mecklenburg.xml`.

Replace all Hessen faction IDs (`583887784`) with Mecklenburg's (`900000000`).

### Technology tree record

Navigate to `unpacked_startpos_dir\technology` and copy `hessen-hessen.xml` renaming it to `mecklenburg-mecklenburg.xml`.

Scroll to the very bottom of the document and replace Hessen's technology tree ID (`585070312`) with Mecklenburg's (`910000000`).

**TIP**: Technology trees are similar for most factions in vanilla with only few exceptions: British technology tree features breach loding rifles, and the Ottoman one features European doctrine. Make sure that the tree you're adding to your new faction has all the same technology records mapped to the faction in DB.

### Unit name allocation records

Navigate to `unpacked_startpos_dir\unit_name_alloc` and copy all `hessen-land-` ... `.xml`'s renaming them to `mecklenburg-land-`.

Also copy `hessen-naval-0001.xml` renaming it to `mecklenburg-naval-0001.xml`.

**TIP**: Unit name allocations in vanilla differ between European, Indian, Middle Eastern and Native American cultures. Otherwise, they are not faction-specific.

### Adding faction record to World

Navigate to `unpacked_startpos_dir\campaign_env` and open `world.xml`.

Search for the following line:
`<ary type="FACTION_ARRAY">`

This array is importing each of the factions' main records. **It also dictates the order of faction turns in campaign**.

Search for Hessen's block:
```xml
  <rec type="FACTION_ARRAY">
   <xml_include path="factions/hessen.xml"/>
  </rec>
```

Now copy the entire block and paste it right before Barbary States' block replacing Hessen's faction record (`hessen.xml`) with Mecklenburg's (`mecklenburg.xml`), so that the result looks like this:
```xml
  <rec type="FACTION_ARRAY">
   <xml_include path="factions/colombia.xml"/>
  </rec>
  <rec type="FACTION_ARRAY">
   <xml_include path="factions/mecklenburg.xml"/>
  </rec>
  <rec type="FACTION_ARRAY">
   <xml_include path="factions/barbary_states.xml"/>
  </rec>
```

### Adding faction's spying record

Don't close the file yet. We also need to add a record in spying array.

Search for the following line:
`<ary type="SPYING_ARRAY">`

Under this array, campaign spying records are listed in the exact same order as they are listed in the previous faction imports array.

Search for Hessen's block:
```xml
  <rec type="SPYING_ARRAY">
   <s>hessen</s>
   <rec type="CAMPAIGN_SPYING">
    <ary type="ARMY_DATA" version="0"/>
    <ary type="NAVY_DATA" version="0"/>
    <ary type="REGION_SLOT_DATA" version="0"/>
    <ary type="FORT_DATA" version="0"/>
    <ary type="SETTLEMENT_DATA" version="0"/>
   </rec>
  </rec>
```

Like previously, copy the entire block and paste it right before Barbary States' block replacing Hessen's faction key (`hessen`) with Mecklenburg's (`mecklenburg`), so that the result looks like this:
```xml
  <rec type="SPYING_ARRAY">
   <s>colombia</s>
   <rec type="CAMPAIGN_SPYING">
    <ary type="ARMY_DATA" version="0"/>
    <ary type="NAVY_DATA" version="0"/>
    <ary type="REGION_SLOT_DATA" version="0"/>
    <ary type="FORT_DATA" version="0"/>
    <ary type="SETTLEMENT_DATA" version="0"/>
   </rec>
  </rec>
  <rec type="SPYING_ARRAY">
   <s>mecklenburg</s>
   <rec type="CAMPAIGN_SPYING">
    <ary type="ARMY_DATA" version="0"/>
    <ary type="NAVY_DATA" version="0"/>
    <ary type="REGION_SLOT_DATA" version="0"/>
    <ary type="FORT_DATA" version="0"/>
    <ary type="SETTLEMENT_DATA" version="0"/>
   </rec>
  </rec>
  <rec type="SPYING_ARRAY">
   <s>barbary_states</s>
   <rec type="CAMPAIGN_SPYING">
    <ary type="ARMY_DATA" version="0"/>
    <ary type="NAVY_DATA" version="0"/>
    <ary type="REGION_SLOT_DATA" version="0"/>
    <ary type="FORT_DATA" version="0"/>
    <ary type="SETTLEMENT_DATA" version="0"/>
   </rec>
  </rec>
```



## Adding trade route records

Trade routes have their own separate sets of records, which also need to be copied.

### Domestic trade routes

Domestic trade routes are trade routes created when a ship occupies a trade segment. In our case they will be empty.

Navigate to `unpacked_startpos_dir\domestic_trade_routes` and copy `hessen.xml` renaming it to `mecklenburg.xml`.

Replace Hessen's faction key (`hessen`) with Mecklenburg's (`mecklenburg`).

### International trade routes

International trade routes are trade routes created when establishing a trade agreement with another faction. In our case they will be empty.

Navigate to `unpacked_startpos_dir\international_trade_routes` and copy `hessen.xml` renaming it to `mecklenburg.xml`.

Replace Hessen's faction key (`hessen`) with Mecklenburg's (`mecklenburg`).

### Adding trade route records to Trade Manager

Navigate to `unpacked_startpos_dir\campaign_env` and open `trade_manager.xml`.

Search for the domestic trade routes array line:
`<ary type="DOMESTIC_TRADE_ROUTES">`

Under this line, search for Hessen's block:
```xml
<xml_include path="domestic_trade_routes/hessen.xml"/>
```

Now copy the entire block and paste it right under `<ary type="DOMESTIC_TRADE_ROUTES">` line replacing Hessen's faction record (`hessen.xml`) with Mecklenburg's (`mecklenburg.xml`), so that the result looks like this:
```xml
 <ary type="DOMESTIC_TRADE_ROUTES">
  <xml_include path="domestic_trade_routes/mecklenburg.xml"/>
  <xml_include path="domestic_trade_routes/saxony.xml"/>
```

Now search for the international trade routes array line:
`<ary type="INTERNATIONAL_TRADE_ROUTES">`

Under this line, search for Hessen's block:
```xml
<xml_include path="international_trade_routes/hessen.xml"/>
```

Now copy the entire block and paste it right under `<ary type="INTERNATIONAL_TRADE_ROUTES">` line replacing Hessen's faction record (`hessen.xml`) with Mecklenburg's (`mecklenburg.xml`), so that the result looks like this:
```xml
 <ary type="INTERNATIONAL_TRADE_ROUTES">
  <xml_include path="international_trade_routes/mecklenburg.xml"/>
  <xml_include path="international_trade_routes/saxony.xml"/>
```



## Adding faction campaign setup record

Campaign setup record contains some important faction information. It is one of the records, where you have to duplicate faction's playability.

Navigate to `unpacked_startpos_dir\campaign_env` and open `campaign_setup-main.xml`.

Search for the following line:
`<ary type="PLAYERS_ARRAY">`

Under this line, search for Hessen's block:
```xml
   <rec type="PLAYERS_ARRAY">
    <rec type="CAMPAIGN_PLAYER_SETUP">
     <victory_conditions year="0" region_count="0" prestige_victory="no" campaign_type="4 (Unplayable)"/>
     <rec type="CAMPAIGN_PLAYER_SETUP_INGAME_MODIFIABLES">
      <i>0</i>
      <i>0</i>
      <i>0</i>
      <no/>
     </rec>
     <s>hessen</s>
     <no/>
     <no/><!-- Playable -->
     <no/>
    </rec>
   </rec>
```

Now copy the entire block and paste it right before Barbary States' block replacing Hessen's faction key (`hessen`) with Mecklenburg's (`mecklenburg`), so that the result looks like this:
```xml
   <rec type="PLAYERS_ARRAY">
    <rec type="CAMPAIGN_PLAYER_SETUP">
     <victory_conditions year="0" region_count="0" prestige_victory="no" campaign_type="4 (Unplayable)"/>
     <rec type="CAMPAIGN_PLAYER_SETUP_INGAME_MODIFIABLES">
      <i>0</i>
      <i>0</i>
      <i>0</i>
      <no/>
     </rec>
     <s>colombia</s>
     <no/>
     <no/><!-- Playable -->
     <no/>
    </rec>
   </rec>
   <rec type="PLAYERS_ARRAY">
    <rec type="CAMPAIGN_PLAYER_SETUP">
     <victory_conditions year="0" region_count="0" prestige_victory="no" campaign_type="4 (Unplayable)"/>
     <rec type="CAMPAIGN_PLAYER_SETUP_INGAME_MODIFIABLES">
      <i>0</i>
      <i>0</i>
      <i>0</i>
      <no/>
     </rec>
     <s>mecklenburg</s>
     <no/>
     <no/><!-- Playable -->
     <no/>
    </rec>
   </rec>
   <rec type="PLAYERS_ARRAY">
    <rec type="CAMPAIGN_PLAYER_SETUP">
     <victory_conditions year="0" region_count="0" prestige_victory="no" campaign_type="4 (Unplayable)"/>
     <rec type="CAMPAIGN_PLAYER_SETUP_INGAME_MODIFIABLES">
      <i>0</i>
      <i>0</i>
      <i>0</i>
      <no/>
     </rec>
     <s>barbary_states</s>
     <no/>
     <yes/><!-- Playable -->
     <no/>
    </rec>
   </rec>
```



## Adding faction preopen map info record

Preopen map info is used to represent a list of playable factions and their corresponding territories and victory conditions when you open Grand Campaign screen from the game's main menu. **It also dictates the order of faction choice in the list**.

This file also contains a duplicate of a faction campaign setup record, so first we need to do the exact same thing as with [adding the faction campaign setup record](#adding-faction-campaign-setup-record).

Navigate to `unpacked_startpos_dir\preopen_map_info` and open `info-main.xml`.

Search for the following line:
`<ary type="PLAYERS_ARRAY">`

Under this line, search for Hessen's block:
```xml
   <rec type="PLAYERS_ARRAY">
    <rec type="CAMPAIGN_PLAYER_SETUP">
     <victory_conditions year="0" region_count="0" prestige_victory="no" campaign_type="4 (Unplayable)"/>
     <rec type="CAMPAIGN_PLAYER_SETUP_INGAME_MODIFIABLES">
      <i>0</i>
      <i>0</i>
      <i>0</i>
      <no/>
     </rec>
     <s>hessen</s>
     <no/>
     <no/><!-- Playable -->
     <no/>
    </rec>
   </rec>
```

Now copy the entire block and paste it right before Barbary States' block replacing Hessen's faction key (`hessen`) with Mecklenburg's (`mecklenburg`), so that the result looks like this:
```xml
   <rec type="PLAYERS_ARRAY">
    <rec type="CAMPAIGN_PLAYER_SETUP">
     <victory_conditions year="0" region_count="0" prestige_victory="no" campaign_type="4 (Unplayable)"/>
     <rec type="CAMPAIGN_PLAYER_SETUP_INGAME_MODIFIABLES">
      <i>0</i>
      <i>0</i>
      <i>0</i>
      <no/>
     </rec>
     <s>colombia</s>
     <no/>
     <no/><!-- Playable -->
     <no/>
    </rec>
   </rec>
   <rec type="PLAYERS_ARRAY">
    <rec type="CAMPAIGN_PLAYER_SETUP">
     <victory_conditions year="0" region_count="0" prestige_victory="no" campaign_type="4 (Unplayable)"/>
     <rec type="CAMPAIGN_PLAYER_SETUP_INGAME_MODIFIABLES">
      <i>0</i>
      <i>0</i>
      <i>0</i>
      <no/>
     </rec>
     <s>mecklenburg</s>
     <no/>
     <no/><!-- Playable -->
     <no/>
    </rec>
   </rec>
   <rec type="PLAYERS_ARRAY">
    <rec type="CAMPAIGN_PLAYER_SETUP">
     <victory_conditions year="0" region_count="0" prestige_victory="no" campaign_type="4 (Unplayable)"/>
     <rec type="CAMPAIGN_PLAYER_SETUP_INGAME_MODIFIABLES">
      <i>0</i>
      <i>0</i>
      <i>0</i>
      <no/>
     </rec>
     <s>barbary_states</s>
     <no/>
     <yes/><!-- Playable -->
     <no/>
    </rec>
   </rec>
```mecklenburg

Now we need to change faction info - this record contains faction description, flag and leader portrait.

Search for the following line:
`<ary type="FACTION_INFOS">`

Under this line, search for Hessen's block:
```xml
  <rec type="FACTION_INFOS">
   <s>hessen</s>
   <s/>
   <no/>
   <no/>
   <i>51</i>
   <s>start_pos_factions_description_1076472315</s>
   <s>data\ui\flags\hessen</s>
   <i>0</i>
  </rec>
```

Now copy the entire block and paste it right before Barbary States' block replacing Hessen's faction key and flag (`hessen`) with Mecklenburg's (`mecklenburg`) **and also picking the right order for Mecklenburg, replacing Hessen's `51` with `57` (pirates are the final faction in the list and their order is `56`)**, so that the result looks like this:
```xml
  <rec type="FACTION_INFOS">
   <s>colombia</s>
   <s/>
   <no/>
   <no/>
   <i>54</i>
   <s>start_pos_factions_description_-932487810</s>
   <s>data\ui\flags\colombia</s>
   <i>0</i>
  </rec>
  <rec type="FACTION_INFOS">
   <s>mecklenburg</s>
   <s/>
   <no/>
   <no/>
   <i>57</i>
   <s>start_pos_factions_description_1076472315</s>
   <s>data\ui\flags\mecklenburg</s>
   <i>0</i>
  </rec>
  <rec type="FACTION_INFOS">
   <s>barbary_states</s>
   <s>ui/portraits/indian/cards/king/old/092.tga</s>
   <no/>
   <yes/>
   <i>55</i>
   <s>start_pos_factions_description_32</s>
   <s>data\ui\flags\barbary_states</s>
   <i>3</i>
  </rec>
```



## Adding CAI records

Now we need to add CAI records. CAI records are responsible for the campaign AI behaviour. A lot of crucial information on which characters and regions are controlled by which faction, what is a faction's outlook on current geopolitics and balance of power, what are it's current plans etc. - are all recorded in **CAI** (campaign AI) and **BDI** (belief–desire–intention) records.

### Faction CAI record

CAI records, unfortunatelly, are not named and only have numeric IDs. In order to find the correct records, we need to copy the main IDs and search for them in all files in a folder of interest - every CAI record has a reference either directly to

Navigate to `unpacked_startpos_dir\cai_factions` and search for Hessen's faction ID (`583887784`) in every file inside. In vanilla main startpos, you should be able to find this ID in `0051.xml`. This is Hessen's CAI faction record. Copy it, rename it to `0058.xml` (the biggest existing record should be `0057.xml`) and open it.

Start replacing the IDs:
- In lines 3 and 7, replace Hessen's faction CAI ID `1415` with Mecklenburg's `80000000`.
- In line 37, replace Hessen's main faction ID `583887784` with Mecklenburg's `900000000`.
- In line 40, replace Hessen's technology tree CAI ID `1417` with Mecklenburg's `81000000`.
- In line 45, replace Hessen's unknown CAI ID `1416` with Mecklenburg's `82000000`.

And now, importantly, you need to clear Hessen's BDI records. In lines 15, 19, 26 and 64, you should find `u4_ary` tags with many numbers inside. Replace these lines with closed tags without BDIs, so that these lines:
`<u4_ary>7904 7930 7931 ......... 76316 76337 76336</u4_ary><!-- BDI Information -->`
Start looking like this:
`<u4_ary/><!-- BDI Information -->`

Do this with all 4 lines.

### CAI tech tree record

Navigate to `unpacked_startpos_dir\cai_tech_trees` and search for Hessen's faction ID (`585070312`) in every file inside. In vanilla main startpos, you should be able to find this ID in `0051.xml`. Copy it, rename it to `0057.xml` (the biggest existing record should be `0056.xml`) and open it.

Start replacing the IDs:
- In line 6, replace Hessen's technology tree CAI ID `1417` with Mecklenburg's `81000000`.
- In line 29, replace Hessen's faction CAI ID `1415` with Mecklenburg's `80000000`.
- In line 30, replace Hessen's main technology tree ID `585070312` with Mecklenburg's `910000000`.

### CAI history record

Navigate to `unpacked_startpos_dir\cai_interface` and open `cai_history.xml`.

Search for the following line:
`<ary type="CAI_HISTORY_EVENTS">`

Under this line, search for Hessen's block:
```xml
  <rec type="CAI_HISTORY_EVENTS">
   <i>14</i>
   <rec type="CAI_HISTORY_EVENT">
    <i>14</i>
    <cai_event_classes>
     type_new_manager_for_faction
     round_1
     faction_hessen
    </cai_event_classes>
   </rec>
   <rec type="CAI_HISTORY_EVENT_NEW_MANAGER_FOR_FACTION">
    <asc>hessen</asc>
    <i>11</i>
   </rec>
  </rec>
```

Now copy the entire block and paste it right before Barbary States' block replacing Hessen's faction key (`hessen`) with Mecklenburg's (`mecklenburg`) **and also `faction_hessen` to `faction_mecklenburg`**, so that the result looks like this:
```xml
  <rec type="CAI_HISTORY_EVENTS">
   <i>14</i>
   <rec type="CAI_HISTORY_EVENT">
    <i>14</i>
    <cai_event_classes>
     type_new_manager_for_faction
     round_1
     faction_colombia
    </cai_event_classes>
   </rec>
   <rec type="CAI_HISTORY_EVENT_NEW_MANAGER_FOR_FACTION">
    <asc>colombia</asc>
    <i>11</i>
   </rec>
  </rec>
  <rec type="CAI_HISTORY_EVENTS">
   <i>14</i>
   <rec type="CAI_HISTORY_EVENT">
    <i>14</i>
    <cai_event_classes>
     type_new_manager_for_faction
     round_1
     faction_mecklenburg
    </cai_event_classes>
   </rec>
   <rec type="CAI_HISTORY_EVENT_NEW_MANAGER_FOR_FACTION">
    <asc>mecklenburg</asc>
    <i>11</i>
   </rec>
  </rec>
  <rec type="CAI_HISTORY_EVENTS">
   <i>14</i>
   <rec type="CAI_HISTORY_EVENT">
    <i>14</i>
    <cai_event_classes>
     type_new_manager_for_faction
     round_1
     faction_barbary_states
    </cai_event_classes>
   </rec>
   <rec type="CAI_HISTORY_EVENT_NEW_MANAGER_FOR_FACTION">
    <asc>barbary_states</asc>
    <i>11</i>
   </rec>
  </rec>
```

### Adding CAI records to CAI World

Navigate to `unpacked_startpos_dir\cai_interface` and open `cai_world.xml`.

Search for the CAI factions array line:
`<ary type="CAI_WORLD_FACTIONS">`

Now append Mecklenburg's (`cai_factions/0058.xml`), so that the result looks like this:
```xml
  <xml_include path="cai_factions/0057.xml"/>
  <xml_include path="cai_factions/0058.xml"/>
 </ary>
```

Now search for the CAI tech trees array line:
`<ary type="CAI_WORLD_TECHNOLOGY_TREES">`

And append Mecklenburg's (`cai_tech_trees/0057.xml`), so that the result looks like this:
```xml
  <xml_include path="cai_tech_trees/0056.xml"/>
  <xml_include path="cai_tech_trees/0057.xml"/>
 </ary>
```

### And how about CAI interface manager?

The more sophisticated startpos modders might start asking: each faction has a CAI interface manager record in `unpacked_startpos_dir\cai_interface_managers` and an associated BDI pool in `unpacked_startpos_dir\bdi_pool`. Are we going to add them?

No, we're not. Because creating the entire faction's BDI is a huge amount of work. However, by not creating the manager we allow the game to **automatically generate it on campaign launch**.



## Finalisation

Open Alsace region record and replace `french_rebels` with `mecklenburg`. When the region rebels, it should now spawn Mecklenburg instead of generic rebels.

Compile the startpos using taw's xml2esf and try replacing the `startpos.esf` file in `Empire Total War\data\campaigns\main` with the one you compiled (don't forget to make a **backup!**).

Launch the game and start as France. Try provoking a rebellion in Alsace. A Mecklenburg faction should emerge. To make sure everything is completely functional, try making peace with it, trading and making an alliance. Try keeping the faction alive for some years to see it recruiting troops, building facilities and engaging in other activities typical for a minor faction. Then try conquering it and making trade with the surrounding factions again.

If you reached this step without bugs and crashes - congratulations! You have completed the tutorial. At this point you can also make Mecklenburg playable by using any of the hybrid or non-hybrid method of your choice.
