#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from sims4communitylib.mod_support.common_mod_info import CommonModInfo


class ModInfo(CommonModInfo):
    _FILE_PATH: str = str(__file__)

    @property
    def _name(self) -> str:
        return 'EditInCAS'

    @property
    def _author(self) -> str:
        return 'o19'

    @property
    def _base_namespace(self) -> str:
        return 'edit_in_cas'

    @property
    def _file_path(self) -> str:
        return ModInfo._FILE_PATH

    @property
    def _version(self) -> str:
        return '0.0.13'


r'''
v0.0.13
    Pause the game before opening the sim picker
    Polish the README
v0.0.12
    Fixed a logger name
v0.0.11
    Cleanup imports
v0.0.10
    Fix CUSTOM_TEXTURE enum value
    Fix add_buff code
    Fix 'exclude' filter and parsing of hex values
    Fix physique
    Added `o19.eicas.tt {filter}` to clone sims without entering CAS. filter==None == use include/exclude values; otherwise clone f(filter)
v0.0.9
    Pretty print applied filter flags (0b0011 == Body Parts, Age)
    Replaced 'filter' with 'include' and 'exclude' filters, cheat commands are used to modify the default filters.
    Default include: Body Parts (Outfits).
    Default exclude: Buffs, Physique and Household Relationships.
    Added support for buffs
v0.0.8
    Added cheat command to filter (include) attributes / parts
    Fix Transfer enum
    Code cleanup
    Fix transfer of genetic_data which will no longer be merged
    Added support for whims, suntan, death type
v0.0.7
    Tested with a new 'The Sims 4' folder as the old save was broken.
    Only Outfits will be copied back from CAS to avoid replacing attributes with random values.
    Names are now properly displayed in CAS.
v0.0.6
    Rework of the clone process, split in two steps.
    Add an 8th sim to improve the synchronization to CAS.
    Names (top) may still not be synchronized properly for all sims (left bottom names are usually fine) 
    Physique (fat-fit) sliders may show wrong values when switching sims.
v0.0.5
    Replace S4CL.clone_sim() with other S4CL calls.
    This needs some more tweaking, currently the last cloned sim is incomplete.
    Transfer also names and pronouns
    Don't modify the 'current outfit' (-1) type.
v0.0.4
    Do no longer clone walk styles, as long as the initial copy fails.
    Log the outfit category and index then cloning body parts
v0.0.3
    Clone sims manually after s4cl.clone_sim()
    Sometimes S4CL fails to clone sims properly
v0.0.2
    Add cheat menu
v0.0.1
    Initial version
'''
