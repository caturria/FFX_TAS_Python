import logging
from enum import IntEnum
from typing import List

import memory
import xbox

logger = logging.getLogger(__name__)


class PlayerMagicNumbers(IntEnum):
    CHAR_STRUCT_SIZE = 0x94
    CHAR_STAT_POINTER = 0x003AB9B0
    BATTLE_STRUCT_SIZE = 0x90
    BATTLE_STATE_STRUCT_SIZE = 0xF90
    BATTLE_STATE_STRUCT_POINTER = 0x00D334CC
    CUR_HP = 0x00D32078
    MAX_HP = 0x00D32080
    BATTLE_CUR_HP = 0x00F3F7A4
    BATTLE_MAX_HP = 0x00F3F7A8
    LUCK = 0x34
    ACCURACY = 0x36
    BATTLE_OVERDRIVE = 0x5BC
    OVERDRIVE = 0x39
    AFFECTION_POINTER = 0x00D2CABC
    SLVL = 0x00D32097
    RNG_COMP = 0x7FFFFFFF
    ESCAPED = 0xDC8
    ACTIVE_BATTLE_SLOTS = 0x00F3F76C
    BACKLINE_BATTLE_SLOTS = 0x00D2C8A3
    ARMOR_ID = 1
    WEAPON_ID = 0


