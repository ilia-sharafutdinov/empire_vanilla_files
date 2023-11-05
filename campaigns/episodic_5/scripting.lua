local core = require "ui/CoreUtils"
core.Require "export_ep5_advice"
core.Require "advice"
local scripting			= core.Require "EpisodicScripting"

scripting.SetCampaign("episodic_5")

--------------------------------------------------------------------------------------------------------------------
-- Define functions here
-- For a list of all supported commands see the wiki page http://console/empire/Empire%20Wiki/Campaign%20Interface.aspx
--------------------------------------------------------------------------------------------------------------------

local camera_pan = 0

local campaign_won = false

local function OnFactionTurnStart(context)
	if conditions.FactionIsLocal(context) then
		if conditions.TurnNumber(context) == 1 then
			scripting.game_interface:add_time_trigger("intro_hold", 2)
			scripting.game_interface:stop_user_input(true)
			
			if scripting.game_interface:optional_extras_for_episodics() == "0" then
				effect.advance_scripted_advice_thread("0742_ep_3_win_battle", 1)
				scripting.game_interface:award_experience_level("faction:united_states", 1)
			else
				effect.advance_scripted_advice_thread("0743_ep_3_lose_battle", 1)
			end

			scripting.game_interface:force_diplomacy("united_states", "britain", "trade agreement", false, false)
			scripting.game_interface:force_diplomacy("united_states", "britain", "military access", false, false)
			scripting.game_interface:force_diplomacy("united_states", "britain", "cancel military access", false, false)
			scripting.game_interface:force_diplomacy("united_states", "britain", "alliance", false, false)
			scripting.game_interface:force_diplomacy("united_states", "britain", "regions", false, false)
			scripting.game_interface:force_diplomacy("united_states", "britain", "technology", false, false)
			scripting.game_interface:force_diplomacy("united_states", "britain", "state_gift", false, false)
			scripting.game_interface:force_diplomacy("united_states", "britain", "payments", false, false)
			scripting.game_interface:force_diplomacy("united_states", "britain", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("united_states", "britain", "peace", false, false)
			scripting.game_interface:force_diplomacy("united_states", "britain", "war", false, false)

			scripting.game_interface:force_diplomacy("britain", "united_states", "trade agreement", false, false)
			scripting.game_interface:force_diplomacy("britain", "united_states", "military access", false, false)
			scripting.game_interface:force_diplomacy("britain", "united_states", "cancel military access", false, false)
			scripting.game_interface:force_diplomacy("britain", "united_states", "alliance", false, false)
			scripting.game_interface:force_diplomacy("britain", "united_states", "regions", false, false)
			scripting.game_interface:force_diplomacy("britain", "united_states", "technology", false, false)
			scripting.game_interface:force_diplomacy("britain", "united_states", "state_gift", false, false)
			scripting.game_interface:force_diplomacy("britain", "united_states", "payments", false, false)
			scripting.game_interface:force_diplomacy("britain", "united_states", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("britain", "united_states", "peace", false, false)
			scripting.game_interface:force_diplomacy("britain", "united_states", "war", false, false)

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

			scripting.game_interface:force_diplomacy("cherokee", "united_states", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("france", "united_states", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("huron", "united_states", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("inuit", "united_states", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("iroquoi", "united_states", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("plains", "united_states", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("pueblo", "united_states", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("spain", "united_states", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("netherlands", "united_states", "protectorate", false, false)

			scripting.game_interface:force_diplomacy("united_states", "cherokee", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("united_states", "france", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("united_states", "huron", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("united_states", "inuit", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("united_states", "iroquoi", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("united_states", "plains", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("united_states", "pueblo", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("united_states", "spain", "protectorate", false, false)
			scripting.game_interface:force_diplomacy("united_states", "netherlands", "protectorate", false, false)

			--cherokee
			--france
			--britain
			--huron
			--inuit
			--iroquoi
			--plains
			--pueblo
			--spain
			--netherlands
			--united_states

		end
	end
end

local function OnPanelOpenedCampaign(context)
	out.ting("Panel opened " .. context.string)
	if conditions.IsComponentType("government_screens", context) then
		scripting.EnableFeature("Hide_arrows_on_government_screen")
	elseif conditions.IsComponentType("missions", context) then
		scripting.HighlightComponent("button_missions", false)
	end
end

local function OnComponentLClickUp(context)
	out.ting("Component clicked " .. context.string)
	if conditions.IsComponentType("tab_victory_conditions", context) then
		scripting.HighlightComponent("tab_victory_conditions", false)
	end
end

local function OnVictoryConditionMet(context)
	scripting.game_interface:register_instant_movie("movies\\RTI_CS6_V01_Bink_Sound.bik")
	scripting.EnableFeature("disable_end_turn")
	scripting.game_interface:declare_episode_three_victory()
	campaign_won = true
end

local function OnPanelClosedCampaign(context)
	if campaign_won then
		scripting.game_interface:advance_to_next_campaign()
		CampaignUI.QuitToMainScreen()
	end
end

local function OnWorldCreated()
	scripting.game_interface:add_unit_model_overrides("faction:united_states,surname:577", "campaign_washington")
end

local skipped = false

local function skip_intro()
	scripting.game_interface:set_zoom_limit(1.0, 0.5)
	CampaignUI.SetCameraZoom(1.0)
	CampaignUI.SetCameraTarget(-513.123, 301.675)
	scripting.ShowHUD(true)
	scripting.game_interface:stop_user_input(false)
	effect.suspend_contextual_advice(false)
	effect.advance_scripted_advice_thread("0753_ep_2_victory_conditions", 1)
	scripting.HighlightComponent("button_missions", true)
	scripting.game_interface:show_shroud(true)
end

local function OnAdviceDismissed(context)
	if conditions.AdviceJustDisplayed("2019565691", context) or conditions.AdviceJustDisplayed("2111059872", context) then
		-- skip intro
		if camera_pan ~= 0 then
  			CampaignUI.StopCamera()
  			camera_pan = 0
  			skip_intro()
		else
			skipped = true
		end
	end
end

local function OnTimeTrigger(context)
	out.ting(context.string)
	local	x, y, z, theatre = CampaignUI.CameraTarget()
	if context.string == "intro_hold" then
		if skipped then
  			skip_intro()
		else
			CampaignUI.ScrollCamera(5,	{-513.123, 301.675, 1.04},
										{-513.123, 301.675, 1})
			camera_pan = 1
		end
	elseif context.string == "intro_camera_zoom_finishes" then
		if skipped then
  			skip_intro()
		else
			scripting.game_interface:set_zoom_limit(1.08, 0.02)
			CampaignUI.ScrollCamera(6,	{-513.123, 301.675, 1},
										--{-506.798, 301.324, 1},
										{-506.798, 301.324, 1.04})

			camera_pan = 2
		end
	elseif context.string == "intro_camera_pan_1_finishes" then
		if skipped then
  			skip_intro()
		else
			scripting.game_interface:add_time_trigger("intro_show_shroud", 17)
			scripting.game_interface:set_zoom_limit(1.08, 0.02)
			CampaignUI.ScrollCamera(25,	{-506.798, 301.324, 1.04},
										{-501.248, 322.729, 1},
										{-533.907, 300.751, 1},
										{-543.304, 267.982, 0.5},
										{-513.123, 301.675, 1})
			camera_pan = 3
		end
	elseif context.string == "intro_show_shroud" then
		scripting.game_interface:show_shroud(true)
	elseif context.string == "intro_camera_pan_finishes" then
		scripting.ShowHUD(true)
		scripting.game_interface:stop_user_input(false)
		effect.suspend_contextual_advice(false)
		effect.advance_scripted_advice_thread("0753_ep_2_victory_conditions", 1)
		scripting.HighlightComponent("button_missions", true)
	end
end

local function OnCameraMoverFinished(context)
	if camera_pan == 1 then
		scripting.game_interface:add_time_trigger("intro_camera_zoom_finishes", 1)
		scripting.game_interface:set_zoom_limit(1.0, 0.5)
	elseif camera_pan == 2 then
		scripting.game_interface:add_time_trigger("intro_camera_pan_1_finishes", 2)
		scripting.game_interface:set_zoom_limit(1.0, 0.5)
	elseif camera_pan == 3 then
		scripting.game_interface:add_time_trigger("intro_camera_pan_finishes", 1)
		scripting.game_interface:set_zoom_limit(1.0, 0.5)
	end
	camera_pan = 0
end

--------------------------------------------------------------------------------------------------------------------
-- Add event callbacks
-- For a list of all events supported create a "documentation" directory in your empire directory, run a debug build of the game and see
-- the events.txt file
--------------------------------------------------------------------------------------------------------------------

scripting.AddEventCallBack("WorldCreated", OnWorldCreated)
scripting.AddEventCallBack("FactionTurnStart", OnFactionTurnStart)
scripting.AddEventCallBack("TimeTrigger", OnTimeTrigger)
scripting.AddEventCallBack("CameraMoverFinished", OnCameraMoverFinished)
scripting.AddEventCallBack("PanelOpenedCampaign", OnPanelOpenedCampaign)
scripting.AddEventCallBack("ComponentLClickUp", OnComponentLClickUp)
scripting.AddEventCallBack("VictoryConditionMet", OnVictoryConditionMet)
scripting.AddEventCallBack("PanelClosedCampaign", OnPanelClosedCampaign)
scripting.AddEventCallBack("AdviceDismissed", OnAdviceDismissed)