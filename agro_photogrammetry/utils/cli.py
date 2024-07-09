from enum import Enum
from constants import Bands, Indices
from constants import AVAILABLE_BANDS, AVAILABLE_INDICES


class Colors(Enum):
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class InvalidBandSelection(Exception):
    def __init__(self, message="Invalid band selection, please try again."):
        self.message = message
        super().__init__(self.message)


def get_bands_from_user():
    print(
        f"{Colors.HEADER.value}Enter bands to use{Colors.ENDC.value}\n{Colors.CYAN.value}{AVAILABLE_BANDS}{Colors.ENDC.value} or {Colors.CYAN.value}'*'{Colors.ENDC.value} for all.\n{Colors.BOLD.value}Separate multiple bands with a space.{Colors.ENDC.value}")
    user_input = input("Bands: ")

    if user_input == '*':
        return AVAILABLE_BANDS

    selected_bands = user_input.strip().lower().split()

    if (Bands.RED.value not in selected_bands) or (Bands.NIR.value not in selected_bands and (Bands.GREEN.value not in selected_bands or Bands.BLUE.value not in selected_bands)):
        raise InvalidBandSelection

    return [Bands[band.upper()].value for band in selected_bands if band.upper() in Bands.__members__]


class InvalidIndexSelection(Exception):
    def __init__(self, message="Invalid index selection, please try again."):
        self.message = message
        super().__init__(self.message)


def get_indices_from_user(selected_bands: list[str]) -> list[str]:
    available_indices = AVAILABLE_INDICES
    if Bands.NIR.value not in selected_bands:
        available_indices.remove(Indices.NDVI.value)
        available_indices.remove(Indices.IPVI.value)
        available_indices.remove(Indices.SAVI.value)
        available_indices.remove(Indices.EVI.value)
    if Bands.RED.value not in selected_bands:
        available_indices.clear()
    if Bands.GREEN.value not in selected_bands:
        available_indices.remove(Indices.VARI.value)
        available_indices.remove(Indices.RI.value)
        available_indices.remove(Indices.BI.value)
    if Bands.BLUE.value not in selected_bands:
        available_indices.remove(Indices.VARI.value)
        available_indices.remove(Indices.RI.value)
        available_indices.remove(Indices.BI.value)
        available_indices.remove(Indices.EVI.value)

    print(
        f"{Colors.HEADER.value}Enter indices to show{Colors.ENDC.value}\n{Colors.CYAN.value}{available_indices}{Colors.ENDC.value} or {Colors.CYAN.value}'*'{Colors.ENDC.value} for all.\n{Colors.BOLD.value}Separate multiple indices with a space.{Colors.ENDC.value}")
    user_input = input("Indices: ")

    if user_input == '*':
        return available_indices

    selected_indices = user_input.strip().lower().split()

    if len(selected_indices) == 0:
        raise InvalidIndexSelection

    return [Indices[index.upper()].value for index in selected_indices if index.upper() in Indices.__members__]
