local core = require "ui/CoreUtils"
core.Require "export_ep3_advice"
core.Require "advice"
local scripting			= core.Require "EpisodicScripting"

scripting.SetCampaign("episodic_3")

--------------------------------------------------------------------------------------------------------------------
-- Define functions here
-- For a list of all supported commands see the wiki page http://console/empire/Empire%20Wiki/Campaign%20Interface.aspx
--------------------------------------------------------------------------------------------------------------------

local part_1_completed = false
local game_progress = 0

local camera_pan = 0
local event_message = 0

local build_dockyard_issued = false
local port_in_queue = 0	-- 1 for fishery, 2 for shipyard, 3 for dockyard

local ship_issued = false
local ship_in_queue = false

local slot_selected = 0
local mission_advice_given = 0

local niagara_french = true
local government = false
local niagara_issued = false
local coast_safe = true

local campaign_won = false
local players_turn = true

local function OnFactionTurnStart(context)
	if conditions.FactionIsLocal(context) then
		players_turn = true
		if conditions.TurnNumber(context) == 1 then
			scripting.EnableFeature("show_shroud_2_1")
			scripting.game_interface:show_shroud(false)
			scripting.game_interface:stop_user_input(true)
			scripting.game_interface:set_zoom_limit(1.08, 0.02)
			CampaignUI.SetCameraZoom(1.06)
			CampaignUI.SetCameraTarget(-558, 305)
			scripting.game_interface:add_time_trigger("intro_hold", 2)
			scripting.game_interface:add_time_trigger("intro_VO_delay", 7)

			scripting.game_interface:add_attack_of_opportunity_overrides("faction:france,x:-470.86,y:309.70,r:1", true)
			scripting.game_interface:add_attack_of_opportunity_overrides("faction:france,x:-433.00,y:318.26,r:1", true)
			scripting.game_interface:add_attack_of_opportunity_overrides("faction:france,x:-450.55,y:310.48,r:1", true)
			scripting.game_interface:add_attack_of_opportunity_overrides("faction:france,x:-424.60,y:330.85,r:1", true)
			scripting.game_interface:add_attack_of_opportunity_overrides("faction:france,x:-426.59,y:347.94,r:1", true)

			scripting.game_interface:add_attack_of_opportunity_overrides("faction:france,x:-551.73,y:296.85,r:1", true)

			scripting.game_interface:force_diplomacy("virginia", "france", "trade agreement", false, false)
			scripting.game_interface:force_diplomacy("virginia", "france", "military access", false, false)
			scripting.game_interface:force_diplomacy("virginia", "france", "cancel military access", false, false)
			scripting.game_interface:force_diplomacy("virginia", "france", "alliance", false, false)
			scripting.game_interface:force_diplomacy("virginia", "france", "regions", false, false)
			scripting.game_interface:force_diplomacy("virginia", "france", "technology", false, false)
			scripting.game_interface:force_diplomacy("virginia", "france", "state_gift", false, false)
			scripting.game_interface:force_diplomacy("virginia", "france", "payments", false, false)
			scripting.game_interface:force_diplomacy("virginia", "france", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("virginia", "france", "peace", false, false)
			scripting.game_interface:force_diplomacy("virginia", "france", "war", false, false)

			scripting.game_interface:force_diplomacy("france", "virginia", "trade agreement", false, false)
			scripting.game_interface:force_diplomacy("france", "virginia", "military access", false, false)
			scripting.game_interface:force_diplomacy("france", "virginia", "cancel military access", false, false)
			scripting.game_interface:force_diplomacy("france", "virginia", "alliance", false, false)
			scripting.game_interface:force_diplomacy("france", "virginia", "regions", false, false)
			scripting.game_interface:force_diplomacy("france", "virginia", "technology", false, false)
			scripting.game_interface:force_diplomacy("france", "virginia", "state_gift", false, false)
			scripting.game_interface:force_diplomacy("france", "virginia", "payments", false, false)
			scripting.game_interface:force_diplomacy("france", "virginia", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("france", "virginia", "peace", false, false)
			scripting.game_interface:force_diplomacy("france", "virginia", "war", false, false)

			scripting.game_interface:force_diplomacy("france", "britain", "trade agreement", false, false)
			scripting.game_interface:force_diplomacy("france", "britain", "military access", false, false)
			scripting.game_interface:force_diplomacy("france", "britain", "cancel military access", false, false)
			scripting.game_interface:force_diplomacy("france", "britain", "alliance", false, false)
			scripting.game_interface:force_diplomacy("france", "britain", "regions", false, false)
			scripting.game_interface:force_diplomacy("france", "britain", "technology", false, false)
			scripting.game_interface:force_diplomacy("france", "britain", "state_gift", false, false)
			scripting.game_interface:force_diplomacy("france", "britain", "payments", false, false)
			scripting.game_interface:force_diplomacy("france", "britain", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("france", "britain", "peace", false, false)
			scripting.game_interface:force_diplomacy("france", "britain", "war", false, false)

			scripting.game_interface:force_diplomacy("britain", "france", "trade agreement", false, false)
			scripting.game_interface:force_diplomacy("britain", "france", "military access", false, false)
			scripting.game_interface:force_diplomacy("britain", "france", "cancel military access", false, false)
			scripting.game_interface:force_diplomacy("britain", "france", "alliance", false, false)
			scripting.game_interface:force_diplomacy("britain", "france", "regions", false, false)
			scripting.game_interface:force_diplomacy("britain", "france", "technology", false, false)
			scripting.game_interface:force_diplomacy("britain", "france", "state_gift", false, false)
			scripting.game_interface:force_diplomacy("britain", "france", "payments", false, false)
			scripting.game_interface:force_diplomacy("britain", "france", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("britain", "france", "peace", false, false)
			scripting.game_interface:force_diplomacy("britain", "france", "war", false, false)

			scripting.game_interface:force_diplomacy("virginia", "britain", "trade agreement", false, false)
			scripting.game_interface:force_diplomacy("virginia", "britain", "military access", false, false)
			scripting.game_interface:force_diplomacy("virginia", "britain", "cancel military access", false, false)
			scripting.game_interface:force_diplomacy("virginia", "britain", "alliance", false, false)
			scripting.game_interface:force_diplomacy("virginia", "britain", "regions", false, false)
			scripting.game_interface:force_diplomacy("virginia", "britain", "technology", false, false)
			scripting.game_interface:force_diplomacy("virginia", "britain", "state_gift", false, false)
			scripting.game_interface:force_diplomacy("virginia", "britain", "payments", false, false)
			scripting.game_interface:force_diplomacy("virginia", "britain", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("virginia", "britain", "peace", false, false)
			scripting.game_interface:force_diplomacy("virginia", "britain", "war", false, false)

			scripting.game_interface:force_diplomacy("britain", "virginia", "trade agreement", false, false)
			scripting.game_interface:force_diplomacy("britain", "virginia", "military access", false, false)
			scripting.game_interface:force_diplomacy("britain", "virginia", "cancel military access", false, false)
			scripting.game_interface:force_diplomacy("britain", "virginia", "alliance", false, false)
			scripting.game_interface:force_diplomacy("britain", "virginia", "regions", false, false)
			scripting.game_interface:force_diplomacy("britain", "virginia", "technology", false, false)
			scripting.game_interface:force_diplomacy("britain", "virginia", "state_gift", false, false)
			scripting.game_interface:force_diplomacy("britain", "virginia", "payments", false, false)
			scripting.game_interface:force_diplomacy("britain", "virginia", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("britain", "virginia", "peace", false, false)
			scripting.game_interface:force_diplomacy("britain", "virginia", "war", false, false)

			scripting.game_interface:force_diplomacy("virginia", "huron", "trade agreement", false, false)
			scripting.game_interface:force_diplomacy("virginia", "huron", "military access", false, false)
			scripting.game_interface:force_diplomacy("virginia", "huron", "cancel military access", false, false)
			scripting.game_interface:force_diplomacy("virginia", "huron", "alliance", false, false)
			scripting.game_interface:force_diplomacy("virginia", "huron", "regions", false, false)
			scripting.game_interface:force_diplomacy("virginia", "huron", "technology", false, false)
			scripting.game_interface:force_diplomacy("virginia", "huron", "state_gift", false, false)
			scripting.game_interface:force_diplomacy("virginia", "huron", "payments", false, false)
			scripting.game_interface:force_diplomacy("virginia", "huron", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("virginia", "huron", "peace", false, false)
			scripting.game_interface:force_diplomacy("virginia", "huron", "war", false, false)

			scripting.game_interface:force_diplomacy("huron", "virginia", "trade agreement", false, false)
			scripting.game_interface:force_diplomacy("huron", "virginia", "military access", false, false)
			scripting.game_interface:force_diplomacy("huron", "virginia", "cancel military access", false, false)
			scripting.game_interface:force_diplomacy("huron", "virginia", "alliance", false, false)
			scripting.game_interface:force_diplomacy("huron", "virginia", "regions", false, false)
			scripting.game_interface:force_diplomacy("huron", "virginia", "technology", false, false)
			scripting.game_interface:force_diplomacy("huron", "virginia", "state_gift", false, false)
			scripting.game_interface:force_diplomacy("huron", "virginia", "payments", false, false)
			scripting.game_interface:force_diplomacy("huron", "virginia", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("huron", "virginia", "peace", false, false)
			scripting.game_interface:force_diplomacy("huron", "virginia", "war", false, false)

			scripting.game_interface:force_diplomacy("france", "huron", "trade agreement", false, false)
			scripting.game_interface:force_diplomacy("france", "huron", "military access", false, false)
			scripting.game_interface:force_diplomacy("france", "huron", "cancel military access", false, false)
			scripting.game_interface:force_diplomacy("france", "huron", "alliance", false, false)
			scripting.game_interface:force_diplomacy("france", "huron", "regions", false, false)
			scripting.game_interface:force_diplomacy("france", "huron", "technology", false, false)
			scripting.game_interface:force_diplomacy("france", "huron", "state_gift", false, false)
			scripting.game_interface:force_diplomacy("france", "huron", "payments", false, false)
			scripting.game_interface:force_diplomacy("france", "huron", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("france", "huron", "peace", false, false)
			scripting.game_interface:force_diplomacy("france", "huron", "war", false, false)

			scripting.game_interface:force_diplomacy("huron", "france", "trade agreement", false, false)
			scripting.game_interface:force_diplomacy("huron", "france", "military access", false, false)
			scripting.game_interface:force_diplomacy("huron", "france", "cancel military access", false, false)
			scripting.game_interface:force_diplomacy("huron", "france", "alliance", false, false)
			scripting.game_interface:force_diplomacy("huron", "france", "regions", false, false)
			scripting.game_interface:force_diplomacy("huron", "france", "technology", false, false)
			scripting.game_interface:force_diplomacy("huron", "france", "state_gift", false, false)
			scripting.game_interface:force_diplomacy("huron", "france", "payments", false, false)
			scripting.game_interface:force_diplomacy("huron", "france", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("huron", "france", "peace", false, false)
			scripting.game_interface:force_diplomacy("huron", "france", "war", false, false)

			scripting.game_interface:force_diplomacy("virginia", "iroquoi", "trade agreement", true, true)
			scripting.game_interface:force_diplomacy("virginia", "iroquoi", "military access", true, true)
			scripting.game_interface:force_diplomacy("virginia", "iroquoi", "cancel military access", true, true)
			scripting.game_interface:force_diplomacy("virginia", "iroquoi", "alliance", true, true)
			scripting.game_interface:force_diplomacy("virginia", "iroquoi", "regions", true, true)
			scripting.game_interface:force_diplomacy("virginia", "iroquoi", "technology", false, false)
			scripting.game_interface:force_diplomacy("virginia", "iroquoi", "state_gift", true, true)
			scripting.game_interface:force_diplomacy("virginia", "iroquoi", "payments", true, true)
			scripting.game_interface:force_diplomacy("virginia", "iroquoi", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("virginia", "iroquoi", "peace", true, true)
			scripting.game_interface:force_diplomacy("virginia", "iroquoi", "war", true, true)

			scripting.game_interface:force_diplomacy("iroquoi", "virginia", "trade agreement", true, true)
			scripting.game_interface:force_diplomacy("iroquoi", "virginia", "military access", true, true)
			scripting.game_interface:force_diplomacy("iroquoi", "virginia", "cancel military access", true, true)
			scripting.game_interface:force_diplomacy("iroquoi", "virginia", "alliance", false, true)
			scripting.game_interface:force_diplomacy("iroquoi", "virginia", "regions", true, true)
			scripting.game_interface:force_diplomacy("iroquoi", "virginia", "technology", false, false)
			scripting.game_interface:force_diplomacy("iroquoi", "virginia", "state_gift", true, true)
			scripting.game_interface:force_diplomacy("iroquoi", "virginia", "payments", true, true)
			scripting.game_interface:force_diplomacy("iroquoi", "virginia", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("iroquoi", "virginia", "peace", true, true)
			scripting.game_interface:force_diplomacy("iroquoi", "virginia", "war", true, true)

		elseif conditions.TurnNumber(context) == 2 then
			if not niagara_issued then
				scripting.game_interface:trigger_custom_mission("ep2_capture_fortniagara", "virginia", "capture_city", 0, "algonquin_territory", "", "mission_text_text_ep2_capture_fort_niagara_text", "mission_text_text_reward_episodic_chapter_2", 0, "", context)
			end
		end
		
		if build_dockyard_issued and port_in_queue ~= 3 then
			effect.advance_scripted_advice_thread("0744_ep_2_building_dockyard", 1)
		elseif ship_issued and not ship_in_queue and slot_selected ~= 1 then
			effect.advance_scripted_advice_thread("0750_ep_2_recruit_frigate", 1)
		end
	else
		players_turn = false

-- ************************************************ FRENCH NAVIES LOCKED DOWN *********************************************

		if coast_safe then
			scripting.game_interface:disable_movement_for_character("faction:france,x:-470.86,y:309.70,r:1")
			scripting.game_interface:disable_movement_for_character("faction:france,x:-433.00,y:318.26,r:1")
			scripting.game_interface:disable_movement_for_character("faction:france,x:-450.55,y:310.48,r:1")
			scripting.game_interface:disable_movement_for_character("faction:france,x:-424.60,y:330.85,r:1")
			scripting.game_interface:disable_movement_for_character("faction:france,x:-426.59,y:347.94,r:1")
		end

-- ************************************************ FORT DUQUESNE *********************************************
		scripting.game_interface:disable_movement_for_character("faction:france,garrison:-1027369615")


-- ************************************************ FORT FRONTENAC *********************************************
		scripting.game_interface:disable_movement_for_character("faction:france,garrison:1222357690")


-- ************************************************ FORT BEAUSEJOUR *********************************************
		scripting.game_interface:disable_movement_for_character("faction:france,garrison:556552615")


-- ************************************************ FORT OSWEGO *********************************************
		scripting.game_interface:disable_movement_for_character("faction:france,garrison:1222336491")


-- ************************************************ FORT CHAMBLY *********************************************
		scripting.game_interface:disable_movement_for_character("faction:france,garrison:1227542677")

		scripting.game_interface:disable_movement_for_ai_under_shroud("virginia", context)
		if niagara_french then
			scripting.game_interface:disable_movement_for_character("faction:france,x:-551.73,y:296.85,r:1")
		end
	end
end

local function OnAdviceIssued(context)
	out.ting("Advice Issued")
	if conditions.AdviceJustDisplayed("1228307946", context) then
		mission_advice_given = 1	-- dockyard mission issued
	elseif conditions.AdviceJustDisplayed("-415261431", context) then
		mission_advice_given = 2	-- build shipyard
	elseif conditions.AdviceJustDisplayed("1010064931", context) then
		mission_advice_given = 3	-- demolish fishery
	elseif conditions.AdviceJustDisplayed("-728588108", context) then
		mission_advice_given = 4	--0750_ep_2_recruit_frigate
	elseif conditions.AdviceJustDisplayed("-1020790875", context) then
		mission_advice_given = 5	--0751_ep_2_recruit_frigate_2
	elseif conditions.AdviceJustDisplayed("1222703105", context) then
		scripting.HighlightComponent("button_government", true)
	end
end

local skipped_1 = false
local skipped_2 = false

local function skip_1()
	scripting.game_interface:set_zoom_limit(1.0, 1.0)
	CampaignUI.SetCameraZoom(1.0)
	CampaignUI.SetCameraTarget(-551, 267)
	scripting.game_interface:show_shroud(true)
	scripting.ShowHUD(true)
	scripting.game_interface:stop_user_input(false)
	effect.suspend_contextual_advice(false)
	scripting.game_interface:trigger_custom_mission("ep2_make_alliance_iroquois", "virginia", "forge_alliance", 0, "iroquoi", "", "mission_text_text_ep2_make_alliance_iroquois_text", "", 500, "", context)
	scripting.HighlightComponent("button_diplomacy", true)
end

local function skip_2()
	scripting.game_interface:set_zoom_limit(0.82, 1.0)
	CampaignUI.SetCameraZoom(1.0)
	CampaignUI.SetCameraTarget(-548, 267)
	scripting.ShowHUD(true)
	scripting.game_interface:stop_user_input(false)
	scripting.game_interface:show_shroud(true)
	scripting.game_interface:trigger_custom_mission("ep2_capture_louisbourg", "virginia", "capture_city", 0, "acadia", "", "mission_text_text_ep2_capture_louisbourg_text", "mission_text_text_reward_episodic_chapter_3", 0, "", context)
	event_message = 4
end

local function OnAdviceDismissed(context)
	if scripting.IsOnCampaignMap() then
		out.ting("Advice Dismissed")
		mission_advice_given = 0
		scripting.HighlightComponent("build_demolish", false)
		if conditions.AdviceJustDisplayed("1353749380", context) then
			-- intro
			if camera_pan ~= 0 then
				CampaignUI.StopCamera()
				skip_1()
				camera_pan = 0
			else
				skipped_1 = true
			end
		elseif conditions.AdviceJustDisplayed("546473525", context) then
			-- shroud 2
			if camera_pan ~= 0 then
				CampaignUI.StopCamera()
				skip_2()
				camera_pan = 0
			else
				skipped_2 = true
			end
		end
	end
end

local function OnMissionIssued(context)
	if conditions.MissionName("ep2_build_shipyard", context) then
		build_dockyard_issued = true
	elseif conditions.MissionName("ep2_recruit_naval_unit", context) then
		ship_issued = true
	elseif conditions.MissionName("ep2_capture_fortniagara", context) then
		niagara_issued = true
	end
end

local function OnMissionSucceeded(context)
	out.ting("Mission success " .. context.string)
	if conditions.MissionName("ep2_capture_fortniagara", context) then
		out.ting("ep2_capture_fortniagara")
		niagara_french = false
		event_message = 1
	elseif conditions.MissionName("ep2_capture_louisbourg", context) then
		out.ting("ep2_capture_louisbourg")
		event_message = 2
	elseif conditions.MissionName("ep2_make_alliance_iroquois", context) then
		out.ting("unlocking natives")
		scripting.EnableFeature("unlockable_natives")
		event_message = 3
	elseif conditions.MissionName("ep2_build_shipyard", context) then
		out.ting("ep2_build_shipyard")
		event_message = 5
		build_dockyard_issued = false
	else
		if conditions.MissionName("ep2_capture_quebec", context) then
			out.ting("ep2_capture_quebec")
			if part_1_completed then
				scripting.EnableFeature("disable_end_turn")
				event_message = 6
			else
				event_message = 0
				part_1_completed = true
			end
		elseif conditions.MissionName("ep2_capture_montreal", context) then
			out.ting("ep2_capture_montreal")
			if part_1_completed then
				scripting.EnableFeature("disable_end_turn")
				event_message = 6
			else
				event_message = 0
				part_1_completed = true
			end
		else
			event_message = 0
		end
	end
end

local function OnPanelOpenedCampaign(context)
	out.ting("Panel opened " .. context.string .. " " .. event_message)
	if conditions.IsComponentType("government_screens", context) then
		scripting.EnableFeature("Hide_excess_on_government_screen")
	elseif conditions.IsComponentType("region_info", context) then
		if government then
			scripting.EnableFeature("Hide_pop_on_region_details")
		else
			scripting.EnableFeature("Hide_excess_on_region_details")
		end
	elseif conditions.IsComponentType("missions", context) then
		scripting.EnableFeature("Hide_excess_on_mission_panel")
	elseif conditions.IsComponentType("diplomatic_relations", context) then
		scripting.HighlightComponent("button_diplomacy", false)
	end
end

local function OnPanelClosedCampaign(context)
	out.ting("panel closed " .. context.string .. "" .. event_message)
	if conditions.IsComponentType("event_message", context) then
		--[[ If you ever need checks exactly what message is up then this is how to do it
		local c = UIComponent(context.component)
		if scripting.game_interface:compare_localised_string(c:Find("dy_fields"), "mission_text_text_ep1_build_a_farm_heading") then
			out.ting("build farm mission panel closed")
		end]]

		-- we can do this simply with an int because the message we are tracking is alway on top
		if campaign_won == true then
			scripting.game_interface:advance_to_next_campaign()
			CampaignUI.QuitToMainScreen()
		elseif event_message == 6 then
			scripting.game_interface:declare_episode_two_victory()
			campaign_won = true
		elseif event_message == 1 then
			scripting.ShowHUD(false)
			scripting.game_interface:stop_user_input(true)
			scripting.game_interface:add_time_trigger("shroud_2_HUD_gone", 1)
			scripting.game_interface:show_shroud(false)
			effect.advance_scripted_advice_thread("0726_ep_2_shroud_2_unlocked", 1)
			game_progress = 1
		elseif event_message == 2 then
			--[[scripting.ShowHUD(false)
			scripting.game_interface:stop_user_input(true)
			scripting.game_interface:add_time_trigger("shroud_3_HUD_gone", 1)
			scripting.game_interface:show_shroud(false)]]--
			scripting.EnableFeature("list")
			scripting.HighlightComponent("button_lists", true)
			
			scripting.game_interface:force_diplomacy("virginia", "huron", "trade agreement", true, true)
			scripting.game_interface:force_diplomacy("virginia", "huron", "military access", true, true)
			scripting.game_interface:force_diplomacy("virginia", "huron", "cancel military access", true, true)
			scripting.game_interface:force_diplomacy("virginia", "huron", "alliance", true, true)
			scripting.game_interface:force_diplomacy("virginia", "huron", "regions", true, true)
			scripting.game_interface:force_diplomacy("virginia", "huron", "technology", false, false)
			scripting.game_interface:force_diplomacy("virginia", "huron", "state_gift", true, true)
			scripting.game_interface:force_diplomacy("virginia", "huron", "payments", true, true)
			scripting.game_interface:force_diplomacy("virginia", "huron", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("virginia", "huron", "peace", true, true)
			scripting.game_interface:force_diplomacy("virginia", "huron", "war", true, true)

			scripting.game_interface:force_diplomacy("huron", "virginia", "trade agreement", true, true)
			scripting.game_interface:force_diplomacy("huron", "virginia", "military access", true, true)
			scripting.game_interface:force_diplomacy("huron", "virginia", "cancel military access", true, true)
			scripting.game_interface:force_diplomacy("huron", "virginia", "alliance", true, true)
			scripting.game_interface:force_diplomacy("huron", "virginia", "regions", true, true)
			scripting.game_interface:force_diplomacy("huron", "virginia", "technology", false, false)
			scripting.game_interface:force_diplomacy("huron", "virginia", "state_gift", true, true)
			scripting.game_interface:force_diplomacy("huron", "virginia", "payments", true, true)
			scripting.game_interface:force_diplomacy("huron", "virginia", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("huron", "virginia", "peace", true, true)
			scripting.game_interface:force_diplomacy("huron", "virginia", "war", true, true)

			scripting.game_interface:force_diplomacy("france", "huron", "trade agreement", true, true)
			scripting.game_interface:force_diplomacy("france", "huron", "military access", true, true)
			scripting.game_interface:force_diplomacy("france", "huron", "cancel military access", true, true)
			scripting.game_interface:force_diplomacy("france", "huron", "alliance", true, true)
			scripting.game_interface:force_diplomacy("france", "huron", "regions", true, true)
			scripting.game_interface:force_diplomacy("france", "huron", "technology", false, false)
			scripting.game_interface:force_diplomacy("france", "huron", "state_gift", true, true)
			scripting.game_interface:force_diplomacy("france", "huron", "payments", true, true)
			scripting.game_interface:force_diplomacy("france", "huron", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("france", "huron", "peace", true, true)
			scripting.game_interface:force_diplomacy("france", "huron", "war", true, true)

			scripting.game_interface:force_diplomacy("huron", "france", "trade agreement", true, true)
			scripting.game_interface:force_diplomacy("huron", "france", "military access", true, true)
			scripting.game_interface:force_diplomacy("huron", "france", "cancel military access", true, true)
			scripting.game_interface:force_diplomacy("huron", "france", "alliance", true, true)
			scripting.game_interface:force_diplomacy("huron", "france", "regions", true, true)
			scripting.game_interface:force_diplomacy("huron", "france", "technology", false, false)
			scripting.game_interface:force_diplomacy("huron", "france", "state_gift", true, true)
			scripting.game_interface:force_diplomacy("huron", "france", "payments", true, true)
			scripting.game_interface:force_diplomacy("huron", "france", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("huron", "france", "peace", true, true)
			scripting.game_interface:force_diplomacy("huron", "france", "war", true, true)
			
			scripting.EnableFeature("show_shroud_2_3")
			scripting.game_interface:set_zoom_limit(1, 0.5)

			scripting.game_interface:trigger_custom_mission("ep2_capture_quebec", "virginia", "capture_city", 0, "new_france", "", "mission_text_text_ep2_capture_quebec_text", "mission_text_text_reward_episodic_complete_2", 0, "", context)
			scripting.game_interface:trigger_custom_mission("ep2_capture_montreal", "virginia", "capture_city", 0, "ontario", "", "mission_text_text_ep2_capture_montreal_text", "mission_text_text_reward_episodic_complete_2", 0, "", context)
			game_progress = 2
			--effect.advance_scripted_advice_thread("0728_ep_2_shroud_3_unlocked", 1)
		elseif event_message == 3 then
			effect.advance_scripted_advice_thread("0741_ep_2_recruit_natives", 1)
			if not niagara_issued then
				scripting.game_interface:trigger_custom_mission("ep2_capture_fortniagara", "virginia", "capture_city", 0, "algonquin_territory", "", "mission_text_text_ep2_capture_fort_niagara_text", "mission_text_text_reward_episodic_chapter_2", 0, "", context)
			end
		elseif event_message == 4 then
			if port_in_queue ~= 3 then
				scripting.game_interface:trigger_custom_mission("ep2_build_shipyard", "virginia", "build_building", 0, "dockyard", "", "mission_text_text_ep2_build_shipyard_text", "", 500, "", context)
			else
				scripting.game_interface:trigger_custom_mission("ep2_recruit_naval_unit", "virginia", "recruit_unit", 0, "episodic_2_5th_rate", "", "mission_text_text_ep2_recruit_ship_of_the_line_text", "", 500, "", context)
			end
		elseif event_message == 5 then
			scripting.game_interface:trigger_custom_mission("ep2_recruit_naval_unit", "virginia", "recruit_unit", 0, "episodic_2_5th_rate", "", "mission_text_text_ep2_recruit_ship_of_the_line_text", "", 500, "", context)
		end
		event_message = 0
	end
end

local function OnCharacterSelected(context)
	if CampaignUI.PlayerSelected() then
		slot_selected = 0
		scripting.HighlightComponent("build_demolish", false)
	end
end

local function OnFortSelected(context)
	if CampaignUI.PlayerSelected() then
		slot_selected = 0
		scripting.HighlightComponent("build_demolish", false)
	end
end

local function OnSettlementSelected(context)
	scripting.EnableFeature("Hide_infrastructure_tab_review_panel")
	if CampaignUI.PlayerSelected() then
		slot_selected = 0
		scripting.HighlightComponent("build_demolish", false)
		if conditions.SettlementIsLocal(context) and conditions.SettlementName("settlement:algonquin_territory:niagara", context) and not government then
			scripting.EnableFeature("government")
			effect.advance_scripted_advice_thread("0727_ep_2_tax", 1)
			government = true
		--elseif conditions.SettlementName("settlement:virginia:williamsburg", context) then
		end
	end
end

local function OnSlotSelected(context)
	scripting.EnableFeature("Hide_infrastructure_tab_review_panel")
	if CampaignUI.PlayerSelected() then
		if conditions.SlotName("port:virginia:yorktown", context) then
			slot_selected = 1
			if mission_advice_given == 1 then
				if port_in_queue == 0 then
					-- you need to build a ship yard
					effect.advance_scripted_advice_thread("0747_ep_2_build_shipyard", 1)
				elseif port_in_queue == 1 then
					-- demolish fishery
					effect.advance_scripted_advice_thread("0745_ep_2_dismantle_chain", 1)
					scripting.HighlightComponent("build_demolish", true)
				elseif port_in_queue == 2 then
					-- upgrade your shipyard into dockyard
					effect.advance_scripted_advice_thread("0749_ep_2_build_dockyard", 1)
				end
			elseif mission_advice_given == 4 then
				-- now click on recuitment
				effect.advance_scripted_advice_thread("0751_ep_2_recruit_frigate_2", 1)
			end
		else
			slot_selected = 0
			scripting.HighlightComponent("build_demolish", false)
		end
	end
end

local function OnComponentLClickUp(context)
	out.ting("Component clicked " .. context.string)
	if conditions.IsComponentType("construction_tab", context) then
		scripting.EnableFeature("Hide_infrastructure_tab_review_panel")
	elseif conditions.IsComponentType("button_lists", context) then
		scripting.HighlightComponent("button_lists", false)
	elseif conditions.IsComponentType("button_government", context) then
		scripting.HighlightComponent("button_government", false)
	elseif conditions.IsComponentType("build_demolish", context) then
		scripting.HighlightComponent("build_demolish", false)
		if mission_advice_given == 3 and slot_selected == 1 then
			port_in_queue = 0
			effect.advance_scripted_advice_thread("0746_ep_2_wait_turn", 1)
		end
	elseif conditions.IsComponentType("naval_recruitment_tab", context) and mission_advice_given == 5 then
		effect.advance_scripted_advice_thread("0752_ep_2_recruit_frigate_3", 1)
	end
end

local function OnLocationEntered(context)
	if conditions.MapPosition(-564, 289, context) then
		scripting.game_interface:trigger_custom_mission("ep2_capture_fort_duquesne_1", "virginia", "capture_fort", 0, "-1027369615", "", "mission_text_text_ep2_capture_fort_duquesne_1_text", "", 500, "", context)
		if players_turn then
			scripting.game_interface:cancel_actions_for(context)
		end
	elseif conditions.MapPosition(-449.57, 326.78, context) then
		coast_safe = false
	end
end

local function OnBuildingConstructionIssuedByPlayer(context)
	if conditions.BuildingLevelName("local_fishery", context) then
		port_in_queue = 1
	elseif conditions.BuildingLevelName("shipyard", context) then
		port_in_queue = 2
		if mission_advice_given == 2 then
			effect.advance_scripted_advice_thread("0748_ep_2_shipyard_building", 1)
		end
	elseif conditions.BuildingLevelName("dockyard", context) then
		port_in_queue = 3
	end	
end

local function OnRecruitmentItemIssuedByPlayer(context)
	if conditions.UnitType("episodic_2_5th_rate", context) then
		ship_in_queue = true
	end
end

local function OnSettlementOccupied(context)
	if conditions.SettlementIsLocal(context) and not conditions.SettlementName("settlement:algonquin_territory:niagara", context) and not government then
		-- when the player capture any settlement except niagara
		scripting.EnableFeature("government")
		effect.advance_scripted_advice_thread("0727_ep_2_tax", 1)
		government = true
	end
end

local function OnSavingGame(context)
	scripting.game_interface:save_value(part_1_completed, context)
	scripting.game_interface:save_value(game_progress, context)

	scripting.game_interface:save_value(build_dockyard_issued, context)
	scripting.game_interface:save_value(port_in_queue, context)
	scripting.game_interface:save_value(ship_issued, context)
	scripting.game_interface:save_value(ship_in_queue, context)
	scripting.game_interface:save_value(niagara_french, context)
	scripting.game_interface:save_value(government, context)
	scripting.game_interface:save_value(niagara_issued, context)
	scripting.game_interface:save_value(coast_safe, context)
end

local function OnLoadingGame(context)
	part_1_completed =			scripting.game_interface:load_value(false, context)
	game_progress =				scripting.game_interface:load_value(0, context)
	
	build_dockyard_issued =		scripting.game_interface:load_value(false, context)
	port_in_queue =				scripting.game_interface:load_value(0, context)
	ship_issued =				scripting.game_interface:load_value(false, context)
	ship_in_queue =				scripting.game_interface:load_value(false, context)
	niagara_french =			scripting.game_interface:load_value(true, context)
	government =	 			scripting.game_interface:load_value(false, context)
	niagara_issued =			scripting.game_interface:load_value(false, context)
	coast_safe =				scripting.game_interface:load_value(true, context)
end

local function OnWorldCreated()
	scripting.game_interface:add_unit_model_overrides("faction:virginia,surname:577", "campaign_washington_young")
end

local function OnUICreated()
	scripting.game_interface:display_turns(true)
	if government then
		scripting.EnableFeature("government")
	end
	if game_progress == 2 then
		scripting.EnableFeature("list")
	end
end

--******************************************************** START POS PAN ********************************************************
local function OnTimeTrigger(context)
	out.ting(context.string)
	local	x, y, z, theatre = CampaignUI.CameraTarget()
--************ FIRST CAMERA PAN CO-ORDINATES ****************************************************
	if context.string == "intro_hold" then
		CampaignUI.ScrollCamera(8,	{x, z, y},
									{x, z, 1.0})
		camera_pan = 1
	elseif context.string == "intro_VO_delay" then
		effect.advance_scripted_advice_thread("0725_ep_2_intro", 1)
	elseif context.string == "intro_camera_zoom_finishes" then
		if skipped_1 then
			skip_1()
		else
			CampaignUI.ScrollCamera(12,	{x, z, y},
										{-563, 286, 1.0},
										{-541, 285, 1.0},
										{-551, 267, 1.0})
			camera_pan = 2
		end
	elseif context.string == "intro_camera_pan_finishes" then
		scripting.game_interface:show_shroud(true)
		scripting.ShowHUD(true)
		scripting.game_interface:stop_user_input(false)
		effect.suspend_contextual_advice(false)
		scripting.game_interface:add_time_trigger("intro_HUD_shown", 2)
	elseif context.string == "intro_HUD_shown" then
		scripting.game_interface:trigger_custom_mission("ep2_make_alliance_iroquois", "virginia", "forge_alliance", 0, "iroquoi", "", "mission_text_text_ep2_make_alliance_iroquois_text", "", 500, "", context)
		scripting.HighlightComponent("button_diplomacy", true)

--************ Second CAMERA PAN CO-ORDINATES ****************************************************
	elseif context.string == "shroud_2_HUD_gone" then
		if skipped_2 then
			skip_2()
		else
			scripting.EnableFeature("show_shroud_2_2")
			scripting.game_interface:set_zoom_limit(1, 0.02)
			CampaignUI.ScrollCamera(10,	{x, z, y},
										{-528.716, 302.126, 1.0},
										--{-516.786, 322.630, 1.0},
										{-489, 325, 0.9},
										{-429.875, 327.096, 1.0})
			camera_pan = 3
		end
	elseif context.string == "shroud_2_camera_pan_1_finishes" then
		if skipped_2 then
			skip_2()
		else
			scripting.game_interface:set_zoom_limit(1.08, 0.02)
			CampaignUI.ScrollCamera(8,	{x, z, y},
										{-517, 273, 0.07},
										{-548, 267, 1.0})
			camera_pan = 4
		end
	elseif context.string == "shroud_2_camera_pan_finishes" then
		scripting.ShowHUD(true)
		scripting.game_interface:stop_user_input(false)
		scripting.game_interface:show_shroud(true)
		scripting.game_interface:add_time_trigger("shroud_2_HUD_shown", 2)
	elseif context.string == "shroud_2_HUD_shown" then
		scripting.game_interface:trigger_custom_mission("ep2_capture_louisbourg", "virginia", "capture_city", 0, "acadia", "", "mission_text_text_ep2_capture_louisbourg_text", "mission_text_text_reward_episodic_chapter_3", 0, "", context)
		event_message = 4

--************ third CAMERA PAN CO-ORDINATES Removed ****************************************************
	elseif context.string == "shroud_3_HUD_gone" then
		scripting.EnableFeature("show_shroud_2_3")
		scripting.game_interface:set_zoom_limit(1, 0.02)
		CampaignUI.ScrollCamera(8,	{x, z, y},
									{-475, 329, 0.9},
									{-504, 335, 1.0})
		camera_pan = 5
	elseif context.string == "shroud_3_camera_pan_1_finishes" then
		scripting.game_interface:set_zoom_limit(1, 0.7)
		CampaignUI.ScrollCamera(3,	{x, z, y},
									{-504, 335, 1.0},
									{-525, 324, 1.0})

		camera_pan = 6
	elseif context.string == "shroud_3_camera_pan_2_finishes" then
		scripting.game_interface:set_zoom_limit(1, 0.7)
		CampaignUI.ScrollCamera(6,	{x, z, y},
									{-489, 325, 0.7},
									{-429, 330, y})

		camera_pan = 7
	elseif context.string == "shroud_3_camera_pan_finishes" then
		scripting.ShowHUD(true)
		scripting.game_interface:stop_user_input(false)
		scripting.game_interface:show_shroud(true)
		scripting.game_interface:add_time_trigger("shroud_3_HUD_shown", 2)
	elseif context.string == "shroud_3_HUD_shown" then
		scripting.game_interface:trigger_custom_mission("ep2_capture_quebec", "virginia", "capture_city", 0, "new_france", "", "mission_text_text_ep2_capture_quebec_text", "mission_text_text_reward_episodic_complete_2", 0, "", context)
		scripting.game_interface:trigger_custom_mission("ep2_capture_montreal", "virginia", "capture_city", 0, "ontario", "", "mission_text_text_ep2_capture_montreal_text", "mission_text_text_reward_episodic_complete_2", 0, "", context)
	end
end

local function OnCameraMoverFinished(context)
	if camera_pan == 1 then
		scripting.game_interface:add_time_trigger("intro_camera_zoom_finishes", 1)
		scripting.game_interface:set_zoom_limit(1.0, 1.0)
	elseif camera_pan == 2 then
		scripting.game_interface:add_time_trigger("intro_camera_pan_finishes", 2)
		scripting.game_interface:set_zoom_limit(1.0, 1.0)
	elseif camera_pan == 3 then
		scripting.game_interface:add_time_trigger("shroud_2_camera_pan_1_finishes", 2)
		scripting.game_interface:set_zoom_limit(1.0, 1.0)
	elseif camera_pan == 4 then
		scripting.game_interface:add_time_trigger("shroud_2_camera_pan_finishes", 2)
		scripting.game_interface:set_zoom_limit(0.82, 1.0)
	elseif camera_pan == 5 then
		scripting.game_interface:add_time_trigger("shroud_3_camera_pan_1_finishes", 2)
		scripting.game_interface:set_zoom_limit(0.5, 1.0)
	elseif camera_pan == 6 then
		scripting.game_interface:add_time_trigger("shroud_3_camera_pan_2_finishes", 2)
		scripting.game_interface:set_zoom_limit(0.5, 1.0)
	elseif camera_pan == 7 then
		scripting.game_interface:add_time_trigger("shroud_3_camera_pan_finishes", 2)
		scripting.game_interface:set_zoom_limit(0.5, 1.0)
	end
	camera_pan = 0
end
--******************************************************** START POS PAN ********************************************************

--[[local function OnUngarrisonedFort(context)
	if conditions.FortName("Fort Duquesne", context) then
		out.ting("fort duquesne emptied")
		niagara_french = false
	end
end]]

--------------------------------------------------------------------------------------------------------------------
-- Add event callbacks
-- For a list of all events supported create a "documentation" directory in your empire directory, run a debug build of the game and see
-- the events.txt file
--------------------------------------------------------------------------------------------------------------------

scripting.AddEventCallBack("UICreated",	OnUICreated)
scripting.AddEventCallBack("WorldCreated", OnWorldCreated)
scripting.AddEventCallBack("FactionTurnStart", OnFactionTurnStart)
scripting.AddEventCallBack("MissionSucceeded", OnMissionSucceeded)
scripting.AddEventCallBack("MissionIssued", OnMissionIssued)
scripting.AddEventCallBack("PanelOpenedCampaign", OnPanelOpenedCampaign)
scripting.AddEventCallBack("PanelClosedCampaign", OnPanelClosedCampaign)
scripting.AddEventCallBack("CharacterSelected", OnCharacterSelected)
scripting.AddEventCallBack("FortSelected", OnFortSelected)
scripting.AddEventCallBack("SettlementSelected", OnSettlementSelected)
scripting.AddEventCallBack("SlotSelected", OnSlotSelected)
scripting.AddEventCallBack("ComponentLClickUp", OnComponentLClickUp)
scripting.AddEventCallBack("LocationEntered", OnLocationEntered)
scripting.AddEventCallBack("TimeTrigger", OnTimeTrigger)
scripting.AddEventCallBack("CameraMoverFinished", OnCameraMoverFinished)
scripting.AddEventCallBack("SavingGame", OnSavingGame)
scripting.AddEventCallBack("LoadingGame", OnLoadingGame)
scripting.AddEventCallBack("RecruitmentItemIssuedByPlayer", OnRecruitmentItemIssuedByPlayer)
scripting.AddEventCallBack("BuildingConstructionIssuedByPlayer", OnBuildingConstructionIssuedByPlayer)
scripting.AddEventCallBack("AdviceIssued", OnAdviceIssued)
scripting.AddEventCallBack("AdviceDismissed", OnAdviceDismissed)
scripting.AddEventCallBack("SettlementOccupied", OnSettlementOccupied)
--scripting.AddEventCallBack("UngarrisonedFort", OnUngarrisonedFort)
