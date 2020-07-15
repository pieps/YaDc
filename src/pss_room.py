#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import discord
import inspect
import os
from typing import Callable, Dict, Iterable, List, Tuple, Union

from cache import PssCache
import pss_assert
import pss_core as core
import pss_entity as entity
import pss_item as item
import pss_lookups as lookups
import settings
import utility as util










# ---------- Constants ----------

ROOM_DESIGN_BASE_PATH = 'RoomService/ListRoomDesigns2?languageKey=en'
ROOM_DESIGN_KEY_NAME = 'RoomDesignId'
ROOM_DESIGN_DESCRIPTION_PROPERTY_NAME = 'RoomName'
ROOM_DESIGN_DESCRIPTION_PROPERTY_NAME_2 = 'RoomShortName'


ROOM_DESIGN_PURCHASE_BASE_PATH = 'RoomService/ListRoomDesignPurchase?languageKey=en'
ROOM_DESIGN_PURCHASE_KEY_NAME = 'RoomDesignPurchaseId'
ROOM_DESIGN_PURCHASE_DESCRIPTION_PROPERTY_NAME = 'RoomName'
ROOM_DESIGN_TYPE_PROPERTY_NAME = 'RoomType'


# RoomType: 'unit'
CAPACITY_PER_TICK_UNITS = {
    'Lift': ' pixel/s',
    'Radar': 's',
    'Stealth': 's'
}


# str: {str, str}
__DISPLAY_NAMES = {
    'ap_dmg': {
        'default': 'AP dmg'
    },
    'build_cost': {
        'default': 'Build cost'
    },
    'build_time': {
        'default': 'Build time'
    },
    'build_requirement': {
        'default': 'Build requirement'
    },
    'cap_per_tick': {
        'default': 'Cap per tick',
        'Lift': 'Speed',
        'Radar': 'Cloak reduction',
        'Stealth': 'Cloak duration'
    },
    'cooldown': {
        'default': 'Cooldown'
    },
    'construction_type': {
        'default': 'Construction type',
        'Storage': 'Storage type'
    },
    'crew_dmg': {
        'default': 'Crew dmg'
    },
    'emp_duration': {
        'default': 'EMP duration'
    },
    'enhanced_by': {
        'default': 'Enhanced by'
    },
    'gas_per_crew': {
        'default': 'Gas per crew'
    },
    'grid_types': {
        'default': 'Grid types'
    },
    'hull_dmg': {
        'default': 'Hull dmg'
    },
    'innate_armor': {
        'default': 'Innate armor',
        'Corridor': None
    },
    'manufacture_speed': {
        'default': 'Manufacture speed',
        'Recycling': None
    },
    'max_crew_blend': {
        'default': 'Max crew blend'
    },
    'max_power_used': {
        'default': 'Max power used'
    },
    'max_storage': {
        'default': 'Max storage',
        'AntiCraft': None,
        'Bedroom': 'Crew slots',
        'Command': 'Max AI lines',
        'Corridor': None,
        'Council': 'Borrow limit',
        'Engine': 'Dodge modifier',
        'Lift': None,
        'Medical': 'Crew HP healed',
        'Radar': None,
        'Shield': 'Shield points',
        'Stealth': None,
        'Training': None,
        'Trap': 'Crew dmg',
        'Wall': 'Armor value'
    },
    'min_hull_lvl': {
        'default': 'Min ship lvl'
    },
    'more_info': {
        'default': 'More info'
    },
    'power_generated': {
        'default': 'Power generated'
    },
    'queue_limit': {
        'default': 'Queue limit',
        'Council': 'Borrow limit',
        'Printer': None
    },
    'reload_speed': {
        'default': 'Reload speed'
    },
    'shield_dmg': {
        'default': 'Shield dmg'
    },
    'shots_fired': {
        'default': 'Shots fired'
    },
    'size': {
        'default': 'Size (WxH)'
    },
    'system_dmg': {
        'default': 'System dmg'
    },
    'wikia': {
        'default': 'Wikia'
    },
}










