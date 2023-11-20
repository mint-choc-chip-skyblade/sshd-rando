import copy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import World
    from .search import Search
    from .entrance import Entrance


class RequirementType:
    NOTHING: int = 1
    IMPOSSIBLE: int = 2
    OR: int = 3
    AND: int = 4
    NOT: int = 5
    ITEM: int = 6
    EVENT: int = 7
    COUNT: int = 8
    CAN_ACCESS: int = 9
    CUSTOM_FUNCTION: int = 10
    DAY: int = 11
    NIGHT: int = 12
    WALLET_CAPACITY: int = 13
    GRATITUDE_CRYSTALS: int = 14


class EvalSuccess:
    NONE: int = 0
    PARTIAL: int = 1
    COMPLETE: int = 2
    UNNECESSARY: int = 3


class TOD:
    NONE: int = 0
    DAY: int = 0b01
    NIGHT: int = 0b10
    ALL: int = 0b11


ALL_TODS = [TOD.DAY, TOD.NIGHT]


class RequirementError(RuntimeError):
    pass


class Requirement:
    def __init__(self, type_: int = None, args_: list = []) -> None:
        self.type = type_
        self.args = args_


# Helper to strip an expression down to whatever is inside
# its outer most parenthesis
def strip_outer_parenthesis(req_str: str):
    return req_str[req_str.index("(") + 1 : req_str.rindex(")")]


