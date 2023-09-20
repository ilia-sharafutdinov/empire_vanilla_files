--[[
Automatically generated via export from Empire.mdb
Edit manually at your own risk
--]]

module(..., package.seeall)

events = require "data.events"
-- Ancillary Declarations

--[[ Ancillary_African_Servant_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if not conditions.CharacterCultureType("tribal", context) and (conditions.CharacterInTheatre(2113354257, context) or conditions.CharacterInTheatre(836795134, context) or conditions.CharacterInTheatre(1197997136, context)) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_African_Servant", 50,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Air_Loom_Operator_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("rake", context) and not conditions.CharacterCultureType("tribal", context) and conditions.CharacterTrait("C_Agent_Spy_Network", context) == 6 and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Air_Loom_Operator", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Amazing_Wine_Cellar_Trigger ]]--

events.CharacterCreated[#events.CharacterCreated+1] =
function (context)
	if conditions.CharacterCultureType("european", context) and conditions.RandomPercentCampaign(5, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Amazing_Wine_Cellar", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Amusing_Cad_Trigger ]]--

events.CharacterCreated[#events.CharacterCreated+1] =
function (context)
	if conditions.CharacterType("minister", context) and not conditions.IsFactionLeader(context) and not conditions.CharacterCultureType("tribal", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Amusing_Cad", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_ADC_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("General", context) and not conditions.CharacterCultureType("tribal", context) and (conditions.CharacterTrait("C_General_Good_Field_Commander", context) >= 2 or conditions.CharacterTrait("C_General_Defender_Good", context) >= 2 or conditions.CharacterTrait("C_General_Attacker_Good", context) >= 2 or conditions.CharacterTrait("C_General_Ambush_Good", context) >= 2) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_ADC", 83,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Aide_Nephew_Trigger ]]--

events.CharacterCreated[#events.CharacterCreated+1] =
function (context)
	if conditions.CharacterType("General", context) and not conditions.CharacterCultureType("tribal", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Aide_Nephew", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Cleric_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("General", context) and conditions.CharacterCultureType("european", context) and not conditions.CharacterWonBattle(context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Cleric", 67,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Drillmaster_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("General", context) and not conditions.CharacterCultureType("tribal", context) and conditions.CharacterTrait("C_General_Martinet", context) >= 2 and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Drillmaster", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_European_Turncoat_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("General", context) and not conditions.CharacterCultureType("european", context) and conditions.CharacterWonBattle(context) and conditions.CharacterFoughtCulture("european", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_European_Turncoat", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Exploring_Officer_Trigger ]]--

events.MovementPointsExhausted[#events.MovementPointsExhausted+1] =
function (context)
	if conditions.CharacterType("General", context) and conditions.CharacterCultureType("european", context) and conditions.CharacterTrait("C_General_Scout", context) >= 1 and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Exploring_Officer", 50,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Galloper_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("General", context) and not conditions.CharacterCultureType("tribal", context) and conditions.CharacterWonBattle(context) and (conditions.CharacterTrait("C_General_of_Cavalry", context) >= 1 or conditions.CharacterTrait("C_General_Good_Field_Commander", context) >= 2) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Galloper", 50,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Hagiographer_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("General", context) and not conditions.CharacterCultureType("tribal", context) and conditions.BattlesFought(8, context) and conditions.CharacterTrait("C_General_Good_Field_Commander", context) >= 3 and conditions.CharacterTrait("C_General_Press_Hero", context) >= 2 and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Hagiographer", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Loyal_Sowar_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("General", context) and not conditions.CharacterCultureType("tribal", context) and conditions.CharacterWonBattle(context) and conditions.CharacterInTheatre(3, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Loyal_Sowar", 66,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Merc_Artilleryman_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("General", context) and not conditions.CharacterCultureType("tribal", context) and conditions.CharacterWonBattle(context) and not conditions.CharacterFactionName("france", context) and (conditions.CharacterTrait("C_General_Turkish_Master_Gunner", context) >= 1 or conditions.CharacterTrait("C_General_Siege_Attack_Good", context) >= 1 or conditions.CharacterTrait("C_General_of_Artillery", context) >= 1) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Merc_Artilleryman", 83,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Merc_Cavalryman_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("General", context) and not conditions.CharacterCultureType("tribal", context) and conditions.CharacterWonBattle(context) and not conditions.CharacterFactionName("britain", context) and (conditions.CharacterTrait("C_General_of_Cavalry", context) >= 2 or conditions.CharacterTrait("C_General_Attacker_Good", context) >= 2 or conditions.CharacterTrait("C_General_Good_Field_Commander", context) >= 2 or conditions.CharacterTrait("C_General_Defender_Good", context) >= 2) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Merc_Cavalryman", 66,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Merc_Infantryman_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("General", context) and not conditions.CharacterCultureType("tribal", context) and conditions.CharacterWonBattle(context) and not conditions.CharacterFactionName("prussia", context) and (conditions.CharacterTrait("C_General_of_Infantry", context) >= 2 or conditions.CharacterTrait("C_General_Attacker_Good", context) >= 2 or conditions.CharacterTrait("C_General_Defender_Good", context) >= 2 or conditions.CharacterTrait("C_General_Martinet", context) >= 2) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Merc_Infantryman", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Military_Artist_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("General", context) and conditions.CharacterCultureType("european", context) and (conditions.CharacterTrait("C_General_Press_Hero", context) >= 2 or conditions.CharacterTrait("C_General_Good_Field_Commander", context) >= 4) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Military_Artist", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Military_Surveyor_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("General", context) and not conditions.CharacterCultureType("tribal", context) and conditions.CharacterTrait("C_General_Scout", context) == 2 and conditions.CharacterTrait("C_General_Good_Field_Commander", context) >= 4 and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Military_Surveyor", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Ottoman_Turncoat_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("General", context) and not conditions.CharacterCultureType("middle_east", context) and conditions.CharacterWonBattle(context) and conditions.CharacterFoughtCulture("middle_east", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Ottoman_Turncoat", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Pox_Doctor_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterCultureType("european", context) and not conditions.IsFactionLeaderFemale(context) and (conditions.CharacterTrait("C_Feck_Vice", context) >= 4 or conditions.CharacterTrait("C_Leader_Debauched", context) >= 1) and conditions.RandomPercentCampaign(70, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Pox_Doctor", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Quartermaster_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("General", context) and not conditions.CharacterCultureType("tribal", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Quartermaster", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Surgeon_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("General", context) and not conditions.CharacterCultureType("tribal", context) and conditions.CharacterWonBattle(context) and (conditions.CharacterTrait("C_General_Bloody", context) >= 1 or conditions.BattleResult("pyrrhic_victory", context)) and conditions.RandomPercentCampaign(40, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Surgeon", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Tribal_Shaman_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("General", context) and conditions.CharacterCultureType("tribal", context) and conditions.CharacterWonBattle(context) and conditions.RandomPercentCampaign(80, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Tribal_Shaman", 66,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Waggonmaster_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("General", context) and not conditions.CharacterCultureType("tribal", context) and conditions.CharacterTrait("C_General_Scout", context) and conditions.RandomPercentCampaign(30, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Waggonmaster", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Artillery_Expert_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("General", context) and conditions.CharacterCultureType("european", context) and (conditions.CharacterTrait("C_General_of_Artillery", context) >= 2 or conditions.CharacterTrait("C_General_Siege_Attack_Good", context) >= 2) and conditions.RandomPercentCampaign(60, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Artillery_Expert", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Assassin_Thug_2_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.CharacterMinisterialPosition("justice", context) and conditions.CharacterCultureType("indian", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Assassin_Thug", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Assassin_Thug_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("assassin", context) and conditions.CharacterCultureType("indian", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Assassin_Thug", 3,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Barber_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("minister", context) and not conditions.IsFactionLeader(context) and not conditions.IsFactionLeaderFemale(context) and conditions.CharacterCultureType("european", context) and conditions.RandomPercentCampaign(10, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Barber", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Blood_Brother_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("General", context) and not conditions.CharacterCultureType("indian", context) and not conditions.CharacterCultureType("middle_east", context) and conditions.CharacterInTheatre("1", context) and conditions.RandomPercentCampaign(10, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Blood_Brother", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Bodysnatcher_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("gentleman", context) and conditions.CharacterCultureType("european", context) and conditions.CharacterTrait("C_Gent_Science_Club", context) >= 1 and conditions.RandomPercentCampaign(10, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Bodysnatcher", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Boxer_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("General", context) and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Boxer", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Duelling_Hidalgo_Fop_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if (conditions.CharacterType("rake", context) or conditions.CharacterType("gentleman", context)) and (conditions.CharacterFactionName("spain", context) or conditions.CharacterFactionName("portugal", context)) and conditions.CharacterTrait("C_Gent_Duelling_Sword", context) >= 3 and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Duelling_Hidalgo_Fop", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Duelling_Minx_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if (conditions.CharacterType("rake", context) or conditions.CharacterType("gentleman", context)) and conditions.CharacterCultureType("european", context) and (conditions.CharacterTrait("C_Gent_Duelling_Sword", context) >= 2 or conditions.CharacterTrait("C_Gent_Duelling_Pistol", context) >= 4) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Duelling_Minx", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Duelling_Pistols_Manton_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if (conditions.CharacterType("rake", context) or conditions.CharacterType("gentleman", context)) and conditions.CharacterFactionName("britain", context) and conditions.CharacterTrait("C_Gent_Duelling_Pistol", context) == 3 and conditions.RandomPercentCampaign(80, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Duelling_Pistols_Manton", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Duelling_Pistols_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if (conditions.CharacterType("rake", context) or conditions.CharacterType("gentleman", context)) and conditions.CharacterCultureType("european", context) and conditions.CharacterTrait("C_Gent_Duelling_Pistol", context) >= 2 and conditions.RandomPercentCampaign(80, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Duelling_Pistols", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_European_Captive_Ferang_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if (conditions.CharacterType("General", context) or conditions.CharacterType("admiral", context)) and conditions.CharacterCultureType("indian", context) and conditions.CharacterFoughtCulture("european", context) or (conditions.CharacterInTheatre(836795134, context) or conditions.CharacterInTheatre(-1133129049, context))  and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_European_Captive_Ferang", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Foodtaster_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.IsFactionLeader(context) or conditions.IsFactionLeaderFemale(context) and (conditions.CharacterCultureType("indian", context) or conditions.CharacterCultureType("middle_east", context)) and conditions.RandomPercentCampaign(60, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Foodtaster", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Garden_Hermit_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and (conditions.IsFactionLeader(context) or conditions.IsFactionLeaderFemale(context)) and conditions.CharacterCultureType("european", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Garden_Hermit", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Architect_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and (conditions.IsFactionLeader(context) or conditions.IsFactionLeaderFemale(context)) and not conditions.CharacterCultureType("tribal", context) and conditions.CharacterTrait("C_Leader_Foreign_Tastes", context) >= 1 and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Architect", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Comptroller_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.CharacterMinisterialPosition("finance", context) and conditions.CharacterCultureType("european", context) and conditions.CharacterTrait("C_Minister_Miser", context) <= 1 and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Comptroller", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Controller_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and not conditions.IsFactionLeader(context) and not conditions.IsFactionLeaderFemale(context) and not conditions.CharacterCultureType("tribal", context) and (conditions.CharacterTrait("C_Minister_Entertainer", context) >= 1 or conditions.CharacterTrait("C_Minister_Industrialist", context) >= 1) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Controller", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Crimper_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.CharacterMinisterialPosition("army", context) and conditions.CharacterCultureType("european", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Crimper", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Cypher_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.CharacterMinisterialPosition("justice", context) and not conditions.CharacterCultureType("tribal", context) and conditions.RandomPercentCampaign(30, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Cypher", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Executioner_Nasty_Trigger ]]--

events.SufferAssassinationAttempt[#events.SufferAssassinationAttempt+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.IsFactionLeader(context) and not conditions.CharacterCultureType("european", context) and not conditions.CharacterCultureType("tribal", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Executioner_Nasty", 50,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Guardian_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.IsFactionLeader(context) and not conditions.CharacterCultureType("european", context) and not conditions.CharacterCultureType("tribal", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Guardian", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Secret_Policeman_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.CharacterMinisterialPosition("justice", context) and not conditions.CharacterCultureType("tribal", context) and (conditions.CharacterTrait("C_Minister_Unjust", context) >= 2 or conditions.FactionLeadersTrait("C_Leader_Harsh_Ruler", context) >= 1) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Secret_Policeman", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Secretary_Efficient_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and not conditions.IsFactionLeader(context) and not conditions.IsFactionLeaderFemale(context) and not conditions.CharacterCultureType("tribal", context) and (conditions.CharacterTrait("C_Minister_Fiscal_Genius", context) >= 1 or conditions.FactionLeadersTrait("C_Leader_Intellectual_Pretensions", context) >= 1) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Secretary_Efficient", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Secretary_Gobby_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and not conditions.IsFactionLeader(context) and not conditions.IsFactionLeaderFemale(context) and not conditions.CharacterCultureType("tribal", context) and (conditions.FactionLeadersTrait("C_Leader_M", context) >= 1 or conditions.FactionLeadersTrait("C_Leader_Mr_Waverley", context) >= 1 or conditions.CharacterTrait("C_Minister_Corrupt", context) >= 1) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Secretary_Gobby", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Spymaster_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.CharacterMinisterialPosition("justice", context) and not conditions.CharacterCultureType("tribal", context) and (conditions.FactionLeadersTrait("C_Leader_M", context) >= 1 or conditions.FactionLeadersTrait("C_Leader_Mr_Waverley", context) >= 1 or conditions.FactionLeadersTrait("C_Leader_Harsh_Ruler", context) >= 1 or conditions.FactionLeadersTrait("C_Leader_Agent_99", context) >= 1) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Spymaster", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Thieftaker_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.CharacterMinisterialPosition("justice", context) and conditions.CharacterCultureType("european", context) and conditions.CharacterTrait("C_Minister_Unjust", context) >= 1 and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Thieftaker", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Vampire_Hunter_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.IsFactionLeader(context) and conditions.CharacterFactionName("austria", context) and conditions.FactionLeadersTrait("C_Personal_Piety", context) >= 2 and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Vampire_Hunter", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Wrestler_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and not conditions.IsFactionLeader(context) and (conditions.CharacterCultureType("indian", context) or conditions.CharacterCultureType("middle_east", context)) and (conditions.CharacterTrait("C_Minister_Unjust", context) >= 2 or conditions.FactionLeadersTrait("C_Leader_Harsh_Ruler", context) >= 1) and conditions.RandomPercentCampaign(50, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Wrestler", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Great_Composer_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.IsFactionLeader(context) and conditions.CharacterCultureType("european", context) and conditions.RandomPercentCampaign(50, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Great_Composer", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Grizzly_Adams_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("General", context) and not conditions.CharacterCultureType("tribal", context) and conditions.CharacterWonBattle(context) and conditions.CharacterInTheatre(1, context) and conditions.RandomPercentCampaign(50, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Grizzly_Adams", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Historian_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.IsFactionLeader(context) and not conditions.CharacterCultureType("tribal", context) and conditions.CharacterTrait("C_Leader_Enlightened_Despot", context) == 1 and conditions.RandomPercentCampaign(30, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Historian", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Inventive_Genius_Astronomer_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if (conditions.CharacterType("gentleman", context) or conditions.CharacterType("Eastern_Scholar", context)) and not conditions.CharacterCultureType("tribal", context) and (conditions.FactionLeadersTrait("C_Leader_Enlightened_Despot", context) == 1 or conditions.FactionLeadersTrait("C_Leader_Intellectual_Pretensions", context) >= 2) and conditions.RandomPercentCampaign(25, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Inventive_Genius_Astronomer", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Inventive_Genius_Loony_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("gentleman", context) and conditions.CharacterCultureType("european", context) and (conditions.FactionLeadersTrait("C_Leader_Enlightened_Despot", context) == 1 or conditions.FactionLeadersTrait("C_Leader_Intellectual_Pretensions", context) >= 2) and conditions.RandomPercentCampaign(15, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Inventive_Genius_Loony", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Inventive_Genius_Mill_Worker_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("gentleman", context) and conditions.CharacterCultureType("european", context) and conditions.CharacterTrait("C_Minister_Industrialist", context) >= 2 and conditions.RandomPercentCampaign(15, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Inventive_Genius_Mill_Worker", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Justice_Witness_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.CharacterMinisterialPosition("justice", context) and conditions.CharacterCultureType("european", context) and (conditions.CharacterTrait("C_Minister_Unjust", context) >= 1 or conditions.FactionLeadersTrait("C_Leader_Harsh_Ruler", context) >= 1) and conditions.RandomPercentCampaign(10, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Justice_Witness", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Landscape_Gardener_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.IsFactionLeader(context) and conditions.CharacterCultureType("european", context) and conditions.CharacterTrait("C_Leader_Philistine", context) < 1 and conditions.CharacterTrait("C_Leader_Uncouth", context) < 1 and conditions.RandomPercentCampaign(25, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Landscape_Gardener", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Madman_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("gentleman", context) and conditions.CharacterCultureType("european", context) and conditions.CharacterTrait("C_Gent_Academic_Honours", context) >= 2 and conditions.RandomPercentCampaign(5, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Madman", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Master_of_Lunacy_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("gentleman", context) and conditions.CharacterCultureType("european", context) and conditions.FactionLeadersTrait("C_Leader_Intellectual_Pretensions", context) >= 2 and conditions.RandomPercentCampaign(5, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Master_of_Lunacy", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Merchant_Corn_Factor_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.CharacterCultureType("european", context) and conditions.CharacterTrait("C_Minister_Trader", context) >= 1 and conditions.RandomPercentCampaign(30, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Merchant_Corn_Factor", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Military_Riding_Master_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("General", context) and conditions.CharacterCultureType("european", context) and conditions.CharacterTrait("C_General_of_Cavalry", context) >= 1 and conditions.RandomPercentCampaign(25, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Military_Riding_Master", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Mistress_Actress_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if (conditions.CharacterType("General", context) or conditions.CharacterType("admiral", context)) and conditions.CharacterCultureType("european", context) and conditions.CharacterTrait("C_Personal_Piety", context) < 1 and conditions.RandomPercentCampaign(10, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Mistress_Actress", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Mistress_Circassian_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.IsFactionLeader(context) and conditions.CharacterCultureType("middle_east", context) and conditions.RandomPercentCampaign(10, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Mistress_Circassian", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Mistress_Common_Floozy_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and not conditions.IsFactionLeader(context) and conditions.CharacterCultureType("european", context) and conditions.RandomPercentCampaign(20, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Mistress_Common_Floozy", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Mistress_Gorgeous_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and not conditions.CharacterCultureType("tribal", context) and conditions.RandomPercentCampaign(15, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Mistress_Gorgeous", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Mistress_Molly_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and not conditions.IsFactionLeader(context) and conditions.CharacterCultureType("european", context) and conditions.RandomPercentCampaign(5, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Mistress_Molly", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Mistress_Noble_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and not conditions.IsFactionLeader(context) and conditions.CharacterCultureType("european", context) and conditions.RandomPercentCampaign(5, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Mistress_Noble", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Mistress_Spycatcher_Lady_Trigger ]]--

events.SpyingAttemptSuccess[#events.SpyingAttemptSuccess+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.CharacterMinisterialPosition("justice", context) and conditions.CharacterCultureType("european", context) and conditions.RandomPercentCampaign(10, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Mistress_Spycatcher_Lady", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Mistress_Spymistress_Trigger ]]--

events.SpyingAttemptSuccess[#events.SpyingAttemptSuccess+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.CharacterMinisterialPosition("justice", context) and not conditions.CharacterCultureType("tribal", context) and conditions.RandomPercentCampaign(10, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Mistress_Spymistress", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Mystic_Mysterious_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("General", context) and conditions.CharacterCultureType("european", context) and conditions.CharacterInTheatre(3, context) and conditions.RandomPercentCampaign(20, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Mystic_Mysterious", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Mystic_Useful_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("General", context) and (conditions.CharacterCultureType("indian", context) or conditions.CharacterCultureType("middle_east", context)) and not conditions.CharacterInTheatre(1, context) and conditions.RandomPercentCampaign(15, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Mystic_Useful", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Navy_Cleric_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("admiral", context) and conditions.CharacterCultureType("european", context) and not conditions.CharacterWonBattle(context) and conditions.CharacterTrait("C_Personal_Piety", context) >= 1 and conditions.RandomPercentCampaign(70, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Navy_Cleric", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Navy_Flag_Lieutenant_Trigger ]]--

events.MovementPointsExhausted[#events.MovementPointsExhausted+1] =
function (context)
	if conditions.CharacterType("admiral", context) and conditions.CharacterCultureType("european", context) and (conditions.CharacterTrait("C_Admiral_Defender_Good", context) >= 2 or conditions.CharacterTrait("C_Admiral_Attacker_Good", context) >= 2) and conditions.RandomPercentCampaign(40, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Navy_Flag_Lieutenant", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Navy_Merc_Sea_Captain_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("admiral", context) and (conditions.CharacterCultureType("indian", context) or conditions.CharacterCultureType("middle_east", context)) and conditions.RandomPercentCampaign(10, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Navy_Merc_Sea_Captain", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Navy_Naval_Architect_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("admiral", context) and conditions.CharacterCultureType("european", context) and conditions.FactionLeadersTrait("C_Leader_Navy_Buff", context) >= 2 and conditions.RandomPercentCampaign(15, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Navy_Naval_Architect", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Navy_Naval_Surveryor_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("admiral", context) and conditions.CharacterCultureType("european", context) and conditions.CharacterTrait("C_Admiral_Mathematician", context) < 1 and conditions.RandomPercentCampaign(15, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Navy_Naval_Surveryor", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Navy_Prize_Agent_Good_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("admiral", context) and conditions.CharacterCultureType("european", context) and conditions.CharacterWonBattle(context) and conditions.CharacterCapturedEnemyShip(context) and conditions.RandomPercentCampaign(50, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Navy_Prize_Agent_Good", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Navy_Purser_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("admiral", context) and not conditions.CharacterCultureType("tribal", context) and conditions.CharacterTrait("C_Admiral_Martinet", context) >= 1 and conditions.RandomPercentCampaign(20, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Navy_Purser", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Navy_Sailing_Master_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("admiral", context) and not conditions.CharacterCultureType("tribal", context) and (conditions.CharacterInTheatre(-1133129049, context) or conditions.CharacterInTheatre(836795134, context) or conditions.CharacterInTheatre(1197997136, context) or conditions.CharacterInTheatre(2113354257, context)) and conditions.RandomPercentCampaign(20, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Navy_Sailing_Master", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Navy_Surgeon_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("admiral", context) and not conditions.CharacterCultureType("tribal", context) and conditions.CharacterWonBattle(context) and conditions.BattleResult("pyrrhic_victory", context) and conditions.RandomPercentCampaign(20, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Navy_Surgeon", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Navy_Watch_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("admiral", context) and not conditions.CharacterCultureType("tribal", context) and conditions.CharacterFactionHasTechType("military_navy_longitude_watch", context) and conditions.RandomPercentCampaign(60, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Navy_Watch", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Numismatist_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and not conditions.IsFactionLeader(context) and conditions.CharacterMinisterialPosition("finance", context) and conditions.CharacterTrait("C_Minister_Corrupt", context) >= 1 and conditions.RandomPercentCampaign(30, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Numismatist", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Outstanding_Choirmaster_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.IsFactionLeader(context) and conditions.CharacterCultureType("european", context) and conditions.RandomPercentCampaign(30, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Outstanding_Choirmaster", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Pamphleteer_Government_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.CharacterMinisterialPosition("justice", context) and conditions.RandomPercentCampaign(20, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Pamphleteer_Government", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Pamphleteer_Radical_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("rake", context) and conditions.CharacterTrait("C_Agent_Spy_Network", context) >= 1 and conditions.RandomPercentCampaign(20, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Pamphleteer_Radical", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Personal_Physician_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("General", context) and conditions.CharacterTrait("C_General_Slacker", context) >= 2 and conditions.NoActionThisTurn(context) and conditions.RandomPercentCampaign(30, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Personal_Physician", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Pet_Monkey_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if (conditions.CharacterType("rake", context) or conditions.CharacterType("assassin", context)) and not conditions.CharacterCultureType("tribal", context) and conditions.CharacterInTheatre(3, context) and conditions.RandomPercentCampaign(30, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Pet_Monkey", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Pet_Sacred_Cow_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.IsFactionLeader(context) and conditions.CharacterFactionSubcultureType("sc_indian_hindu", context) and conditions.RandomPercentCampaign(5, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Pet_Sacred_Cow", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Pet_Tiger_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.IsFactionLeader(context) and conditions.CharacterCultureType("indian", context) and conditions.RandomPercentCampaign(15, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Pet_Tiger", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Poet_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.IsFactionLeader(context) and conditions.CharacterCultureType("european", context) and conditions.CharacterTrait("C_Leader_Intellectual_Pretensions", context) >= 2 and conditions.RandomPercentCampaign(40, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Poet", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Police_Torturer_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.CharacterMinisterialPosition("justice", context) and not conditions.CharacterCultureType("tribal", context) and conditions.RandomPercentCampaign(30, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Police_Torturer", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Presentation_Sword_1_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("General", context) and conditions.CharacterCultureType("european", context) and conditions.CharacterWonBattle(context) and conditions.BattleResult("heroic_victory", context) and conditions.BattlesFought(15, context) and conditions.RandomPercentCampaign(10, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Presentation_Sword_1", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Presentation_Sword_2_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("admiral", context) and conditions.CharacterCultureType("european", context) and conditions.CharacterWonBattle(context) and conditions.BattleResult("heroic_victory", context) and conditions.BattlesFought(15, context) and conditions.RandomPercentCampaign(10, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Presentation_Sword_2", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Rake_Bawd_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("rake", context) and conditions.CharacterTrait("C_Agent_Spy_Network", context) >= 1 and conditions.RandomPercentCampaign(10, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Rake_Bawd", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Rake_Professional_Second_Trigger ]]--

events.DuelFought[#events.DuelFought+1] =
function (context)
	if (conditions.CharacterType("rake", context) or conditions.CharacterType("gentleman", context)) and conditions.CharacterWonDuel(context) and conditions.RandomPercentCampaign(10, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Rake_Professional_Second", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Religion_Bishop_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.IsFactionLeader(context) and conditions.CharacterCultureType("european", context) and conditions.RandomPercentCampaign(20, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Religion_Bishop", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Religion_Imam_Learned_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.IsFactionLeader(context) and conditions.CharacterCultureType("middle_east", context) and conditions.RandomPercentCampaign(20, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Religion_Imam_Learned", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Religion_Imam_Rabblerouser_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.IsFactionLeader(context) and conditions.CharacterCultureType("middle_east", context) and conditions.RandomPercentCampaign(5, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Religion_Imam_Rabblerouser", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Religion_Methodist_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.IsFactionLeader(context) and (conditions.CharacterFactionName("britain", context) or conditions.CharacterFactionName("sweden", context) or conditions.CharacterFactionName("denmark", context) or conditions.CharacterFactionName("prussia", context) or conditions.CharacterFactionName("united_states", context) or conditions.CharacterFactionName("hannover", context) or conditions.CharacterFactionName("netherlands", context) or conditions.CharacterFactionName("norway", context)) and conditions.RandomPercentCampaign(10, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Religion_Methodist", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Research_Librarian_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if (conditions.CharacterType("gentleman", context) or conditions.CharacterType("Eastern_Scholar", context)) and not conditions.CharacterCultureType("tribal", context) and conditions.RandomPercentCampaign(20, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Research_Librarian", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Research_Lunatic_Jack_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if (conditions.CharacterType("gentleman", context) or conditions.CharacterType("Eastern_Scholar", context)) and not conditions.CharacterCultureType("tribal", context) and conditions.RandomPercentCampaign(10, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Research_Lunatic_Jack", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Research_Taxonomist_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("gentleman", context) and conditions.CharacterCultureType("european", context) and conditions.RandomPercentCampaign(5, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Research_Taxonomist", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Tax_Farmer_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.CharacterMinisterialPosition("finance", context) and not conditions.CharacterCultureType("tribal", context) and conditions.RandomPercentCampaign(15, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Tax_Farmer", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Wife_Ambitious_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and not conditions.IsFactionLeader(context) and conditions.CharacterCultureType("european", context) and conditions.RandomPercentCampaign(5, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Wife_Ambitious", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Wife_Unpleasant_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and not conditions.IsFactionLeader(context) and conditions.CharacterCultureType("european", context) and conditions.RandomPercentCampaign(5, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Wife_Unpleasant", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancilllary_Dead_Parrot_Pirate_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("admiral", context) and conditions.CharacterCultureType("european", context) and conditions.RandomPercentCampaign(5, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancilllary_Dead_Parrot_Pirate", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancilllary_Pet_Parrot_Nasty_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("admiral", context) and conditions.CharacterCultureType("european", context) and conditions.RandomPercentCampaign(5, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancilllary_Pet_Parrot_Nasty", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancilllary_Pet_Parrot_Ordinary_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("admiral", context) and conditions.CharacterCultureType("european", context) and conditions.RandomPercentCampaign(5, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancilllary_Pet_Parrot_Ordinary", 100,  context)
		end
		return true
	end
	return false
end

--[[ Government_Spying_Locksmith_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("rake", context) and not conditions.CharacterCultureType("tribal", context) and conditions.CharacterTrait("C_Agent_Spy_Network", context) >= 3 and conditions.RandomPercentCampaign(15, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Government_Spying_Locksmith", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Vampire_Hunter_2_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterBuildingConstructed("rel_catholic_2", context) and (conditions.IsFactionLeader(context) or conditions.CharacterMinisterialPosition("head_of_government", context)) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Vampire_Hunter", 50,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Great_Composer_2_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if not conditions.OnAWarFooting(context) and conditions.CharacterBuildingConstructed("grand_opera_house", context) and conditions.RandomPercentCampaign(17, context) and (conditions.IsFactionLeader(context) or conditions.CharacterMinisterialPosition("head_of_government", context)) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Great_Composer", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_European_Captive_Ferang_2_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if (conditions.CharacterType("admiral", context) or conditions.CharacterType("General", context)) and conditions.CharacterInBuildingOfChain("port-trade", context) and conditions.CharacterMPPercentageRemaining(context) >= 50 and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_European_Captive_Ferang", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Amusing_Cad_2_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.IsFactionLeader(context) and conditions.CharacterBuildingConstructed("bawdy_house", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Amusing_Cad", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Assassin_Thug_3_Trigger ]]--

events.AssassinationAttemptSuccess[#events.AssassinationAttemptSuccess+1] =
function (context)
	if (conditions.CharacterType("rake", context) or conditions.CharacterType("assassin", context)) and conditions.CharacterInTheatre(3, context) and conditions.CharacterAttribute("subterfuge", context) >= 2 and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Assassin_Thug", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Air_Loom_Operator_2_Trigger ]]--

events.SpyingAttemptSuccess[#events.SpyingAttemptSuccess+1] =
function (context)
	if conditions.CharacterInTheatre(2, context) and conditions.CharacterType("rake", context) and (conditions.CharacterFactionName("france", context) or conditions.CharacterFactionName("britain", context)) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Air_Loom_Operator", 50,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Pox_Doctor_2_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Pox_Doctor", 50,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Navy_Merc_Sea_Captain_2_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("admiral", context) and (conditions.CharacterCultureType("indian", context) or conditions.CharacterCultureType("middle_east", context)) and conditions.CharacterFoughtCulture("european", context) and conditions.RandomPercentCampaign(33, context) and not conditions.CharacterWasAttacker(context) and not conditions.CharacterWonBattle(context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Navy_Merc_Sea_Captain", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Navy_Watch_2_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("admiral", context) and conditions.CharacterAttribute("command_sea", context) >= 4 and conditions.CharacterFactionHasTechType("military_navy_longitude_watch", context) and conditions.CharacterInBuildingOfChain("port-navy", context) and conditions.RandomPercentCampaign(17, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Navy_Watch", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Merc_Artilleryman_2_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("General", context) and conditions.CharacterCultureType("indian", context) and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Merc_Artilleryman", 83,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Merc_Cavalryman_2_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("General", context) and conditions.CharacterCultureType("indian", context) and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Merc_Cavalryman", 66,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Merc_Infantryman_2_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("General", context) and conditions.CharacterCultureType("indian", context) and not conditions.CharacterWasAttacker(context) and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Merc_Infantryman", 66,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Blood_Brother_2_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("General", context) and not conditions.CharacterCultureType("tribal", context) and conditions.CharacterFoughtCulture("tribal", context) and conditions.CharacterInTheatre(1, context) and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Blood_Brother", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Exploring_Officer_2_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("General", context) and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Exploring_Officer", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Waggonmaster_2_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("General", context) and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Waggonmaster", 50,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Quartermaster_2_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("General", context) and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Quartermaster", 50,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Tribal_Shaman_2_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("General", context) and conditions.CharacterCultureType("tribal", context) and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Tribal_Shaman", 66,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Loyal_Sowar_2_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("General", context) and not conditions.CharacterCultureType("tribal", context) and conditions.CharacterInTheatre(3, context) and conditions.CharacterWonBattle(context) and conditions.CommanderFoughtInMelee(context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Loyal_Sowar", 83,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Hagiographer_2_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("General", context) and conditions.CharacterWasAttacker(context) and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Hagiographer", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Surgeon_2_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("General", context) and not conditions.CharacterCultureType("tribal", context) and conditions.CharacterWonBattle(context) and conditions.CharacterTrait("C_General_Bloody", context) <= 1 and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Surgeon", 50,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Ottoman_Turncoat_2_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("General", context) and not conditions.CharacterFactionName("ottomans", context) and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Ottoman_Turncoat", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Military_Artist_2_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("General", context) and conditions.CharacterTrait("C_General_Scout", context) >= 1 and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Military_Artist", 50,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Military_Surveyor_2_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("General", context) and conditions.CharacterTrait("C_General_Scout", context) == 1 and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Military_Surveyor", 66,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Cleric_2_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("General", context) and conditions.CharacterWonBattle(context) and conditions.EnemyArmyGreaterCombatStrength(context) and not conditions.CharacterWasAttacker(context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Cleric", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Drillmaster_2_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("General", context) and conditions.CampaignBattleType("land_normal", context) and conditions.CampaignPercentageOfUnitCategory("infantry", context) >= 40 and not conditions.CharacterWonBattle(context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Drillmaster", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Artillery_Expert_2_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("General", context) and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Artillery_Expert", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Barber_2_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("General", context) and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Barber", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Aide_Nephew_2_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("General", context) and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Aide_Nephew", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Research_Librarian_2_Trigger ]]--

events.ResearchCompleted[#events.ResearchCompleted+1] =
function (context)
	if conditions.CharacterType("gentleman", context) and conditions.CharacterInBuildingOfChain("education", context) and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Research_Librarian", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Inventive_Genius_Loony_2_Trigger ]]--

events.ResearchCompleted[#events.ResearchCompleted+1] =
function (context)
	if conditions.CharacterType("gentleman", context) and conditions.CharacterInBuildingOfChain("education", context) and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Inventive_Genius_Loony", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Inventive_Genius_Mill_Worker_2_Trigger ]]--

events.ResearchCompleted[#events.ResearchCompleted+1] =
function (context)
	if conditions.CharacterType("gentleman", context) and conditions.CharacterInBuildingOfChain("education", context) and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Inventive_Genius_Mill_Worker", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Research_Taxonomist_2_Trigger ]]--

events.ResearchCompleted[#events.ResearchCompleted+1] =
function (context)
	if conditions.CharacterType("gentleman", context) and conditions.CharacterInBuildingOfChain("education", context) and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Research_Taxonomist", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Inventive_Genius_Astronomer_2_Trigger ]]--

events.ResearchCompleted[#events.ResearchCompleted+1] =
function (context)
	if (conditions.CharacterType("gentleman", context) or conditions.CharacterType("Eastern_Scholar", context)) and conditions.CharacterInBuildingOfChain("education", context) and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Inventive_Genius_Astronomer", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Bodysnatcher_2_Trigger ]]--

events.ResearchCompleted[#events.ResearchCompleted+1] =
function (context)
	if conditions.CharacterType("gentleman", context) and conditions.CharacterInBuildingOfChain("education", context) and conditions.ResearchCategory("philosophy", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Bodysnatcher", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Research_Lunatic_Jack_2_Trigger ]]--

events.ResearchCompleted[#events.ResearchCompleted+1] =
function (context)
	if conditions.CharacterType("gentleman", context) and conditions.CharacterInBuildingOfChain("education", context) and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Research_Lunatic_Jack", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Madman_2_Trigger ]]--

events.ResearchCompleted[#events.ResearchCompleted+1] =
function (context)
	if conditions.CharacterType("gentleman", context) and conditions.CharacterTrait("C_Gent_Science_Club", context) >= 1 and conditions.CharacterInBuildingOfChain("education", context) and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Madman", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Landscape_Gardener_2_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("minister", context) and (conditions.CharacterBuildingConstructed("corn_great_estates", context) or conditions.CharacterBuildingConstructed("sheep_great_estates", context) or conditions.CharacterBuildingConstructed("wheat_great_estates", context)) and conditions.RandomPercentCampaign(17, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Landscape_Gardener", 100,  context)
		end
		return true
	end
	return false
end

--[[ Government_Spying_Locksmith_2_Trigger ]]--

events.SufferSpyingAttempt[#events.SufferSpyingAttempt+1] =
function (context)
	if conditions.CharacterType("minister", context) and (conditions.CharacterMinisterialPosition("head_of_government", context) or conditions.CharacterMinisterialPosition("justice", context)) and (conditions.FactionLeadersTrait("C_Leader_M", context) == 1 or conditions.FactionLeadersTrait("C_Leader_Mr_Waverley", context) ==1) and conditions.RandomPercentCampaign(17, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Government_Spying_Locksmith", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Wife_Ambitious_2_Trigger ]]--

events.CharacterCreated[#events.CharacterCreated+1] =
function (context)
	if conditions.CharacterType("minister", context) and not conditions.IsFactionLeader(context) and (conditions.FactionLeadersTrait("C_Leader_Dullard", context) >= 1 or conditions.FactionLeadersTrait("C_Leader_Favourites", context) >= 1 or conditions.FactionLeadersTrait("C_Leader_Inbred", context) >= 1 or conditions.FactionLeadersTrait("C_Leader_Huntin_Shootin_Fishin", context) >= 1) and conditions.FactionLeadersAttribute("management", context) <= 3 and conditions.RandomPercentCampaign(17, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Wife_Ambitious", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Wife_Unpleasant_2_Trigger ]]--

events.CharacterCreated[#events.CharacterCreated+1] =
function (context)
	if conditions.CharacterType("minister", context) and not conditions.IsFactionLeader(context) and (conditions.FactionLeadersTrait("C_Leader_Merit", context) >= 1 or conditions.FactionLeadersTrait("C_Leader_Mad", context) >= 1) and conditions.FactionLeadersAttribute("management", context) <= 2 and conditions.RandomPercentCampaign(17, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Wife_Unpleasant", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Architect_2_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and (conditions.IsFactionLeader(context) or conditions.CharacterMinisterialPosition("finance", context)) and conditions.CharacterBuildingConstructed("imperial_palace", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Architect", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Controller_2_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("minister", context) and (conditions.IsFactionLeader(context) or conditions.CharacterMinisterialPosition("finance", context)) and conditions.CharacterBuildingConstructed("royal_palace", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Controller", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Comptroller_2_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and (conditions.IsFactionLeader(context) or conditions.CharacterMinisterialPosition("finance", context)) and conditions.CharacterAttribute("management", context) <= 2 and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Comptroller", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Wrestler_2_Trigger ]]--

events.SufferAssassinationAttempt[#events.SufferAssassinationAttempt+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.RandomPercentCampaign(17, context) and (conditions.IsFactionLeader(context) or conditions.CharacterMinisterialPosition("justice", context)) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Wrestler", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Military_Riding_Master_2_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.CharacterMinisterialPosition("army", context) and not conditions.CharacterFactionName("hungary", context) and conditions.CharacterBuildingConstructed("army_staff_college", context) and conditions.RandomPercentCampaign(17, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Military_Riding_Master", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_African_Servant_2_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.CharacterMinisterialPosition("governor_america", context) and conditions.CharacterBuildingConstructed("large_cotton_plantation", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_African_Servant", 66,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Executioner_Nasty_2_Trigger ]]--

events.SufferAssassinationAttempt[#events.SufferAssassinationAttempt+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.CharacterMinisterialPosition("justice", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Executioner_Nasty", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Justice_Witness_2_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.CharacterMinisterialPosition("justice", context) and conditions.RandomPercentCampaign(17, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Justice_Witness", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Garden_Hermit_2_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.IsFactionLeader(context) and (conditions.CharacterBuildingConstructed("corn_great_royal_palace", context) or conditions.CharacterBuildingConstructed("sheep_great_royal_palace", context) or conditions.CharacterBuildingConstructed("wheat_great_royal_palace", context)) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Garden_Hermit", 50,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Secretary_Gobby_2_Trigger ]]--

events.CharacterCreated[#events.CharacterCreated+1] =
function (context)
	if conditions.CharacterType("minister", context) and not conditions.IsFactionLeader(context) and conditions.FactionLeadersTrait("C_Leader_Favourites", context) >= 1 and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Secretary_Gobby", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Secretary_Efficient_2_Trigger ]]--

events.CharacterCreated[#events.CharacterCreated+1] =
function (context)
	if conditions.CharacterType("minister", context) and not conditions.IsFactionLeader(context) and conditions.FactionLeadersTrait("C_Leader_Merit", context) >= 1 and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Secretary_Efficient", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Crimper_2_Trigger ]]--

events.CharacterCreated[#events.CharacterCreated+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.CharacterMinisterialPosition("army", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Crimper", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Cypher_2_Trigger ]]--

events.SpyingAttemptSuccess[#events.SpyingAttemptSuccess+1] =
function (context)
	if conditions.CharacterType("rake", context) and false then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Cypher", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Spymaster_2_Trigger ]]--

events.SpyingAttemptSuccess[#events.SpyingAttemptSuccess+1] =
function (context)
	if conditions.CharacterType("minister", context) and (conditions.IsFactionLeader(context) or conditions.CharacterMinisterialPosition("head_of_government", context)) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Spymaster", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Secret_Policeman_2_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and (conditions.IsFactionLeader(context) or conditions.CharacterMinisterialPosition("justice", context)) and conditions.InsurrectionCrushed(context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Secret_Policeman", 50,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Thieftaker_2_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.CharacterType("minister", context) and conditions.CharacterCultureType("european", context) and (conditions.IsFactionLeader(context) or conditions.CharacterMinisterialPosition("justice", context)) and conditions.CharacterAttribute("management", context) >= 3 and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Thieftaker", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_European_Turncoat_2_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterWonBattle(context) and conditions.CharacterType("General", context) and conditions.CharacterWasAttacker(context) and (conditions.CharacterCultureType("indian", context) or conditions.CharacterCultureType("tribal", context) or conditions.CharacterFactionName("ottomans", context)) and conditions.BattleResult("major_victory", context) and conditions.CharacterFoughtCulture("european", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_European_Turncoat", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_Galloper_2_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterWonBattle(context) and conditions.CharacterType("General", context) and conditions.CharacterWasAttacker(context) and conditions.CommanderFoughtInMelee(context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_Galloper", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Grizzly_Adams_2_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterWonBattle(context) and conditions.CharacterType("General", context) and conditions.CharacterWasAttacker(context) and conditions.CharacterInTheatre(1, context) and conditions.RandomPercentCampaign(17, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Grizzly_Adams", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Army_ADC_2_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterWonBattle(context) and conditions.CharacterType("General", context) and conditions.CharacterWasAttacker(context) and not conditions.CommanderFoughtInMelee(context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Army_ADC", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Duelling_Pistols_Manton_2_Trigger ]]--

events.DuelFought[#events.DuelFought+1] =
function (context)
	if conditions.CharacterWonDuel(context) and conditions.CharacterDuelWeapon("duelling_pistols", context) and conditions.CharacterFactionName("britain", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Duelling_Pistols_Manton", 8,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Duelling_Pistols_2_Trigger ]]--

events.DuelFought[#events.DuelFought+1] =
function (context)
	if conditions.CharacterWonDuel(context) and conditions.CharacterDuelWeapon("duelling_pistols", context) and not conditions.CharacterFactionName("britain", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Duelling_Pistols", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Duelling_Hidalgo_Fop_2_Trigger ]]--

events.DuelFought[#events.DuelFought+1] =
function (context)
	if conditions.CharacterWonDuel(context) and conditions.CharacterDuelWeapon("duelling_sword", context) and conditions.CharacterFactionName("spain", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Duelling_Hidalgo_Fop", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Duelling_Minx_2_Trigger ]]--

events.DuelFought[#events.DuelFought+1] =
function (context)
	if conditions.CharacterWonDuel(context) and conditions.CharacterInBuildingOfChain("happiness", context) and conditions.CharacterTrait("C_Feck_Vice", context) >= 1 and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Duelling_Minx", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Historian_2_Trigger ]]--

events.CharacterTurnEnd[#events.CharacterTurnEnd+1] =
function (context)
	if conditions.FactionDestroyedByCharacterFaction(context) and conditions.IsFactionLeader(context) and conditions.CharacterTrait("C_Leader_Dullard", context) < 1 and conditions.RandomPercentCampaign(17, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Historian", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Outstanding_Choirmaster_2_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.IsFactionLeader(context) and not conditions.CharacterTrait("C_Leader_Dullard", context) >= 1 and conditions.CharacterBuildingConstructed("grand_opera_house", context) and conditions.RandomPercentCampaign(17, context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Numismatist", 100,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Foodtaster_2_Trigger ]]--

events.SufferAssassinationAttempt[#events.SufferAssassinationAttempt+1] =
function (context)
	if (conditions.IsFactionLeader(context) or conditions.IsFactionLeaderFemale(context)) and conditions.CharacterAttribute("management", context) >= 3 and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Foodtaster", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Government_Guardian_2_Trigger ]]--

events.SufferAssassinationAttempt[#events.SufferAssassinationAttempt+1] =
function (context)
	if conditions.IsFactionLeader(context) and conditions.CharacterAttribute("management", context) <= 5 and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Government_Guardian", 17,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Boxer_2_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if not conditions.CharacterWonDuel(context) and (conditions.CharacterAttribute("duelling_pistols", context) <= 4 or conditions.CharacterAttribute("duelling_swords", context) <= 4) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Boxer", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancillary_Amazing_Wine_Cellar_2_Trigger ]]--

events.DummyEvent[#events.DummyEvent+1] =
function (context)
	if conditions.CharacterBuildingConstructed("winery", context) and conditions.CharacterType("minister", context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancillary_Amazing_Wine_Cellar", 33,  context)
		end
		return true
	end
	return false
end

--[[ Ancilllary_Dead_Parrot_Pirate_2_Trigger ]]--

events.CharacterCompletedBattle[#events.CharacterCompletedBattle+1] =
function (context)
	if conditions.CharacterType("admiral", context) and conditions.CharacterCultureType("european", context) and not conditions.CharacterWonBattle(context) and not conditions.CampaignName("episodic_1", context) and not conditions.CampaignName("episodic_3", context) and (conditions.CommanderAncillary("Ancilllary_Pet_Parrot_Nasty", context) or conditions.CommanderAncillary("Ancilllary_Pet_Parrot_Ordinary", context) or conditions.CommanderAncillary("Ancilllary_Pet_Parrot_Pirate", context)) then
		if conditions.DateInRange(1700, 1900, context) then 
			effect.ancillary("Ancilllary_Dead_Parrot_Pirate", 75,  context)
		end
		effect.remove_ancillary("Ancilllary_Pet_Parrot_Nasty", context)
		effect.remove_ancillary("Ancilllary_Pet_Parrot_Ordinary", context)
		effect.remove_ancillary("Ancilllary_Pet_Parrot_Pirate", context)
		return true
	end
	return false
end

