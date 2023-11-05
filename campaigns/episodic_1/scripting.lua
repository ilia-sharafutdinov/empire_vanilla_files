local core = require "ui/CoreUtils"
core.Require "export_ep1_advice"
core.Require "advice"
local scripting			= core.Require "EpisodicScripting"

scripting.SetCampaign("episodic_1")

--------------------------------------------------------------------------------------------------------------------
-- Define functions here
-- For a list of all supported commands see the wiki page http://console/empire/Empire%20Wiki/Campaign%20Interface.aspx
--------------------------------------------------------------------------------------------------------------------

local build_farm_issued = false
local farm_in_queue = false

local build_fishery_issued = false
local fishery_in_queue = false

local build_plantation_issued = false
local plantation_in_queue = false

local train_unit_issued = false
local unit_in_queue = false
local unit_trained = 0

local slot_selected = 0
local mission_advice_given = 0

local first_turn = true
local advice_on_screen = false

local protect_village = true
local protect_pass = true

local camera_pan = 0
local event_message = 0
local campaign_won = false
local players_turn = true

local function OnFactionTurnStart(context)
	if conditions.FactionIsLocal(context) then
		players_turn = true
		if conditions.TurnNumber(context) == 1 then
			scripting.EnableFeature("show_shroud_1_1")
			scripting.game_interface:set_zoom_limit(1.08, 0.02)
			CampaignUI.SetCameraZoom(1.06)
			CampaignUI.SetCameraTarget(-546.819, 265.053)
			scripting.game_interface:add_time_trigger("intro_hold", 1)
			scripting.game_interface:add_time_trigger("intro_VO_delay", 1)
			scripting.game_interface:stop_user_input(true)

			scripting.game_interface:add_attack_of_opportunity_overrides("faction:powhatan,x:-535.585,y:293.602,r:1", true)

			scripting.game_interface:force_diplomacy("powhatan", "virginia_colonists", "trade agreement", false, false)
			scripting.game_interface:force_diplomacy("powhatan", "virginia_colonists", "military access", false, false)
			scripting.game_interface:force_diplomacy("powhatan", "virginia_colonists", "cancel military access", false, false)
			scripting.game_interface:force_diplomacy("powhatan", "virginia_colonists", "alliance", false, false)
			scripting.game_interface:force_diplomacy("powhatan", "virginia_colonists", "regions", false, false)
			scripting.game_interface:force_diplomacy("powhatan", "virginia_colonists", "technology", false, false)
			scripting.game_interface:force_diplomacy("powhatan", "virginia_colonists", "state_gift", false, false)
			scripting.game_interface:force_diplomacy("powhatan", "virginia_colonists", "payments", false, false)
			scripting.game_interface:force_diplomacy("powhatan", "virginia_colonists", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("powhatan", "virginia_colonists", "peace", false, false)
			scripting.game_interface:force_diplomacy("powhatan", "virginia_colonists", "war", false, false)
			
			scripting.game_interface:add_time_trigger("end_turn_prod", 120)
		end

		if unit_trained ~= 0 and slot_selected ~= 4 then
			effect.advance_scripted_advice_thread("0715_ep_1_garrisoned_units_1", 1)
		end
		if build_farm_issued and not farm_in_queue and slot_selected ~= 1 then
			effect.advance_scripted_advice_thread("0723_ep_1_construct_farm_1", 1)
		end
		if build_fishery_issued and not fishery_in_queue and slot_selected ~= 2 then
			effect.advance_scripted_advice_thread("0708_ep_1_construct_fishery_1", 1)
		end
		--[[if build_plantation_issued and not plantation_in_queue and slot_selected ~= 3 then
			effect.advance_scripted_advice_thread("0706_ep_1_construct_plantation_1", 1)
		end]]
		if train_unit_issued and not unit_in_queue and slot_selected ~= 4 then
			effect.advance_scripted_advice_thread("0710_ep_recruit_unit_1", 1)
		end
	else
		scripting.HighlightComponent("button_end_turn", false)

		players_turn = false
		scripting.game_interface:disable_movement_for_ai_under_shroud("virginia_colonists", context)
		scripting.game_interface:set_campaign_ai_force_all_factions_boardering_humans_to_have_invasion_behaviour(false)
		scripting.game_interface:set_campaign_ai_force_all_factions_boardering_human_protectorates_to_have_invasion_behaviour(false)

-- ************************************************ Wahun...***************************************************
		--[[if protect_village then
			scripting.game_interface:disable_movement_for_character("faction:powhatan,x:-540.00,y:276.00,r:1")
		end]]

-- ************************************************ Shackamaxon *********************************************
		if protect_pass then
			scripting.game_interface:disable_movement_for_character("faction:powhatan,x:-535.585,y:293.602,r:1")
		end

		scripting.game_interface:disable_movement_for_character("faction:powhatan,garrison:settlement:pennsylvania:ep_1_philadelphia")
		scripting.game_interface:disable_movement_for_character("faction:powhatan,garrison:settlement:maryland:annapolis")

	end
end

local function OnFactionTurnEnd()
	first_turn = false
end

local function OnAdviceIssued(context)
	out.ting("Advice Issued")
	advice_on_screen = true
	if conditions.AdviceJustDisplayed("1219323522", context) then
		mission_advice_given = 1	-- farm
	elseif conditions.AdviceJustDisplayed("1222098470", context) then
		mission_advice_given = 1	-- farm level 2
	elseif conditions.AdviceJustDisplayed("1278367614", context) then
		mission_advice_given = 2	-- fishery
	elseif conditions.AdviceJustDisplayed("655610075", context) then
		scripting.HighlightConstructionItem("corn_peasant_farms", true)
	elseif conditions.AdviceJustDisplayed("1874367125", context) then
		mission_advice_given = 2	-- fishery level 2
	elseif conditions.AdviceJustDisplayed("1297297515", context) then
		mission_advice_given = 3	-- plantation
	elseif conditions.AdviceJustDisplayed("-1749073444", context) then
		mission_advice_given = 4	-- recruit1
	elseif conditions.AdviceJustDisplayed("-1396032595", context) then
		mission_advice_given = 5	-- recruit2
	elseif conditions.AdviceJustDisplayed("571171380", context) then
		mission_advice_given = 6	-- unit trained
	elseif conditions.AdviceJustDisplayed("1193994377", context) then
		mission_advice_given = 7	-- unit trained2
		scripting.HighlightComponent("army_tab", true)
	elseif conditions.AdviceJustDisplayed("1152775702", context) then
		mission_advice_given = 8	-- unit trained3
	end
end

local function OnAdviceDismissed(context)
	out.ting("Advice Dismissed")
	if conditions.AdviceJustDisplayed("655610075", context) then
		scripting.HighlightConstructionItem("corn_peasant_farms", false)
	elseif conditions.AdviceJustDisplayed("1193994377", context) then
		scripting.HighlightComponent("army_tab", false)
	elseif conditions.AdviceJustDisplayed("1218036552", context) or conditions.AdviceJustDisplayed("-772138412", context) then
		-- skip intro
		if camera_pan == 1 then
  			CampaignUI.StopCamera()
  			camera_pan = 0
  			scripting.game_interface:set_zoom_limit(1.0, 1.0)
  			CampaignUI.SetCameraZoom(1.0)
  			CampaignUI.SetCameraTarget(-546.819, 265.053)
			scripting.ShowHUD(true)
			scripting.game_interface:stop_user_input(false)
			effect.suspend_contextual_advice(false)
			scripting.game_interface:trigger_custom_mission("ep1_build_farm", "virginia_colonists", "build_building", 0, "corn_peasant_farms", "", "mission_text_text_ep1_build_a_farm_text", "", 500, "", context)
		end
	elseif conditions.AdviceJustDisplayed("-132949274", context) then
		if camera_pan == 2 then
  			CampaignUI.StopCamera()
  			camera_pan = 0
  			scripting.game_interface:set_zoom_limit(1.0, 1.0)
  			CampaignUI.SetCameraZoom(1.0)
  			CampaignUI.SetCameraTarget(-548, 267)
			scripting.ShowHUD(true)
			scripting.game_interface:stop_user_input(false)
			scripting.game_interface:trigger_custom_mission("ep1_capture_settlement_maryland", "virginia_colonists", "capture_city", 0, "maryland", "", "mission_text_text_ep1_capture_enemy_village_text", "mission_text_text_reward_episodic_chapter_3", 0, "", context)
		end
	elseif conditions.AdviceJustDisplayed("-1164861841", context) then
		if camera_pan == 3 then
  			CampaignUI.StopCamera()
  			camera_pan = 0
  			scripting.game_interface:set_zoom_limit(1.0, 1.0)
  			CampaignUI.SetCameraZoom(1.0)
  			CampaignUI.SetCameraTarget(-540, 273)
			scripting.ShowHUD(true)
			scripting.game_interface:stop_user_input(false)
			scripting.game_interface:trigger_custom_mission("ep1_capture_settlement_pennsylvania", "virginia_colonists", "capture_city", 0, "pennsylvania", "", "mission_text_text_ep1_capture_enemy_city_text", "mission_text_text_reward_episodic_complete_1", 0, "", context)
		end
	end
	advice_on_screen = false
	mission_advice_given = 0
end

local function OnMissionSucceeded(context)
	out.ting("Mission success " .. context.string)
	if conditions.MissionName("ep1_build_farm", context) then
		out.ting("ep1_build_farm")
		event_message = 1
	elseif conditions.MissionName("ep1_build_fishery", context) then
		out.ting("ep1_build_fishery")
		scripting.game_interface:episodic_defend("powhatan", "maryland")
		scripting.game_interface:add_location_trigger( -546, 280, 7.0, "virginia_colonists" )
		event_message = 2
	elseif conditions.MissionName("ep1_capture_settlement_maryland", context) then
		out.ting("ep1_capture_settlement_maryland")
		scripting.game_interface:episodic_defend("powhatan", "pennsylvania")
		protect_village = false
		event_message = 3
	elseif conditions.MissionName("ep1_capture_settlement_pennsylvania", context) then
		event_message = 4
		scripting.EnableFeature("disable_end_turn")
	else
		event_message = 0
	end
end

local function OnSettlementOccupied(context)
	out.ting("Settlement taken " .. context.string)
	if conditions.SettlementName("settlement:pennsylvania:ep_1_philadelphia", context) then
		out.ting("pennsylvania:ep_1_philadelphia")
	end
end

local function OnPanelOpenedCampaign(context)
	out.ting("Panel opened " .. context.string)
	if conditions.IsComponentType("region_info", context) then
		scripting.EnableFeature("Hide_excess_on_region_details")
	elseif conditions.IsComponentType("missions", context) then
		scripting.EnableFeature("Hide_excess_on_mission_panel")
	end
end

local function OnPanelClosedCampaign(context)
	out.ting("panel closed " .. context.string)
	if conditions.IsComponentType("event_message", context) then
		--[[ If you ever need checks exactly what message is up then this is how to do it
		local c = UIComponent(context.component)
		if scripting.game_interface:compare_localised_string(c:Find("dy_fields"), "mission_text_text_ep1_build_a_farm_heading") then
			out.ting("build farm mission panel closed")
		end]]
		if campaign_won == true then
			scripting.game_interface:advance_to_next_campaign()
			CampaignUI.QuitToMainScreen()
		elseif event_message == 1 then
			scripting.EnableFeature("spawn_port")
			scripting.game_interface:trigger_custom_mission("ep1_build_fishery", "virginia_colonists", "build_building", 0, "local_fishery", "", "mission_text_text_ep1_build_fishery_text", "mission_text_text_reward_episodic_chapter_2", 0, "", context)
		elseif event_message == 2 then
			scripting.ShowHUD(false)
			scripting.game_interface:add_time_trigger("shroud_2_HUD_gone", 0.5)
			scripting.game_interface:stop_user_input(true)
		elseif event_message == 3 then
			scripting.ShowHUD(false)
			scripting.game_interface:add_time_trigger("shroud_3_HUD_gone", 0.5)
			scripting.game_interface:stop_user_input(true)
		elseif event_message == 4 then
			scripting.game_interface:declare_episode_one_victory()
			campaign_won = true
		end
		event_message = 0
	end
end

local function OnComponentLClickUp(context)
	out.ting("Component clicked " .. context.string .. " Current Advice " .. mission_advice_given)
	if conditions.IsComponentType("construction_tab", context) then
		scripting.EnableFeature("Hide_excess_on_review_panel")
	elseif conditions.IsComponentType("recruitment_tab", context) and mission_advice_given == 5 then
		effect.advance_scripted_advice_thread("0712_ep_1_recruit_unit_3", 1)
	elseif conditions.IsComponentType("army_tab", context) and mission_advice_given == 7 then
		effect.advance_scripted_advice_thread("0717_ep_1_garrisoned_units_3", 1)
	elseif conditions.IsComponentType("unit16", context) and mission_advice_given == 8 then
		effect.advance_scripted_advice_thread("0718_ep_1_garrisoned_units_4", 1)
	end
end

local function OnCharacterSelected(context)
	if CampaignUI.PlayerSelected() then
		out.ting("Character selected")
		slot_selected = 0
		effect.advance_scripted_advice_thread("0713_ep_1_select_player_army", 1)
	end
end

local function OnFortSelected(context)
	if CampaignUI.PlayerSelected() then
		out.ting("fort selected")
		slot_selected = 0
	end
	scripting.EnableFeature("Hide_excess_on_review_panel")
end

local function OnSettlementSelected(context)
	if CampaignUI.PlayerSelected() then
		out.ting("Settlement selected. Current Advice " .. mission_advice_given)
		if conditions.SettlementName("settlement:virginia:williamsburg", context) then
			slot_selected = 4
			if mission_advice_given == 4 then
				effect.advance_scripted_advice_thread("0711_ep_1_recruit_unit_2", 1)
			elseif mission_advice_given == 6 then
				effect.advance_scripted_advice_thread("0716_ep_1_garrisoned_units_2", 1)
			else
				effect.advance_scripted_advice_thread("0701_ep1_settlement_basics", 1)
			end
		else
			slot_selected = 0
		end
	end
	scripting.EnableFeature("Hide_excess_on_review_panel")
end

local function OnSlotSelected(context)
	if CampaignUI.PlayerSelected() then
		out.ting("Slot selected, current advice is ", mission_advice_given)
		if conditions.SlotName("corn:virginia:north", context) then
			out.ting("Corn")
			slot_selected = 1
			if mission_advice_given == 1 then
				effect.advance_scripted_advice_thread("0724_ep1_construct_farm_2", 1)
			end
		elseif conditions.SlotName("port:virginia:yorktown", context) then
			out.ting("Port")
			slot_selected = 2
			if mission_advice_given == 2 then
				effect.advance_scripted_advice_thread("0709_ep_1_construct_fishery_2", 1)
			end
		elseif conditions.SlotName("southern_usa:virginia:central", context) then
			out.ting("Plantation")
			slot_selected = 3
			effect.advance_scripted_advice_thread("0737_ep_1_Jamestown_slots", 1)
			if mission_advice_given == 3 then
				effect.advance_scripted_advice_thread("0707_ep_1_construct_plantation_2", 1)
			end
		else
			slot_selected = 0
		end
	end
	scripting.EnableFeature("Hide_excess_on_review_panel")
end

local function OnMissionIssued(context)
	if conditions.MissionName("ep1_build_farm", context) then
		build_farm_issued = true
	elseif conditions.MissionName("ep1_build_fishery", context) then
		build_fishery_issued = true
	--[[elseif conditions.MissionName("small_tobacco_plantation", context) then
		build_plantation_issued = true]]
	elseif conditions.MissionName("ep1_recruit_unit", context) then
		train_unit_issued = true
	end
end

local function OnBuildingConstructionIssuedByPlayer(context)
	effect.advance_scripted_advice_thread("0705_ep_1_build_queues", 1)
	out.ting("Building added")
	if conditions.BuildingLevelName("corn_peasant_farms", context) then
		out.ting("farm")
		farm_in_queue = true
		scripting.HighlightComponent("button_end_turn", false)
	elseif conditions.BuildingLevelName("local_fishery", context) then
		out.ting("fishery")
		fishery_in_queue = true
	--[[elseif conditions.BuildingLevelName("small_tobacco_plantation", context) then
		out.ting("tobacco plantation")
		plantation_in_queue = true]]
	end
end

local function OnRecruitmentItemIssuedByPlayer(context)
	effect.advance_scripted_advice_thread("0735_ep_1_recruitment_queue", 1)
	out.ting("Unit added")
	if conditions.UnitType("episodic_1_arquebusiers", context) then
		out.ting("episodic_1_arquebusiers added")
		unit_in_queue = true;
	end
end

local function OnMovementPointsExhausted(context)
	if conditions.TurnNumber(context) == 1 then
		effect.advance_scripted_advice_thread("0714_ep1_end_turn", 1)
	end
end

local function OnUnitTrained(context)
	unit_trained = unit_trained + 1
end

local function OnLocationEntered(context)
	if conditions.MapPosition(-546, 280, context) and unit_trained == 0 then
		scripting.game_interface:trigger_custom_mission("ep1_recruit_unit", "virginia_colonists", "recruit_unit", 0, "episodic_1_arquebusiers", "", "mission_text_text_ep1_recruit_unit_text", "", 500, "", context)
		if players_turn then
			scripting.game_interface:cancel_actions_for(context)
		end
	elseif conditions.MapPosition(-546, 290, context) then
		protect_pass = false
	end
end

local function OnWorldCreated()
	scripting.game_interface:add_unit_model_overrides("faction:virginia_colonists,surname:522", "campaign_john_smith")
end

local function OnSavingGame(context)
	scripting.game_interface:save_value(build_farm_issued, context)
	scripting.game_interface:save_value(farm_in_queue, context)

	scripting.game_interface:save_value(build_fishery_issued, context)
	scripting.game_interface:save_value(fishery_in_queue, context)

	scripting.game_interface:save_value(build_plantation_issued, context)
	scripting.game_interface:save_value(plantation_in_queue, context)

	scripting.game_interface:save_value(train_unit_issued, context)
	scripting.game_interface:save_value(unit_in_queue, context)
	scripting.game_interface:save_value(unit_trained, context)
	
	scripting.game_interface:save_value(first_turn, context)
	scripting.game_interface:save_value(protect_village, context)
	scripting.game_interface:save_value(protect_pass, context)
end

local function OnLoadingGame(context)
	build_farm_issued =			scripting.game_interface:load_value(false, context)
	farm_in_queue =				scripting.game_interface:load_value(false, context)

	build_fishery_issued =		scripting.game_interface:load_value(false, context)
	fishery_in_queue =			scripting.game_interface:load_value(false, context)

	build_plantation_issued =	scripting.game_interface:load_value(false, context)
	plantation_in_queue =		scripting.game_interface:load_value(false, context)

	train_unit_issued =			scripting.game_interface:load_value(false, context)
	unit_in_queue =				scripting.game_interface:load_value(false, context)
	unit_trained =				scripting.game_interface:load_value(0, context)
	
	first_turn =				scripting.game_interface:load_value(true, context)
	protect_village =			scripting.game_interface:load_value(true, context)
	protect_pass =				scripting.game_interface:load_value(true, context)
end

--******************************************************** START POS PAN ********************************************************
local function OnTimeTrigger(context)
	out.ting(context.string)
	local	x, y, z, theatre = CampaignUI.CameraTarget()
--************ FIRST CAMERA PAN CO-ORDINATES ****************************************************
	if context.string == "intro_hold" then
		scripting.game_interface:set_zoom_limit(1.08, 0.02)
		CampaignUI.ScrollCamera(22,	{-546.819, 265.053, 1.06},
									{-546.819, 265.053, 1.0})
		camera_pan = 1
	elseif context.string == "intro_VO_delay" then
		if scripting.game_interface:optional_extras_for_episodics() == "0" then
			effect.advance_scripted_advice_thread("0739_ep_1_win_battle", 1)
			scripting.game_interface:award_experience_level("faction:virginia_colonists", 1)
		else
			effect.advance_scripted_advice_thread("0700_ep_1_intro", 1)
		end
	elseif context.string == "intro_camera_pan_finishes" then
		scripting.ShowHUD(true)
		scripting.game_interface:stop_user_input(false)
		effect.suspend_contextual_advice(false)
		scripting.game_interface:add_time_trigger("intro_HUD_shown", 2)
	elseif context.string == "intro_HUD_shown" then
		scripting.game_interface:trigger_custom_mission("ep1_build_farm", "virginia_colonists", "build_building", 0, "corn_peasant_farms", "", "mission_text_text_ep1_build_a_farm_text", "", 500, "", context)

--************ Second CAMERA PAN CO-ORDINATES ****************************************************
	elseif context.string == "shroud_2_HUD_gone" then
		effect.advance_scripted_advice_thread("0703_ep_1_shroud_2_unlocked", 1)
		scripting.EnableFeature("show_shroud_1_2")
		scripting.game_interface:set_zoom_limit(1.08, 0.02)
		CampaignUI.ScrollCamera(20,	{x, z, y},
									--{-545.949, 278.413, 1.0},
									{-542.155, 273.630, 1.0},
									{-548, 267, y})
		camera_pan = 2
	elseif context.string == "shroud_2_camera_pan_finishes" then
		scripting.ShowHUD(true)
		scripting.game_interface:stop_user_input(false)
		scripting.game_interface:add_time_trigger("shroud_2_HUD_shown", 2)
	elseif context.string == "shroud_2_HUD_shown" then
		scripting.game_interface:trigger_custom_mission("ep1_capture_settlement_maryland", "virginia_colonists", "capture_city", 0, "maryland", "", "mission_text_text_ep1_capture_enemy_village_text", "mission_text_text_reward_episodic_chapter_3", 0, "", context)

--************ third CAMERA PAN CO-ORDINATES ****************************************************
	elseif context.string == "shroud_3_HUD_gone" then
		effect.advance_scripted_advice_thread("0704_ep_1_shroud_3_unlocked", 1)
		scripting.EnableFeature("show_shroud_1_3")
		scripting.game_interface:set_zoom_limit(1.08, 0.02)
		CampaignUI.ScrollCamera(20,	{x, z, y},
									{-541.545, 295.147, 1.03},
									{-540, 273, y})
		camera_pan = 3
	elseif context.string == "shroud_3_camera_pan_finishes" then
		scripting.ShowHUD(true)
		scripting.game_interface:stop_user_input(false)
		scripting.game_interface:add_time_trigger("shroud_3_HUD_shown", 2)
	elseif context.string == "shroud_3_HUD_shown" then
		scripting.game_interface:trigger_custom_mission("ep1_capture_settlement_pennsylvania", "virginia_colonists", "capture_city", 0, "pennsylvania", "", "mission_text_text_ep1_capture_enemy_city_text", "mission_text_text_reward_episodic_complete_1", 0, "", context)
	elseif context.string == "end_turn_prod" then
		if first_turn then
			if not advice_on_screen then
				scripting.game_interface:add_time_trigger("end_turn_prod", 120)
				effect.advance_scripted_advice_thread("0738_ep_1_end", 1)
			else
				scripting.game_interface:add_time_trigger("end_turn_prod", 30)
			end
		end
	end
end

local function OnCameraMoverFinished(context)
	scripting.game_interface:set_zoom_limit(1.0, 1.0)
	if camera_pan == 1 then
		scripting.game_interface:add_time_trigger("intro_camera_pan_finishes", 1)
	elseif camera_pan == 2 then
		scripting.game_interface:add_time_trigger("shroud_2_camera_pan_finishes", 1)
	elseif camera_pan == 3 then
		scripting.game_interface:add_time_trigger("shroud_3_camera_pan_finishes", 1)
	end
	camera_pan = 0
end
--******************************************************** START POS PAN ********************************************************

local function OnUICreated()
	scripting.game_interface:display_turns(true)
end

--------------------------------------------------------------------------------------------------------------------
-- Add event callbacks
-- For a list of all events supported create a "documentation" directory in your empire directory, run a debug build of the game and see
-- the events.txt file
--------------------------------------------------------------------------------------------------------------------

scripting.AddEventCallBack("UICreated",	OnUICreated)
scripting.AddEventCallBack("FactionTurnStart", OnFactionTurnStart)
scripting.AddEventCallBack("WorldCreated", OnWorldCreated)
scripting.AddEventCallBack("FactionTurnEnd", OnFactionTurnEnd)
scripting.AddEventCallBack("MissionIssued", OnMissionIssued)
scripting.AddEventCallBack("MissionSucceeded", OnMissionSucceeded)
scripting.AddEventCallBack("SettlementOccupied", OnSettlementOccupied)
scripting.AddEventCallBack("PanelOpenedCampaign", OnPanelOpenedCampaign)
scripting.AddEventCallBack("PanelClosedCampaign", OnPanelClosedCampaign)
scripting.AddEventCallBack("CharacterSelected", OnCharacterSelected)
scripting.AddEventCallBack("FortSelected", OnFortSelected)
scripting.AddEventCallBack("SettlementSelected", OnSettlementSelected)
scripting.AddEventCallBack("SlotSelected", OnSlotSelected)
scripting.AddEventCallBack("ComponentLClickUp", OnComponentLClickUp)
scripting.AddEventCallBack("BuildingConstructionIssuedByPlayer", OnBuildingConstructionIssuedByPlayer)
scripting.AddEventCallBack("RecruitmentItemIssuedByPlayer", OnRecruitmentItemIssuedByPlayer)
scripting.AddEventCallBack("AdviceIssued", OnAdviceIssued)
scripting.AddEventCallBack("AdviceDismissed", OnAdviceDismissed)
scripting.AddEventCallBack("MovementPointsExhausted", OnMovementPointsExhausted)
scripting.AddEventCallBack("UnitTrained", OnUnitTrained)
scripting.AddEventCallBack("TimeTrigger", OnTimeTrigger)
scripting.AddEventCallBack("CameraMoverFinished", OnCameraMoverFinished)
scripting.AddEventCallBack("LocationEntered", OnLocationEntered)
scripting.AddEventCallBack("SavingGame", OnSavingGame)
scripting.AddEventCallBack("LoadingGame", OnLoadingGame)