# Takes a logic expression and translates it into a requirement object
# that's evaluated during the the search algorithm
def parse_requirement_string(
    req_str: str, world: "World", area_id: int = None
) -> Requirement:
    # Get a new copy of an empty requirement
    req = copy.deepcopy(Requirement())

    assert len(req.args) == 0

    macros = world.macros
    settings = world.setting_map.settings

    # Change the requirement string into a list of characters so we can modfy it
    req_chars = list(req_str)

    # First, we make sure that the expression has no missing or extra parenthesis
    # and that the nesting level at the beginning is the same at the end.
    #
    # Logic expressions are split up via spaces, but we only want to evaluate the parts of
    # the expression at the highest nesting level for the string that was passed in.
    # (We'll recursively call the function later to evaluate deeper levels.) So we replace
    # all the spaces on the highest nesting level with an arbitrarily chosen delimeter
    # that should never be used in logic statements.
    # (in this case: '+').
    nesting_level: int = 1
    delimeter: str = "+"

    for i in range(len(req_chars)):
        if req_chars[i] == "(":
            nesting_level += 1
        elif req_chars[i] == ")":
            nesting_level -= 1
        # Only replace spaces on the highest level
        elif req_chars[i] == " " and nesting_level == 1:
            req_chars[i] = delimeter

    # If the nesting level isn't the same as what we started with
    # then the logic expression is invalid
    if nesting_level != 1:
        raise RequirementError(
            f'Extra or missing parenthesis in logic statement "{req_str}"'
        )

    # Now split up the expression by the delimeter in the previous step
    new_req_str = "".join(req_chars)
    split_req_str: list[str] = []
    pos: int = 0
    # We can't split it up just using .split(delimeter) since
    # we need to do some special checking for setting evaluations
    while delimeter in new_req_str:
        pos = new_req_str.index(delimeter)
        char_before = new_req_str[pos - 1]
        char_after = new_req_str[pos + 1]
        if (char_before not in ["!", "=", ">", "<"]) and (
            char_after not in ["!", "=", ">", "<"]
        ):
            split_req_str.append(new_req_str[:pos])
            new_req_str = new_req_str[pos + 1 :]
        else:
            list_req_str = list(new_req_str)
            list_req_str.pop(pos)
            new_req_str = "".join(list_req_str)

    # Append the last remaining split
    split_req_str.append(new_req_str)

    # Now that we have the different parts of our expression, we can use
    # the number of parts we have to determine what kind of expression it is

    # All requirement types with 1 part
    if len(split_req_str) == 1:
        arg = split_req_str[0]

        # First check for no requirements

        if arg == "Nothing":
            req.type = RequirementType.NOTHING
        # Then macros...
        elif arg.replace("_", " ") in macros:
            return world.get_macro(arg)
        # Then items...
        elif arg.replace("_", " ") in world.item_table:
            req.type = RequirementType.ITEM
            req.args.append(world.get_item(arg))
        # Then events...
        elif arg[0] == "'":
            req.type = RequirementType.EVENT
            arg = arg.replace("'", "")
            world.add_event(arg)
            req.args.append(world.events[arg])
        # Then counts...
        elif arg.startswith("count("):
            req.type = RequirementType.COUNT
            arg = strip_outer_parenthesis(arg)
            # Get rid of spaces
            arg = arg.replace(" ", "")
            split_arg = arg.split(",")

            assert len(split_arg) == 2
            # TODO: count arguments that vary by setting

            count = int(split_arg[0])
            item = world.get_item(split_arg[1])

            req.args.append(count)
            req.args.append(item)
        # Then setting comparison check...
        # Since settings don't change curing seed generation,
        # we can resolve them to NOTHING or IMPOSSIBLE requirements now
        elif "==" in arg or "!=" in arg or ">=" in arg or "<=" in arg:
            # Split up the comparison using the second comparison character (which will always be '=')
            split_pos = arg.rindex("=")
            compared_option_str = arg[split_pos + 1 :]
            setting_name = arg[: split_pos - 1]

            if setting_name not in settings:
                raise RequirementError(
                    f'Setting "{setting_name}" is not a known setting'
                )

            actual_option = world.setting(setting_name).value_index()
            compared_option = world.setting(setting_name).value_index(
                compared_option_str
            )
            if (
                ("==" in arg and actual_option == compared_option)
                or ("!=" in arg and actual_option != compared_option)
                or (">=" in arg and actual_option >= compared_option)
                or ("<=" in arg and actual_option <= compared_option)
            ):
                req.type = RequirementType.NOTHING
            else:
                req.type = RequirementType.IMPOSSIBLE
        # Then boolean setting checks
        elif arg in settings:
            req.type = (
                RequirementType.NOTHING
                if world.setting(arg) == "on"
                else RequirementType.IMPOSSIBLE
            )
        # Then area access...
        elif arg.startswith("can_access("):
            req.type = RequirementType.CAN_ACCESS
            area_name = strip_outer_parenthesis(arg)
            world.add_area(area_name)
            req.args.append(world.area_ids[area_name])
        # Then crystals...
        elif arg.startswith("gratitude_crystals("):
            req.type = RequirementType.GRATITUDE_CRYSTALS
            crystal_count = int(strip_outer_parenthesis(arg))
            req.args.append(crystal_count)
        # Then wallet capacity...
        elif arg.startswith("wallet_capacity("):
            req.type = RequirementType.WALLET_CAPACITY
            rupees = int(strip_outer_parenthesis(arg))
            req.args.append(rupees)
        # Then day...
        elif arg == "Day":
            req.type = RequirementType.DAY
        # Then night...
        elif arg == "Night":
            req.type = RequirementType.NIGHT
        # Check Impossible last since it's least common
        elif arg == "Impossible":
            req.type = RequirementType.IMPOSSIBLE

        # If the requirement doesn't have a type, then something is wrong with it
        if req.type == None:
            raise RequirementError(f'Unrecognized logic symbol: "{arg}"')

        return req

    # If our expression has two parts, then the only type of requirement
    # that can currently be is a NOT requirement
    elif len(split_req_str) == 2:
        if split_req_str[0] == "not":
            req.type = RequirementType.NOT
            # The second part of the not expression is another expression
            # so we evaluate that one as well
            expression = split_req_str[1]
            # Get rid of parenthesis around expression if it has them
            if expression[0] == "(":
                expression = expression[1:-1]
            req.args.append(parse_requirement_string(expression, world, area_id))
            return req
        else:
            raise RequirementError(
                f"Unrecognized 2 part logic expression {split_req_str}"
            )

    # If we have more than two parts to our expression, then we have either AND or OR
    and_type: bool = "and" in split_req_str
    or_type: bool = "or" in split_req_str

    # If we have both of them, there's a problem with the expression
    if and_type and or_type:
        raise RequirementError(
            f'"and" & "or" in same nesting level when parsing {split_req_str}'
        )

    # If we have neither, that's also a problem
    if not and_type and not or_type:
        raise RequirementError(
            f"Could not determine logical operator type from expression {split_req_str}"
        )

    req.type = RequirementType.AND if and_type else RequirementType.OR

    # Filter out the "and"s and "or"s
    split_req_str = list(filter(lambda s: s != "and" and s != "or", split_req_str))

    # Recombine deeper NOT expressions (they were separated by the deliminator earlier)
    while "not" in split_req_str:
        pos = split_req_str.index("not")
        split_req_str[pos] = "not " + split_req_str[pos + 1]
        del split_req_str[pos + 1]

    # For each deeper expression, parse it and add it as an argument to the requirement
    for arg in split_req_str:
        # Get rid of outer parenthesis
        if arg[0] == "(":
            arg = strip_outer_parenthesis(arg)
        # Parse
        req.args.append(parse_requirement_string(arg, world, area_id))

        # TODO: AND and OR short-circuiting

    return req