# ---------- Create EntityDesignDetails ----------

def __create_room_design_details_from_info(room_design_info: entity.EntityDesignInfo, rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData) -> entity.EntityDesignDetails:
    return entity.EntityDesignDetails(room_design_info, __properties['title'], __properties['description'], __properties['long'], __properties['short'], __properties['long'], rooms_designs_data, items_designs_data)


def __create_room_design_details_list_from_infos(rooms_designs_infos: List[entity.EntityDesignInfo], rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData) -> List[entity.EntityDesignDetails]:
    return [__create_room_design_details_from_info(room_design_info, rooms_designs_data, items_designs_data) for room_design_info in rooms_designs_infos]


def __create_rooms_designs_details_collection_from_infos(rooms_designs_infos: List[entity.EntityDesignInfo], rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData) -> entity.EntityDesignDetailsCollection:
    rooms_designs_details = __create_room_design_details_list_from_infos(rooms_designs_infos, rooms_designs_data, items_designs_data)
    result = entity.EntityDesignDetailsCollection(rooms_designs_details, big_set_threshold=3)
    return result










# ---------- Transformation functions ----------

def __convert_room_flags(room_info: entity.EntityDesignInfo, rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData, **kwargs) -> str:
    if __is_allowed_room_type(room_info, kwargs.get('allowed_room_types')):
        flags = room_info.get('Flags')
        if flags:
            result = []
            flags = int(flags)
            if result:
                return ', '.join(result)
            else:
                return None
        else:
            return None
    else:
        return None


def __get_build_cost(room_info: entity.EntityDesignInfo, rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData, **kwargs) -> str:
    if __is_allowed_room_type(room_info, kwargs.get('allowed_room_types')):
        price_string = room_info.get('PriceString')
        if price_string:
            resource_type, amount = price_string.split(':')
            cost = util.get_reduced_number_compact(amount)
            currency_emoji = lookups.CURRENCY_EMOJI_LOOKUP[resource_type.lower()]
            result = f'{cost} {currency_emoji}'
            return result
        else:
            return None
    else:
        return None


def __get_build_requirement(room_info: entity.EntityDesignInfo, rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData, **kwargs) -> str:
    if __is_allowed_room_type(room_info, kwargs.get('allowed_room_types')):
        requirement_string = room_info.get('RequirementString')
        if requirement_string:
            requirement_string = requirement_string.lower()
            required_type, required_id = requirement_string.split(':')

            if 'x' in required_id:
                required_id, required_amount = required_id.split('x')
            else:
                required_amount = '1'

            if required_type == 'item':
                item_info = items_designs_data[required_id]
                result = f'{required_amount}x {item_info[item.ITEM_DESIGN_DESCRIPTION_PROPERTY_NAME]}'
                return result
            else:
                return requirement_string
        else:
            return None
    else:
        return None


def __get_capacity_per_tick(room_info: entity.EntityDesignInfo, rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData, **kwargs) -> str:
    if __is_allowed_room_type(room_info, kwargs.get('allowed_room_types')):
        room_type = room_info.get(ROOM_DESIGN_TYPE_PROPERTY_NAME)
        capacity = room_info.get('Capacity')
        if capacity:
            cap_per_tick = util.convert_ticks_to_seconds(int(capacity))
            result = f'{util.format_up_to_decimals(cap_per_tick, 3)}{CAPACITY_PER_TICK_UNITS[room_type]}'
            return result
        else:
            return None
    else:
        return None


def __get_damage(room_info: entity.EntityDesignInfo, rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData, **kwargs) -> str:
    if __is_allowed_room_type(room_info, kwargs.get('allowed_room_types')):
        dmg = kwargs.get('entity_property')
        print_percent = kwargs.get('print_percent')
        reload_time = room_info.get('ReloadTime')
        max_power = room_info.get('MaxSystemPower')
        volley = room_info.get('MissileDesign.Volley')
        volley_delay = room_info.get('MissileDesign.VolleyDelay')
        result = __get_dmg_for_dmg_type(dmg, reload_time, max_power, volley, volley_delay, print_percent)
        return result
    else:
        return None


