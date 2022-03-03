from .system import Battery, SysInfo, _cmd

battery = Battery()
system = SysInfo()

class AbstractHandler:
    chain_response = {}

    _next_handler = None
    # def __init__(self):
    #     self._chain_response = {}

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    # @abstractmethod
    def handle(self, request) -> dict:
        if self._next_handler:
            return self._next_handler.handle(request)

        return AbstractHandler.chain_response

class MemoryHandler(AbstractHandler):
    def handle(self, request) -> dict:
        # print("request: ", request)
        # breakpoint()
        if "memory" in request:
            super().chain_response['memory'] = system.getMemoryUsage()
        return super().handle(request)

class BatteryLevelHandler(AbstractHandler):
    def handle(self, request) -> dict:
        if "battery" in request :
            super().chain_response['battery'] = battery.getCapacity()
        return super().handle(request)

class BatteryPredicationHandler(AbstractHandler):
    def handle(self, request) -> dict:
        if "batteryPrediction" in request :
            super().chain_response['batteryPrediction'] = battery.getTimePrediction()
        return super().handle(request)

class LoadHandler(AbstractHandler):
    def handle(self, request) -> dict:
        if "load" in request:
            super().chain_response['load'] = system.getLoad()
        return super().handle(request)

class DisksHandler(AbstractHandler):
    def handle(self, request) -> dict:
        if "disks" in request:
            super().chain_response['disks'] = system.getDisksInfo()
        return super().handle(request)

stat_chain = MemoryHandler()
stat_chain.set_next(
    BatteryLevelHandler()
    ).set_next(
        BatteryPredicationHandler()
        ).set_next(
            LoadHandler()
            ).set_next(
                DisksHandler()
            )
# test = 'test'

def is_afk(time_limit=5): 
    afk_time = int(_cmd(['xssstate', '-i']).decode('utf-8'))
    return afk_time > time_limit*60000 # 1*60 0000 1minute 


if "__main__" == __name__:
    # print(
    #     stat_chain.handle(["memory", "load"])
    # )
    print( is_afk() )



