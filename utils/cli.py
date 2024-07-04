from index_calculator import AVAILABLE_BANDS, AVAILABLE_INDICES, Band, Index

class InvalidBandSelection(Exception):
    def __init__(self, message="Invalid band selection, please try again."):
        self.message = message
        super().__init__(self.message)

def get_bands_from_user():
    print(f"Enter bands to use\n{AVAILABLE_BANDS} or '*' for all.\nSeparate multiple bands with a space.")
    user_input = input("Bands: ")
    
    if user_input == '*':
        return AVAILABLE_BANDS

    selected_bands = user_input.strip().lower().split()

    if (Band.RED.value not in selected_bands) or (Band.NIR.value not in selected_bands and (Band.GREEN.value not in selected_bands or Band.BLUE.value not in selected_bands)):
        raise InvalidBandSelection

    return [Band[band.upper()].value for band in selected_bands if band.upper() in Band.__members__]

class InvalidIndexSelection(Exception):
    def __init__(self, message="Invalid index selection, please try again."):
        self.message = message
        super().__init__(self.message)

def get_indices_from_user(selected_bands):
    available_indices = AVAILABLE_INDICES
    if Band.NIR.value not in selected_bands:
        available_indices.remove(Index.NDVI.value)
        available_indices.remove(Index.IPVI.value)
    elif Band.GREEN.value not in selected_bands or Band.BLUE.value not in selected_bands:
        available_indices.remove(Index.VARI.value)
        available_indices.remove(Index.RI.value)
        available_indices.remove(Index.BI.value)

    print(f"Enter indices to show\n{available_indices} or '*' for all.\nSeparate multiple indices with a space.")
    user_input = input("Indices: ")
    
    if user_input == '*':
        return available_indices

    selected_indices = user_input.strip().lower().split()

    if len(selected_indices) == 0:
        raise InvalidIndexSelection

    return [Index[index.upper()].value for index in selected_indices if index.upper() in Index.__members__]