def __get_innate_armor(room_info: entity.EntityDesignInfo, rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData, **kwargs) -> str:
    if __is_allowed_room_type(room_info, kwargs.get('allowed_room_types')):
        default_defense_bonus = room_info.get('DefaultDefenceBonus')
        if default_defense_bonus and default_defense_bonus != '0':
            reduction = (1.0 - 1.0 / (1.0 + (float(default_defense_bonus) / 100.0))) * 100
            result = f'{default_defense_bonus} ({util.format_up_to_decimals(reduction, 2)}% dmg reduction)'
            return result
        else:
            return None
    else:
        return None


def __get_is_allowed_in_extension_grids(room_info: entity.EntityDesignInfo, rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData, **kwargs) -> str:
    if __is_allowed_room_type(room_info, kwargs.get('allowed_room_types')):
        supported_grid_types = int(room_info.get('SupportedGridTypes', '0'))
        if (supported_grid_types & 2) != 0:
            return 'Allowed in extension grids'
        else:
            return None
    else:
        return None


def __get_manufacture_rate(room_info: entity.EntityDesignInfo, rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData, **kwargs) -> str:
    if __is_allowed_room_type(room_info, kwargs.get('allowed_room_types')):
        manufacture_rate = room_info.get('ManufactureRate')
        if manufacture_rate:
            manufacture_rate = float(manufacture_rate)
            manufacture_speed = 1.0 / manufacture_rate
            manufacture_rate_per_hour = manufacture_rate * 3600
            result = f'{util.format_up_to_decimals(manufacture_speed)}s ({util.format_up_to_decimals(manufacture_rate_per_hour)}/hour)'
            return result
        else:
            return None
    else:
        return None


def __get_max_storage_and_type(room_info: entity.EntityDesignInfo, rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData, **kwargs) -> str:
    if __is_allowed_room_type(room_info, kwargs.get('allowed_room_types')):
        capacity = room_info.get('Capacity')
        manufacture_capacity = room_info.get('ManufactureCapacity')
        manufacture_rate = room_info.get('ManufactureRate')
        manufacture_type = room_info.get('ManufactureType')
        room_type = room_info.get(ROOM_DESIGN_TYPE_PROPERTY_NAME)
        if capacity and ((not manufacture_capacity or not manufacture_rate) or (room_type and room_type == 'Recycling')):
            value = __parse_value(capacity)
        elif manufacture_capacity and manufacture_rate:
            value = __parse_value(manufacture_capacity)
        else:
            value = None

        if value:
            print_type = (capacity and not manufacture_rate) or (manufacture_capacity and manufacture_rate)
            if print_type:
                construction_type = ''
                if manufacture_type:
                    lower = manufacture_type.lower()
                    if lower in lookups.CURRENCY_EMOJI_LOOKUP.keys():
                        construction_type = lookups.CURRENCY_EMOJI_LOOKUP[lower]
                    else:
                        construction_type = manufacture_type
                if construction_type:
                    return f'{value} {construction_type}'
                else:
                    return value
            else:
                return value
        else:
            return None
    else:
        return None


def __get_queue_limit(room_info: entity.EntityDesignInfo, rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData, **kwargs) -> str:
    if __is_allowed_room_type(room_info, kwargs.get('allowed_room_types')):
        manufacture_capacity = kwargs.get('ManufactureCapacity')
        manufacture_rate = kwargs.get('ManufactureRate')
        if manufacture_capacity and not manufacture_rate:
            return __parse_value(manufacture_capacity)
        else:
            return None
    else:
        return None


def __get_reload_time(room_info: entity.EntityDesignInfo, rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData, **kwargs) -> str:
    if __is_allowed_room_type(room_info, kwargs.get('allowed_room_types')):
        reload_time = room_info.get('ReloadTime')
        if reload_time:
            reload_ticks = float(reload_time)
            reload_seconds = reload_ticks / 40.0
            reload_speed = 60.0 / reload_seconds
            result = f'{reload_seconds:0.{settings.DEFAULT_FLOAT_PRECISION}f}s (~ {util.format_up_to_decimals(reload_speed)}/min)'
            return result
        else:
            return None
    else:
        return None


