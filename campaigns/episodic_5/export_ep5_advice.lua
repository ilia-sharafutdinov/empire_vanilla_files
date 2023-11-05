--[[
Automatically generated via export from Empire.mdb
Edit manually at your own risk
--]]

module(..., package.seeall)

events = require "data.events"
-- Advice Triggers

--[[ 0001_Battle_Advice_Friendly_Fire_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0001_Battle_Advice_Friendly_Fire_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0002_Battle_Advice_Enemy_Forming_Up_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0002_Battle_Advice_Enemy_Forming_Up_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0003_Battle_Advice_Enemy_Holding_Ground_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0003_Battle_Advice_Enemy_Holding_Ground_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0004_Battle_Advice_Enemy_Holding_Crossing_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0004_Battle_Advice_Enemy_Holding_Crossing_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0005_Battle_Advice_Enemy_Holding_Crossing_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0005_Battle_Advice_Enemy_Holding_Crossing_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0006_Battle_Advice_Player_Outnumbered_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0006_Battle_Advice_Player_Outnumbered_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0007_Battle_Advice_Enemy_Defending_Hill_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0007_Battle_Advice_Enemy_Defending_Hill_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0008_Battle_Advice_Player_Defending_Hill_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0008_Battle_Advice_Player_Defending_Hill_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0009_Battle_Advice_Fatigue_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0009_Battle_Advice_Fatigue_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0010_Battle_Advice_Change_Cavalry_Formation_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0010_Battle_Advice_Change_Cavalry_Formation_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0011_Battle_Advice_Preserve_Skirmishers_Triggers ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0011_Battle_Advice_Preserve_Skirmishers_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0012_Battle_Advice_Enemy_Sitting_Targets_Thread ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0012_Battle_Advice_Enemy_Sitting_Targets_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0013_Battle_Advice_Missile_Superiority_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0013_Battle_Advice_Missile_Superiority_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0014_Battle_Advice_Chasing_Skirmishers_Thread ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0014_Battle_Advice_Chasing_Skirmishers_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0015_Battle_Advice_Close_Gaps_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0015_Battle_Advice_Close_Gaps_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0016_Battle_Advice_Draw_Their_Fire_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0016_Battle_Advice_Draw_Their_Fire_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0017_Battle_Advice_Counter_Charge_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0017_Battle_Advice_Counter_Charge_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0018_Battle_Advice_Fight_To_The_Death_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0018_Battle_Advice_Fight_To_The_Death_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0019_Battle_Advice_Fight_To_The_Death_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0019_Battle_Advice_Fight_To_The_Death_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0020_Battle_Advice_Expendable_Troops_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0020_Battle_Advice_Expendable_Troops_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0021_Battle_Advice_Go_For_The_Throat_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0021_Battle_Advice_Go_For_The_Throat_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0022_Battle_Advice_Fixing_And_Killing_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0022_Battle_Advice_Fixing_And_Killing_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0023_Battle_Advice_Outflanking_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0023_Battle_Advice_Outflanking_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0024_Battle_Advice_Outflanking_With_Cavalry_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0024_Battle_Advice_Outflanking_With_Cavalry_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0025_Battle_Advice_Find_Weak_Spots_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0025_Battle_Advice_Find_Weak_Spots_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0026_Battle_Advice_Avoid_Flanking_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0026_Battle_Advice_Avoid_Flanking_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0027_Battle_Advice_Reserves_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0027_Battle_Advice_Reserves_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0028_Battle_Advice_Wavy_Line_Formation_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0028_Battle_Advice_Wavy_Line_Formation_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0029_Battle_Advice_Attacking_Hills_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0029_Battle_Advice_Attacking_Hills_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0030_Battle_Advice_Fighting_With_Cavalry_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0030_Battle_Advice_Fighting_With_Cavalry_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0031_Battle_Advice_Defending_With_Cavalry_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0031_Battle_Advice_Defending_With_Cavalry_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0032_Battle_Advice_Cavalry_In_Reserve_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0032_Battle_Advice_Cavalry_In_Reserve_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0033_Battle_Advice_Cavalry_Cycle_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0033_Battle_Advice_Cavalry_Cycle_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0035_Battle_Advice_Cavalry_Against_Points_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0035_Battle_Advice_Cavalry_Against_Points_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0036_Battle_Advice_Cavalry_Against_Points_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0036_Battle_Advice_Cavalry_Against_Points_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0037_Battle_Advice_Cavalry_Against_Points_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0037_Battle_Advice_Cavalry_Against_Points_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0038_Battle_Advice_Defence_Against_Cavalry_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0038_Battle_Advice_Defence_Against_Cavalry_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0039_Battle_Advice_Defence_Against_Cavalry_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0039_Battle_Advice_Defence_Against_Cavalry_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0040_Battle_Advice_Defence_Against_Cavalry_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0040_Battle_Advice_Defence_Against_Cavalry_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0041_Battle_Advice_Cavalry_Against_Camels_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0041_Battle_Advice_Cavalry_Against_Camels_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0042_Battle_Advice_Cavalry_Against_Camels_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0042_Battle_Advice_Cavalry_Against_Camels_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0043_Battle_Advice_Cavalry_Against_Camels_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0043_Battle_Advice_Cavalry_Against_Camels_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0044_Battle_Advice_Camels_Against_Cavalry_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0044_Battle_Advice_Camels_Against_Cavalry_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0045_Battle_Advice_Camels_Against_Cavalry_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0045_Battle_Advice_Camels_Against_Cavalry_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0046_Battle_Advice_Fighting_Skirmishers_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0046_Battle_Advice_Fighting_Skirmishers_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0047_Battle_Advice_Good_Artillery_Target_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0047_Battle_Advice_Good_Artillery_Target_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0048_Battle_Advice_Good_Artillery_Target_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0048_Battle_Advice_Good_Artillery_Target_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0049_Battle_Advice_Poor_Artillery_Target_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0049_Battle_Advice_Poor_Artillery_Target_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0050_Battle_Advice_Risky_Elephant_Attack_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0050_Battle_Advice_Risky_Elephant_Attack_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0051_Battle_Advice_Points_Against_Points_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0051_Battle_Advice_Points_Against_Points_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0052_Battle_Advice_Driving_Off_Skirmishers_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0052_Battle_Advice_Driving_Off_Skirmishers_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0053_Battle_Advice_Artillery_Vs_Elephants_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0053_Battle_Advice_Artillery_Vs_Elephants_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0055_Battle_Advice_Light_Cavalry_Tactics_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0055_Battle_Advice_Light_Cavalry_Tactics_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0056_Battle_Advice_Selective_Targeting_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0056_Battle_Advice_Selective_Targeting_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0058_Battle_Advice_Stay_In_Cover_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0058_Battle_Advice_Stay_In_Cover_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0059_Campaign_Advice_Offer_Ambush_Bait_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.FactionIsLocal(context) and conditions.TurnNumber(context) >= 10 then
		effect.advance_contextual_advice_thread("0059_Campaign_Advice_Offer_Ambush_Bait_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0060_Battle_Advice_Feigning_A_Rout_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0060_Battle_Advice_Feigning_A_Rout_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0061_Battle_Advice_Entice_The_Enemy_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0061_Battle_Advice_Entice_The_Enemy_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0062_Battle_Advice_Study_Their_Lines_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0062_Battle_Advice_Study_Their_Lines_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0063_Battle_Advice_Enrage_The_Enemy_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0063_Battle_Advice_Enrage_The_Enemy_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0064_Battle_Advice_Encircle_The_Enemy_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0064_Battle_Advice_Encircle_The_Enemy_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0065_Battle_Advice_Outnumbered_By_The_Enemy_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0065_Battle_Advice_Outnumbered_By_The_Enemy_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0066_Battle_Advice_Take_The_Initiative_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0066_Battle_Advice_Take_The_Initiative_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0067_Battle_Advice_Distract_The_Enemy_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0067_Battle_Advice_Distract_The_Enemy_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0068_Battle_Advice_Overcommitment_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0068_Battle_Advice_Overcommitment_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0069_Battle_Advice_High_Ground_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0069_Battle_Advice_High_Ground_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0070_Battle_Advice_Avoid_Elite_Units_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0070_Battle_Advice_Avoid_Elite_Units_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0071_Battle_Advice_Keep_Enemy_Occupied_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0071_Battle_Advice_Keep_Enemy_Occupied_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0072_Campaign_Advice_Mountain_Passes_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.FactionIsLocal(context) and conditions.TurnNumber(context) >= 10 then
		effect.advance_contextual_advice_thread("0072_Campaign_Advice_Mountain_Passes_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0073_Battle_Advice_Mountain_Passes_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0073_Battle_Advice_Mountain_Passes_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0074_Battle_Advice_Fight_Downhill_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0074_Battle_Advice_Fight_Downhill_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0075_Battle_Advice_Artillery_Deployment_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0075_Battle_Advice_Artillery_Deployment_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0076_Battle_Advice_Skirmish_Mode_Button_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0076_Battle_Advice_Skirmish_Mode_Button_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0077_Battle_Advice_Fire_At_Will_Button_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0077_Battle_Advice_Fire_At_Will_Button_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0078_Battle_Advice_Guard_Mode_Button_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0078_Battle_Advice_Guard_Mode_Button_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0079_Battle_Advice_Group_Formations_Button_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0079_Battle_Advice_Group_Formations_Button_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0080_Battle_Advice_Withdraw_Button_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0080_Battle_Advice_Withdraw_Button_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0081_Battle_Advice_Cancel_Order_Button_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0081_Battle_Advice_Cancel_Order_Button_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0082_Battle_Advice_Group_Button_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0082_Battle_Advice_Group_Button_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0083_Battle_Advice_Group_Formations_Button_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0083_Battle_Advice_Group_Formations_Button_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0084_Battle_Advice_Routing_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0084_Battle_Advice_Routing_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0085_Battle_Advice_Fighting_Elephants_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0085_Battle_Advice_Fighting_Elephants_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0086_Battle_Advice_Fighting_Elephants_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0086_Battle_Advice_Fighting_Elephants_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0087_Battle_Advice_Elephants_Amok_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0087_Battle_Advice_Elephants_Amok_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0089_Battle_Advice_Facing_Artillery_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0089_Battle_Advice_Facing_Artillery_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0090_Battle_Advice_Missile_Cavalry_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0090_Battle_Advice_Missile_Cavalry_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0091_Battle_Advice_Facing_Cavalry_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0091_Battle_Advice_Facing_Cavalry_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0092_Battle_Advice_Rallying_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0092_Battle_Advice_Rallying_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0093_Battle_Advice_General_Threatened_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0093_Battle_Advice_General_Threatened_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0094_Battle_Advice_Line_Wavering_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0094_Battle_Advice_Line_Wavering_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0095_Battle_Advice_Wedge_Formations_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0095_Battle_Advice_Wedge_Formations_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0096_Battle_Advice_Skirmish_Mode_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0096_Battle_Advice_Skirmish_Mode_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0097_Battle_Advice_Crossing_Attack_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0097_Battle_Advice_Crossing_Attack_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0098_Battle_Advice_Crossing_Defence_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0098_Battle_Advice_Crossing_Defence_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0099_Battle_Advice_Ambush_Attack_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0099_Battle_Advice_Ambush_Attack_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0100_Battle_Advice_Radar_Map_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0100_Battle_Advice_Radar_Map_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0101_Battle_Advice_Hour_Glass_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0101_Battle_Advice_Hour_Glass_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0102_Battle_Advice_Cavalry_Charges_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0102_Battle_Advice_Cavalry_Charges_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0103_Battle_Advice_Melee_Button_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0103_Battle_Advice_Melee_Button_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0103a_Battle_Advice_Melee_Button_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if not false then
		return true
	end
	return false
end

--[[ 0104_Battle_Advice_Run_Button_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0104_Battle_Advice_Run_Button_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0105_Battle_Advice_Fighting_Irregulars_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0105_Battle_Advice_Fighting_Irregulars_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0106_Battle_Advice_Killometer_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0106_Battle_Advice_Killometer_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0107_Battle_Advice_Bombardment_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0107_Battle_Advice_Bombardment_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0108_Battle_Advice_Defences_Stakes_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0108_Battle_Advice_Defences_Stakes_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0109_Battle_Advice_Defences_Stakes_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0109_Battle_Advice_Defences_Stakes_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0110_Battle_Advice_Defences_Chevaux_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0110_Battle_Advice_Defences_Chevaux_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0111_Battle_Advice_Defences_Fougasse_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0111_Battle_Advice_Defences_Fougasse_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0112_Battle_Advice_Defences_Earthworks_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0112_Battle_Advice_Defences_Earthworks_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0113_Battle_Advice_Defences_Gabionades_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0113_Battle_Advice_Defences_Gabionades_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0114_Battle_Advice_Siege_Ladders_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0114_Battle_Advice_Siege_Ladders_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0115_Battle_Advice_Grenadiers_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0115_Battle_Advice_Grenadiers_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0116_Battle_Advice_Dragoons_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0116_Battle_Advice_Dragoons_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0117_Battle_Advice_Light_Dragoons_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0117_Battle_Advice_Light_Dragoons_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0118_Battle_Advice_First_Shot_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0118_Battle_Advice_First_Shot_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0119_Battle_Advice_Unlimbering_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0119_Battle_Advice_Unlimbering_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0120_Battle_Advice_Limbering_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0120_Battle_Advice_Limbering_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0121_Battle_Advice_Galloper_Guns_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0121_Battle_Advice_Galloper_Guns_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0122_Battle_Advice_Mortars_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0122_Battle_Advice_Mortars_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0123_Battle_Advice_Howitzers_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0123_Battle_Advice_Howitzers_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0124_Battle_Advice_Round_Shot_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0124_Battle_Advice_Round_Shot_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0125_Battle_Advice_Explosive_Shells_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0125_Battle_Advice_Explosive_Shells_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0126_Battle_Advice_Percussive_Shells_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0126_Battle_Advice_Percussive_Shells_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0127_Battle_Advice_Cannister_Shot_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0127_Battle_Advice_Cannister_Shot_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0128_Battle_Advice_Spherical_Case_Shot_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0128_Battle_Advice_Spherical_Case_Shot_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0129_Battle_Advice_Carcass_Shot_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0129_Battle_Advice_Carcass_Shot_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0130_Battle_Advice_Quicklime_Shells_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0130_Battle_Advice_Quicklime_Shells_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0131_Battle_Advice_Infantry_Square_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0131_Battle_Advice_Infantry_Square_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0132_Battle_Advice_Supporting_Squares_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0132_Battle_Advice_Supporting_Squares_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0133_Battle_Advice_Lancers_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0133_Battle_Advice_Lancers_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0135_Battle_Advice_Irregular_Troops_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0135_Battle_Advice_Irregular_Troops_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0136_Battle_Advice_Plug_Bayonets_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0136_Battle_Advice_Plug_Bayonets_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0137_Battle_Advice_Ring_Bayonets_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0137_Battle_Advice_Ring_Bayonets_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0138_Battle_Advice_Socket_Bayonets_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0138_Battle_Advice_Socket_Bayonets_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0139_Battle_Advice_Deployment_Image_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0139_Battle_Advice_Deployment_Image_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0140_Battle_Advice_Select_All_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0140_Battle_Advice_Select_All_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0141_Battle_Advice_Terrain_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0141_Battle_Advice_Terrain_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0142_Battle_Advice_Sabres_Muskets_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0142_Battle_Advice_Sabres_Muskets_Thread", 1, context)
		effect.advance_contextual_advice_thread("1042_Campaign_Advice_UI_Incoming_Message_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0144_Battle_Advice_Defending_Forts_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0144_Battle_Advice_Defending_Forts_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0145_Battle_Advice_Kill_Their_General_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0145_Battle_Advice_Kill_Their_General_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0146_Battle_Advice_Buildings_As_Cover_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0146_Battle_Advice_Buildings_As_Cover_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0148_Battle_Advice_Special_Abilities_Button_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0148_Battle_Advice_Special_Abilities_Button_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0149_Battle_Advice_Walls_As_Cover_Trigger ]]--

events.BattleUnitAttacksEnemyUnit[#events.BattleUnitAttacksEnemyUnit+1] =
function (context)
	if not false then
		effect.advance_contextual_advice_thread("0149_Battle_Advice_Walls_As_Cover_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0150_Battle_Advice_Target_Their_Weaknesses_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0150_Battle_Advice_Target_Their_Weaknesses_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0151_Battle_Advice_Sinking_Ship_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0151_Battle_Advice_Sinking_Ship_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0152_Battle_Advice_Dismasted_Ship_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0152_Battle_Advice_Dismasted_Ship_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0153_Battle_Advice_Sails_Destroyed_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0153_Battle_Advice_Sails_Destroyed_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0154_Battle_Advice_Hull_Damaged_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0154_Battle_Advice_Hull_Damaged_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0155_Battle_Advice_Ship_Collision_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0155_Battle_Advice_Ship_Collision_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0156_Battle_Advice_Ship_Aground_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0156_Battle_Advice_Ship_Aground_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0157_Battle_Advice_Ship_Ablaze_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0157_Battle_Advice_Ship_Ablaze_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0158_Battle_Advice_Magazine_Explosion_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0158_Battle_Advice_Magazine_Explosion_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0159_Battle_Advice_Magazine_Explosion_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0159_Battle_Advice_Magazine_Explosion_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0160_Battle_Advice_Ship_Routing_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0160_Battle_Advice_Ship_Routing_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0161_Battle_Advice_Ship_Routing_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0161_Battle_Advice_Ship_Routing_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0162_Battle_Advice_Ship_Routing_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0162_Battle_Advice_Ship_Routing_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0163_Battle_Advice_Ship_Captured_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.BattleUnitIsPlayers(context) then
		effect.advance_contextual_advice_thread("0163_Battle_Advice_Ship_Captured_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0164_Battle_Advice_Ship_Captured_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if not conditions.BattleUnitIsPlayers(context) then
		effect.advance_contextual_advice_thread("0164_Battle_Advice_Ship_Captured_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0165_Battle_Advice_Ship_Rallying_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0165_Battle_Advice_Ship_Rallying_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0166_Battle_Advice_Ship_Rallying_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0166_Battle_Advice_Ship_Rallying_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0167_Battle_Advice_Sloop_Characteristics_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0167_Battle_Advice_Sloop_Characteristics_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0168_Battle_Advice_Brig_Characteristics_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0168_Battle_Advice_Brig_Characteristics_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0169_Battle_Advice_Frigate_Characteristics_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0169_Battle_Advice_Frigate_Characteristics_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0170_Battle_Advice_Lineship_Characteristics_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0170_Battle_Advice_Lineship_Characteristics_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0171_Battle_Advice_Galley_Characteristics_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0171_Battle_Advice_Galley_Characteristics_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0172_Battle_Advice_Xebec_Characteristics_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0172_Battle_Advice_Xebec_Characteristics_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0173_Battle_Advice_Steam_Characteristics_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0173_Battle_Advice_Steam_Characteristics_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0174_Battle_Advice_Razee_Characteristics_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0174_Battle_Advice_Razee_Characteristics_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0175_Battle_Advice_Wind_Direction_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0175_Battle_Advice_Wind_Direction_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0176_Battle_Advice_Sailing_Into_Wind_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0176_Battle_Advice_Sailing_Into_Wind_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0177_Battle_Advice_Line_Astern_Formation_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0177_Battle_Advice_Line_Astern_Formation_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0178_Battle_Advice_Crescent_Formation_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0178_Battle_Advice_Crescent_Formation_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0178a_Battle_Advice_Crescent_Formation_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("crescent_envelope", context) and not conditions.AdviceDisplayed("2106012703", context) then
		return true
	end
	return false
end

--[[ 0180_Battle_Advice_Line_Abreast_Formation_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0180_Battle_Advice_Line_Abreast_Formation_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0181_Battle_Advice_Outgunned_Avoidance_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0181_Battle_Advice_Outgunned_Avoidance_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0182_Battle_Advice_Crossing_The_T_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0182_Battle_Advice_Crossing_The_T_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0183_Battle_Advice_Weather_Gauge_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0183_Battle_Advice_Weather_Gauge_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0184_Battle_Advice_Hiding_At_Sea_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0184_Battle_Advice_Hiding_At_Sea_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0185_Battle_Advice_Naval_Round_Shot_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0185_Battle_Advice_Naval_Round_Shot_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0186_Battle_Advice_Naval_Grape_Shot_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0186_Battle_Advice_Naval_Grape_Shot_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0187_Battle_Advice_Naval_Chain_Shot_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0187_Battle_Advice_Naval_Chain_Shot_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0188_Battle_Advice_Naval_Radar_Map_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0188_Battle_Advice_Naval_Radar_Map_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0189_Battle_Advice_Naval_Manoeuvre_Compass_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0189_Battle_Advice_Naval_Manoeuvre_Compass_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0193_Battle_Advice_Naval_Grouping_Ships_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0193_Battle_Advice_Naval_Grouping_Ships_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0195_Battle_Advice_Naval_Withdraw_Button_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0195_Battle_Advice_Naval_Withdraw_Button_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0196_Battle_Advice_Naval_Fire_At_Will_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0196_Battle_Advice_Naval_Fire_At_Will_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0197_Battle_Advice_Naval_Boarding_Button_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0197_Battle_Advice_Naval_Boarding_Button_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0198_Battle_Advice_Naval_Formations_Button_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0198_Battle_Advice_Naval_Formations_Button_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0199_Battle_Advice_Naval_Killometer_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0199_Battle_Advice_Naval_Killometer_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0200_Battle_Advice_Naval_Speed_Slider_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0200_Battle_Advice_Naval_Speed_Slider_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0201_Battle_Advice_Naval_Review_Panel_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0201_Battle_Advice_Naval_Review_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0202_Battle_Advice_Siege_Sapping_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0202_Battle_Advice_Siege_Sapping_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0203_Battle_Advice_Siege_Sapping_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0203_Battle_Advice_Siege_Sapping_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0204_Battle_Advice_Siege_Assault_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0204_Battle_Advice_Siege_Assault_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0206_Battle_Advice_Siege_Defence_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0206_Battle_Advice_Siege_Defence_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0207_Battle_Advice_Walls_Breached_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0207_Battle_Advice_Walls_Breached_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0208_Battle_Advice_Walls_Breached_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0208_Battle_Advice_Walls_Breached_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0209_Battle_Advice_Concentrate_Fire_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0209_Battle_Advice_Concentrate_Fire_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0211_Battle_Advice_Siege_Ladders_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("0211_Battle_Advice_Siege_Ladders_Thread", 1, context)
		return true
	end
	return false
end

--[[ 0213_Battle_Advice_Deployment_Phase_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		return true
	end
	return false
end

--[[ 0215_Battle_Advice_Camera_Controls_Trigger ]]--

events.AdviceDismissed[#events.AdviceDismissed+1] =
function (context)
	if conditions.AdviceJustDisplayed("2032462934", context) then
		return true
	end
	return false
end

--[[ 0216_Battle_Advice_Unit_Morale_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if not false then
		return true
	end
	return false
end

--[[ 0217_Battle_Advice_Wavering_Morale_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if not false then
		return true
	end
	return false
end

--[[ 0218_Battle_Advice_Wavering_Morale_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if not false then
		return true
	end
	return false
end

--[[ 0219_Battle_Advice_Bayonet_Charge_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if not false then
		return true
	end
	return false
end

--[[ 0220_Battle_Advice_Ammo_Types_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if true then
		return true
	end
	return false
end


--[[ 1013_Campaign_Advice_UI_Diplomacy_Panel_Trigger ]]--

events.PanelOpenedCampaign[#events.PanelOpenedCampaign+1] =
function (context)
	if conditions.IsComponentType("diplomatic_relations", context) then
		effect.advance_contextual_advice_thread("1013_Campaign_Advice_UI_Diplomacy_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1014_Campaign_Advice_UI_Diplomacy_Panel_Trigger ]]--

events.PanelOpenedCampaign[#events.PanelOpenedCampaign+1] =
function (context)
	if conditions.IsComponentType("diplomacy_panel", context) then
		effect.advance_contextual_advice_thread("1014_Campaign_Advice_UI_Diplomacy_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1014a_Campaign_Advice_UI_Diplomacy_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("diplomacy_button_trade", context) then
		effect.advance_contextual_advice_thread("1014a_Campaign_Advice_UI_Diplomacy_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1014b_Campaign_Advice_UI_Diplomacy_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("diplomacy_button_alliance", context) then
		effect.advance_contextual_advice_thread("1014b_Campaign_Advice_UI_Diplomacy_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1014c_Campaign_Advice_UI_Diplomacy_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("diplomacy_button_state_gift", context) then
		effect.advance_contextual_advice_thread("1014c_Campaign_Advice_UI_Diplomacy_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1014d_Campaign_Advice_UI_Diplomacy_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("diplomacy_button_protector", context) then
		effect.advance_contextual_advice_thread("1014d_Campaign_Advice_UI_Diplomacy_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1014e_Campaign_Advice_UI_Diplomacy_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("diplomacy_button_war", context) then
		effect.advance_contextual_advice_thread("1014e_Campaign_Advice_UI_Diplomacy_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1014f_Campaign_Advice_UI_Diplomacy_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("diplomacy_button_access", context) then
		effect.advance_contextual_advice_thread("1014f_Campaign_Advice_UI_Diplomacy_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1014g_Campaign_Advice_UI_Diplomacy_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("diplomacy_button_regions", context) then
		effect.advance_contextual_advice_thread("1014g_Campaign_Advice_UI_Diplomacy_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1014h_Campaign_Advice_UI_Diplomacy_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("diplomacy_button_technology", context) then
		effect.advance_contextual_advice_thread("1014h_Campaign_Advice_UI_Diplomacy_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1014j_Campaign_Advice_UI_Diplomacy_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("diplomacy_button_payments", context) then
		effect.advance_contextual_advice_thread("1014j_Campaign_Advice_UI_Diplomacy_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1019_Campaign_Advice_UI_Technology_Panel_Trigger ]]--

events.PanelOpenedCampaign[#events.PanelOpenedCampaign+1] =
function (context)
	if conditions.IsComponentType("technology", context) then
		effect.advance_contextual_advice_thread("1019_Campaign_Advice_UI_Technology_Panel_Thread", 1, context)
		return true
	end
	return false
end


--[[ 1020_Campaign_Advice_UI_Set_Taxes_Button_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("button_taxes", context) then
		effect.advance_contextual_advice_thread("1020_Campaign_Advice_UI_Set_Taxes_Button_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1022b_Campaign_Advice_UI_Set_Taxes_Slider_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsChildOf("tx_classes_upper", context) and conditions.IsComponentType("handle", context) then
		effect.advance_contextual_advice_thread("1022b_Campaign_Advice_UI_Set_Taxes_Slider_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1023_Campaign_Advice_UI_Lists_Panel_Trigger ]]--

events.PanelOpenedCampaign[#events.PanelOpenedCampaign+1] =
function (context)
	if conditions.IsComponentType("entity_lists", context) then
		effect.advance_contextual_advice_thread("1023_Campaign_Advice_UI_Lists_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1024_Campaign_Advice_UI_Lists_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("fleets", context) then
		effect.advance_contextual_advice_thread("1024_Campaign_Advice_UI_Lists_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1025_Campaign_Advice_UI_Lists_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("regions", context) then
		effect.advance_contextual_advice_thread("1025_Campaign_Advice_UI_Lists_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1026_Campaign_Advice_UI_Lists_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("agents", context) then
		effect.advance_contextual_advice_thread("1026_Campaign_Advice_UI_Lists_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1027_Campaign_Advice_UI_Lists_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("armies", context) then
		effect.advance_contextual_advice_thread("1027_Campaign_Advice_UI_Lists_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1028_Campaign_Advice_UI_Government_Panel_Trigger ]]--

events.PanelOpenedCampaign[#events.PanelOpenedCampaign+1] =
function (context)
	if conditions.IsComponentType("government_screens", context) then
		effect.advance_contextual_advice_thread("1028_Campaign_Advice_UI_Government_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1029_Campaign_Advice_UI_Government_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("tab_taxes", context) then
		effect.advance_contextual_advice_thread("1029_Campaign_Advice_UI_Government_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1030_Campaign_Advice_UI_Government_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("tab_ministers", context) then
		effect.advance_contextual_advice_thread("1030_Campaign_Advice_UI_Government_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1030a_Campaign_Advice_UI_Government_Panel_Trigger ]]--

events.PanelOpenedCampaign[#events.PanelOpenedCampaign+1] =
function (context)
	if conditions.IsComponentType("royal_family", context) then
		effect.advance_contextual_advice_thread("1030a_Campaign_Advice_UI_Government_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1030b_Campaign_Advice_UI_Government_Panel_Trigger ]]--

events.AdviceDismissed[#events.AdviceDismissed+1] =
function (context)
	if conditions.AdviceJustDisplayed("-389996354", context) and conditions.FactionGovernmentType("gov_absolute_monarchy", context) then
		effect.advance_contextual_advice_thread("1030b_Campaign_Advice_UI_Government_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1030c_Campaign_Advice_UI_Government_Panel_Trigger ]]--

events.AdviceDismissed[#events.AdviceDismissed+1] =
function (context)
	if conditions.AdviceJustDisplayed("-389996354", context) and (conditions.FactionGovernmentType("gov_constitutional_monarchy", context) or conditions.FactionGovernmentType("gov_republic", context)) then
		effect.advance_contextual_advice_thread("1030c_Campaign_Advice_UI_Government_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1030d_Campaign_Advice_UI_Government_Panel_Trigger ]]--

events.AdviceDismissed[#events.AdviceDismissed+1] =
function (context)
	if conditions.AdviceJustDisplayed("-250658412", context) then
		effect.advance_contextual_advice_thread("1030d_Campaign_Advice_UI_Government_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1031_Campaign_Advice_UI_Government_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("tab_trade", context) then
		effect.advance_contextual_advice_thread("1031_Campaign_Advice_UI_Government_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1032_Campaign_Advice_UI_Government_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("tab_national_summary", context) then
		effect.advance_contextual_advice_thread("1032_Campaign_Advice_UI_Government_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1033_Campaign_Advice_UI_Review_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("map", context) then
		effect.advance_contextual_advice_thread("1033_Campaign_Advice_UI_Review_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1034_Campaign_Advice_UI_Review_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("funds", context) then
		effect.advance_contextual_advice_thread("1034_Campaign_Advice_UI_Review_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1036_Campaign_Advice_UI_Review_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("season_icon", context) then
		effect.advance_contextual_advice_thread("1036_Campaign_Advice_UI_Review_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1037_Campaign_Advice_UI_Review_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("review_DY", context) then
		effect.advance_contextual_advice_thread("1037_Campaign_Advice_UI_Review_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1039_Campaign_Advice_UI_Prebattle_Panel_Trigger ]]--

events.PanelOpenedCampaign[#events.PanelOpenedCampaign+1] =
function (context)
	if conditions.IsComponentType("popup_pre_battle", context) then
		effect.advance_contextual_advice_thread("1039_Campaign_Advice_UI_Prebattle_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1040_Campaign_Advice_UI_Postbattle_Panel_Trigger ]]--

events.PanelOpenedCampaign[#events.PanelOpenedCampaign+1] =
function (context)
	if conditions.IsComponentType("popup_battle_results", context) then
		effect.advance_contextual_advice_thread("1040_Campaign_Advice_UI_Postbattle_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1041_Campaign_Advice_UI_Incoming_Message_Trigger ]]--

events.IncomingMessage[#events.IncomingMessage+1] =
function (context)
	if true then
		effect.advance_contextual_advice_thread("1041_Campaign_Advice_UI_Incoming_Message_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1048_Campaign_Advice_UI_Review_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("construction_tab", context) then
		effect.advance_contextual_advice_thread("1048_Campaign_Advice_UI_Review_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1049_Campaign_Advice_UI_Review_Panel_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("recruitment_tab", context) then
		effect.advance_contextual_advice_thread("1049_Campaign_Advice_UI_Review_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1050_Campaign_Advice_UI_Exchange_Panel_Trigger ]]--

events.PanelOpenedCampaign[#events.PanelOpenedCampaign+1] =
function (context)
	if conditions.IsComponentType("unit_exchange", context) then
		effect.advance_contextual_advice_thread("1050_Campaign_Advice_UI_Exchange_Panel_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1051_Campaign_Advice_Army_Promotions_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("army_tab", context) then
		effect.advance_contextual_advice_thread("1051_Campaign_Advice_Army_Promotions_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1052_Campaign_Advice_Navy_Promotions_Trigger ]]--

events.ComponentLClickUp[#events.ComponentLClickUp+1] =
function (context)
	if conditions.IsComponentType("navy_tab", context) then
		effect.advance_contextual_advice_thread("1052_Campaign_Advice_Navy_Promotions_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1053_Campaign_Advice_Missions_Clock_Ticking_Trigger ]]--

events.MissionNearingExpiry[#events.MissionNearingExpiry+1] =
function (context)
	if true then
		effect.advance_contextual_advice_thread("1053_Campaign_Advice_Missions_Clock_Ticking_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1058_Campaign_Advice_Slot_Selected_Trigger ]]--

events.SlotSelected[#events.SlotSelected+1] =
function (context)
	if conditions.SlotIsLocal(context) and (conditions.SlotType("sheep", context) or conditions.SlotType("wheat", context) or conditions.SlotType("rice", context) or conditions.SlotType("corn", context) or conditions.SlotType("cattle", context)) then
		effect.advance_contextual_advice_thread("1058_Campaign_Advice_Slot_Selected_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1059_Campaign_Advice_Slot_Selected_Trigger ]]--

events.SlotSelected[#events.SlotSelected+1] =
function (context)
	if conditions.SlotIsLocal(context) and (conditions.SlotType("iron", context) or conditions.SlotType("silver", context) or conditions.SlotType("gold", context) or conditions.SlotType("gems", context)) then
		effect.advance_contextual_advice_thread("1059_Campaign_Advice_Slot_Selected_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1060_Campaign_Advice_Slot_Selected_Trigger ]]--

events.SlotSelected[#events.SlotSelected+1] =
function (context)
	if conditions.SlotIsLocal(context) and conditions.SlotType("wine", context) then
		effect.advance_contextual_advice_thread("1060_Campaign_Advice_Slot_Selected_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1061_Campaign_Advice_Slot_Selected_Trigger ]]--

events.SlotSelected[#events.SlotSelected+1] =
function (context)
	if conditions.SlotIsLocal(context) and conditions.SlotType("fur", context) then
		effect.advance_contextual_advice_thread("1061_Campaign_Advice_Slot_Selected_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1062_Campaign_Advice_Slot_Selected_Trigger ]]--

events.SlotSelected[#events.SlotSelected+1] =
function (context)
	if conditions.SlotIsLocal(context) and conditions.SlotType("timber", context) then
		effect.advance_contextual_advice_thread("1062_Campaign_Advice_Slot_Selected_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1063_Campaign_Advice_Slot_Selected_Trigger ]]--

events.SlotSelected[#events.SlotSelected+1] =
function (context)
	if conditions.SlotIsLocal(context) and (conditions.SlotType("southern_usa", context) or conditions.SlotType("caribbean", context) or conditions.SlotType("cuba", context) or conditions.SlotType("egypt", context) or conditions.SlotType("india_highlands", context) or conditions.SlotType("tropical_humid", context)) then
		effect.advance_contextual_advice_thread("1063_Campaign_Advice_Slot_Selected_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1064_Campaign_Advice_Slot_Selected_Trigger ]]--

events.FortSelected[#events.FortSelected+1] =
function (context)
	if conditions.SlotIsLocal(context) and conditions.SlotType("fort", context) then
		effect.advance_contextual_advice_thread("1064_Campaign_Advice_Slot_Selected_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1065_Campaign_Advice_Character_Selected_Trigger ]]--

events.CharacterSelected[#events.CharacterSelected+1] =
function (context)
	if conditions.CharacterIsLocalCampaign(context) and (conditions.CharacterType("General", context) or conditions.CharacterType("colonel", context)) then
		effect.advance_contextual_advice_thread("1065_Campaign_Advice_Character_Selected_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1066_Campaign_Advice_Character_Selected_Trigger ]]--

events.CharacterSelected[#events.CharacterSelected+1] =
function (context)
	if conditions.CharacterIsLocalCampaign(context) and (conditions.CharacterType("admiral", context) or conditions.CharacterType("captain", context)) then
		effect.advance_contextual_advice_thread("1066_Campaign_Advice_Character_Selected_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1077_Campaign_Advice_Character_Selected_Trigger ]]--

events.CharacterSelected[#events.CharacterSelected+1] =
function (context)
	if not conditions.CharacterIsLocalCampaign(context) and (conditions.CharacterType("General", context) or conditions.CharacterType("colonel", context) or conditions.CharacterType("admiral", context) or conditions.CharacterType("captain", context) or conditions.CharacterType("gentleman", context) or conditions.CharacterType("rake", context) or conditions.CharacterType("Eastern_Scholar", context) or conditions.CharacterType("assassin", context) or conditions.CharacterType("catholic_missionary", context) or conditions.CharacterType("Protestant_Missionary", context) or conditions.CharacterType("orthodox_missionary", context) or conditions.CharacterType("middle_east_missionary", context) or conditions.CharacterType("indian_missionary", context)) then
		effect.advance_contextual_advice_thread("1077_Campaign_Advice_Character_Selected_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1079a_Campaign_Advice_Right_Click_Details_Trigger ]]--

events.CharacterInfoPanelOpened[#events.CharacterInfoPanelOpened+1] =
function (context)
	if conditions.CharacterIsLocalCampaign(context) and conditions.CharacterType("General", context) then
		effect.advance_contextual_advice_thread("1079a_Campaign_Advice_Right_Click_Details_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1079b_Campaign_Advice_Right_Click_Details_Trigger ]]--

events.CharacterInfoPanelOpened[#events.CharacterInfoPanelOpened+1] =
function (context)
	if conditions.CharacterIsLocalCampaign(context) and conditions.CharacterType("admiral", context) then
		effect.advance_contextual_advice_thread("1079b_Campaign_Advice_Right_Click_Details_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1080_Campaign_Advice_Right_Click_Details_Trigger ]]--

events.CharacterInfoPanelOpened[#events.CharacterInfoPanelOpened+1] =
function (context)
	if not conditions.CharacterIsLocalCampaign(context) then
		effect.advance_contextual_advice_thread("1080_Campaign_Advice_Right_Click_Details_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1081_Campaign_Advice_Right_Click_Details_Trigger ]]--

events.PanelOpenedCampaign[#events.PanelOpenedCampaign+1] =
function (context)
	if conditions.IsComponentType("region_info", context) then
		effect.advance_contextual_advice_thread("1081_Campaign_Advice_Right_Click_Details_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1082_Campaign_Advice_Right_Click_Details_Trigger ]]--

events.PanelOpenedCampaign[#events.PanelOpenedCampaign+1] =
function (context)
	if conditions.IsComponentType("UnitInfoPopup", context) then
		effect.advance_contextual_advice_thread("1082_Campaign_Advice_Right_Click_Details_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1083_Campaign_Advice_Right_Click_Details_Trigger ]]--

events.PanelOpenedCampaign[#events.PanelOpenedCampaign+1] =
function (context)
	if conditions.IsComponentType("BuildingInfoPopup", context) then
		effect.advance_contextual_advice_thread("1083_Campaign_Advice_Right_Click_Details_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1086_Campaign_Advice_Ambush_Trigger ]]--

events.MovementPointsExhausted[#events.MovementPointsExhausted+1] =
function (context)
	if conditions.CharacterIsLocalCampaign(context) and false then
		effect.advance_contextual_advice_thread("1086_Campaign_Advice_Ambush_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1087_Campaign_Advice_Settlement_Occupied_Trigger ]]--

events.SettlementOccupied[#events.SettlementOccupied+1] =
function (context)
	if not conditions.SettlementIsLocal(context) then
		effect.advance_contextual_advice_thread("1087_Campaign_Advice_Settlement_Occupied_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1090_Campaign_Advice_Multi_Turn_Moves_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterIsLocalCampaign(context) then
		effect.advance_contextual_advice_thread("1090_Campaign_Advice_Multi_Turn_Moves_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1091_Campaign_Advice_Movement_Exhausted_Trigger ]]--

events.MovementPointsExhausted[#events.MovementPointsExhausted+1] =
function (context)
	if conditions.CharacterIsLocalCampaign(context) then
		effect.advance_contextual_advice_thread("1091_Campaign_Advice_Movement_Exhausted_Thread", 1, context)
		return true
	end
	return false
end


--[[ 1096a_Campaign_Advice_Ungarrisoned_Fort_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.SlotIsLocal(context) and not conditions.CampaignName("episodic_1", context) then
		effect.advance_contextual_advice_thread("1096a_Campaign_Advice_Ungarrisoned_Fort_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1096b_Campaign_Advice_Ungarrisoned_Region_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.RegionIsLocal(context) and not conditions.CampaignName("episodic_1", context) then
		effect.advance_contextual_advice_thread("1096b_Campaign_Advice_Ungarrisoned_Region_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1103_Campaign_Advice_Warning_Undeveloped_Farm_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("1103_Campaign_Advice_Undeveloped_Farm_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1104_Campaign_Advice_Warning_Undeveloped_Port_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("1104_Campaign_Advice_Undeveloped_Port_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1105_Campaign_Advice_Warning_Undeveloped_Plantation_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("1105_Campaign_Advice_Undeveloped_Plantation_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1106_Campaign_Advice_Warning_Undeveloped_Town_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("1106_Campaign_Advice_Undeveloped_Town_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1107_Campaign_Advice_Warning_Unexploited_Resources_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("1107_Campaign_Advice_Unexploited_Resources_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1108_Campaign_Advice_Bookmarks_Trigger ]]--

events.FactionTurnStart[#events.FactionTurnStart+1] =
function (context)
	if conditions.FactionIsLocal(context) and conditions.TurnNumber(context) == 3 and not conditions.CampaignName("episodic_1", context) then
		effect.advance_contextual_advice_thread("1108_Campaign_Advice_Bookmarks_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1114_Campaign_Advice_Keyboard_Shortcuts_Trigger ]]--

events.FactionTurnStart[#events.FactionTurnStart+1] =
function (context)
	if conditions.FactionIsLocal(context) and conditions.TurnNumber(context) >= 6 and not conditions.CampaignName("episodic_1", context) then
		effect.advance_contextual_advice_thread("1114_Campaign_Advice_Keyboard_Shortcuts_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1117_Campaign_Advice_Merging_Armies_Trigger ]]--

events.FactionTurnStart[#events.FactionTurnStart+1] =
function (context)
	if conditions.FactionIsLocal(context) and conditions.TurnNumber(context) >= 6 and not conditions.CampaignName("episodic_1", context) then
		effect.advance_contextual_advice_thread("1117_Campaign_Advice_Merging_Armies_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1123_Campaign_Advice_Warning_Upkeep_Trigger ]]--

events.FactionTurnStart[#events.FactionTurnStart+1] =
function (context)
	if conditions.FactionIsLocal(context) and conditions.LosingMoney(context) and false then
		effect.advance_contextual_advice_thread("1123_Campaign_Advice_Warning_Upkeep_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1124_Campaign_Advice_Warning_Bankrupt_Trigger ]]--

events.FactionTurnStart[#events.FactionTurnStart+1] =
function (context)
	if conditions.FactionIsLocal(context) and conditions.LosingMoney(context) and conditions.FactionTreasury(context) <= 0 and conditions.UnusedInternationalTradeRoute(context) then
		effect.advance_contextual_advice_thread("1124_Campaign_Advice_Warning_Bankrupt_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1124a_Campaign_Advice_Warning_Bankrupt_Trigger ]]--

events.FactionTurnStart[#events.FactionTurnStart+1] =
function (context)
	if conditions.FactionIsLocal(context) and conditions.LosingMoney(context) and conditions.FactionTreasury(context) <= 0 then
		effect.advance_contextual_advice_thread("1124a_Campaign_Advice_Warning_Bankrupt_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1125_Campaign_Advice_Warning_Bankrupt_Trigger ]]--

events.FactionTurnStart[#events.FactionTurnStart+1] =
function (context)
	if conditions.FactionIsLocal(context) and conditions.LosingMoney(context) and false then
		effect.advance_contextual_advice_thread("1125_Campaign_Advice_Warning_Bankrupt_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1126_Campaign_Advice_Warning_Cashflow_Trigger ]]--

events.FactionTurnStart[#events.FactionTurnStart+1] =
function (context)
	if conditions.FactionIsLocal(context) and (conditions.FactionTaxLevel("upper_classes", context) < conditions.TaxLevel("tax_extortionate", context) or conditions.FactionTaxLevel("lower_classes", context) < conditions.TaxLevel("tax_extortionate", context)) and conditions.FactionTreasury(context) < 200 then
		effect.advance_contextual_advice_thread("1126_Campaign_Advice_Warning_Cashflow_Trigger", 1, context)
		return true
	end
	return false
end


--[[ 1130_Campaign_Advice_Warning_Wealth_Growth_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("1130_Campaign_Advice_Warning_Wealth_Growth_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1133_Campaign_Advice_Warning_High_Tax_Trigger ]]--

events.RegionTurnStart[#events.RegionTurnStart+1] =
function (context)
	if conditions.RegionIsLocal(context) and conditions.RegionTaxLevel("upper_classes", context) == conditions.TaxLevel("tax_extortionate", context) then
		effect.advance_contextual_advice_thread("1133_Campaign_Advice_Warning_High_Tax_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1134_Campaign_Advice_Warning_High_Tax_Trigger ]]--

events.RegionTurnStart[#events.RegionTurnStart+1] =
function (context)
	if conditions.RegionIsLocal(context) and conditions.RegionTaxLevel("lower_classes", context) == conditions.TaxLevel("tax_extortionate", context) then
		effect.advance_contextual_advice_thread("1134_Campaign_Advice_Warning_High_Tax_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1138_Campaign_Advice_Warning_Population_Trigger ]]--

events.RegionTurnStart[#events.RegionTurnStart+1] =
function (context)
	if conditions.RegionIsLocal(context) and conditions.RegionHasFoodShortages(context) and conditions.RegionPopulationLow(context) then
		effect.advance_contextual_advice_thread("1138_Campaign_Advice_Warning_Population_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1140_Campaign_Advice_Warning_Population_Trigger ]]--

events.RegionTurnStart[#events.RegionTurnStart+1] =
function (context)
	if conditions.RegionIsLocal(context) and conditions.RegionPopulationLow(context) then
		effect.advance_contextual_advice_thread("1140_Campaign_Advice_Warning_Population_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1141_Campaign_Advice_Warning_Population_Trigger ]]--

events.RegionTurnStart[#events.RegionTurnStart+1] =
function (context)
	if conditions.RegionIsLocal(context) and conditions.RegionPopulationLow(context) and conditions.RegionTaxLevel("lower_classes", context) >= conditions.TaxLevel("tax_high", context) then
		effect.advance_contextual_advice_thread("1141_Campaign_Advice_Warning_Population_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1144_Campaign_Advice_Trade_Route_Raided_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if false then
		effect.advance_contextual_advice_thread("1144_Campaign_Advice_Trade_Route_Raided_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1148_Campaign_Advice_Port_Blockaded_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if not conditions.IsColony(context) and conditions.SlotType("port", context) and conditions.IsBuildingInChain("port-navy", context) then
		effect.advance_contextual_advice_thread("1148_Campaign_Advice_Port_Blockaded_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1149_Campaign_Advice_Port_Blockaded_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if not conditions.IsColony(context) and conditions.SlotType("port", context) and conditions.IsBuildingInChain("port-navy", context) then
		effect.advance_contextual_advice_thread("1149_Campaign_Advice_Port_Blockaded_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1150_Campaign_Advice_Port_Blockaded_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if not conditions.IsColony(context) and conditions.SlotType("port", context) and conditions.IsBuildingInChain("port-fish", context) then
		effect.advance_contextual_advice_thread("1150_Campaign_Advice_Port_Blockaded_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1151_Campaign_Advice_Port_Blockaded_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if not conditions.IsColony(context) and conditions.SlotType("port", context) and conditions.IsBuildingInChain("port-fish", context) then
		effect.advance_contextual_advice_thread("1151_Campaign_Advice_Port_Blockaded_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1156_Campaign_Advice_Port_Occupied_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.SlotIsLocal(context) and conditions.SlotType("port", context) then
		effect.advance_contextual_advice_thread("1156_Campaign_Advice_Port_Occupied_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1157_Campaign_Advice_Port_Occupied_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if not conditions.SlotIsLocal(context) and conditions.SlotType("port", context) then
		effect.advance_contextual_advice_thread("1157_Campaign_Advice_Port_Occupied_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1181_Campaign_Advice_Devastation_Trigger ]]--

events.FactionTurnStart[#events.FactionTurnStart+1] =
function (context)
	if conditions.FactionIsLocal(context) and conditions.TurnNumber(context) >= 6 and not conditions.CampaignName("episodic_1", context) then
		effect.advance_contextual_advice_thread("1181_Campaign_Advice_Devastation_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1184_Campaign_Advice_Warning_Bankrupt_Trigger ]]--

events.FactionTurnStart[#events.FactionTurnStart+1] =
function (context)
	if conditions.FactionIsLocal(context) and conditions.LosingMoney(context) and conditions.FactionTreasury(context) <= 0 and conditions.TaxCollectionLimited(context) then
		effect.advance_contextual_advice_thread("1184_Campaign_Advice_Warning_Bankrupt_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1185_Campaign_Advice_Warning_Infrastructure_Trigger ]]--

events.FactionTurnStart[#events.FactionTurnStart+1] =
function (context)
	if conditions.FactionIsLocal(context) and conditions.LosingMoney(context) and conditions.FactionTreasury(context) <= 2000 and conditions.TaxCollectionLimited(context) then
		effect.advance_contextual_advice_thread("1185_Campaign_Advice_Warning_Infrastructure_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1188_Campaign_Advice_Camera_Controls_Trigger ]]--

events.AdviceDismissed[#events.AdviceDismissed+1] =
function (context)
	if conditions.AdviceJustDisplayed("1392703367", context) then
		effect.advance_contextual_advice_thread("1188_Campaign_Advice_Camera_Controls_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1189_Campaign_Advice_UI_Help_Buttons_Trigger ]]--

events.FactionTurnStart[#events.FactionTurnStart+1] =
function (context)
	if conditions.FactionIsLocal(context) and conditions.TurnNumber(context) >= 6 and not conditions.CampaignName("episodic_1", context) then
		effect.advance_contextual_advice_thread("1189_Campaign_Advice_UI_Help_Buttons_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1190_Campaign_Advice_UI_Help_Lists_Trigger ]]--

events.PanelAdviceRequestedCampaign[#events.PanelAdviceRequestedCampaign+1] =
function (context)
	if conditions.IsComponentType("entity_lists", context) then
		effect.advance_contextual_advice_thread("1190_Campaign_Advice_UI_Help_Lists_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1193_Campaign_Advice_UI_Help_Diplomacy_Trigger ]]--

events.PanelAdviceRequestedCampaign[#events.PanelAdviceRequestedCampaign+1] =
function (context)
	if conditions.IsComponentType("diplomatic_relations", context) then
		effect.advance_contextual_advice_thread("1193_Campaign_Advice_UI_Help_Diplomacy_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1194_Campaign_Advice_UI_Help_Diplomacy_Trigger ]]--

events.PanelAdviceRequestedCampaign[#events.PanelAdviceRequestedCampaign+1] =
function (context)
	if conditions.IsComponentType("diplomacy_panel", context) then
		effect.advance_contextual_advice_thread("1194_Campaign_Advice_UI_Help_Diplomacy_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1195_Campaign_Advice_UI_Help_Missions_Trigger ]]--

events.PanelAdviceRequestedCampaign[#events.PanelAdviceRequestedCampaign+1] =
function (context)
	if conditions.IsComponentType("missions", context) then
		effect.advance_contextual_advice_thread("1195_Campaign_Advice_UI_Help_Missions_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1196_Campaign_Advice_UI_Help_Government_Trigger ]]--

events.PanelAdviceRequestedCampaign[#events.PanelAdviceRequestedCampaign+1] =
function (context)
	if conditions.IsComponentType("government_screens", context) then
		effect.advance_contextual_advice_thread("1196_Campaign_Advice_UI_Help_Government_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1197_Campaign_Advice_UI_Help_Prebattle_Trigger ]]--

events.PanelAdviceRequestedCampaign[#events.PanelAdviceRequestedCampaign+1] =
function (context)
	if conditions.IsComponentType("popup_pre_battle", context) then
		effect.advance_contextual_advice_thread("1197_Campaign_Advice_UI_Help_Prebattle_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1198_Campaign_Advice_UI_Help_Postbattle_Trigger ]]--

events.PanelAdviceRequestedCampaign[#events.PanelAdviceRequestedCampaign+1] =
function (context)
	if conditions.IsComponentType("popup_battle_results", context) then
		effect.advance_contextual_advice_thread("1198_Campaign_Advice_UI_Help_Postbattle_Trigger", 1, context)
		return true
	end
	return false
end

--[[ 1201_Campaign_Advice_UI_Help_Units_Trigger ]]--

events.PanelAdviceRequestedCampaign[#events.PanelAdviceRequestedCampaign+1] =
function (context)
	if conditions.IsComponentType("UnitInfoPopup", context) then
		effect.advance_contextual_advice_thread("1201_Campaign_Advice_UI_Help_Units_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1202_Campaign_Advice_UI_Help_Buildings_Trigger ]]--

events.PanelAdviceRequestedCampaign[#events.PanelAdviceRequestedCampaign+1] =
function (context)
	if conditions.IsComponentType("BuildingInfoPopup", context) then
		effect.advance_contextual_advice_thread("1202_Campaign_Advice_UI_Help_Buildings_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1203_Campaign_Advice_UI_Help_Characters_Trigger ]]--

events.PanelAdviceRequestedCampaign[#events.PanelAdviceRequestedCampaign+1] =
function (context)
	if conditions.IsComponentType("CharacterInfoPopup", context) then
		effect.advance_contextual_advice_thread("1203_Campaign_Advice_UI_Help_Characters_Thread", 1, context)
		return true
	end
	return false
end

--[[ 1204_Campaign_Advice_UI_Help_Exchange_Trigger ]]--

events.PanelAdviceRequestedCampaign[#events.PanelAdviceRequestedCampaign+1] =
function (context)
	if conditions.IsComponentType("unit_exchange", context) then
		effect.advance_contextual_advice_thread("1204_Campaign_Advice_UI_Help_Exchange_Thread", 1, context)
		return true
	end
	return false
end

--[[ 2189_Campaign_Advice_Flying_Columns_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if n then
		effect.advance_contextual_advice_thread("2189_Campaign_Advice_Flying_Columns_Thread", 1, context)
		return true
	end
	return false
end

