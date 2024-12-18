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
from sims4communitylib.utils.sims.common_sim_gender_option_utils import CommonSimGenderOptionUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from ts4lib.custom_enums.custom_outfit_category import CustomOutfitCategory
from ts4lib.utils.outfit_utilities import OutfitUtilities

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'TransferTools')
log.enable()


class TransferTools:
    def clone_sim(self, src_sim_info: SimInfo, dst_sim_info: SimInfo, flags: int = Transfer.ALL.value):
        resend_physical_attributes = False
        resend_age = False
        resend_extended_species = False
        resend_preload_outfit_list = False
        resend_current_outfit = False
        resend_physique = False
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
            resend_none = True

        if Transfer.SPECIES.value == Transfer.SPECIES.value & flags:
            self._transfer_attributes(src_sim_info, dst_sim_info, {"species", })
            resend_extended_species = True

        if Transfer.WALK_STYLES.value == Transfer.WALK_STYLES.value & flags:
            self._transfer_walk_style(src_sim_info, dst_sim_info)
            resend_none = True

        if Transfer.TRAITS.value == Transfer.TRAITS.value & flags:
            self._transfer_traits(src_sim_info, dst_sim_info)
            resend_none = True

        if Transfer.GENDER_DETAILS.value == Transfer.GENDER_DETAILS.value & flags:
            self._transfer_gender_details(src_sim_info, dst_sim_info)
            resend_none = True

        if Transfer.GENDER_SEXUAL_ORIENTATION.value == Transfer.GENDER_SEXUAL_ORIENTATION.value & flags:
            self._transfer_gender_sexual_orientation(src_sim_info, dst_sim_info)
            resend_none = True

        if Transfer.GENDER_ROMANCE_SETTINGS.value == Transfer.GENDER_ROMANCE_SETTINGS.value & flags:
            self._transfer_gender_romance_settings(src_sim_info, dst_sim_info)
            resend_none = True

        if ((Transfer.ALL_BASE_ATTRIBUTES.value + Transfer.ALL_PHYSICAL_ATTRIBUTES.value) | flags) > 0:

            if Transfer.ALL_BASE_ATTRIBUTES.value == Transfer.ALL_BASE_ATTRIBUTES.value & flags:
                self._transfer_all_base_attributes(src_sim_info, dst_sim_info)
                resend_age = True
                resend_physical_attributes = True
            else:
                if Transfer.AGE.value == Transfer.AGE.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"age", })
                    resend_age = True
                if Transfer.GENDER.value == Transfer.GENDER.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"gender", })
                    resend_none = True
                    resend_age = True
                    resend_physical_attributes = True
                if Transfer.EXTENDED_SPECIES.value == Transfer.EXTENDED_SPECIES.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"extended_species", })
                    resend_extended_species = True

            if Transfer.ALL_PHYSICAL_ATTRIBUTES .value == Transfer.ALL_PHYSICAL_ATTRIBUTES.value & flags:
                self._transfer_all_physical_attributes(src_sim_info, dst_sim_info)
                resend_physical_attributes = True
                resend_physique = True
            else:
                if Transfer.ALL_FACIAL_ATTRIBUTES.value == Transfer.ALL_FACIAL_ATTRIBUTES.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"facial_attributes", })
                    resend_facial_attributes = True
                elif Transfer.ALL_FACIAL_ATTRIBUTES.value | flags > 0:
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
                if Transfer.PHYSIQUE.value == Transfer.PHYSIQUE.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"physique", })
                    resend_physique = True
                if Transfer.VOICE_ACTOR.value == Transfer.VOICE_ACTOR.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"voice_actor", })
                    resend_physical_attributes = True
                if Transfer.VOICE_EFFECT.value == Transfer.VOICE_EFFECT.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"voice_effect", })
                    resend_physical_attributes = True
                if Transfer.VOICE_PITCH.value == Transfer.VOICE_PITCH.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"voice_pitch", })
                    resend_physical_attributes = True
                if Transfer.SKIN_TONE.value == Transfer.SKIN_TONE.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"skin_tone", })
                    resend_physical_attributes = True
                if Transfer.SKIN_TONE_VAL_SHIFT.value == Transfer.SKIN_TONE_VAL_SHIFT.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"skin_tone_val_shift", })
                    resend_physical_attributes = True
                if Transfer.FLAGS.value == Transfer.FLAGS.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"flages", })
                    resend_physical_attributes = True
                if Transfer.PELT_LAYERS.value == Transfer.PELT_LAYERS.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"pelt_layers", })
                    resend_physical_attributes = True
                if Transfer.EXTENDED_SPECIES.value == Transfer.EXTENDED_SPECIES.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"extended_species", })
                    resend_physical_attributes = True
                if Transfer.BASE_TRAIT_IDS.value == Transfer.BASE_TRAIT_IDS.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"base_trait_ids", })
                    resend_physical_attributes = True
                if Transfer.GENETIC_DATA.value == Transfer.GENETIC_DATA.value & flags:
                    self._transfer_attributes(src_sim_info, dst_sim_info, {"genetic_data", })
                    resend_physical_attributes = True

        # Send updates one time
        if resend_physical_attributes:
            SimInfoBaseWrapper.resend_physical_attributes(dst_sim_info)
        if resend_age:
            dst_sim_info.resend_age()
        if resend_extended_species:
            dst_sim_info.resend_extended_species()
        if resend_physique:
            dst_sim_info.resend_physique()
        if resend_physique or resend_physical_attributes:
            dst_sim_info.update_fitness_state()
        if resend_preload_outfit_list:
            dst_sim_info.resend_preload_outfit_list()
        if resend_current_outfit or resend_preload_outfit_list:
            dst_sim_info.resend_current_outfit()

    def _transfer_attributes(self, src_sim_info: SimInfo, dst_sim_info: SimInfo, attributes: Set[str]) -> bool:
        """ Supported attributes:
        "first_name", "first_name_key", "last_name", "last_name_key", "full_name_key", "breed_name", "breed_name_key",
        "gender", "age", "species", "extended_species",
        "skin_tone", "skin_tone_val_shift", "pelt_layers", "custom_texture",
         "voice_pitch", "voice_actor", "voice_effect", "physique", "facial_attributes", "genetic_data", "flags", "packed_pronouns",
         "base_trait_ids"
          """
        log.debug(f"Transfer '{attributes}'")
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

    def _transfer_gender_romance_settings(self, src_sim_info: SimInfo, dst_sim_info: SimInfo) -> bool:
        log.debug(f"Not implemented: Transfer gender romance settings")
        # log.warn(f"Could not transfer gender romance settings from '{src_sim_info}' to '{dst_sim_info}' ({e}).")
        return False

    def _transfer_traits(self, src_sim_info: SimInfo, dst_sim_info: SimInfo) -> bool:
        log.debug(f"Transfer traits")
        rv = False
        try:
            del_traits: list = CommonTraitUtils.get_equipped_traits(dst_sim_info)
            add_traits: list = CommonTraitUtils.get_equipped_traits(src_sim_info)
            for trait in del_traits:
                if trait in add_traits:
                    continue  # trait in both lists, don't delete this trait
                try:
                    CommonTraitUtils.remove_trait(dst_sim_info, trait)
                except Exception as e:
                    log.warn(f"\tCould not remove trait '{trait}' from '{dst_sim_info}' ({e})")
                    rv = False

            for trait in add_traits:
                if trait in del_traits:
                    continue  # trait in both lists, don't add this trait
                try:
                    CommonTraitUtils.add_trait(dst_sim_info, trait)
                except Exception as e:
                    log.warn(f"\tCould not add trait to '{dst_sim_info}' '{trait}' ({e})")
                    rv = False

        except Exception as e:
            log.warn(f"Could not transfer traits from '{src_sim_info}' to '{dst_sim_info}' ({e}).")
            rv = False
        return rv

    def _transfer_walk_style(self, src_sim_info: SimInfo, dst_sim_info: SimInfo) -> bool:
        log.debug(f"Transfer all walk styles")
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
            log.warn(f"\tCould not transfer walk styles from '{src_sim_info}' to '{dst_sim_info}' ({e})")
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
