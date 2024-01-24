from logic.requirements import Requirement, RequirementType, parse_requirement_string
from logic.world import World


class ConditionalPatchHandler:
    def __init__(self, world: World):
        self.world = world

    # Recursively iterate through the given onlyif statement and output if it
    # is True or False. Statements use the same principles as the Requirements
    # use in the logic files and that code has been reused here.
    def evaluate_statements(self, statement: Requirement) -> bool:
        if isinstance(statement, Requirement):
            if statement.type == RequirementType.NOTHING:
                return True
            elif statement.type == RequirementType.IMPOSSIBLE:
                return False
            elif statement.type == RequirementType.OR:
                return any([self.evaluate_statements(arg) for arg in statement.args])
            elif statement.type == RequirementType.AND:
                return all([self.evaluate_statements(arg) for arg in statement.args])
            elif statement.type == RequirementType.NOT:
                return not ([self.evaluate_statements(arg) for arg in statement.args])
            elif statement.type == RequirementType.COUNT:
                count = statement.args[0]
                item = statement.args[1]
                return self.world.starting_item_pool[item] >= count
            else:
                raise Exception(
                    f"Invalid onlyif statement. Found statement with type {statement.type}."
                )

    def evaluate_onlyif(self, onlyif: str) -> bool:
        # print(f"Onlyif: {onlyif}")
        requirement = parse_requirement_string(onlyif, self.world, force_logic=True)

        return self.evaluate_statements(requirement)
