#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from ts4lib.custom_enums.enum_types.custom_enum import CustomEnum


class Transfer(CustomEnum):
    r""" Binary enum, to get an idea about the used flags print them with
    log.debug(f"{flags:028_b}" == 1111_1111_1111_1111_1111_1111_1111_1111
    """
    NONE = 0

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
    PHYSIQUE = 2 ** 7
    VOICE_ACTOR = 2 ** 8
    VOICE_EFFECT = 2 ** 9
    VOICE_PITCH = 2 ** 10
    ALL_VOICE = VOICE_ACTOR + VOICE_EFFECT + VOICE_PITCH
    SKIN_TONE = 2 ** 11
    SKIN_TONE_VAL_SHIFT = 2 ** 12
    ALL_SKIN_TONE = SKIN_TONE + SKIN_TONE_VAL_SHIFT
    FLAGS = 2 ** 13
    PELT_LAYERS = 2 ** 14
    BASE_TRAIT_IDS = 2 ** 15
    GENETIC_DATA = 2 ** 16
    # GENETIC_DATA_B = GENETIC_DATA
    ALL_PHYSICAL_ATTRIBUTES = ALL_FACIAL_ATTRIBUTES + ALL_VOICE + ALL_SKIN_TONE + FLAGS + PELT_LAYERS + EXTENDED_SPECIES + BASE_TRAIT_IDS + GENETIC_DATA

    # other data
    WALK_STYLES = 2 ** 17
    TRAITS = 2 ** 18  # includes GENDER_PREGNANCY traits
    CUSTOM_TEXTURE = 22 ** 19
    NAME = 2 ** 20
    PRONOUNS = 2 ** 21
    GENDER_DETAILS = 2 ** 22  # contains a few traits
    GENDER_SEXUAL_ORIENTATION = 2 ** 23
    GENDER_ROMANCE_SETTINGS = 2 ** 24
    SPECIES = 2 ** 25

    ALL = 2 ** 32 - 1

r"""
KEY							| COPY: SimInfoBaseWrapper / self								    	| RESEND: SimInfoBaseWrapper 
BODY_PARTS					| - / _transfer_body_parts										        | resend_physical_attributes resend_outfits resend_current_outfit
							|																    	| resend_preload_outfit_list

AGE							| copy_base_attributes / _ta.age						            	| resend_age
GENDER						| copy_base_attributes / _ta.gender  						        	| -
EXTENDED_SPECIES			| copy_base_attributes / _ta.extended_species			        		| resend_extended_species
∑ ALL_BASE_ATTRIBUTES

FACIAL_ATTRIBUTE_SCULPTS	| copy_physical_attributes / -							        		| resend_physical_attributes resend_facial_attributes
FACIAL_FACE_MODIFIERS		| copy_physical_attributes / -							        		| resend_physical_attributes resend_facial_attributes
FACIAL_BODY_MODIFIERS		| copy_physical_attributes / -								           	| resend_physical_attributes resend_facial_attributes
∑ ALL_FACIAL_ATTRIBUTES
PHYSIQUE					| copy_physical_attributes / _transfer_physique			        		| resend_physical_attributes resend_physique
VOICE_ACTOR					| copy_physical_attributes / _ta.voice_actor				        	| resend_physical_attributes resend_voice_actor
VOICE_EFFECT				| copy_physical_attributes / _ta.voice_effect					        | resend_physical_attributes resend_voice_effect
VOICE_PITCH					| copy_physical_attributes / _ta.voice_pitch				        	| resend_physical_attributes resend_voice_pitch
∑ ALL_VOICE
SKIN_TONE					| copy_physical_attributes / _transfer_skin_tones					    | resend_physical_attributes resend_skin_tone
SKIN_TONE_VAL_SHIFT		    | copy_physical_attributes / _transfer_skin_tones				        | resend_physical_attributes resend_skin_tone
∑ ALL_SKIN_TONE
ALL_SKIN_TONE
FLAGS						| copy_physical_attributes / _ta.flags							        | -
PELT_LAYERS					| copy_physical_attributes / _ta.pelt_layers	        				| resend_physical_attributes resend_pelt_layers
BASE_TRAIT_IDS				| copy_physical_attributes / _ta.base_trait_ids	    					| resend_physical_attributes resend_trait_ids
GENETIC_DATA				| copy_physical_attributes copy_genetic_data / _transfer_genetic_data   | resend_physical_attributes resend_genetic_data
∑ ALL_PHYSICAL_ATTRIBUTES

WALK_STYLES					| - / _transfer_walk_style				   				        		| -
TRAITS						| - / _transfer_traits									        		| -
CUSTOM_TEXTURE				| - / _ta.custom_texture		    						        	| resend_physical_attributes resend_custom_texture
NAME						| - / _ta.first_name,...,breed_name_key		    			   			| -
PRONOUNS					| - / _ta.packed_pronouns		            					    	| -
GENDER_DETAILS				| - / _transfer_gender_details							        		| -
GENDER_SEXUAL_ORIENTATION	| - / -													        		| -
GENDER_ROMANCE_SETTINGS		| - / -													        		| -
SPECIES                     | - / _ta.species                                                       | -
"""