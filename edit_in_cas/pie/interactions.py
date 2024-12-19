#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from typing import Any

from edit_in_cas.main import Main
from interactions.context import InteractionContext
from sims.sim import Sim


from sims4communitylib.classes.interactions.common_immediate_super_interaction import CommonImmediateSuperInteraction
from sims4communitylib.classes.testing.common_execution_result import CommonExecutionResult
from sims4communitylib.classes.testing.common_test_result import CommonTestResult


class EditInCAS(CommonImmediateSuperInteraction):

    @classmethod
    def on_test(cls, interaction_sim: Sim, interaction_target: Any, interaction_context: InteractionContext, **kwargs) -> CommonTestResult:
        return CommonTestResult.TRUE

    def on_started(self, interaction_sim: Sim, interaction_target: Any) -> bool:
        Main().do_it()
        return CommonExecutionResult.TRUE
