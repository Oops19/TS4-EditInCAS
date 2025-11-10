#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from typing import Tuple

from edit_in_cas.copy_sims import CopySims
from edit_in_cas.modinfo import ModInfo

from sims.sim_info import SimInfo

from sims4communitylib.dialogs.option_dialogs.common_choose_sims_option_dialog import CommonChooseSimsOptionDialog
from sims4communitylib.dialogs.option_dialogs.options.sims.common_dialog_sim_option import CommonDialogSimOption
from sims4communitylib.dialogs.option_dialogs.options.sims.common_dialog_sim_option_context import CommonDialogSimOptionContext
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils

log: CommonLog = CommonLogRegistry.get().register_log(ModInfo.get_identity(), 'SimPicker')
log.enable()


class SimPicker:
    def show_sim_picker_dialog(self, title: str, description: str):
        def _on_submit(sim_info_list: Tuple[SimInfo]):
            CopySims().copy_sims(sim_info_list)

        title_tokens = (CommonLocalizationUtils.create_localized_string(0xFC089996, tokens=(title,)),)
        description_tokens = (CommonLocalizationUtils.create_localized_string(0xFC089996, tokens=(description,)),)

        # Create the dialog and show a number of Sims in 4 columns and being able to select up to 5 Sims.
        option_dialog = CommonChooseSimsOptionDialog(
            0xFC089996,
            0xFC089996,
            title_tokens=title_tokens,
            description_tokens=description_tokens,
            mod_identity=ModInfo.get_identity()
        )

        for sim_info in CommonSimUtils.get_sim_info_for_all_sims_generator():
            should_select = False  # random.choice((True, False))
            is_enabled = True  # random.choice((True, False))
            option_dialog.add_option(
                CommonDialogSimOption(
                    sim_info,
                    CommonDialogSimOptionContext(
                        is_enabled=is_enabled,
                        is_selected=should_select
                    )
                )
            )

        option_dialog.show(
            sim_info=CommonSimUtils.get_active_sim_info(),
            column_count=8,
            max_selectable=7,
            on_submit=_on_submit
        )
