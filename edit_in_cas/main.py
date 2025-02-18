#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#
import re

from edit_in_cas.enums.transfer import Transfer
from edit_in_cas.modinfo import ModInfo
from edit_in_cas.persistent_store import PersistentStore
from edit_in_cas.sim_picker import SimPicker
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'Main')
log.enable()
log.debug(f"Thank you for using {ModInfo.get_identity().name}!")


class Main:
    initialized = False

    def __init__(self):
        if Main.initialized:
            return
        Main.initialized = True

    def do_it(self):
        SimPicker().show_sim_picker_dialog('Edit Sims in CAS', 'Select 1-8 sims. 1 TYAE sim is required to exit CAS.')

    @staticmethod
    @CommonConsoleCommand(ModInfo.get_identity(), 'o19.edit_in_cas', "Description ...", ('o19.eicas', ))
    def o19_cheat_edit_in_cas(output: CommonConsoleCommandOutput):
        try:
            Main().do_it()
        except Exception as e:
            output(f"Error {e}")
        output(f"OK")

    @staticmethod
    @CommonConsoleCommand(
        ModInfo.get_identity(), 'o19.edit_in_cas.include', "Description ...", ('o19.eicas.i', ),
        command_arguments=(
                CommonConsoleCommandArgument('flags', 'string', 'The filter pattern', is_optional=True, default_value=None),
        )
    )
    def o19_cheat_edit_in_cas_include(output: CommonConsoleCommandOutput, _flags: str = None):
        try:
            flags = Transfer.BODY_PARTS.value
            if isinstance(_flags, int):
                flags = _flags
            elif isinstance(_flags, str):
                if re.match(r'0b[01_]*[01]$', _flags):
                    flags = int(_flags, 2)
                elif re.match(r'0x[0-9A-F_]*[0-9A-F]$', _flags, re.RegexFlag.IGNORECASE):
                    flags = int(_flags, 16)

            PersistentStore().set_include_filter(flags)
            output(f"Include filter set to 0b{flags:049_b} / 0x{flags:012_X} / {flags}")  # 0b: 40 + 9x_; 0x: 10 + 2x_
            log.debug(f"Include filter set to 0b{flags:049_b} / 0x{flags:012_X} / {flags}")

            s_flags = Transfer.transfer_bits_as_string(flags)
            output(f"Flags: {s_flags}")
            log.debug(f"\tFlags: {s_flags}")
        except Exception as e:
            output(f"Error {e}")

    @staticmethod
    @CommonConsoleCommand(
        ModInfo.get_identity(), 'o19.edit_in_cas.exclude', "Description ...", ('o19.eicas.e', ),
        command_arguments=(
                CommonConsoleCommandArgument('flags', 'string', 'The filter pattern', is_optional=True, default_value=None),
        )
    )
    def o19_cheat_edit_in_cas_exclude(output: CommonConsoleCommandOutput, _flags: str = None):
        try:
            flags = Transfer.BUFFS.value | Transfer.HOUSEHOLD_RELATIONSHIPS.value
            if isinstance(_flags, int):
                flags = _flags
            elif isinstance(_flags, str):
                if re.match(r'0b[01_]*[01]$', _flags):
                    flags = int(_flags, 2)
                elif re.match(r'0x[0-9A-F_]*[0-9A-F]$', _flags, re.RegexFlag.IGNORECASE):
                    flags = int(_flags, 16)

            PersistentStore().set_exclude_filter(flags)
            output(f"Exclude filter set to 0b{flags:049_b} / 0x{flags:012_X} / {flags}")  # 0b: 40 + 9x_; 0x: 10 + 2x_
            log.debug(f"Exclude filter set to 0b{flags:049_b} / 0x{flags:012_X} / {flags}")

            s_flags = Transfer.transfer_bits_as_string(flags)
            output(f"Flags: {s_flags}")
            log.debug(f"\tFlags: {s_flags}")
        except Exception as e:
            output(f"Error {e}")


Main()
