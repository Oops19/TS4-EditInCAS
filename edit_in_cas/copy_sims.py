#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


import time
from typing import Tuple, Dict, Union, List

import distributor
import services
import sims4
import sims4.commands
from clock import ClockSpeedMode
from distributor.ops import SwitchActiveHouseholdControl
from distributor.system import Distributor
from edit_in_cas.enums.stage import Stage
from edit_in_cas.enums.transfer import Transfer
from edit_in_cas.modinfo import ModInfo
from edit_in_cas.persistent_store import PersistentStore
from edit_in_cas.transfer_tools import TransferTools
from objects import ALL_HIDDEN_REASONS, HiddenReasonFlag
from routing.walkstyle.walkstyle_request import WalkStyleRequest
from sims.household import Household
from sims.outfits.outfit_enums import OutfitCategory
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from sims.sim_spawner import SimSpawner
from sims4communitylib.enums.tags_enum import CommonGameTag
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.interval.common_interval_event_service import CommonIntervalEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from sims4communitylib.utils.common_time_utils import CommonTimeUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
from sims4communitylib.utils.sims.common_sim_spawn_utils import CommonSimSpawnUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from ts4lib.custom_enums.custom_outfit_category import CustomOutfitCategory
from ts4lib.utils.outfit_utilities import OutfitUtilities
from ts4lib.utils.simple_ui_notification import SimpleUINotification
from ui.ui_dialog_notification import UiDialogNotification

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'CopySims')
log.enable()


