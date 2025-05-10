def singleton(cls):
    instances = {}
    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance

@singleton
class Memory:
    def __init__(self):  # Added colon
        self.memory: dict = {}

    def get(self, variable_name: str) -> object:
        assert variable_name in self.memory, f"{variable_name} not found in memory"
        return self.memory[variable_name]["value"]

    def set(self, variable_name: str, value: object, data_type: type):
        self.memory[variable_name] = {"value": value, "data_type": data_type}

    def __repr__(self) -> str:
        string = "Name\tValue\tData Type\n" + "-" * 30 + "\n"
        for var, data in self.memory.items():
            string += f"{var}\t{data['value']}\t{data['data_type'].__name__}\n"
        return string