def __get_room_name(room_info: entity.EntityDesignInfo, rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData, **kwargs) -> str:
    room_name = room_info[ROOM_DESIGN_DESCRIPTION_PROPERTY_NAME]
    room_short_name = room_info[ROOM_DESIGN_DESCRIPTION_PROPERTY_NAME_2]
    if room_short_name:
        short_name = room_short_name.split(':')[0]
    else:
        short_name = None
    if short_name:
        result = f'{room_name} [{short_name}]'
    else:
        result = room_name
    return result


def __get_shots_fired(room_info: entity.EntityDesignInfo, rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData, **kwargs) -> str:
    if __is_allowed_room_type(room_info, kwargs.get('allowed_room_types')):
        volley = room_info.get('MissileDesign.Volley')
        volley_delay = room_info.get('MissileDesign.VolleyDelay')
        if volley and volley != '1':
            volley = int(volley)
            volley_delay = int(volley_delay)
            volley_delay_seconds = util.format_up_to_decimals(util.convert_ticks_to_seconds(volley_delay), 3)
            result = f'{volley:d} (Delay: {volley_delay_seconds}s)'
            return result
        else:
            return None
    else:
        return None


def __get_size(room_info: entity.EntityDesignInfo, rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData, **kwargs) -> str:
    if __is_allowed_room_type(room_info, kwargs.get('allowed_room_types')):
        columns = room_info.get('Columns')
        rows = room_info.get('Rows')
        if columns and rows:
            result = f'{columns}x{rows}'
            return result
        else:
            return None
    else:
        return None


def __get_value(room_info: entity.EntityDesignInfo, rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData, **kwargs) -> str:
    if __is_allowed_room_type(room_info, kwargs.get('allowed_room_types')):
        value = kwargs.get('entity_property')
        if value:
            max_decimal_count = kwargs.get('max_decimal_count', settings.DEFAULT_FLOAT_PRECISION)
            result = __parse_value(value, max_decimal_count)
            return result
        else:
            return None
    else:
        return None


def __get_value_as_duration(room_info: entity.EntityDesignInfo, rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData, **kwargs) -> str:
    if __is_allowed_room_type(room_info, kwargs.get('allowed_room_types')):
        value = kwargs.get('entity_property')
        if value:
            result = util.get_formatted_duration(int(value), include_relative_indicator=False)
            return result
        else:
            return None
    else:
        return None


def __get_value_as_seconds(room_info: entity.EntityDesignInfo, rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData, **kwargs) -> str:
    if __is_allowed_room_type(room_info, kwargs.get('allowed_room_types')):
        value = kwargs.get('entity_property')
        if value:
            value_seconds = util.convert_ticks_to_seconds(int(value))
            result = f'{util.format_up_to_decimals(value_seconds, 3)}s'
            return result
        else:
            return None
    else:
        return None


async def __get_wikia_link(room_info: entity.EntityDesignInfo, rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData, **kwargs) -> str:
    if __is_allowed_room_type(room_info, kwargs.get('allowed_room_types')):
        room_name = room_info.get(ROOM_DESIGN_DESCRIPTION_PROPERTY_NAME)
        if room_name:
            room_name = room_name.split(' Lv')[0]
            room_name = '_'.join([part.lower().capitalize() for part in room_name.split(' ')])
            result = await util.get_wikia_link(room_name)
            if await util.check_hyperlink(result):
                return f'<{result}>'
            else:
                return None
        else:
            return None
    else:
        return None


def __is_allowed_room_type(room_info: entity.EntityDesignInfo, allowed_room_types: Iterable) -> bool:
    room_type = room_info.get(ROOM_DESIGN_TYPE_PROPERTY_NAME)
    return (not allowed_room_types) or (room_type not in allowed_room_types)










# ---------- Helper functions ----------

