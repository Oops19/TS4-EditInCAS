# Edit random Sims and Outfits in CAS
This funky mod allows to pick 1-8 sims and to edit their standard outfits in CAS.

It is not meant to edit Bathing, Situation, Career, Special, Towel, Fashion and/or Batuu outfits.
I suggest to create these outfits as Everyday 3-5, Swimming 3-5, etc. and to use [Copy Outfits](https://github.com/Oops19/TS4-CopyOutfits) to transfer them.

It ignores occults, at least nothing has been added to support them.

## Usage
Enable cheat menus (unless already enabled). Shift-Click on a sim and select 'Modify Sims in CAS.
Or open the cheat console with Shift+Ctrl+C and enter the cheat command `o19.eicas` or `o19.edit_in_cas` to open the sim picker and to enter CAS.

In CAS the outfits can be modified and new outfits can be added.
All CAS parts including makeup, hats, etc. can be modified

### Important
After exiting CAS answer the 'Save Game?' question with 'Just Switch to Household'.
In case you click 'Cancel' manually change to the previously played household to finish the outfit edit.

If you don't switch to the previously played household TS4 will have a new household with the sims selected and edited before.
'Cancel' is a valid choice to add a new household and to keep the new household.
To keep the household change it to played households in CAS and then save and exit the game.
Without exiting the game it may still be deleted when switching back to the previously played household. 

## Issues
When cloning sims to a new household this works properly within the game.
Anyhow the UI (CAS) is not always updated properly.
Copying attributes from 'Occult' sims can fail, even when they are in their normal form.  

### Things to avoid in CAS:
* Add, import and/or delete sims (new, replaced and/or removed sims are ignored)
* Remove outfits (they will not be removed from the original sim, new outfits will be added)
* Modify age (except in the range Teen - Elder)
* Add, remove or modify occults. This seems to work only for some occults.

### Transferred attributes
The code used is from Copy Outfits, so it works fine and supports filtering.
The copy process of attributes itself works fine, displaying the copied data in CAS may fail.

Currently only 'Outfits' are copied back from CAS to the sim.
There is no way to detect which values have been replaced by TS4 with random values and which have been modified.

* Body Parts / All Outfits (++)
* Base Attributes
  * Age (+)
  * Gender (+)
  * Extended Species (?)
* Physical Attributes
  * Facial Attributes (+)
    * Sculpts (individual transfer not possible)
    * Face Modifiers (individual transfer not possible)
    * Body Modifiers (individual transfer not possible)
  * Physique (?)
  * Voice
    * Voice Actor (+)
    * Voice Pitch (+)
    * Voice Effect (+)
  * Skin
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
* Buffs (?%)


* `?` To be tested
* `-`or `not implemented` Replaced by random values in CAS
* `%` Can't be edited in CAS, to be used in 'Copy Sims & Outfits'
* `+` Works as expected
* `*1` Should work for all trait related settings


## Filters / Custom transfer settings
With `o19.eicas.i 1` (or `o19.edit_in_cas.incllude 1`) one can specify filter flags to include attributes.

With `o19.eicas.e n` (or `o19.edit_in_cas.exclude n`) one can specify filter flags (based on binary bits) to exclude attributes to be transferred from CAS (actually from the temporary household) back to the selected sims.
Excluded parts will never be transferred, even if they are specified in the include filter.
The default excluded attributes are: Buffs and Household Relationships. 

Custom filters should be set before selecting the sims.
As an alternative option one can click 'Cancel' after exiting CAS, then use the filter commands and finally click on the front door of the lot and select 'Switch To Household'.

Individual values from below can be added, when using `ALL_*` values make sure not to include similar individual values.
Values must not be added multiple times, (AGE + AGE == GENDER and thus a different filter).
Otherwise, use 'or' to get a proper filter pattern (AGE | AGE == AGE).

Individual facial filters are not supported, always use ALL_FACIAL_ATTRIBUTES to transfer sculpts and sliders.

To transfer body parts, age and skin tones use:
```python
flags = 2**0 + 2**1 + 2**11 + 2**12  # == 1 + 2 + 2048 + 4096 == 6147 = 0x00_0000_1803 = 0b0000_0000_0000_0000_0000_0000_0001_1000_0000_0011
# The filter flag parameter can be specified in decimal, hexadecimal or binary format. Leading zeros can be omitted.
# Parameter -1 restores the default values
# o19.eicas.i 6147
# or o19.eicas.i 0x1803
# or o19.eicas.i 0b1_1000_0000_0011
```

To transfer everything, including the broken PHYSIQUE values, use:
```python
flags = 2 ** 40 - 1  # == 1099511627775 == 0x00FF_FFFF_FFFF == 0b1111_1111_1111_1111_1111_1111_1111_1111_1111_1111
# o19.eicas.i 0x00FF_FFFF_FFFF
# o19.eicas.e 0
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
BUFFS = 2 ** 33

ALL = 2 ** 40 - 1
```
---

# 📝 Addendum

## 🔄 Game compatibility
This mod has been tested with `The Sims 4` 1.119.109, S4CL 3.15, TS4Lib 0.3.42.
It is expected to remain compatible with future releases of TS4, S4CL, and TS4Lib.

## 📦 Dependencies
Download the ZIP file - not the source code.
Required components:
* [This Mod](../../releases/latest)
* [TS4-Library](https://github.com/Oops19/TS4-Library/releases/latest)
* [S4CL](https://github.com/ColonolNutty/Sims4CommunityLibrary/releases/latest)
* [The Sims 4](https://www.ea.com/games/the-sims/the-sims-4)

If not already installed, download and install TS4 and the listed mods. All are available for free.

## 📥 Installation
* Locate the localized `The Sims 4` folder (it contains the `Mods` folder).
* Extract the ZIP file directly into this folder.

This will create:
* `Mods/_o19_/$mod_name.ts4script`
* `Mods/_o19_/$mod_name.package`
* `mod_data/$mod_name/*`
* `mod_documentation/$mod_name/*` (optional)
* `mod_sources/$mod_name/*` (optional)

Additional notes:
* CAS and Build/Buy UGC without scripts will create `Mods/o19/$mod_name.package`.
* A log file `mod_logs/$mod_name.txt` will be created once data is logged.
* You may safely delete `mod_documentation/` and `mod_sources/` folders if not needed.

### 📂 Manual Installation
If you prefer not to extract directly into `The Sims 4`, you can extract to a temporary location and copy files manually:
* Copy `mod_data/` contents to `The Sims 4/mod_data/` (usually required).
* `mod_documentation/` is for reference only — not required.
* `mod_sources/` is not needed to run the mod.
* `.ts4script` files can be placed in a folder inside `Mods/`, but storing them in `_o19_` is recommended for clarity.
* `.package` files can be placed in a anywhere inside `Mods/`.

## 🛠️ Troubleshooting
If installed correctly, no troubleshooting should be necessary.
For manual installs, verify the following:
* Does your localized `The Sims 4` folder exist? (e.g. localized to Die Sims 4, Les Sims 4, Los Sims 4, The Sims 4, ...)
  * Does it contain a `Mods/` folder?
    * Does Mods/_o19_/ contain:
      * `ts4lib.ts4script` and `ts4lib.package`?
      * `{mod_name}.ts4script` and/or `{mod_name}.package`
* Does `mod_data/` contain `{mod_name}/` with files?
* Does `mod_logs/` contain:
  * `Sims4CommunityLib_*_Messages.txt`?
  * `TS4-Library_*_Messages.txt`?
  * `{mod_name}_*_Messages.txt`?
* Are there any `last_exception.txt` or `last_exception*.txt` files in `The Sims 4`?


* When installed properly this is not necessary at all.
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

If issues persist, share:
`mod_logs/Sims4CommunityLib_*_Messages.txt`
`mod_logs/{mod_name}_*_Messages.txt`

## 🕵️ Usage Tracking / Privacy
This mod does not send any data to external servers.
The code is open source, unobfuscated, and fully reviewable.

Note: Some log entries (especially warnings or errors) may include your local username if file paths are involved.
Share such logs with care.

## 🔗 External Links
[Sources](https://github.com/Oops19/)
[Support](https://discord.gg/d8X9aQ3jbm)
[Donations](https://www.patreon.com/o19)

## ⚖️ Copyright and License
* © 2020-2025 [Oops19](https://github.com/Oops19)
* `.package` files: [Electronic Arts TOS for UGC](https://tos.ea.com/legalapp/WEBTERMS/US/en/PC/)  
* All other content (unless otherwise noted): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 

You may use and adapt this mod and its code — even without owning The Sims 4.
Have fun extending or integrating it into your own mods!

Oops19 / o19 is not affiliated with or endorsed by Electronic Arts or its licensors.
Game content and materials © Electronic Arts Inc. and its licensors.
All trademarks are the property of their respective owners.

## 🧾 Terms of Service
* Do not place this mod behind a paywall.
* Avoid creating mods that break with every TS4 update.
* For simple tuning mods, consider using:
  * [Patch-XML](https://github.com/Oops19/TS4-PatchXML) 
  * [LiveXML](https://github.com/Oops19/TS4-LiveXML).
* To verify custom tuning structures, use:
  * [VanillaLogs](https://github.com/Oops19/TS4-VanillaLogs).

## 🗑️ Removing the Mod
Installing this mod creates files in several directories. To fully remove it, delete:
* `The Sims 4/Mods/_o19_/$mod_name.*`
* `The Sims 4/mod_data/_o19_/$mod_name/`
* `The Sims 4/mod_documentation/_o19_/$mod_name/`
* `The Sims 4/mod_sources/_o19_/$mod_name/`

To remove all of my mods, delete the following folders:
* `The Sims 4/Mods/_o19_/`
* `The Sims 4/mod_data/_o19_/`
* `The Sims 4/mod_documentation/_o19_/`
* `The Sims 4/mod_sources/_o19_/`