def evaluate_requirement_at_time(
    req: Requirement, search: "Search", time: int, world: "World"
) -> bool:
    match req.type:
        case RequirementType.NOTHING:
            return True

        case RequirementType.IMPOSSIBLE:
            return False

        case RequirementType.OR:
            return any(
                [
                    evaluate_requirement_at_time(arg, search, time, world)
                    for arg in req.args
                ]
            )

        case RequirementType.AND:
            return all(
                [
                    evaluate_requirement_at_time(arg, search, time, world)
                    for arg in req.args
                ]
            )

        case RequirementType.NOT:
            return not evaluate_requirement_at_time(req.args[0], search, time, world)

        case RequirementType.ITEM:
            item = req.args[0]
            return search.owned_items[item] > 0

        case RequirementType.COUNT:
            count = req.args[0]
            item = req.args[1]
            return search.owned_items[item] >= count

        case RequirementType.EVENT:
            id = req.args[0]
            return id in search.owned_events

        case RequirementType.CAN_ACCESS:
            area_id = req.args[0]
            return area_id in search.area_time

        case RequirementType.CUSTOM_FUNCTION:
            # TODO
            return False

        case RequirementType.DAY:
            return time & TOD.DAY

        case RequirementType.NIGHT:
            return time & TOD.NIGHT

        case RequirementType.WALLET_CAPACITY:
            expected_capacity = req.args[0]
            base_wallet = 300
            num_prog_wallets = search.owned_items[world.get_item("Progressive Wallet")]
            num_extra_wallets = search.owned_items[world.get_item("Extra Wallet")]
            match num_prog_wallets:
                case 1:
                    base_wallet = 500
                case 2:
                    base_wallet = 1000
                case 3:
                    base_wallet = 5000
                case 4:
                    base_wallet = 9000
            return (num_extra_wallets * 300) + base_wallet >= expected_capacity

        case RequirementType.GRATITUDE_CRYSTALS:
            expected_crystals = req.args[0]
            num_single_crystals = search.owned_items[
                world.get_item("Gratitude Crystal")
            ]
            num_crystal_packs = search.owned_items[
                world.get_item("Gratitude Crystal Pack")
            ]
            return num_single_crystals + (num_crystal_packs * 5) >= expected_crystals


def evaluate_exit_requirement(search: "Search", exit_: "Entrance") -> int:
    if exit_.connected_area == None:
        # This should only be hit when splitting entrances
        # in the entrance shuffling algorithm
        return EvalSuccess.UNNECESSARY

    parent_area = exit_.parent_area
    connected_area = exit_.connected_area
    parent_area_time = search.area_time[parent_area.id]
    potential_exit_times = (
        TOD.ALL
        if exit_ not in parent_area.world.exit_time_cache
        else parent_area.world.exit_time_cache[exit_]
    )
    connected_area_time = (
        TOD.NONE
        if connected_area.id not in search.area_time
        else search.area_time[connected_area.id]
    )

    # If there's no potential to spread time to the new area, then this
    # exit isn't going to be a success
    potential_time_spread = ~connected_area_time & (
        parent_area_time & potential_exit_times
    )
    # print(f"{exit_} potential time spread {format(potential_time_spread, '02b')}")
    # print(f"{format(connected_area_time, '02b')} {format(parent_area_time, '02b')} {format(connected_area.allowed_tod, '02b')}")
    eval_success = EvalSuccess.NONE
    if potential_time_spread == 0:
        return EvalSuccess.NONE

    for time in ALL_TODS:
        if potential_time_spread & time:
            eval_test = evaluate_requirement_at_time(
                exit_.requirement, search, time, exit_.world
            )
            if eval_test:
                if connected_area.id not in search.area_time:
                    search.area_time[connected_area.id] = TOD.NONE
                search.area_time[connected_area.id] |= time
                # print(f"expanding {format(time, '02b')} to {connected_area}")
                # print(f"potential_time_spread: {format(potential_time_spread, '02b')}")
                eval_success = EvalSuccess.PARTIAL

    if eval_success != EvalSuccess.NONE:
        if connected_area.can_sleep:
            search.area_time[connected_area.id] = TOD.ALL
            # print(f"Sleeping in {connected_area}")

        connected_area_time = (
            TOD.NONE
            if connected_area.id not in search.area_time
            else search.area_time[connected_area.id]
        )
        # If the connected area now has complete access, then we mark a complete success
        # instead of just a partial one
        if ~connected_area_time & potential_exit_times == 0:
            eval_success = EvalSuccess.COMPLETE

    return eval_success


def evaluate_event_requirement(search: "Search", event) -> int:
    time = search.area_time[event.area.id]
    if evaluate_requirement_at_time(event.req, search, time, event.area.world):
        return EvalSuccess.COMPLETE
    return EvalSuccess.NONE


def evaluate_location_requirement(search: "Search", loc_access) -> int:
    time = search.area_time[loc_access.area.id]
    if evaluate_requirement_at_time(
        loc_access.req, search, time, loc_access.area.world
    ):
        return EvalSuccess.COMPLETE
    return EvalSuccess.NONE
