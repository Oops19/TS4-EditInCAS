#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#
import re
from typing import Any

from edit_in_cas.modinfo import ModInfo
from edit_in_cas.persistent_store import PersistentStore
from edit_in_cas.sim_picker import SimPicker
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

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
        ModInfo.get_identity(), 'o19.edit_in_cas.filterx', "Description ...", ('o19.eicas.fx', ),
        command_arguments=(
                CommonConsoleCommandArgument('flags', 'int', 'The filter pattern', is_optional=True, default_value='1'),
        )
    )
    def o19_cheat_edit_in_cas_filter_1(output: CommonConsoleCommandOutput, flags: str = '1'):
        try:
            if re.match(r'0b[01_]*[01]$', flags):
                _flags = int(flags, 2)
            elif re.match(r'0x[0-9A-F_]*[0-9A-F]$', flags):
                _flags = int(flags, 16)
            else:
                _flags = int(flags)
            PersistentStore().set_filter(_flags)
            output(f"Filter set to 0b{flags:034_b} / 0x{flags:012X} / {flags}")
        except Exception as e:
            output(f"Error {e}")
        output(f"OK")

    @staticmethod
    @CommonConsoleCommand(
        ModInfo.get_identity(), 'o19.edit_in_cas.filter', "Description ...", ('o19.eicas.f', ),
        command_arguments=(
                CommonConsoleCommandArgument('flags', 'int', 'The filter pattern', is_optional=True, default_value='1'),
        )
    )
    def o19_cheat_edit_in_cas_filter_1(output: CommonConsoleCommandOutput, flags: int = 1):
        try:
            if re.match(r'0b[01_]*[01]$', str(flags)):
                _flags = int(str(flags), 2)
            elif re.match(r'0x[0-9A-F_]*[0-9A-F]$', str(flags)):
                _flags = int(str(flags), 16)
            else:
                _flags = flags
            PersistentStore().set_filter(_flags)
            output(f"Filter set to 0b{flags:034_b} / 0x{flags:012X} / {flags}")
        except Exception as e:
            output(f"Error {e}")
        output(f"OK")


Main()
