#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from typing import Union, Tuple, List, Set

from edit_in_cas.enums.transfer import Transfer
from edit_in_cas.modinfo import ModInfo
from routing.walkstyle.walkstyle_request import WalkStyleRequest
from sims.outfits.outfit_enums import OutfitCategory
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from sims4communitylib.enums.tags_enum import CommonGameTag
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.utils.cas.common_outfit_utils import CommonOutfitUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry, CommonLog
from sims4communitylib.utils.sims.common_buff_utils import CommonBuffUtils
from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from ts4lib.custom_enums.custom_outfit_category import CustomOutfitCategory
from ts4lib.utils.outfit_utilities import OutfitUtilities

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'TransferTools')
log.enable()


class TransferTools:
    def clone_sim(self, src_sim_info: SimInfo, dst_sim_info: SimInfo, flags: int = Transfer.ALL.value):
        resend_age = False
        resend_extended_species = False
        resend_physical_attributes = False
        resend_facial_attributes = False
        resend_physique = False
        resend_voice_actor = False
        resend_voice_effect = False
        resend_voice_pitch = False
        resend_skin_tone = False
        resend_skin_tone_val_shift = False
        resend_pelt_layers = False
        resend_trait_ids = False
        resend_genetic_data = False

        resend_custom_texture = False
        resend_preload_outfit_list = False
        resend_current_outfit = False
        resend_primary_aspiration = False
        resend_death_type = False  # not implemented
        resend_tan_level = False
        resend_current_whims = False
        resend_none = False  # for attributes which don't support resent

        if Transfer.BODY_PARTS.value == Transfer.BODY_PARTS.value & flags:
            self._transfer_body_parts(src_sim_info, dst_sim_info)
            resend_current_outfit = True

        if Transfer.NAME.value == Transfer.NAME.value & flags:
            self._transfer_attributes(src_sim_info, dst_sim_info, {"first_name", "first_name_key", "last_name", "last_name_key", "full_name_key", "breed_name", "breed_name_key", })
            resend_none = True

        if Transfer.PRONOUNS.value == Transfer.PRONOUNS.value & flags:
            self._transfer_attributes(src_sim_info, dst_sim_info, {"packed_pronouns", })
            resend_none = True

        if Transfer.CUSTOM_TEXTURE.value == Transfer.CUSTOM_TEXTURE.value & flags:
            self._transfer_attributes(src_sim_info, dst_sim_info, {"custom_texture", })
            resend_custom_texture = True

        if Transfer.SPECIES.value == Transfer.SPECIES.value & flags:
            self._transfer_attributes(src_sim_info, dst_sim_info, {"species", })
            resend_extended_species = True

        if Transfer.ASPIRATION.value == Transfer.ASPIRATION.value & flags:
            self._transfer_attributes(src_sim_info, dst_sim_info, {"_primary_aspiration", })
            resend_primary_aspiration = True

        if Transfer.PRELOAD_OUTFIT_LIST.value == Transfer.PRELOAD_OUTFIT_LIST.value & flags:
            self._transfer_attributes(src_sim_info, dst_sim_info, {"_preload_outfit_list", })
            resend_preload_outfit_list = True

        if Transfer.TAN_LEVEL.value == Transfer.TAN_LEVEL.value & flags:
            self._transfer_attributes(src_sim_info, dst_sim_info, {"_tan_level", })
            resend_tan_level = True

        if Transfer.DEATH_CAUSE.value == Transfer.DEATH_CAUSE.value & flags:
            self._transfer_attributes(src_sim_info, dst_sim_info, {"_death_tracker", })
            resend_death_type = True

        if Transfer.WHIMS.value == Transfer.WHIMS.value & flags:
            self._transfer_attributes(src_sim_info, dst_sim_info, {"_current_whims", })
            resend_current_whims = True

        if Transfer.WALK_STYLES.value == Transfer.WALK_STYLES.value & flags:
            self._transfer_walk_style(src_sim_info, dst_sim_info)
            resend_none = True

        if Transfer.TRAITS.value == Transfer.TRAITS.value & flags:
            self._transfer_traits(src_sim_info, dst_sim_info)
            resend_none = True

        if Transfer.BUFFS.value == Transfer.BUFFS.value & flags:
            self._transfer_buffs(src_sim_info, dst_sim_info)
            resend_none = True

        if Transfer.GENDER_DETAILS.value == Transfer.GENDER_DETAILS.value & flags:
            self._transfer_gender_details(src_sim_info, dst_sim_info)
            resend_none = True

        if Transfer.GENDER_SEXUAL_ORIENTATION.value == Transfer.GENDER_SEXUAL_ORIENTATION.value & flags:
            self._transfer_gender_sexual_orientation(src_sim_info, dst_sim_info)
            resend_none = True

        if Transfer.GENDER_ROMANTIC_BOUNDARIES.value == Transfer.GENDER_ROMANTIC_BOUNDARIES.value & flags:
            self._transfer_gender_romantic_boundaries(src_sim_info, dst_sim_info)
            resend_none = True

        if ((Transfer.ALL_BASE_ATTRIBUTES.value + Transfer.ALL_PHYSICAL_ATTRIBUTES.value) | flags) > 0:

            if Transfer.ALL_BASE_ATTRIBUTES.value == Transfer.ALL_BASE_ATTRIBUTES.value & flags:
                self._transfer_all_base_attributes(src_sim_info, dst_sim_info)
                resend_age = True
                resend_extended_species = True
            else:
                if Transfer.AGE.value == Transfer.AGE.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"age", })
                    resend_age = True
                if Transfer.GENDER.value == Transfer.GENDER.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"gender", })
                    resend_none = True
                    resend_age = True
                    resend_extended_species = True
                if Transfer.EXTENDED_SPECIES.value == Transfer.EXTENDED_SPECIES.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"extended_species", })
                    resend_extended_species = True

            if Transfer.PHYSIQUE.value == Transfer.PHYSIQUE.value & flags:
                src_sim_info._get_fit_fat()
                self._transfer_attributes(src_sim_info, dst_sim_info, {"physique", "fat", "fit"})
                resend_physique = True
            if Transfer.ALL_PHYSICAL_ATTRIBUTES .value == Transfer.ALL_PHYSICAL_ATTRIBUTES.value & flags:
                src_sim_info._get_fit_fat()
                self._transfer_all_physical_attributes(src_sim_info, dst_sim_info)
                resend_physical_attributes = True
            else:
                if Transfer.ALL_FACIAL_ATTRIBUTES.value == Transfer.ALL_FACIAL_ATTRIBUTES.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"facial_attributes", })
                    resend_facial_attributes = True
                elif Transfer.ALL_FACIAL_ATTRIBUTES.value & flags > 0:
                    # TODO: REMOVE_ME - Temporarily transfer all attributes even if only 1-2 flags has been specified
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"facial_attributes", })
                    resend_facial_attributes = True
                else:
                    # currently not supported as this requires a lot of work
                    if Transfer.FACIAL_ATTRIBUTE_SCULPTS.value == Transfer.FACIAL_ATTRIBUTE_SCULPTS.value & flags:
                        pass
                        resend_facial_attributes = True
                    if Transfer.FACIAL_FACE_MODIFIERS.value == Transfer.FACIAL_FACE_MODIFIERS.value & flags:
                        pass
                        resend_facial_attributes = True
                    if Transfer.FACIAL_BODY_MODIFIERS.value == Transfer.FACIAL_BODY_MODIFIERS.value & flags:
                        pass
                        resend_facial_attributes = True

                if Transfer.VOICE_ACTOR.value == Transfer.VOICE_ACTOR.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"voice_actor", })
                    resend_voice_actor = True
                if Transfer.VOICE_EFFECT.value == Transfer.VOICE_EFFECT.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"voice_effect", })
                    resend_voice_effect = True
                if Transfer.VOICE_PITCH.value == Transfer.VOICE_PITCH.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"voice_pitch", })
                    resend_voice_pitch = True
                if Transfer.SKIN_TONE.value == Transfer.SKIN_TONE.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"skin_tone", })
                    resend_skin_tone = True
                if Transfer.SKIN_TONE_VAL_SHIFT.value == Transfer.SKIN_TONE_VAL_SHIFT.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"skin_tone_val_shift", })
                    resend_skin_tone_val_shift = True
                if Transfer.FLAGS.value == Transfer.FLAGS.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"flags", })
                    resend_physical_attributes = True
                if Transfer.PELT_LAYERS.value == Transfer.PELT_LAYERS.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"pelt_layers", })
                    resend_pelt_layers = True
                if Transfer.EXTENDED_SPECIES.value == Transfer.EXTENDED_SPECIES.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"extended_species", })
                    resend_extended_species = True
                if Transfer.BASE_TRAIT_IDS.value == Transfer.BASE_TRAIT_IDS.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"base_trait_ids", })
                    resend_trait_ids = True
                if Transfer.GENETIC_DATA.value == Transfer.GENETIC_DATA.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"genetic_data", })
                    resend_genetic_data = True


        # Send updates one time
        if resend_age:
            dst_sim_info.resend_age()
        if resend_extended_species:
            dst_sim_info.resend_extended_species()
        if resend_physique:
            dst_sim_info._setup_fitness_commodities()
            dst_sim_info.resend_physique()
        if resend_physical_attributes:
            SimInfoBaseWrapper.resend_physical_attributes(dst_sim_info)
        else:
            if resend_facial_attributes:
                dst_sim_info.resend_facial_attributes()
            if resend_voice_actor:
                dst_sim_info.resend_voice_actor()
            if resend_voice_effect:
                dst_sim_info.resend_voice_effect()
            if resend_voice_pitch:
                dst_sim_info.resend_voice_pitch()
            if resend_skin_tone:
                dst_sim_info.resend_skin_tone()
            if resend_skin_tone_val_shift:
                dst_sim_info.resend_skin_tone_val_shift()
            if resend_pelt_layers:
                dst_sim_info.resend_pelt_layers()
            if resend_trait_ids:
                dst_sim_info.resend_trait_ids()
            if resend_genetic_data:
                dst_sim_info.resend_genetic_data()

        if resend_custom_texture:
            dst_sim_info.resend_custom_texture()
        if resend_preload_outfit_list:
            dst_sim_info.resend_preload_outfit_list()
        if resend_current_outfit:
            dst_sim_info.resend_current_outfit()
        if resend_primary_aspiration:
            dst_sim_info.resend_primary_aspiration()
        if resend_death_type:
            dst_sim_info.resend_death_type()
        if resend_tan_level:
            dst_sim_info.resend_suntan_data()
        if resend_current_whims:
            dst_sim_info.resend_current_whims()

    def _transfer_attributes(self, src_sim_info: SimInfo, dst_sim_info: SimInfo, attributes: Set[str]) -> bool:
        log.debug(f"Transfer '{' ,'.join(attributes)}'")
        rv = True
        for attribute in attributes:
            try:
                if hasattr(src_sim_info, attribute):
                    attribute_value = getattr(src_sim_info, attribute)
                    log.debug(f"\tTransfer {attribute}: {type(attribute_value)} = {attribute_value}")
                    if attribute == "base_trait_ids":
                        attribute_value = list(attribute_value)  # TODO do we really need this?
                        log.debug(f"\tTransfer {attribute}: {type(attribute_value)} = {attribute_value}")
                    elif attribute == "genetic_data" and hasattr(attribute_value, 'SerializeToString'):
                        attribute_value = attribute_value.SerializeToString()
                        log.debug(f"\tTransfer {attribute}: {type(attribute_value)} = {attribute_value}")
                    setattr(dst_sim_info, attribute, attribute_value)
            except Exception as e:
                log.warn(f"Could not transfer '{attribute}' from '{src_sim_info}' to '{dst_sim_info}' ({e}).")
                rv = False
        return rv

    def _transfer_gender_details(self, src_sim_info: SimInfo, dst_sim_info: SimInfo) -> bool:
        log.debug(f"Transfer gender details")
        try:
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
            log.warn(f"Could not transfer gender details from '{src_sim_info}' to '{dst_sim_info}' ({e}).")
            return False
        return True

    def _transfer_gender_sexual_orientation(self, src_sim_info: SimInfo, dst_sim_info: SimInfo) -> bool:
        log.debug(f"Not implemented: Transfer gender sexual orientation")
        # log.warn(f"Could not transfer gender sexual orientation from '{src_sim_info}' to '{dst_sim_info}' ({e}).")
        return False

    def _transfer_gender_romantic_boundaries(self, src_sim_info: SimInfo, dst_sim_info: SimInfo) -> bool:
        log.debug(f"Not implemented: Transfer gender romance settings")
        # log.warn(f"Could not transfer gender romance settings from '{src_sim_info}' to '{dst_sim_info}' ({e}).")
        return False

    def _merge_values(self, add_values: List[int], del_values: List[int]) -> Tuple[Set, Set]:
        remove_values: Set = set()
        append_values: Set = set()
        for value in del_values:
            if value in add_values:
                continue  # value in both lists, don't delete this value
            remove_values.add(value)

        for value in add_values:
            if value in del_values:
                continue  # value in both lists, don't add this value
            append_values.add(value)
        return append_values, remove_values

    def _transfer_buffs(self, src_sim_info: SimInfo, dst_sim_info: SimInfo) -> bool:
        log.debug(f"Transfer buffs")
        rv = False
        try:
            src_sim_buffs: list = CommonBuffUtils.get_buffs(src_sim_info)
            dst_sim_buffs: list = CommonBuffUtils.get_buffs(dst_sim_info)
            append_values, remove_values = self._merge_values(src_sim_buffs, dst_sim_buffs)
            for value in remove_values:
                try:
                    CommonBuffUtils.remove_buff(dst_sim_info, value)
                except Exception as e:
                    log.warn(f"\tCould not remove buff '{value}' to '{dst_sim_info}' ({e})")
                    rv = False
            for value in append_values:
                try:
                    CommonBuffUtils.add_buff(dst_sim_info, value)
                except Exception as e:
                    log.warn(f"\tCould not add buff '{value}' to '{dst_sim_info}' ({e})")
                    rv = False
        except Exception as e:
            log.warn(f"Could not transfer buffs from '{src_sim_info}' to '{dst_sim_info}' ({e}).")
            rv = False
        return rv

    def _transfer_traits(self, src_sim_info: SimInfo, dst_sim_info: SimInfo) -> bool:
        log.debug(f"Transfer traits")
        rv = False
        try:
            src_sim_traits: list = CommonTraitUtils.get_equipped_traits(src_sim_info)
            dst_sim_traits: list = CommonTraitUtils.get_equipped_traits(dst_sim_info)

            append_values, remove_values = self._merge_values(src_sim_traits, dst_sim_traits)
            for value in remove_values:
                try:
                    CommonTraitUtils.remove_trait(dst_sim_info, value)
                except Exception as e:
                    log.warn(f"\tCould not remove trait '{value}' to '{dst_sim_info}' '{value}' ({e})")
                    rv = False
            for value in append_values:
                try:
                    CommonTraitUtils.add_trait(dst_sim_info, value)
                except Exception as e:
                    log.warn(f"\tCould not add trait '{value}' to '{dst_sim_info}' ({e})")
                    rv = False
        except Exception as e:
            log.warn(f"Could not transfer traits from '{src_sim_info}' to '{dst_sim_info}' ({e}).")
            rv = False
        return rv

    def _transfer_walk_style(self, src_sim_info: SimInfo, dst_sim_info: SimInfo) -> bool:
        log.debug(f"Transfer walk styles")
        rv = True
        try:
            src_sim: Sim = CommonSimUtils.get_sim_instance(src_sim_info)
            dst_sim: Sim = CommonSimUtils.get_sim_instance(dst_sim_info)
            walkstyle_requests: List[WalkStyleRequest] = src_sim.routing_component.get_walkstyle_requests()
            for walkstyle_request in walkstyle_requests:
                try:
                    WalkStyleRequest(dst_sim, walkstyle=walkstyle_request.walkstyle, priority=walkstyle_request.priority)
                except Exception as e:
                    log.warn(f"\t\tCould not transfer walk style '{walkstyle_request}' from '{src_sim_info}' to '{dst_sim_info}' ({e})")
                    rv = False
        except Exception as e:
            log.warn(f"\tCould not transfer all walk styles from '{src_sim_info}' to '{dst_sim_info}' ({e})")
            rv = False
        return rv

    def _transfer_all_physical_attributes(self, src_sim_info: SimInfo, dst_sim_info: SimInfo) -> bool:
        log.debug(f"Transfer all physical attributes")
        try:
            SimInfoBaseWrapper.copy_physical_attributes(dst_sim_info, src_sim_info)
        except Exception as e:
            log.warn(f"Could not transfer all physical attributes from '{src_sim_info}' to '{dst_sim_info}' ({e})")
            return False
        return True

    def _transfer_all_base_attributes(self, src_sim_info: SimInfo, dst_sim_info: SimInfo) -> bool:
        log.debug(f"Transfer all base attributes")
        try:
            SimInfoBaseWrapper.copy_base_attributes(dst_sim_info, src_sim_info)
        except Exception as e:
            log.warn(f"Could not transfer all base attributes from '{src_sim_info}' to '{dst_sim_info}' ({e})")
            return False
        return True

    def _transfer_body_parts(self, src_sim_info: SimInfo, dst_sim_info: SimInfo) -> bool:
        log.debug(f"Transfer all body parts")
        outfits: List = []
        current_outfit_category_and_index = CommonOutfitUtils.get_current_outfit(src_sim_info)
        for outfit_category in CustomOutfitCategory.__members__.values():
            if outfit_category == CustomOutfitCategory.CURRENT_OUTFIT:
                continue  # non-exiting outfit -1
            _maximum_outfits = OutfitUtilities.get_maximum_outfits_for_category(outfit_category)
            outfit_category_id: OutfitCategory = OutfitUtilities.get_ts4_outfit_category(outfit_category)
            for outfit_index_id in range(0, _maximum_outfits):
                outfit_category_and_index = (outfit_category_id, outfit_index_id)
                if current_outfit_category_and_index == outfit_category_and_index:
                    continue  # add this last
                if CommonOutfitUtils.has_outfit(src_sim_info, outfit_category_and_index):
                    # copy and paste this outfit
                    outfits.append(outfit_category_and_index)

        # copy and paste also the current outfit
        outfits.append(current_outfit_category_and_index)
        log.debug(f"\tOutfits: {outfits}")

        # Process one outfit after the other, finish with the current outfit
        rv = True
        for outfit_category_and_index in outfits:
            rv &= self._transfer_body_part(src_sim_info, dst_sim_info, outfit_category_and_index)
        return rv

    def _transfer_body_part(self, src_sim_info: SimInfo, dst_sim_info: SimInfo,
                             outfit_category_and_index: Tuple[Union[OutfitCategory, int], int],
                             create_missing_outfit: bool = True) -> bool:
        """
        @return: False if nothing is copied. Reasons for this: 1) No SRC outfit; 2) No DST outfit and create_missing_outfit=False; 3) Unexpected error
        """
        try:
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
            log.warn(f"Could not transfer all '{outfit_category_and_index}' body parts from '{src_sim_info}' to '{dst_sim_info}' ({e})")
            return False
        return True
