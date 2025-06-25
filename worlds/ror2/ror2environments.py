from typing import Dict, List, TypeVar

# TODO probably move to Locations

environment_vanilla_orderedstage_1_table: Dict[str, int] = {
    "Distant Roost":                           10,  # blackbeach
    "Distant Roost (2)":                       11,  # blackbeach2
    "Titanic Plains":                          18,  # golemplains
    "Titanic Plains (2)":                      19,  # golemplains2
    "Verdant Falls":                           33,  # lakes
}
environment_vanilla_orderedstage_2_table: Dict[str, int] = {
    "Abandoned Aqueduct":                      20,  # goolake
    "Wetland Aspect":                          15,  # foggyswamp
}
environment_vanilla_orderedstage_3_table: Dict[str, int] = {
    "Rallypoint Delta":                        16,  # frozenwall
    "Scorched Acres":                          59,  # wispgraveyard
}
environment_vanilla_orderedstage_4_table: Dict[str, int] = {
    "Abyssal Depths":                          13,  # dampcavesimple
    "Siren's Call":                            47,  # shipgraveyard
    "Sundered Grove":                          45,  # rootjungle
}
environment_vanilla_orderedstage_5_table: Dict[str, int] = {
    "Sky Meadow":                              48,  # skymeadow
}

environment_vanilla_hidden_realm_table: Dict[str, int] = {
    "Hidden Realm: Bulwark's Ambry":            5,  # artifactworld
    "Hidden Realm: Bazaar Between Time":        9,  # bazaar
    "Hidden Realm: Gilded Coast":              17,  # goldshores
    "Hidden Realm: A Moment, Whole":           36,  # limbo
    "Hidden Realm: A Moment, Fractured":       43,  # mysteryspace
}

environment_vanilla_special_table: Dict[str, int] = {
    "Void Fields":                              4,  # arena
    "Commencement":                            42,  # moon2
}

environment_sotv_orderedstage_1_table: Dict[str, int] = {
    "Siphoned Forest":                         49,  # snowyforest
}
environment_sotv_orderedstage_2_table: Dict[str, int] = {
    "Aphelian Sanctuary":                       3,  # ancientloft
}
environment_sotv_orderedstage_3_table: Dict[str, int] = {
    "Sulfur Pools":                            51,  # sulfurpools
}

environment_sotv_special_table: Dict[str, int] = {
    "Void Locus":                              58,  # voidstage
    "The Planetarium":                         57,  # voidraid
}

environment_sots_orderedstage_1_table: Dict[str, int] = {
    "Viscous Falls":                           34,  # lakesnight
    "Shattered Abodes":                        52,  # village
    "Disturbed Impact":                        53,  # villagenight
}

environment_sots_orderedstage_5_table: Dict[str, int] = {
    "Helminth Hatchery":                       23,  # helminthroost
}

environment_sots_colossus_table: Dict[str, int] = {
    "Reformed Altar":                          35,  # lemuriantemple
    "Treeborn Colony":                         21,  # habitat
    "Golden Dieback":                          22,  # habitatfall
    "Prime Meridian":                          40,  # meridian
}

environment_sots_hidden_realm_table: Dict[str, int] = {
    "Hidden Realm: Bulwark's Ambry (Aphelian)": 6,  # artifactworld01
    "Hidden Realm: Bulwark's Ambry (Tar)":      7,  # artifactworld02
    "Hidden Realm: Bulwark's Ambry (Wisp)":     8,  # artifactworld03
}

X = TypeVar("X")
Y = TypeVar("Y")


def compress_dict_list_horizontal(list_of_dict: List[Dict[X, Y]]) -> Dict[X, Y]:
    """Combine all dictionaries in a list together into one dictionary."""
    compressed: Dict[X, Y] = {}
    for individual in list_of_dict:
        compressed.update(individual)
    return compressed


def collapse_dict_list_vertical(list_of_dict_1: List[Dict[X, Y]], *args: List[Dict[X, Y]]) -> List[Dict[X, Y]]:
    """Combine all parallel dictionaries in lists together to make a new list of dictionaries of the same length."""
    # find the length of the longest list
    length = len(list_of_dict_1)
    for list_of_dict_n in args:
        length = max(length, len(list_of_dict_n))

    # create a combined list with a length the same as the longest list
    collapsed: List[Dict[X, Y]] = [{}] * length
    # The reason the list_of_dict_1 is not directly used to make collapsed is
    #   side effects can occur if all the dictionaries are not manually unioned.

    # merge contents from list_of_dict_1
    for i in range(len(list_of_dict_1)):
        collapsed[i] = {**collapsed[i], **list_of_dict_1[i]}

    # merge contents of remaining lists_of_dicts
    for list_of_dict_n in args:
        for i in range(len(list_of_dict_n)):
            collapsed[i] = {**collapsed[i], **list_of_dict_n[i]}

    return collapsed


# TODO potentially these should only be created when they are directly referenced
#  (unsure of the space/time cost of creating these initially)

environment_vanilla_orderedstages_table = \
    [environment_vanilla_orderedstage_1_table, environment_vanilla_orderedstage_2_table,
     environment_vanilla_orderedstage_3_table, environment_vanilla_orderedstage_4_table,
     environment_vanilla_orderedstage_5_table]
environment_vanilla_table = \
    {**compress_dict_list_horizontal(environment_vanilla_orderedstages_table),
     **environment_vanilla_hidden_realm_table, **environment_vanilla_special_table}

environment_sotv_orderedstages_table = \
    [environment_sotv_orderedstage_1_table, environment_sotv_orderedstage_2_table,
     environment_sotv_orderedstage_3_table]
environment_sotv_table = \
    {**compress_dict_list_horizontal(environment_sotv_orderedstages_table), **environment_sotv_special_table}

environment_sots_orderedstages_table = \
    [environment_sots_orderedstage_1_table, environment_sots_orderedstage_5_table]
environment_sots_table = \
    {**compress_dict_list_horizontal(environment_sots_orderedstages_table), **environment_sots_colossus_table,
     **environment_sots_hidden_realm_table}

environment_non_orderedstages_table = \
    {**environment_vanilla_hidden_realm_table, **environment_vanilla_special_table, **environment_sotv_special_table}
environment_orderedstages_table = \
    collapse_dict_list_vertical(environment_vanilla_orderedstages_table, environment_sotv_orderedstages_table,
    environment_sots_orderedstages_table)
environment_all_table = {**environment_vanilla_table, **environment_sotv_table, **environment_sots_table}


def shift_by_offset(dictionary: Dict[str, int], offset: int) -> Dict[str, int]:
    """Shift all indexes in a dictionary by an offset"""
    return {name: index+offset for name, index in dictionary.items()}
