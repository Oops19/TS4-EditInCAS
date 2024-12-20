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
    ALL_PHYSICAL_ATTRIBUTES = ALL_FACIAL_ATTRIBUTES + ALL_VOICE + ALL_SKIN_TONE + FLAGS + PELT_LAYERS + EXTENDED_SPECIES + BASE_TRAIT_IDS + GENETIC_DATA

    # other data
    WALK_STYLES = 2 ** 17
    TRAITS = 2 ** 18  # includes GENDER_* traits
    CUSTOM_TEXTURE = 22 ** 19
    NAME = 2 ** 20
    PRONOUNS = 2 ** 21
    GENDER_DETAILS = 2 ** 22  # based on traits
    GENDER_SEXUAL_ORIENTATION = 2 ** 23  # based on traits?
    GENDER_ROMANTIC_BOUNDARIES = 2 ** 24  # based on traits?
    SPECIES = 2 ** 25
    ASPIRATION = 2 ** 26
    LIKES_DISLIKES = 2 ** 27
    DEATH_CAUSE = 2 ** 28
    WHIMS = 2 ** 29
    TAN_LEVEL = 2 ** 30
    PRELOAD_OUTFIT_LIST = 2 ** 31
    HOUSEHOLD_RELATIONSHIPS = 2 ** 32
    BUFFS = 2 ** 33
    # = 2 ** 34
    # ...
    # = 2 ** 40
    ALL = 2 ** 40 - 1

    @staticmethod
    def transfer_bits_as_string(flags, reverse: bool = False) -> str:
        """
        @param flags:
        @param reverse:
        @return: String with high-bit left and low-bit right, set reverse=False for a reverse order
        """
        filters = []
        values = [e.value for e in Transfer]  # low-bit left, high-bit right
        if reverse:
            values = sorted(values, reverse=True)  # high-bit left, low-bit right
        for value in values:
            if value == Transfer.NONE.value:
                continue
            if value & flags == value:
                filters.append(Transfer(value).name.title().replace('_', ' '))
        if not filters:
            filters.append(Transfer(Transfer.NONE.value).name.title().replace('_', ' '))
        _filters = ', '.join(filters)
        return _filters

r"""
KEY							| COPY: SimInfoBaseWrapper / self								    	| RESEND: SimInfoBaseWrapper 
BODY_PARTS					| - / _transfer_body_parts										        | resend_physical_attributes resend_outfits resend_current_outfit

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
GENDER_SEXUAL_ORIENTATION	| - / TODO												        		| -
GENDER_ROMANTIC_BOUNDARIES  | - / TODO												        		| -
SPECIES                     | - / _ta.species                                                       | resend_extended_species (like school_data in EXTENDED_SPECIES)
ASPIRATION	               	| - / _ta._primary_aspiration							        		| si.resend_primary_aspiration
LIKES_DISLIKES	        	| - / TODO												        		| -
DEATH_CAUSE	            	| - / _ta._death_tracker											    | si.resend_death_type _death_tracker
WHIMS                       | - / _ta._current_whims                                                | si.resend_current_whims  
TAN_LEVEL                   | - / _ta._tan_level                                                    | si.resend_suntan_data
PRELOAD_OUTFIT_LIST         | - / _ta._preload_outfit_list							        		| resend_preload_outfit_list
HOUSEHOLD_RELATIONSHIPS     | - / -												        		    | -
BUFFS                       | - / -                                                                 | -
"""