def __get_dmg_for_dmg_type(dmg: str, reload_time: str, max_power: str, volley: str, volley_delay: str, print_percent: bool) -> str:
    """Returns base dps and dps per power"""
    if dmg:
        dmg = float(dmg)
        reload_time = int(reload_time)
        reload_seconds = util.convert_ticks_to_seconds(reload_time)
        max_power = int(max_power)
        volley = int(volley)
        if volley_delay:
            volley_delay = int(volley_delay)
        else:
            volley_delay = 0
        volley_duration_seconds = util.convert_ticks_to_seconds((volley - 1) * volley_delay)
        reload_seconds += volley_duration_seconds
        full_volley_dmg = dmg * float(volley)
        dps = full_volley_dmg / reload_seconds
        dps_per_power = dps / max_power
        if print_percent:
            percent = '%'
        else:
            percent = ''
        if volley > 1:
            single_volley_dmg = f'per shot: {util.format_up_to_decimals(dmg, 2)}, '
        else:
            single_volley_dmg = ''
        full_volley_dmg = util.format_up_to_decimals(full_volley_dmg, 2)
        dps = util.format_up_to_decimals(dps, 3)
        dps_per_power = util.format_up_to_decimals(dps_per_power, 3)
        result = f'{full_volley_dmg}{percent} ({single_volley_dmg}dps: {dps}{percent}, per power: {dps_per_power}{percent})'
        return result
    else:
        return None


def __get_parents(room_info: dict, rooms_designs_data: dict) -> list:
    parent_room_design_id = room_info['UpgradeFromRoomDesignId']
    if parent_room_design_id == '0':
        parent_room_design_id = None

    if parent_room_design_id is not None:
        parent_info = rooms_designs_data[parent_room_design_id]
        result = __get_parents(parent_info, rooms_designs_data)
        result.append(parent_info)
        return result
    else:
        return []


def __get_property_display_name(room_design_info: entity.EntityDesignInfo, rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData, **kwargs) -> str:
    display_name_key = kwargs.get('display_name_key')
    display_names = kwargs.get('display_names')
    room_type = room_design_info.get(ROOM_DESIGN_TYPE_PROPERTY_NAME)
    result = None
    if display_name_key and room_type:
        display_name = display_names.get(display_name_key, {})
        if display_name:
            result = display_names.get(room_type, display_names.get('default'))
        else:
            raise Exception(f'Get room property display name: Could not find a display name with the key \'{display_name_key}\'! Please contact the author about this.')
    return result


def __parse_value(value: str, max_decimal_count: int = settings.DEFAULT_FLOAT_PRECISION) -> str:
    if value and value.lower() != 'none':
        try:
            i = float(value)
            if i:
                return util.get_reduced_number_compact(i, max_decimal_count=max_decimal_count)
            else:
                return None
        except:
            pass

        return value
    else:
        return None










# ---------- Room info ----------

def get_room_design_details_by_id(room_design_id: str, rooms_designs_data: entity.EntitiesDesignsData, items_designs_data: entity.EntitiesDesignsData) -> entity.EntityDesignDetails:
    if room_design_id and room_design_id in rooms_designs_data:
        result = __create_room_design_details_from_info(rooms_designs_data[room_design_id], rooms_designs_data, items_designs_data)
    else:
        result = None
    return result


async def get_room_details_by_name(room_name: str, as_embed: bool = settings.USE_EMBEDS) -> Union[List[str], discord.Embed]:
    pss_assert.valid_entity_name(room_name, allowed_values=__allowed_room_names)

    rooms_designs_data = await rooms_designs_retriever.get_data_dict3()
    rooms_designs_infos = await rooms_designs_retriever.get_entities_designs_infos_by_name(room_name, entities_designs_data=rooms_designs_data)

    if not rooms_designs_infos:
        return [f'Could not find a room named **{room_name}**.'], False
    else:
        items_designs_data = await item.items_designs_retriever.get_data_dict3()
        rooms_designs_details_collection = __create_rooms_designs_details_collection_from_infos(rooms_designs_infos, rooms_designs_data, items_designs_data)
        if as_embed:
            return await rooms_designs_details_collection.get_entity_details_as_embed(), True
        else:
            return await rooms_designs_details_collection.get_entity_details_as_text(), True


