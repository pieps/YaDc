#!/usr/bin/env python
# -*- coding: UTF-8 -*-

COLLECTION_PERK_LOOKUP = {
    'BloodThirstSkill': 'Vampirism',
    'EmpSkill': 'EMP Discharge',
    'FreezeAttackSkill': 'Cryo Field',
    'InstantKillSkill': 'Headshot',
    'MedicalSkill': 'Combat Medic',
    'ResurrectSkill': 'Resurrection',
    'SharpShooterSkill': 'Sharpshooter'
}


EQUIPMENT_MASK_LOOKUP = {
    1: 'head',
    2: 'body',
    4: 'leg',
    8: 'weapon',
    16: 'accessory'}


GAS_COSTS_LEGENDARY_LOOKUP = [
    0, 130000, 162500, 195000, 227500,
    260000, 292500, 325000, 357500, 390000,
	422500, 455000, 487500, 520000, 552500,
	585000, 617500, 650000, 682500, 715000,
	747500, 780000, 812500, 845000, 877500,
	910000, 942000, 975000, 1007500, 1040000,
	1072500, 1105000, 1137500, 1170000, 1202500,
	1235000, 1267500, 1300000, 1332500, 1365000]


GAS_COSTS_LOOKUP = [
    0, 0, 17, 33, 65,
    130, 325, 650, 1300, 3200,
    6500, 9700, 13000, 19500, 26000,
    35700, 43800, 52000, 61700, 71500,
    84500, 104000, 117000, 130000, 156000,
    175000, 201000, 227000, 253000, 279000,
    312000, 351000, 383000, 422000, 468000,
    507000, 552000, 604000, 650000, 715000]


SPECIAL_ABILITIES_LOOKUP = {
    'AddReload': 'Rush Command',
    'DamageToCurrentEnemy': 'Critical Strike',
    'DamageToRoom': 'Ultra Dismantle',
    'DamageToSameRoomCharacters': 'Poison Gas',
    'DeductReload': 'System Hack',
    'FireWalk': 'Fire Walk',
    'Freeze': 'Freeze',
    'HealRoomHp': 'Urgent Repair',
    'HealSameRoomCharacters': 'Healing Rain',
    'HealSelfHp': 'First Aid',
    'SetFire': 'Arson'}


XP_COSTS_LEGENDARY_LOOKUP = [
    0, 0, 810, 1350, 1890,
	2430, 3060, 3690, 4320, 4950,
	5580, 6360, 7090, 7840, 8610,
	9400, 10210, 11040, 11890, 12760,
	13650, 14560, 15490, 16440, 17410,
	18400, 19410, 20440, 21490, 24660,
	23650, 24760, 25890, 27040, 28210,
	29400, 30610, 31840, 33090, 34360]


XP_COSTS_LOOKUP = [
    0, 90, 270, 450, 630,
	810, 1020, 1230, 1440, 1650,
	1860, 2130, 2400, 2670, 2940,
	3210, 3540, 3870, 4200, 4530,
	4860, 5220, 5580, 5940, 6300,
	6660, 7050, 7440, 7830, 8220,
	8610, 9030, 9450, 9870, 10290,
	10710, 11160, 11610, 12060, 12510]