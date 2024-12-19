#
# LICENSE https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2024 https://github.com/Oops19
#


from edit_in_cas.enums.stage import Stage
from sims.sim import Sim
from ts4lib.utils.singleton import Singleton
from typing import Tuple, Dict, Union

try:
    from sims.household import Household
    from sims.sim_info import SimInfo
except:
    from typing import Any as Household
    from typing import Any as SimInfo


class PersistentStore(metaclass=Singleton):
    initialized = False

    def __init__(self):
        if PersistentStore.initialized:
            return
        self._storage: Union[Tuple[int, int, int, Dict[int, Tuple[int, int, bool]]], None] = None  # (active_hh_id, active_si_id, tmp_hh_id, {tmp_si_id: (hh_id, si_id, de-spawn_sim)}, ... })
        self._restore: Union[Tuple[int, int, int, str], None] = None  # (sim_id, zone_id, household_id, household_name)
        self._stage = Stage.IDLE  # 0=no data, 1=data, return from CAS, 2=data, switching HH
        self._edit_sim: Union[Tuple[Sim, int], None] = None
        self._filter_value: int = 1

    def save_data(self, active_household_id: int, active_sim_info_id: int, tmp_household_id: int, sim_data: Dict[int, Tuple[int, int, bool]], stage: Stage = Stage.HOUSEHOLD_DATA):
        self._storage = (active_household_id, active_sim_info_id, tmp_household_id, sim_data)
        self._stage = stage

    def get_data(self) -> Tuple[int, int, int, Dict[int, Tuple[int, int, bool]]]:
        return self._storage

    def save_restore(self, sim_id: int, zone_id: int, household_id: int, household_name: str):
        self._restore = (sim_id, zone_id, household_id, household_name)

    def get_restore(self) -> Tuple[int, int, int, str]:
        return self._restore

    def set_stage(self, stage: Stage):
        self._stage = stage

    def get_stage(self) -> Stage:
        return self._stage

    def clear(self):
        self._storage = None
        self._restore = None
        self._stage = Stage.IDLE

    # Currently not used, to be used to enter CAS with some delay
    def save_edit_sim(self, sim: Sim, client_id: int):
        self._edit_sim = sim, client_id

    def get_edit_sim(self) -> Tuple[Sim, int]:
        return self._edit_sim

    def set_filter(self, filter_value: int):
        self._filter_value = filter_value

    def get_filter(self) -> int:
        return self._filter_value


PersistentStore()