def _get_key_for_room_sort(room_info: dict, rooms_designs_data: dict) -> str:
    result = ''
    parent_infos = __get_parents(room_info, rooms_designs_data)
    if parent_infos:
        for parent_info in parent_infos:
            result += parent_info[ROOM_DESIGN_KEY_NAME].zfill(4)
    result += room_info[ROOM_DESIGN_KEY_NAME].zfill(4)
    return result










# ---------- Initilization ----------

rooms_designs_retriever: entity.EntityDesignsRetriever
rooms_designs_purchases_retriever: entity.EntityDesignsRetriever
__allowed_room_names: List[str]
__display_name_properties: Dict[str, entity.EntityDesignDetailProperty]
__properties: Dict[str, entity.EntityDesignDetailProperty]


async def init():
    global rooms_designs_retriever
    global rooms_designs_purchases_retriever
    rooms_designs_retriever = entity.EntityDesignsRetriever(
        ROOM_DESIGN_BASE_PATH,
        ROOM_DESIGN_KEY_NAME,
        ROOM_DESIGN_DESCRIPTION_PROPERTY_NAME,
        cache_name='RoomDesigns',
        sorted_key_function=_get_key_for_room_sort
    )
    rooms_designs_purchases_retriever = entity.EntityDesignsRetriever(
        ROOM_DESIGN_PURCHASE_BASE_PATH,
        ROOM_DESIGN_PURCHASE_KEY_NAME,
        ROOM_DESIGN_PURCHASE_DESCRIPTION_PROPERTY_NAME,
        cache_name='RoomDesignPurchases'
    )

    global __allowed_room_names
    rooms_designs_data = await rooms_designs_retriever.get_data_dict3()
    __allowed_room_names = sorted(__get_allowed_room_short_names(rooms_designs_data))

    global __display_name_properties
    __display_name_properties = __create_display_name_properties(__DISPLAY_NAMES)

    global __properties
    __properties = {
        'title': entity.EntityDesignDetailProperty('Room name', False, omit_if_none=False, transform_function=__get_room_name),
        'description': entity.EntityDesignDetailProperty('Description', False, omit_if_none=False, entity_property_name='RoomDescription'),
        'long': [
            entity.EntityDesignDetailProperty(__display_name_properties['size'], True, transform_function=__get_size),
            entity.EntityDesignDetailProperty(__display_name_properties['max_power_used'], True, entity_property_name='MaxSystemPower', transform_function=__get_value),
            entity.EntityDesignDetailProperty(__display_name_properties['power_generated'], True, entity_property_name='MaxPowerGenerated', transform_function=__get_value),
            entity.EntityDesignDetailProperty(__display_name_properties['innate_armor'], True, transform_function=__get_innate_armor),
            entity.EntityDesignDetailProperty(__display_name_properties['enhanced_by'], True, entity_property_name='EnhancementType', transform_function=__get_value),
            entity.EntityDesignDetailProperty(__display_name_properties['min_hull_lvl'], True, entity_property_name='MinShipLevel', transform_function=__get_value),
            entity.EntityDesignDetailProperty(__display_name_properties['reload_speed'], True, transform_function=__get_reload_time),
            entity.EntityDesignDetailProperty(__display_name_properties['shots_fired'], True, transform_function=__get_shots_fired),
            entity.EntityDesignDetailProperty(__display_name_properties['system_dmg'], True, entity_property_name='MissileDesign.SystemDamage', transform_function=__get_damage, print_percent=False),
            entity.EntityDesignDetailProperty(__display_name_properties['shield_dmg'], True, entity_property_name='MissileDesign.ShieldDamage', transform_function=__get_damage, print_percent=False),
            entity.EntityDesignDetailProperty(__display_name_properties['crew_dmg'], True, entity_property_name='MissileDesign.CharacterDamage', transform_function=__get_damage, print_percent=False),
            entity.EntityDesignDetailProperty(__display_name_properties['hull_dmg'], True, entity_property_name='MissileDesign.HullDamage', transform_function=__get_damage, print_percent=False),
            entity.EntityDesignDetailProperty(__display_name_properties['ap_dmg'], True, entity_property_name='MissileDesign.DirectSystemDamage', transform_function=__get_damage, print_percent=False),
            entity.EntityDesignDetailProperty(__display_name_properties['emp_duration'], True, entity_property_name='MissileDesign.EMPLength', transform_function=__get_value_as_seconds),
            entity.EntityDesignDetailProperty(__display_name_properties['max_storage'], True, transform_function=__get_max_storage_and_type),
            entity.EntityDesignDetailProperty(__display_name_properties['cap_per_tick'], True, transform_function=__get_capacity_per_tick, allowed_room_types=CAPACITY_PER_TICK_UNITS.keys()),
            entity.EntityDesignDetailProperty(__display_name_properties['cooldown'], True, entity_property_name='Cooldown', transform_function=__get_value_as_seconds),
            entity.EntityDesignDetailProperty(__display_name_properties['queue_limit'], True, transform_function=__get_queue_limit),
            entity.EntityDesignDetailProperty(__display_name_properties['manufacture_speed'], True, transform_function=__get_manufacture_rate),
            entity.EntityDesignDetailProperty(__display_name_properties['gas_per_crew'], True, entity_property_name='ManufactureRate', transform_function=__get_value, allowed_room_types=['Recycling']),
            entity.EntityDesignDetailProperty(__display_name_properties['max_crew_blend'], True, entity_property_name='ManufactureCapacity', transform_function=__get_value, allowed_room_types=['Recycling']),
            entity.EntityDesignDetailProperty(__display_name_properties['build_time'], True, entity_property_name='ConstructionTime', transform_function=__get_value_as_duration),
            entity.EntityDesignDetailProperty(__display_name_properties['build_cost'], True, transform_function=__get_build_cost),
            entity.EntityDesignDetailProperty(__display_name_properties['build_requirement'], True, transform_function=__get_build_requirement),
            entity.EntityDesignDetailProperty(__display_name_properties['grid_types'], True, transform_function=__get_is_allowed_in_extension_grids),
            entity.EntityDesignDetailProperty(__display_name_properties['more_info'], True, transform_function=__convert_room_flags),
            entity.EntityDesignDetailProperty(__display_name_properties['wikia'], True, transform_function=__get_wikia_link),
        ],
        'short': [
            entity.EntityDesignDetailProperty('Enhanced by', True, entity_property_name='EnhancementType', transform_function=__get_value),
            entity.EntityDesignDetailProperty('Ship lvl', True, entity_property_name='MinShipLevel', transform_function=__get_value),
        ]
    }


def __create_display_name_properties(display_names: List[str]) -> Dict[str, entity.EntityDesignDetailProperty]:
    result = {key: __create_display_name_property(key, display_names) for key in display_names.keys()}
    return result


def __create_display_name_property(display_name_key: str, display_names: Dict[str, Dict[str, str]]) -> entity.EntityDesignDetailProperty:
    result = entity.EntityDesignDetailProperty('', False, transform_function=__get_property_display_name, display_name_key=display_name_key, display_names=display_names)
    return result


def __get_allowed_room_short_names(rooms_designs_data: dict):
    result = []
    for room_design_data in rooms_designs_data.values():
        if room_design_data[ROOM_DESIGN_DESCRIPTION_PROPERTY_NAME_2]:
            room_short_name = room_design_data[ROOM_DESIGN_DESCRIPTION_PROPERTY_NAME_2].split(':')[0]
            if room_short_name not in result:
                result.append(room_short_name)
    return result










# ---------- Testing ----------

#if __name__ == '__main__':
#    test_rooms = ['ion']
#    for room_name in test_rooms:
#        os.system('clear')
#        result = await get_room_details_from_name(room_name, as_embed=False)
#        for line in result[0]:
#            print(line)
#        result = ''