class CopySims:

    def _clone_sim_into_new_household(self, sim_info: SimInfo, target_household: Household) -> SimInfo:
        """
        Clone a sim and return SimInfo of new sim
        @param sim_info: Sim to copy
        @param target_household: Household to paste to
        @return: SimInfo of new sim
        """

        # new_sim_info = CommonSimSpawnUtils.clone_sim(sim_info, add_to_household=False)  # breaks the sim
        new_sim_info = CommonSimSpawnUtils.create_human_sim_info(age=sim_info.age, gender=sim_info.gender, first_name=sim_info.first_name, last_name=sim_info.last_name)
        self._make_sim_instance(new_sim_info)
        TransferTools().clone_sim(sim_info, new_sim_info)  # copied attributes may or may not show in CAS
        # TransferTools()._clone_sim(sim_info, new_sim_info, flags=Transfer.BODY_PARTS.value) # Clone only Body Parts
        CommonHouseholdUtils.move_sim_to_household(new_sim_info, target_household.id)
        return new_sim_info


    def _make_sim_instance(self, sim_info: SimInfo) -> bool:
        if not sim_info.is_instanced(allow_hidden_flags=ALL_HIDDEN_REASONS):
            log.debug(f"\tSpawning sim '{sim_info}'")
            SimSpawner.spawn_sim(sim_info)

        if not sim_info.is_instanced(allow_hidden_flags=ALL_HIDDEN_REASONS):
            log.warn(f"Could not create a sim instance of '{sim_info}'")
            return False
        return True

    def copy_sims(self, sim_info_list: Tuple[SimInfo]):
        log.debug(f"Creating temporary household for {sim_info_list} ...")
        tmp_household: Household = CommonHouseholdUtils.create_empty_household(starting_funds=0, as_hidden_household=True)
        if tmp_household is None:
            log.warn(f"Could not create temporary household.")
            return
        tmp_household.name = f"o19.tmp.{int(time.time())}"

        edit_sim = None
        sim_infos: Dict[int, Tuple[int, int, bool]] = {}  # {tmp_si_id: (hh_id, si_id, de-spawn_sim), ...}

        xxx = {}
        for sim_info in sim_info_list:
            if sim_info.is_instanced(allow_hidden_flags=HiddenReasonFlag.NONE):
                de_spawn_sim = False
            else:
                de_spawn_sim = True
            is_sim_instance = self._make_sim_instance(sim_info)
            if not is_sim_instance:
                log.debug(f"Skipping sim {sim_info}")
                continue

            household: Household = CommonHouseholdUtils.get_household(sim_info)
            if not household:
                log.warn(f"No household found for '{sim_info}'")

            tmp_sim_info = self._clone_sim_into_new_household(sim_info, tmp_household)
            log.debug(f"tmp_sim_info = {tmp_sim_info}")
            if not tmp_sim_info:
                log.warn(f"Could not copy '{sim_info}'")
                continue

            if edit_sim is None:
                edit_sim = tmp_sim_info.get_sim_instance(allow_hidden_flags=ALL_HIDDEN_REASONS)
                log.debug(f"edit_sim = {edit_sim}")

            # tmp_household.add_sim_info_to_household(tmp_sim_info, reason=HouseholdChangeOrigin.CLONING)
            sim_infos.update({tmp_sim_info.id: (household.id, sim_info.id, de_spawn_sim)})
            xxx.update({sim_info: tmp_sim_info})

        if edit_sim is None:
            log.warn(f"No sim found. Can't enter CAS.")
            return
        client_id: int = self.get_client_id()
        log.debug(f"edit_sim = {edit_sim} {edit_sim.id} {edit_sim.household_id} {client_id}")
        tmp_household.save_data()

        active_sim_info = CommonSimUtils.get_active_sim_info()
        active_household = CommonHouseholdUtils.get_active_household()
        log.debug(f"Persisting ({active_household}, {active_sim_info}, {tmp_household}, {sim_infos})")
        PersistentStore().save_data(active_household.id, active_sim_info.id, tmp_household.id, sim_infos)
        PersistentStore().save_restore(active_sim_info.sim_id, active_sim_info.zone_id, active_sim_info.household_id, services.get_persistence_service().get_sim_proto_buff(active_sim_info.sim_id).household_name)
        PersistentStore().save_edit_sim(edit_sim, client_id)

        log.debug(f"Launching CAS. Waiting for '_exit_cas'")
        exit_to_cas_immediate_delay: int = 0  # in millisecond
        if exit_to_cas_immediate_delay == 0:
            sims4.commands.client_cheat(f"sims.exit2caswithhouseholdid {edit_sim.id} {edit_sim.household_id}", client_id)
        else:
            # Async call with 'exit_to_cas_immediate_delay' ms delay
            CommonTimeUtils.set_clock_speed(ClockSpeedMode.NORMAL)
            CommonIntervalEventRegistry().register_dispatcher(ModInfo.get_identity(), milliseconds=exit_to_cas_immediate_delay, listening_func=self.exit2cas, run_once=True)
            # CommonIntervalEventRegistry.get()._add_tracker(ModInfo.get_identity(), milliseconds=exit_to_cas_immediate_delay, listening_func=self.exit2cas, run_once=True)

    @staticmethod
    @CommonIntervalEventRegistry.run_once(ModInfo.get_identity().name, )
    def exit2cas():
        _edit_sim, _client_id = PersistentStore().get_edit_sim()
        sims4.commands.client_cheat(f"sims.exit2caswithhouseholdid {_edit_sim.id} {_edit_sim.household_id}", _client_id)

    def get_client_id(self) -> int:
        try:
            client_id = services.client_manager().get_first_client().id
        except:
            client_id = 1
        return client_id

    r"""
    Register 1st zone_loaded_cleanup_household and 2nd zone_loaded_exit_cas.
    They will be called in this order every time a zone loads.
    copy_sims() makes sure that _exit_cas() is executed.
    _exit_cas() makes sure that _cleanup_household() is executed.
    """
    @ staticmethod
    @ CommonEventRegistry.handle_events(ModInfo.get_identity())
    def zone_loaded_cleanup_household(event_data: S4CLZoneLateLoadEvent):
        CopySims()._cleanup_household()

    @ staticmethod
    @ CommonEventRegistry.handle_events(ModInfo.get_identity().name)
    def zone_loaded_exit_cas(event_data: S4CLZoneLateLoadEvent):
        CopySims()._exit_cas()

    def _exit_cas(self):
        ps = PersistentStore()
        stage = ps.get_stage()
        log.debug(f"_exit_cas stage: {stage}")
        if stage != Stage.HOUSEHOLD_DATA:
            return
        active_household_id, active_sim_info_id, tmp_household_id, sim_infos = ps.get_data()  # Tuple[int, int, int, Dict[int, Tuple[int, int, bool]]]
        log.debug(f"\tdata = {sim_infos}")

        for tmp_sim_info_id, _data in sim_infos.items():  # sim_infos: Dict[tmp.SimInfo.id, Tuple[Household.id, SimInfo.id, b.de-spawn]] = {}
            household_id, sim_info_id, de_spawn_sim = _data
            if household_id == active_sim_info_id == 0:
                continue
            try:
                log.debug(f"Transfer data from {tmp_sim_info_id} to {sim_info_id} ...")
                tmp_sim_info: SimInfo = CommonSimUtils.get_sim_info(tmp_sim_info_id)
                sim_info: SimInfo = CommonSimUtils.get_sim_info(sim_info_id)
                self._make_sim_instance(tmp_sim_info)
                self._make_sim_instance(sim_info)
                # TODO - All data which can be copied successfully to CAS and modified there should be applied to the sim
                # Right now limited to the body parts / outfits.
                flags = ps.get_include_filter()
                flags = flags & (ps.get_exclude_filter() ^ Transfer.ALL.value)
                s_flags = Transfer.transfer_bits_as_string(flags)
                log.debug(f"Transfer data {flags:049_b} from {tmp_sim_info} to {sim_info} ...")
                log.debug(f"\tFlags: {s_flags}")
                TransferTools().clone_sim(tmp_sim_info, sim_info, flags)

            except Exception as e:
                log.debug(f"Transfer data from {tmp_sim_info_id} to {sim_info_id} failed with '{e}'")

        # Here we can't delete the household as TS4 needs an active household
        # To avoid any issues do not modify the temporary household at all

        # Switch back to the original household
        (sim_id, zone_id, household_id, household_name) = ps.get_restore()
        ps.set_stage(Stage.CLEANUP)
        log.debug(f"Switching back to household '{household_name} ({household_id})' of '{sim_id}' ...")
        SimpleUINotification().show('Edit in CAS', "Click 'Just Switch to Household' to continue.", urgency=UiDialogNotification.UiDialogNotificationUrgency.URGENT)
        op = SwitchActiveHouseholdControl(sim_id=sim_id, zone_id=zone_id, household_id=household_id, household_name=household_name)
        distributor.system.Distributor.instance().send_op_with_no_owner_immediate(op)
        # send_op_with_no_owner_immediate() runs with a tiny delay. The next line is logged and more code may be executed before switching.
        log.debug(f"Waiting for switch into '_cleanup_household'")

    def _cleanup_household(self):
        ps = PersistentStore()
        stage = ps.get_stage()
        log.debug(f"_cleanup_household stage: {stage}")
        if stage != Stage.CLEANUP:
            return
        active_household_id, active_sim_info_id, tmp_household_id, sim_infos = ps.get_data()
        log.debug(f"\tdata = {sim_infos}")

        active_household: Household = services.household_manager().get(active_household_id)
        tmp_household: Household = services.household_manager().get(tmp_household_id)

        if active_household_id != CommonHouseholdUtils.get_active_household_id():
            log.debug(f"Not the right household ({active_household_id} != {CommonHouseholdUtils.get_active_household_id()})")
            return
        else:
            tmp_household.set_to_hidden()

        try:
            for tmp_sim_info_id, _data in sim_infos.items():
                household_id, sim_info_id, de_spawn_sim = _data
                if de_spawn_sim:
                    log.debug(f"\tDe-spawning sim {sim_info_id}")
                    sim_info: SimInfo = CommonSimUtils.get_sim_info(sim_info_id)
                    CommonSimSpawnUtils.despawn_sim(sim_info)

                log.debug(f"\tDeleting temporary sim '{tmp_sim_info_id}' (cloned before)")
                try:
                    tmp_sim_info: SimInfo = CommonSimUtils.get_sim_info(tmp_sim_info_id)
                    CommonSimSpawnUtils.despawn_sim(tmp_sim_info)
                    tmp_sim_info.remove_permanently(household=tmp_household)
                except Exception as e:
                    log.warn(f"\t\tError '{e}' removing temporary sim")

            remaining_sim_infos = tmp_household._sim_infos
            for tmp_sim_info in remaining_sim_infos:
                log.debug(f"\tDeleting sim '{tmp_sim_info}' (unexpected sim)")
                try:
                    tmp_sim_info.remove_permanently(household=tmp_household)
                except Exception as e:
                    log.warn(f"\t\tError '{e}' removing temporary sim")
        except Exception as e:
            log.warn(f"\tError '{e}' removing temporary sims")

        try:
            log.debug(f"Deleting temporary household '{tmp_household}'")
            CommonHouseholdUtils.delete_household(tmp_household)
        except Exception as e:
            log.warn(f"\tError '{e}' removing temporary household")

        ps.clear()
