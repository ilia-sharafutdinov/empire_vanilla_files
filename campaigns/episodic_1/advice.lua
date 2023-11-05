local core = require "ui/CoreUtils"
local scripting = core.Require "EpisodicScripting"

local function OnAdviceIssued(context)
out.ting("Advice issued, hightlight")

	-- 0701_ep1_settlement_basics_Initial_Turns_Thread
	if conditions.AdviceJustDisplayed("1218461593", context) then
		scripting.HighlightComponent("TabGroup", true)
	
	-- 0707_ep_1_construct_plantation_2_Initial_Turns_Thread
	elseif conditions.AdviceJustDisplayed("-1730173744", context) then
--		scripting.HighlightComponent("Constructable1", true)
	
	-- 0709_ep_1_construct_fishery_2_Initial_Turns_Thread
	elseif conditions.AdviceJustDisplayed("-1997236953", context) then
--		scripting.HighlightComponent("Constructable1", true)
		
	-- 0724_ep1_construct_farm_2_Initial_Turns_Thread
	elseif conditions.AdviceJustDisplayed("655610075", context) then
		scripting.HighlightComponent("ConstructionCardGroup", true)
	
	-- 0714_ep1_end_turn_Initial_Turns_Thread
	elseif conditions.AdviceJustDisplayed("74393512", context) then
		scripting.HighlightComponent("button_end_turn", true)

	-- 0738_ep_1_end
	elseif conditions.AdviceJustDisplayed("1228132991", context) then
		scripting.HighlightComponent("button_end_turn", true)
		
	-- 0711_ep_1_recruit_unit_2_Initial_Turns_Thread
	elseif conditions.AdviceJustDisplayed("-1396032595", context) then
		scripting.HighlightComponent("TabGroup", true)
	
	-- 0712_ep_1_recruit_unit_3_Initial_Turns_Thread
	elseif conditions.AdviceJustDisplayed("1533668202", context) then
		scripting.HighlightComponent("episodic_1_arquebusiers!recruitable!", true)
	
	-- 0733_ep_1_recruitment_tab_Initial_Turns_Thread
	elseif conditions.AdviceJustDisplayed("1221662969", context) then
		scripting.HighlightComponent("UnitCardGroup", true)
		
	-- 0734_ep_1_construction_tab_Initial_Turns_Thread
	elseif conditions.AdviceJustDisplayed("-898557498", context) then
		scripting.HighlightComponent("ConstructionCardGroup", true)
		
	-- 0736_ep_1_Jamestown_recruitment_Initial_Turns_Thread
	elseif conditions.AdviceJustDisplayed("96726372", context) then
		scripting.HighlightComponent("UnitCardGroup", true)

	end
end

local function OnAdviceDismissed(context)
out.ting("Advice Dismissed, hightlight")

	if conditions.AdviceJustDisplayed("1218461593", context) then
		scripting.HighlightComponent("TabGroup", false)
		
	elseif conditions.AdviceJustDisplayed("-1730173744", context) then
--		scripting.HighlightComponent("Constructable1", false)
	
	elseif conditions.AdviceJustDisplayed("-1997236953", context) then
--		scripting.HighlightComponent("Constructable1", false)
		
	elseif conditions.AdviceJustDisplayed("655610075", context) then
		scripting.HighlightComponent("ConstructionCardGroup", false)
	
	elseif conditions.AdviceJustDisplayed("-1396032595", context) then
		scripting.HighlightComponent("TabGroup", false)

	elseif conditions.AdviceJustDisplayed("1533668202", context) then
		scripting.HighlightComponent("episodic_1_arquebusiers!recruitable!", false)
	
	elseif conditions.AdviceJustDisplayed("1221662969", context) then
		scripting.HighlightComponent("UnitCardGroup", false)
	
	elseif conditions.AdviceJustDisplayed("-898557498", context) then
		scripting.HighlightComponent("ConstructionCardGroup", false)
		
	elseif conditions.AdviceJustDisplayed("96726372", context) then
		scripting.HighlightComponent("UnitCardGroup", false)

	end
end

--------------------------------------------------------------------------------------------------------------------
-- Add event callbacks
-- For a list of all events supported create a "documentation" directory in your empire directory, run a debug build of the game and see
-- the events.txt file
--------------------------------------------------------------------------------------------------------------------
scripting.AddEventCallBack("AdviceIssued", OnAdviceIssued)
scripting.AddEventCallBack("AdviceDismissed", OnAdviceDismissed)
scripting.AddEventCallBack("AdviceSuperseded", OnAdviceDismissed)