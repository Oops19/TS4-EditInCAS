#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#
import re

from edit_in_cas.copy_sims import CopySims
from edit_in_cas.enums.transfer import Transfer
from edit_in_cas.modinfo import ModInfo
from edit_in_cas.persistent_store import PersistentStore
from edit_in_cas.transfer_tools import TransferTools
from objects.components.consumable_component import ConsumableComponent
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand, CommonConsoleCommandArgument
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_spawn_utils import CommonSimSpawnUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_species_utils import CommonSpeciesUtils

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'TestClone')
log.enable()


class TestClone:

    @staticmethod
    @CommonConsoleCommand(
        ModInfo.get_identity(), 'o19.edit_in_cas.test_transfer', "Class to test cloning of sims.", ('o19.eicas.tt', ),
          command_arguments=(
                  CommonConsoleCommandArgument('flags', 'string', 'The filter pattern', is_optional=True, default_value=None),
          )
      )
    def o19_cheat_edit_in_cas_clone_flags(output: CommonConsoleCommandOutput, _flags: str = None):
        output(f"Test cloning of active sim")
        try:
            if _flags is not None:
                flags = -1
                if isinstance(_flags, int):
                    flags = _flags
                else:
                    if re.match(r'0b[01_]*[01]$', _flags):
                        flags = int(_flags, 2)
                    elif re.match(r'0x[0-9A-F_]*[0-9A-F]$', _flags, re.RegexFlag.IGNORECASE):
                        flags = int(_flags, 16)
                if flags == -1:
                    flags = Transfer.BODY_PARTS.value
            else:
                ps = PersistentStore()
                flags = ps.get_include_filter()
                flags = flags & (ps.get_exclude_filter() ^ Transfer.ALL.value)

            s_flags = Transfer.transfer_bits_as_string(flags)
            output(f"Flags: '{s_flags}'")

            src_sim_info = CommonSimUtils.get_active_sim_info()
            _is_src_sim_info = CopySims()._make_sim_instance(src_sim_info)
            _src_species = CommonSpeciesUtils.get_species(src_sim_info)
            new_sim_info = CommonSimSpawnUtils.create_sim_info(species=_src_species)
            # set flags Age, Gender, Name for this:
            # new_sim_info = CommonSimSpawnUtils.create_sim_info(species=CommonSpeciesUtils.get_species(src_sim_info), age=src_sim_info.age, gender=src_sim_info.gender, first_name=src_sim_info.first_name, last_name=src_sim_info.last_name)
            _is_new_sim_info = CopySims()._make_sim_instance(new_sim_info)
            output(f"is_src_sim_info={_is_src_sim_info}; is_new_sim_info={_is_new_sim_info}; species={_src_species}")
            if CommonHouseholdUtils.has_free_household_slots(src_sim_info):
                CommonHouseholdUtils.move_sim_to_household(new_sim_info, CommonHouseholdUtils.get_household(src_sim_info).id)
            TransferTools().clone_sim(src_sim_info, new_sim_info, flags)
            new_sim_info.first_name = f"{src_sim_info.first_name[:3]}©{new_sim_info.first_name}"
            new_sim_info.last_name = f"{src_sim_info.last_name[:3]}©{new_sim_info.last_name}"

        except Exception as e:
            output(f"Error {e}")
        output(f"OK")


TestClone()