class Player:
    def __init__(self, name: str, id: int, battle_menu: List[int]):
        self.name = name
        self.id = id
        self.struct_offset = id * PlayerMagicNumbers.CHAR_STRUCT_SIZE
        self.char_rng = 20 + id
        self.battle_menu = battle_menu

    def __eq__(self, other):
        if isinstance(other, int):
            return self.id == other
        else:
            return self.id == other.id

    def __lt__(self, other):
        if isinstance(other, int):
            return self.id < other
        else:
            return self.id < other.id

    def __gt__(self, other):
        return not self == other and not self < other

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other

    def __ne__(self, other):
        return not self == other

    def __str__(self) -> str:
        return self.name

    def _read_char_offset_address(self, address):
        return memory.main.read_val(address + self.struct_offset)

    def _read_char_battle_offset_address(self, address, offset):
        return memory.main.read_val(
            address + ((PlayerMagicNumbers.BATTLE_STRUCT_SIZE * offset))
        )

    def _read_char_battle_state_address(self, offset):
        pointer = memory.main.read_val(
            PlayerMagicNumbers.BATTLE_STATE_STRUCT_POINTER, 4
        )
        new_offset = (PlayerMagicNumbers.BATTLE_STATE_STRUCT_SIZE * self.id) + offset
        return memory.main.read_val(pointer + new_offset, 1, find_base=False)

    def _read_char_stat_offset_address(self, address):
        pointer = memory.main.read_val(PlayerMagicNumbers.CHAR_STAT_POINTER, 4)
        return memory.main.read_val(
            pointer + self.struct_offset + address, 1, find_base=False
        )

    def navigate_to_battle_menu(self, target):
        """Different characters have different menu orders."""
        current_position = memory.main.battle_menu_cursor()
        while current_position == 255:
            current_position = memory.main.battle_menu_cursor()
        target_position = self.battle_menu.index(target)
        while current_position != target:
            if current_position == 255:
                pass
            elif self.battle_menu.index(current_position) > target_position:
                xbox.tap_up()
            else:
                xbox.tap_down()
            current_position = memory.main.battle_menu_cursor()

    def luck(self) -> int:
        return self._read_char_stat_offset_address(PlayerMagicNumbers.LUCK)

    def accuracy(self) -> int:
        return self._read_char_stat_offset_address(PlayerMagicNumbers.ACCURACY)

    def affection(self) -> int:
        if self.id == 0:
            return 255
        return memory.main.read_val(
            PlayerMagicNumbers.AFFECTION_POINTER + ((4 * self.id)), 1
        )

    def next_crits(self, enemy_luck: int, length: int = 20) -> List[int]:
        """Note that this says the number of increments, so the previous roll will be a hit, and this one will be the crit."""
        results = []
        cur_rng = memory.main.rng_from_index(self.char_rng)
        cur_rng = memory.main.roll_next_rng(cur_rng, self.char_rng)
        cur_rng = memory.main.roll_next_rng(cur_rng, self.char_rng)
        index = 2
        while len(results) < length:
            crit_roll = memory.main.s32(cur_rng & PlayerMagicNumbers.RNG_COMP) % 101
            crit_chance = self.luck() - enemy_luck
            if crit_roll < crit_chance:
                results.append(index)
                index += 1
            cur_rng = memory.main.roll_next_rng(cur_rng, self.char_rng)
        return results

    def next_crit(self, enemy_luck) -> int:
        return self.next_crits(enemy_luck, length=1)[0]

    def overdrive(self, *args, **kwargs):
        raise NotImplementedError()

    def overdrive_active(self):
        raise NotImplementedError()

    def overdrive_percent(self, combat=False) -> int:
        if combat:
            return self._read_char_battle_state_address(
                PlayerMagicNumbers.BATTLE_OVERDRIVE
            )
        else:
            return self._read_char_stat_offset_address(PlayerMagicNumbers.OVERDRIVE)

    def has_overdrive(self, combat=False) -> bool:
        return self.overdrive_percent(combat=combat) == 100

    def is_turn(self) -> bool:
        return memory.main.get_battle_char_turn() == self.id

    def in_danger(self, danger_threshold, combat=False) -> bool:
        return self.hp(combat) <= danger_threshold

    def is_dead(self) -> bool:
        return memory.main.state_dead(self.id)

    def is_status_ok(self) -> bool:
        if not self.active():
            return True
        return not any(
            func(self.id)
            for func in [
                memory.main.state_petrified,
                memory.main.state_confused,
                memory.main.state_dead,
                memory.main.state_berserk,
                memory.main.state_sleep,
            ]
        )

    def escaped(self) -> bool:
        return self._read_char_battle_state_address(PlayerMagicNumbers.ESCAPED)

    def hp(self, combat=False) -> int:
        if not combat:
            return self._read_char_offset_address(PlayerMagicNumbers.CUR_HP)
        else:
            return self._read_char_battle_offset_address(
                PlayerMagicNumbers.BATTLE_CUR_HP, self.battle_slot()
            )

    def max_hp(self, combat=False) -> int:
        if not combat:
            return self._read_char_offset_address(PlayerMagicNumbers.MAX_HP)
        else:
            return self._read_char_battle_offset_address(
                PlayerMagicNumbers.BATTLE_MAX_HP, self.battle_slot()
            )

    def active(self) -> bool:
        return self in memory.main.get_active_battle_formation()

    def battle_slot(self) -> int:
        for i in range(0, 3):
            if (
                memory.main.read_val(PlayerMagicNumbers.ACTIVE_BATTLE_SLOTS + (2 * i))
                == self.id
            ):
                return i

        offset = 0
        for i in range(0, 7):
            val = memory.main.read_val(PlayerMagicNumbers.BACKLINE_BATTLE_SLOTS + i)
            if val == 255:
                offset += 1
                continue
            elif val == self.id:
                return i + 3 - offset
        return 255

    def formation_slot(self) -> int:
        try:
            return memory.main.get_order_seven().index(self.id)
        except Exception:
            return 255

    def slvl(self) -> int:
        return self._read_char_offset_address(PlayerMagicNumbers.SLVL)

    def armors(self) -> List[memory.main.Equipment]:
        equipments = memory.main.all_equipment()
        return [
            x
            for x in equipments
            if (
                x.owner() == self.id
                and x.equipment_type() == PlayerMagicNumbers.ARMOR_ID
            )
        ]

    def equipped_armor(self) -> memory.main.Equipment:
        return [x for x in self.armors() if x.is_equipped()][0]

    def weapons(self) -> List[memory.main.Equipment]:
        equipments = memory.main.all_equipment()
        return [
            x
            for x in equipments
            if (
                x.owner() == self.id
                and x.equipment_type() == PlayerMagicNumbers.WEAPON_ID
            )
        ]

    def equipped_weapon(self) -> memory.main.Equipment:
        return [x for x in self.weapons() if x.is_equipped()][0]

    def main_menu_index(self) -> int:
        return memory.main.get_character_index_in_main_menu(self.id)