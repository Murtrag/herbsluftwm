from .system import Battery, SysInfo

class AbstractHandler:
    chain_response = {}

    _next_handler = None
    def __init__(self):
        self._chain_response = {}

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    # @abstractmethod
    def handle(self, request) -> dict:
        if self._next_handler:
            return self._next_handler.handle(request)

        return AbstractHandler.chain_response

class MemoryHandler(AbstractHandler):
    system = SysInfo()

    def handle(self, request) -> dict:
        if "memory" in request:
            print('memory')
            super().chain_response['memory'] = MemoryHandler.system.getMemoryUsage()
        return super().handle(request)

class BatteryLevelHandler(AbstractHandler):
    battery = Battery()
    def handle(self, request) -> dict:
        if "battery" in request :
            super().chain_response['battery'] = BatteryLevelHandler.battery.getCapacity()
        return super().handle(request)

class BatteryPredicationHandler(AbstractHandler):
    battery = Battery()
    def handle(self, request) -> dict:
        if "batteryPrediction" in request :
            super().chain_response['batteryPrediction'] = BatteryPredicationHandler.battery.getTimePrediction()
        return super().handle(request)

class LoadHandler(AbstractHandler):
    system = SysInfo()

    def handle(self, request) -> dict:
        if "load" in request:
            super().chain_response['load'] = LoadHandler.system.getLoad()
        return super().handle(request)

stat_chain = MemoryHandler()
stat_chain.set_next(
    BatteryLevelHandler()
).set_next(
    BatteryPredicationHandler()
).set_next(
    LoadHandler()
)
# test = 'test'

# if "__main__" == __name__:
#     print(
#         stat_chain.handle(["memory", "load"])
#     )



