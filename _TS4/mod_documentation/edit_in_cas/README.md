# Edit random Sims and Outfits in CAS
This funky mod allows to pick 1-8 sims and to edit their standard outfits in CAS.

It is not meant to edit Bathing, Situation, Career, Special, Towel, Fashion and/or Batuu outfits.
I suggest to create these outfits as Everyday 3-5, Swimming 3-5, etc. and to use [Copy Outfits](https://github.com/Oops19/TS4-CopyOutfits) to transfer them.

It ignores occults, at least nothing has been added to support them.

## Usage
Enable cheat menus (unless already enabled). Shift-Click on a sim and select 'Modify Sims in CAS.
Or open the cheat console with Shift+Ctrl+C and enter the cheat command `o19.eicas` or `o19.edit_in_cas` to open the sim picker and to enter CAS.

In CAS the outfits can be modified and new outfits can be added.
Also makeup, hats, etc. can be modified

## Issues
When cloning sims to a new household this works properly within the game.
Anyhow the UI (CAS) is not always updated properly.  

### Things to avoid in CAS:
* Add, import and/or delete sims (new, replaced and/or removed sims are ignored)
* Remove outfits (they will not be removed from the original sim)
* Modify age (except in the range Teen - Elder)
* Add, remove or modify occults.

### Transferred attributes
The code used is from Copy Outfits, so it should work fine and support also filtering in the future.
While the copy process itself works fine, displaying the copied data in CAS may fail.

Currently only 'Outfits' are copied back from CAS to the sim.
There is no way to detect which values have been replaced by TS4 with random values.
* All Outfits (++)
* Base Attributes (?)
  * Age (+)
  * Gender (+)
  * Extended Species (?)
* Physical Attributes (?)
  * Facial Attributes (+)
    * Sculpts (+)
    * Face Modifiers (+)
    * Body Modifiers (+)
  * Physique (-)
  * Voice Pitch (+)
  * Voice Actor (+)
  * Voice Effect (+)
  * Skin Tone (+)
  * Skin Tone Value Shift (+)
  * Flags (?)
  * Pelt Layers (?)
  * Extended Species (?)
  * Base Trait IDs (?)
  * Genetic Data (+%)
* Walk Styles (+)
* Traits (+)
* Custom Texture (?) 
* Name (+)
* Pronouns (?)
* Gender / Details (? *1)
* Gender / Sexual Orientation (not implemented *1)
* Gender / Romantic Boundaries (not implemented *1)
* Species (+)
* Aspiration (not implemented)
* Likes & Dislikes (not implemented)
* Death Cause (?)
* Household Relationships (not implemented)
* Preload Outfit List (?%)
* Tan Level (?%)
* Whims (?%)


* `?` To be tested
* `-`or `not implemented` Replaced by random values in CAS
* `%` Can't be edited in CAS
* `+` Works as expected
* `++` Transferred from CAS back into the game
* `*1` Should work for all trait related settings


### Important
After exiting CAS answer the 'Save Game?' question with 'Just Switch to Household'.
In case you click 'Cancel' manually change to the previously played household to finish the outfit edit.

If you don't switch to the previously played household TS4 will have a new household with the sims selected and edited before.
'Cancel' is a valid choice to add a new household and to keep the new household.
To keep the household change it to played households in CAS and then save and exit the game.
Without exiting the game it may still be deleted when switching back to the previously played household.  

## Custom transfer settings
With `o19.eicas.f 1` (or `o19.edit_in_cas.filter 1`) one can specify filter flags (based on binary bits) to select the attributes / parts to be transferred from CAS (actually from the temporary household) back to the selected sims.

This should be done before selecting the sims. As an alternative option one can click 'Cancel' after exiting CAS, then use this command and then click on the front door of the lot and select 'Switch To Household'.

Individual values from below can be added, when using `ALL_*` values make sure not to include similar individual values.
Otherwise use 'or' to get a proper filter pattern.

Individual facial filters are not supported, always use ALL_FACIAL_ATTRIBUTES to transfer sculpts and sliders.

To transfer body parts, age and skin tones use:
```python
flags = 2**0 + 2**1 + 2**11 + 2**12  # == 1 + 2 + 2048 + 4096 == 6147 = 0x00_0000_1803 = 0b0001_1000_0000_0011
# o19.eicas.f 6147
```

To transfer everything, including the broken PHYSIQUE values, use:
```python
flags = 2 ** 33 - 1  # == 8589934591 == 0x0001_FFFF_FFFF == 0b0001_1111_1111_1111_1111_1111_1111_1111_1111
# o19.eicas.f 0b1_1111_1111_1111_1111_1111_1111_1111_1111
# The filter flag parameter can be specified in decimal, hexadecimal or binary format.
```

#### Filter flag values
```python
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
ALL = 2 ** 33 - 1
```

# Addendum

## Game compatibility
This mod has been tested with `The Sims 4` 1.111.102, S4CL 3.9, TS4Lib 0.3.36.
It is expected to be compatible with many upcoming releases of TS4, S4CL and TS4Lib.

## Dependencies
Download the ZIP file, not the sources.
* [This Mod](../../releases/latest)
* [TS4-Library](https://github.com/Oops19/TS4-Library/releases/latest)
* [S4CL](https://github.com/ColonolNutty/Sims4CommunityLibrary/releases/latest)
* [The Sims 4](https://www.ea.com/games/the-sims/the-sims-4)

If not installed download and install TS4 and these mods.
All are available for free.

## Removal of the mod
Ths mod installation with unzip writes to a few directories.
To remove this mod and all related files locate the files and folders and remove them:
* `The Sims 4/Mods/_o19_/$mod_name.*`
* `The Sims 4/mod_data/_o19_/$mod_name/`
* `The Sims 4/mod_documentation/_o19_/$mod_name/`
* `The Sims 4/mod_sources/_o19_/$mod_name/`

To remove all of my mods locate these folders and remove them:
* `The Sims 4/Mods/_o19_/`
* `The Sims 4/mod_data/_o19_/`
* `The Sims 4/mod_documentation/_o19_/`
* `The Sims 4/mod_sources/_o19_/`
 
## Installation
* Locate the localized `The Sims 4` folder which contains the `Mods` folder.
* Extract the ZIP file into this `The Sims 4` folder.
* It will create the directories/files `Mods/_o19_/$mod_name.ts4script`, `Mods/_o19_/$mod_name.package`, `mod_data/$mod_name/*` and/or `mod_documentation/$mod_name/*` and/or `mod_sources/$mod_name/*`
* CAS and build-buy UGC without scripts will create `Mods/o19/$mod_name.package`.
* `mod_logs/$mod_name.txt` will be created as soon as data is logged.
* `mod_documentation/$mod_name/` and/or `mod_sources/$mod_name/` are not required and can be deleted.

### Manual Installation
If you don't want to extract the ZIP file into `The Sims 4` folder you might want to read this.
You can extract the ZIP file to a temporary directory and copy the folders manually.
* The files in `ZIP-File/mod_data` are usually required and should be extracted to `The Sims 4/mod_data`.
* The files in `ZIP-File/mod_documentation` are for you to read it. They are not needed to use this mod.
* The files in `ZIP-File/mod_sources` are not needed to use this mod.
* The `Mods/_o19_/*.ts4script` files can be stored in a random folder within `Mods` or directly in `Mods`. I highly recommend to store it in `_o19_` so you know who created it.

## Troubleshooting
When installed properly this is not necessary at all.
For manual installations check these things and make sure each question can be answered with 'yes'.
* Does 'The Sims 4' (localized to Die Sims 4, Les Sims 4, Los Sims 4, The Sims 4, ...) exist?
  * Does `The Sims 4` contain the folder `Mods`?
    * Does `Mods` contain the folder `_o19_`? 
      * Does `_19_` contain `ts4lib.ts4script` and `ts4lib.package` files?
      * Does `_19_` contain `{mod_name}.ts4script` and/or `{mod_name}.package` files?
  * Does `The Sims 4` contain the folder `mod_data`?
    * Does `mod_data` contain the folder `{mod_name}`?
      * Does `{mod_name}` contain files or folders?
  * Does `The Sims 4` contain the `mod_logs` ?
    * Does `mod_logs` contain the file `Sims4CommunityLib_*_Messages.txt`?
    * Does `mod_logs` contain the file `TS4-Library_*_Messages.txt`?
      * Is this the most recent version or can it be updated?
    * Does `mod_logs` contain the file `{mod_name}_*_Messages.txt`?
      * Is this the most recent version or can it be updated?
  * Doesn't `The Sims 4` contain the file(s) `last_exception.txt`  and/or `last_exception*.txt` ?
* Share the `The Sims 4/mod_logs/Sims4CommunityLib_*_Messages.txt` and `The Sims 4/mod_logs/{mod_name}_*_Messages.txt`  file.

## Usage Tracking / Privacy
This mod does not send any data to tracking servers. The code is open source, not obfuscated, and can be reviewed.

Some log entries in the log file ('mod_logs' folder) may contain the local username, especially if files are not found (WARN, ERROR).

## External Links
[Sources](https://github.com/Oops19/)
[Support](https://discord.gg/d8X9aQ3jbm)
[Donations](https://www.patreon.com/o19)

## Copyright and License
* © 2024 [Oops19](https://github.com/Oops19)
* License for '.package' files: [Electronic Arts TOS for UGC](https://tos.ea.com/legalapp/WEBTERMS/US/en/PC/)  
* License for other media unless specified differently: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) unless the Electronic Arts TOS for UGC overrides it.
This allows you to use this mod and re-use the code even if you don't own The Sims 4.
Have fun extending this mod and/or integrating it with your mods.

Oops19 / o19 is not endorsed by or affiliated with Electronic Arts or its licensors.
Game content and materials copyright Electronic Arts Inc. and its licensors. 
Trademarks are the property of their respective owners.

### TOS
* Please don't put it behind a paywall.
* Please don't create mods which break with every TS4 update.
* For simple tuning modifications use [Patch-XML](https://github.com/Oops19/TS4-PatchXML) 
* or [LiveXML](https://github.com/Oops19/TS4-LiveXML).
* To check the XML structure of custom tunings use [VanillaLogs](https://github.com/Oops19/TS4-VanillaLogs).
