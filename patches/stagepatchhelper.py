from sslib.utils import mask_shift_set


def patch_additional_properties(obj: dict, prop: str, value: int):
    unsupported_prop_execption = f"Cannot patch object with unsupported property.\nUnsupported property: {prop}\nObject: {obj}"

    if obj["name"].startswith("Npc"):
        if prop == "trigstoryfid":
            obj["params1"] = mask_shift_set(obj["params1"], 0x7FF, 10, value)
        elif prop == "untrigstoryfid":
            obj["params1"] = mask_shift_set(obj["params1"], 0x7FF, 21, value)
        elif prop == "talk_behaviour":
            obj["anglez"] = value

        elif obj["name"] == "NpcTke":
            if prop == "trigscenefid":
                obj["anglex"] = mask_shift_set(obj["anglex"], 0xFF, 0, value)
            elif prop == "untrigscenefid":
                obj["anglex"] = mask_shift_set(obj["anglex"], 0xFF, 8, value)
            elif prop == "subtype":
                obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 0, value)
            else:
                raise Exception(unsupported_prop_execption)
        else:
            raise Exception(unsupported_prop_execption)

    elif obj["name"] == "TBox":
        if prop == "spawnscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 20, value)
        elif prop == "setscenefid":
            obj["anglex"] = mask_shift_set(obj["anglex"], 0xFF, 0, value)
        elif prop == "itemid":
            obj["anglez"] = mask_shift_set(obj["anglez"], 0x1FF, 0, value)
        else:
            raise Exception(unsupported_prop_execption)

    elif obj["name"] == "EvntTag":
        if prop == "trigscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 16, value)
        elif prop == "setscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 8, value)
        elif prop == "event":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 0, value)
        else:
            raise Exception(unsupported_prop_execption)

    elif obj["name"] == "EvfTag":
        if prop == "trigstoryfid":
            obj["params1"] = mask_shift_set(obj["params1"], 0x7FF, 19, value)
        elif prop == "setstoryfid":
            obj["params1"] = mask_shift_set(obj["params1"], 0x7FF, 8, value)
        elif prop == "event":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 0, value)
        else:
            raise Exception(unsupported_prop_execption)

    elif obj["name"] == "ScChang":
        if prop == "trigstoryfid":
            obj["anglex"] = mask_shift_set(obj["anglex"], 0x7FF, 0, value)
        elif prop == "untrigstoryfid":
            obj["anglez"] = mask_shift_set(obj["anglez"], 0x7FF, 0, value)
        elif prop == "scen_link":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 0, value)
        elif prop == "trigscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 24, value)
        else:
            raise Exception(unsupported_prop_execption)

    elif obj["name"] == "SwAreaT":
        if prop == "setstoryfid":
            obj["anglex"] = mask_shift_set(obj["anglex"], 0x7FF, 0, value)
        elif prop == "unsetstoryfid":
            obj["anglez"] = mask_shift_set(obj["anglez"], 0x7FF, 0, value)
        elif prop == "setscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 0, value)
        elif prop == "unsetscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 8, value)
        else:
            raise Exception(unsupported_prop_execption)

    elif obj["name"] == "TgTimer":
        if prop == "subtype":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 0, value)
        elif prop == "timer":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 8, value)
        elif prop == "trigscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 16, value)
        elif prop == "setscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 24, value)
        else:
            raise Exception(unsupported_prop_execption)

    elif obj["name"] == "DieTag":
        if prop == "setscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 4, value)
        else:
            raise Exception(unsupported_prop_execption)

    elif obj["name"] == "PushBlk":
        if prop == "pathIdx":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 4, value)
        elif prop == "goalscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 12, value)
        elif prop == "useLargerRadius":
            obj["params1"] = mask_shift_set(obj["params1"], 0x03, 30, value)
        elif prop == "isSwitchGoal":
            obj["params1"] = mask_shift_set(obj["params1"], 0x03, 28, value)
        else:
            raise Exception(unsupported_prop_execption)

    else:
        raise Exception(f"Unsupported object to patch: {obj}")
