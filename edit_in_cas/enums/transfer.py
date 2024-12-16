#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from ts4lib.custom_enums.enum_types.custom_enum import CustomEnum


class Transfer(CustomEnum):

    # multiple OUTFITS
    BODY_PARTS = 2 ** 0

    # ALL_BASE_ATTRIBUTES contains:
    AGE = 2 ** 1
    GENDER = 2 ** 2
    EXTENDED_SPECIES = 2 ** 3
    ALL_BASE_ATTRIBUTES = AGE + GENDER + EXTENDED_SPECIES

    # ALL_PHYSICAL_ATTRIBUTES contains:
    # ALL_FACIAL_ATTRIBUTES contains:
    FACIAL_ATTRIBUTE_SCULPTS = 2 ** 4
    FACIAL_FACE_MODIFIERS = 2 ** 5
    FACIAL_BODY_MODIFIERS = 2 ** 6
    ALL_FACIAL_ATTRIBUTES = FACIAL_ATTRIBUTE_SCULPTS + FACIAL_FACE_MODIFIERS + FACIAL_BODY_MODIFIERS
    VOICE_PITCH = 2 ** 7
    VOICE_ACTOR = 2 ** 8
    SKIN_TONE = 2 ** 9
    SKIN_TONE_VAL_SHIFT = 2 ** 10
    FLAGS = 2 ** 11
    PELT_LAYERS = 2 ** 12
    BASE_TRAIT_IDS = 2 ** 13
    GENETIC_DATA = 2 ** 14
    ALL_PHYSICAL_ATTRIBUTES = ALL_FACIAL_ATTRIBUTES + VOICE_PITCH + VOICE_ACTOR + SKIN_TONE + SKIN_TONE_VAL_SHIFT + FLAGS + PELT_LAYERS + EXTENDED_SPECIES + BASE_TRAIT_IDS + GENETIC_DATA

    # other data
    WALK_STYLES = 2 ** 16
    TRAITS = 2 ** 17  # includes GENDER_PREGNANCY traits
    GENDER_PREGNANCY = 2 ** 18  # contains a few traits




