from random import randint, uniform
from database.world.WorldDatabaseManager import WorldDatabaseManager
from game.world.managers.objects.LootManager import LootManager, LootHolder
from game.world.managers.objects.item.ItemManager import ItemManager
from utils.constants.ObjectCodes import LootTypes


class CreatureLootManager(LootManager):
    def __init__(self, creature_mgr):
        super(CreatureLootManager, self).__init__(creature_mgr)

    # override
    def generate_loot(self):
        # TODO: Implement loot group handling
        money = randint(self.world_obj.creature_template.gold_min, self.world_obj.creature_template.gold_max)
        self.current_money = money

        for loot_item in self.loot_template:
            chance = float(round(uniform(0.0, 1.0), 2) * 100)
            item_template = WorldDatabaseManager.item_template_get_by_entry(loot_item.item)
            if item_template:
                item_chance = loot_item.ChanceOrQuestChance
                item_chance = item_chance if item_chance > 0 else item_chance * -1

                if item_chance >= 100 or chance - item_chance < 0:
                    item = ItemManager.generate_item_from_entry(item_template.entry)
                    if item:
                        self.current_loot.append(LootHolder(item, randint(loot_item.mincountOrRef, loot_item.maxcount)))

    # override
    def populate_loot_template(self):
        return WorldDatabaseManager.CreatureLootTemplateHolder\
            .creature_loot_template_get_by_creature(self.world_obj.entry)

    # override
    def get_loot_type(self, player, victim):
        loot_type = LootTypes.LOOT_TYPE_NOTALLOWED

        # killed_by is None or looter is the actual killer, allow.
        if not victim.killed_by or victim.killed_by == player:
            loot_type = LootTypes.LOOT_TYPE_CORPSE

        # Looter is part of the killer_by player party, allow.
        elif victim.killed_by.group_manager and victim.killed_by.group_manager.is_party_member(player):
            loot_type = LootTypes.LOOT_TYPE_CORPSE

        return loot_type
