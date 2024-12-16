#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


import time
from typing import Tuple, Dict, Union

import distributor
import services
import sims4
import sims4.commands
from distributor.ops import SwitchActiveHouseholdControl
from distributor.system import Distributor
from edit_in_cas.enums.stage import Stage
from edit_in_cas.enums.transfer import Transfer
from edit_in_cas.modinfo import ModInfo
from edit_in_cas.persistent_store import PersistentStore
from objects import ALL_HIDDEN_REASONS, HiddenReasonFlag
from routing.walkstyle.walkstyle_request import WalkStyleRequest
from sims.household import Household
from sims.household_enums import HouseholdChangeOrigin
from sims.outfits.outfit_enums import OutfitCategory
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from sims.sim_spawner import SimSpawner
from sims4communitylib.enums.tags_enum import CommonGameTag
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
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

    def _copy_sim_to_household(self, sim_info: SimInfo, household: Household) -> SimInfo:
        """
        Clone a sim and return SimInfo of new sim
        @param sim_info: Sim to copy
        @param household: Household to paste to
        @return: SimInfo of new sim
        """
        new_sim_info = CommonSimSpawnUtils.clone_sim(sim_info, add_to_household=False, household_override=household)
        # Do we need to copy outfits, skins, ...?
        return new_sim_info

    def _clone_sim(self, src_sim_info: SimInfo, dst_sim_info: SimInfo, flags: int = 2 ** 24 - 1):
        resend_attributes = False

        if Transfer.BODY_PARTS.value == Transfer.BODY_PARTS.value & flags:
            for outfit_category in CustomOutfitCategory.__members__.values():
                if outfit_category == CustomOutfitCategory.CURRENT_OUTFIT:
                    continue
                _maximum_outfits = OutfitUtilities.get_maximum_outfits_for_category(outfit_category)
                outfit_category_id: OutfitCategory = OutfitUtilities().get_ts4_outfit_category(outfit_category)
                for outfit_index_id in range(0, _maximum_outfits):
                    outfit_category_and_index = (outfit_category_id, outfit_index_id)
                    if CommonOutfitUtils.has_outfit(src_sim_info, outfit_category_and_index):
                        # copy and paste this outfit
                        self._transfer_body_parts(src_sim_info, dst_sim_info, outfit_category_and_index)

        if bool((Transfer.ALL_BASE_ATTRIBUTES.value + Transfer.ALL_PHYSICAL_ATTRIBUTES.value) | flags):
            resend_attributes = True

            if Transfer.ALL_BASE_ATTRIBUTES.value == Transfer.ALL_BASE_ATTRIBUTES.value & flags:
                self._transfer_all_base_attributes(src_sim_info, dst_sim_info)
            else:
                if Transfer.AGE.value == Transfer.AGE.value & flags:
                    pass
                if Transfer.GENDER.value == Transfer.GENDER.value & flags:
                    pass
                if Transfer.EXTENDED_SPECIES.value == Transfer.EXTENDED_SPECIES.value & flags:
                    pass

            if Transfer.ALL_PHYSICAL_ATTRIBUTES .value == Transfer.ALL_PHYSICAL_ATTRIBUTES.value & flags:
                self._transfer_all_physical_attributes(src_sim_info, dst_sim_info)
            else:
                if Transfer.ALL_FACIAL_ATTRIBUTES.value == Transfer.ALL_FACIAL_ATTRIBUTES.value & flags:
                    self._transfer_all_facial_attributes(src_sim_info, dst_sim_info)
                else:
                    if Transfer.FACIAL_ATTRIBUTE_SCULPTS.value == Transfer.FACIAL_ATTRIBUTE_SCULPTS.value & flags:
                        pass
                    if Transfer.FACIAL_FACE_MODIFIERS.value == Transfer.FACIAL_FACE_MODIFIERS.value & flags:
                        pass
                    if Transfer.FACIAL_BODY_MODIFIERS.value == Transfer.FACIAL_BODY_MODIFIERS.value & flags:
                        pass
                if Transfer.VOICE_PITCH.value == Transfer.VOICE_PITCH.value & flags:
                    pass
                if Transfer.VOICE_ACTOR.value == Transfer.VOICE_ACTOR.value & flags:
                    pass
                if Transfer.SKIN_TONE.value == Transfer.SKIN_TONE.value & flags:
                    pass
                if Transfer.SKIN_TONE_VAL_SHIFT.value == Transfer.SKIN_TONE_VAL_SHIFT.value & flags:
                    self._transfer_skin_tones(src_sim_info, dst_sim_info)
                if Transfer.FLAGS.value == Transfer.FLAGS.value & flags:
                    pass
                if Transfer.PELT_LAYERS.value == Transfer.PELT_LAYERS.value & flags:
                    pass
                if Transfer.EXTENDED_SPECIES.value == Transfer.EXTENDED_SPECIES.value & flags:
                    pass
                if Transfer.BASE_TRAIT_IDS.value == Transfer.BASE_TRAIT_IDS.value & flags:
                    pass
                if Transfer.GENETIC_DATA.value == Transfer.GENETIC_DATA.value & flags:
                    self._transfer_genetic_data(src_sim_info, dst_sim_info)

        if Transfer.WALK_STYLES.value == Transfer.WALK_STYLES.value & flags:
            self._transfer_walk_style(src_sim_info, dst_sim_info)

        if Transfer.TRAITS.value == Transfer.TRAITS.value & flags:
            self._transfer_traits(src_sim_info, dst_sim_info)

        if Transfer.GENDER_PREGNANCY.value == Transfer.GENDER_PREGNANCY.value & flags:
            self._transfer_traits(src_sim_info, dst_sim_info)

        # TEST TODO REMOVE ME
        self._transfer_skin_tones(src_sim_info, dst_sim_info)
        self._transfer_all_facial_attributes(src_sim_info, dst_sim_info)

        if resend_attributes:
            SimInfoBaseWrapper.resend_physical_attributes(dst_sim_info)

    def _transfer_skin_tones(self, src_sim_info: SimInfo, dst_sim_info: SimInfo) -> bool:
        try:
            log.debug(f"Transfer skin tones")
            dst_sim_info.skin_tone = src_sim_info.skin_tone
            dst_sim_info.skin_tone_val_shift = src_sim_info.skin_tone_val_shift
        except Exception as e:
            log.warn(f"Could not transfer skin tones from '{src_sim_info}' to '{dst_sim_info}' ({e}).")
            return False
        return True

    def _transfer_gender_pregnancy(self, src_sim_info: SimInfo, dst_sim_info: SimInfo) -> bool:
        try:
            log.debug(f"Transfer gender pregnancy settings")
            # CommonSimGenderOptionUtils.update_body_frame() !CommonSimGenderOptionUtils.get_body_frame()
            if CommonTraitUtils.has_trait(src_sim_info, CommonTraitId.GENDER_OPTIONS_FRAME_MASCULINE).result:
                CommonTraitUtils.add_trait(dst_sim_info, CommonTraitId.GENDER_OPTIONS_FRAME_MASCULINE)
            else:
                CommonTraitUtils.remove_trait(dst_sim_info, CommonTraitId.GENDER_OPTIONS_FRAME_MASCULINE)
            if CommonTraitUtils.has_trait(src_sim_info, CommonTraitId.GENDER_OPTIONS_FRAME_FEMININE).result:
                CommonTraitUtils.add_trait(dst_sim_info, CommonTraitId.GENDER_OPTIONS_FRAME_FEMININE)
            else:
                CommonTraitUtils.remove_trait(dst_sim_info, CommonTraitId.GENDER_OPTIONS_FRAME_FEMININE)

            # CommonSimGenderOptionUtils.update_clothing_preference() !CommonSimGenderOptionUtils.get_clothing_preference()
            if CommonTraitUtils.has_trait(src_sim_info, CommonTraitId.GENDER_OPTIONS_CLOTHING_MENS_WEAR).result:
                CommonTraitUtils.add_trait(dst_sim_info, CommonTraitId.GENDER_OPTIONS_CLOTHING_MENS_WEAR)
            else:
                CommonTraitUtils.remove_trait(dst_sim_info, CommonTraitId.GENDER_OPTIONS_CLOTHING_MENS_WEAR)
            if CommonTraitUtils.has_trait(src_sim_info, CommonTraitId.GENDER_OPTIONS_CLOTHING_WOMENS_WEAR).result:
                CommonTraitUtils.add_trait(dst_sim_info, CommonTraitId.GENDER_OPTIONS_CLOTHING_WOMENS_WEAR)
            else:
                CommonTraitUtils.remove_trait(dst_sim_info, CommonTraitId.GENDER_OPTIONS_CLOTHING_WOMENS_WEAR)

            CommonSimGenderOptionUtils.update_can_be_impregnated(dst_sim_info, CommonSimGenderOptionUtils.can_be_impregnated(src_sim_info).result)
            CommonSimGenderOptionUtils.update_can_impregnate(dst_sim_info, CommonSimGenderOptionUtils.can_impregnate(src_sim_info).result)
            CommonSimGenderOptionUtils.update_can_reproduce(dst_sim_info, CommonSimGenderOptionUtils.can_reproduce(src_sim_info).result)
            CommonSimGenderOptionUtils.update_has_breasts(dst_sim_info, CommonSimGenderOptionUtils.has_breasts(src_sim_info).result)

            # !can_use_toilet_standing() set_can_use_toilet_standing()
            toilet_standing_trait: CommonTraitId = CommonSimGenderOptionUtils.determine_toilet_standing_trait(src_sim_info)
            if toilet_standing_trait:
                CommonTraitUtils.add_trait(dst_sim_info, toilet_standing_trait)
            else:
                CommonTraitUtils.remove_trait(dst_sim_info, toilet_standing_trait)

            # !can_use_toilet_standing() set_can_use_toilet_standing()
            uses_toilet_sitting: CommonTraitId = CommonSimGenderOptionUtils.determine_toilet_sitting_trait(src_sim_info)
            if uses_toilet_sitting:
                CommonTraitUtils.add_trait(dst_sim_info, uses_toilet_sitting)
            else:
                CommonTraitUtils.remove_trait(dst_sim_info, uses_toilet_sitting)
        except Exception as e:
            log.warn(f"Could not transfer traits from '{src_sim_info}' to '{dst_sim_info}' ({e}).")
            return False
        return True

    def _transfer_traits(self, src_sim_info: SimInfo, dst_sim_info: SimInfo) -> bool:
        try:
            log.debug(f"Transfer traits")
            errors = False
            del_traits: list = CommonTraitUtils.get_equipped_traits(dst_sim_info)
            add_traits: list = CommonTraitUtils.get_equipped_traits(src_sim_info)
            for trait in del_traits:
                if trait in add_traits:
                    continue  # trait in both lists, don't delete this trait
                try:
                    CommonTraitUtils.remove_trait(dst_sim_info, trait)
                except Exception as e:
                    log.warn(f"\tCould not remove trait '{trait}' from '{dst_sim_info}' ({e})")
                    errors = True

            for trait in add_traits:
                if trait in del_traits:
                    continue  # trait in both lists, don't add this trait
                try:
                    CommonTraitUtils.add_trait(dst_sim_info, trait)
                except Exception as e:
                    log.warn(f"\tCould not add trait to '{dst_sim_info}' '{trait}' ({e})")
                    errors = True

            if errors:
                log.warn(f"Could not transfer all traits from '{src_sim_info}' to '{dst_sim_info}'")
                return False
        except Exception as e:
            log.warn(f"Could not transfer traits from '{src_sim_info}' to '{dst_sim_info}' ({e}).")
            return False
        return True

    def _transfer_walk_style(self, src_sim_info: SimInfo, dst_sim_info: SimInfo) -> bool:
        try:
            log.debug(f"Transfer walk styles")
            src_sim: Sim = CommonSimUtils.get_sim_instance(src_sim_info)
            dst_sim: Sim = CommonSimUtils.get_sim_instance(dst_sim_info)
            walkstyle_requests: list = src_sim.routing_component.get_walkstyle_requests()
            for walkstyle_request in walkstyle_requests:
                WalkStyleRequest(dst_sim, walkstyle=walkstyle_request.walkstyle, priority=walkstyle_request.priority)
        except Exception as e:
            log.warn(f"Could not transfer walk styles from '{src_sim_info}' to '{dst_sim_info}' ({e})")
            return False
        return True

    def _transfer_genetic_data(self, src_sim_info: SimInfo, dst_sim_info: SimInfo) -> bool:
        try:
            log.debug(f"Transfer genetic data")
            SimInfoBaseWrapper.copy_genetic_data(dst_sim_info, src_sim_info)
        except Exception as e:
            log.warn(f"Could not transfer genetic data from '{src_sim_info}' to '{dst_sim_info}' ({e})")
            return False
        return True

    def _transfer_all_physical_attributes(self, src_sim_info: SimInfo, dst_sim_info: SimInfo) -> bool:
        try:
            log.debug(f"Transfer all physical attributes")
            SimInfoBaseWrapper.copy_physical_attributes(dst_sim_info, src_sim_info)
        except Exception as e:
            log.warn(f"Could not transfer all physical attributes from '{src_sim_info}' to '{dst_sim_info}' ({e})")
            return False
        return True

    def _transfer_all_facial_attributes(self, src_sim_info: SimInfo, dst_sim_info: SimInfo) -> bool:
        try:
            log.debug(f"Transfer all facial attributes")
            dst_sim_info.facial_attributes = src_sim_info.facial_attributes
        except Exception as e:
            log.warn(f"Could not transfer all facial attributes from '{src_sim_info}' to '{dst_sim_info}' ({e})")
            return False
        return True

    def _transfer_all_base_attributes(self, src_sim_info: SimInfo, dst_sim_info: SimInfo) -> bool:
        try:
            log.debug(f"Transfer all base attributes")
            SimInfoBaseWrapper.copy_base_attributes(dst_sim_info, src_sim_info)
        except Exception as e:
            log.warn(f"Could not transfer all base attributes from '{src_sim_info}' to '{dst_sim_info}' ({e})")
            return False
        return True

    def _transfer_body_parts(self, src_sim_info: SimInfo, dst_sim_info: SimInfo, outfit_category_and_index: Tuple[Union[OutfitCategory, int], int], create_missing_outfit: bool = True) -> bool:
        """
        @return: False if nothing is copied. Reasons for this: 1) No SRC outfit; 2) No DST outfit and create_missing_outfit=False; 3) Unexpected error
        """
        try:
            log.debug(f"Transfer all body parts")
            if not CommonOutfitUtils.has_outfit(src_sim_info, outfit_category_and_index):
                return False
            if not CommonOutfitUtils.has_outfit(dst_sim_info, outfit_category_and_index):
                if create_missing_outfit:
                    # Add missing outfit in bathing style
                    tag_list = (CommonGameTag.OUTFIT_CATEGORY_BATHING, )
                    CommonOutfitUtils.generate_outfit(dst_sim_info, outfit_category_and_index, tag_list)
                else:
                    return False
            parts = CommonOutfitUtils.get_outfit_parts(src_sim_info, outfit_category_and_index)
            OutfitUtilities.apply_outfit(dst_sim_info, parts, outfit_category_and_index)
        except Exception as e:
            log.warn(f"Could not copy all '{outfit_category_and_index}' body parts from '{src_sim_info}' to '{dst_sim_info}' ({e})")
            return False
        return True

    def _make_sim_instance(self, sim_info: SimInfo, household: Union[None, Household]) -> bool:
        if not sim_info.is_instanced(allow_hidden_flags=ALL_HIDDEN_REASONS):
            SimSpawner.spawn_sim(sim_info)

        if household and not sim_info.is_instanced(allow_hidden_flags=ALL_HIDDEN_REASONS):
            sim_info.inject_into_inactive_zone(household.home_zone_id)

        if not sim_info.is_instanced(allow_hidden_flags=ALL_HIDDEN_REASONS):
            if household:
                log.warn(f"Could not create a sim instance of '{sim_info}'")
            else:
                log.info(f"Could not create a sim instance of '{sim_info}' (Household None)")
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

        for sim_info in sim_info_list:
            if sim_info.is_instanced(allow_hidden_flags=HiddenReasonFlag.NONE):
                de_spawn_sim = False
            else:
                de_spawn_sim = True
            is_sim_instance = self._make_sim_instance(sim_info, None)
            household: Household = CommonHouseholdUtils.get_household(sim_info)
            if not household:
                log.warn(f"No household found for '{sim_info}'")

            if not is_sim_instance:
                if not self._make_sim_instance(sim_info, household):
                    log.debug(f"Skipping sim {sim_info}")
                    continue

            tmp_sim_info = self._copy_sim_to_household(sim_info, tmp_household)
            log.debug(f"tmp_sim_info = {tmp_sim_info}")
            if not tmp_sim_info:
                log.warn(f"Could not copy '{sim_info}'")
                continue

            self._make_sim_instance(tmp_sim_info, household)

            if edit_sim is None:
                edit_sim = tmp_sim_info.get_sim_instance(allow_hidden_flags=ALL_HIDDEN_REASONS)
                log.debug(f"edit_sim = {edit_sim}")

            tmp_household.add_sim_info_to_household(tmp_sim_info, reason=HouseholdChangeOrigin.CLONING)
            sim_infos.update({tmp_sim_info.id: (household.id, sim_info.id, de_spawn_sim)})

        if edit_sim is None:
            log.warn(f"No sim found. Can't enter CAS.")
            return
        client_id: int = self.get_client_id()
        log.debug(f"{edit_sim} {edit_sim.id} {edit_sim.household_id} {client_id}")

        active_sim_info = CommonSimUtils.get_active_sim_info()
        active_household = CommonHouseholdUtils.get_active_household()
        log.debug(f"Persisting ({active_household}, {active_sim_info}, {tmp_household}, {sim_infos})")
        PersistentStore().save_data(active_household.id, active_sim_info.id, tmp_household.id, sim_infos)
        PersistentStore().save_restore(active_sim_info.sim_id, active_sim_info.zone_id, active_sim_info.household_id, services.get_persistence_service().get_sim_proto_buff(active_sim_info.sim_id).household_name)
        sims4.commands.client_cheat(f"sims.exit2caswithhouseholdid {edit_sim.id} {edit_sim.household_id}", client_id)
        # 2 options to enter CAS:
        # 'sims.modify_in_cas' - sims4.commands.client_cheat('sims.exit2cas {} {} {}'.format(sim.id, sim.household_id, services.get_active_sim().id), _connection)
        # 'sims.modify_in_cas_with_householdId' - sims4.commands.client_cheat('sims.exit2caswithhouseholdid {} {}'.format(sim.id, sim.household_id), _connection)

    def get_client_id(self) -> int:
        try:
            client_id = services.client_manager().get_first_client().id
        except:
            client_id = 1
        return client_id

    r"""
    Register 1st zone_loaded_cleanup_household and 2nd zone_loaded_exit_cas.
    They will be called in this order every time a zone loads.
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
        active_household_id, active_sim_info_id, tmp_household_id, sim_infos = ps.get_data()
        log.debug(f"\tdata = {sim_infos}")

        active_household: Household = services.household_manager().get(active_household_id)
        tmp_household: Household = services.household_manager().get(tmp_household_id)

        for tmp_sim_info_id, _data in sim_infos.items():  # sim_infos: Dict[SimInfo, Tuple[Household, SimInfo]] = {}
            household_id, sim_info_id, de_spawn_sim = _data
            if household_id == active_sim_info_id == 0:
                continue
            log.debug(f"\tCopying outfit from {tmp_sim_info_id} to {sim_info_id} ...")
            tmp_sim_info: SimInfo = CommonSimUtils.get_sim_info(tmp_sim_info_id)
            sim_info: SimInfo = CommonSimUtils.get_sim_info(sim_info_id)
            self._make_sim_instance(tmp_sim_info, tmp_household)
            self._make_sim_instance(sim_info, active_household)
            CopySims()._clone_sim(tmp_sim_info, sim_info)

        # Here we can't delete the household as TS4 needs an active household
        # To avoid any issues do not modify the temporary household at all
        # Switch back to the original household
        (sim_id, zone_id, household_id, household_name) = ps.get_restore()
        ps.set_stage(Stage.CLEANUP)

        log.debug(f"Switching back to household '{household_name} ({household_id})' of '{sim_id}' ...")
        SimpleUINotification().show('Edit Outfits in CAS', "Click 'Just Switch to Household' to continue.", urgency=UiDialogNotification.UiDialogNotificationUrgency.URGENT)
        op = SwitchActiveHouseholdControl(sim_id=sim_id, zone_id=zone_id, household_id=household_id, household_name=household_name)
        distributor.system.Distributor.instance().send_op_with_no_owner_immediate(op)
        # send_op_with_no_owner_immediate() runs in a moment. The next line is logged before switching and more code may be executed.
        log.debug(f"Waiting for switch ...")

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

                log.debug(f"\tDeleting temporary sim '{tmp_sim_info_id}' (1)")
                try:
                    tmp_sim_info: SimInfo = CommonSimUtils.get_sim_info(tmp_sim_info_id)
                    CommonSimSpawnUtils.despawn_sim(tmp_sim_info)
                    tmp_sim_info.remove_permanently(household=tmp_household)
                except Exception as e:
                    log.warn(f"\t\tError '{e}' removing temporary sim")

            remaining_sim_infos = tmp_household._sim_infos
            for tmp_sim_info in remaining_sim_infos:
                log.debug(f"\tDeleting sim '{tmp_sim_info}' (2)")
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

        PersistentStore().clear()
