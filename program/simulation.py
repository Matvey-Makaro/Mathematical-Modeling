import random
from enum import Enum


# Найти:
# Время простоя и работы обработчиков
# A - среднее число заявок, обслуживаемых в СМО в единицу времени (абсолютная пропускная способность СМО)
# L_smo - среднее число заявок, находящихся в СМО
# L_queue - среднее число заявок, находящихся в очереди
# L_obs - среднее число заявок, находящихся на обслуживании

class Customer:
    def __init__(self, num_of_stages: int):
        self.queue_times = [0 for _ in range(num_of_stages)]
        self.processing_times = [0 for _ in range(num_of_stages)]


class Handler:
    def __init__(self, nu: float):
        self._is_active = False
        self._next_event_time = None
        self._nu = nu
        self._customer = None

    def start_handle(self, customer: Customer, curr_time: int) -> None:
        self._is_active = True
        self._next_event_time = curr_time + random.expovariate(self._nu)
        self._customer = customer

    def finish_handle(self) -> None:
        self._is_active = False
        self._next_event_time = None
        self._customer = None

    def is_active(self) -> bool:
        return self._is_active

    def get_next_event_time(self) -> int:
        return self._next_event_time

    def get_customer(self) -> Customer:
        return self._customer


class EventType(Enum):
    NEW_CUSTOMER = 0,
    CUSTOMER_HANDLED = 1,
    UNKNOWN = 2


class Event:
    def __init__(self, event_type: EventType = EventType.UNKNOWN, time: int = 0, stage: int = -1, handler: int = -1):
        self._event_type = event_type
        self._time = time
        self._stage = stage
        self._handler = handler

    def set_event_type(self, event_type) -> None:
        self._event_type = event_type

    def get_event_type(self) -> EventType:
        return self._event_type

    def set_time(self, time) -> None:
        self._time = time

    def get_time(self) -> int:
        return self._time

    def set_stage(self, stage: int) -> None:
        self._stage = stage

    def get_stage(self) -> int:
        return self._stage

    def set_handler(self, handler: int) -> None:
        self._handler = handler

    def get_handler(self) -> int:
        return self._handler


class Stage:
    def __init__(self):
        self.handlers = []
        self.queue = []
        self.L_queue_stat = []
        self.L_obs_stat = []
        self.L_smo_stat = []


class Simulation:
    def __init__(self, lambd: float, stage1_n: int, stage1_nu: float, stage2_nu: float, stage3_n: int,
                 stage3_nu: float, simulation_time: int):
        self._lambd = lambd
        self._stage1_n = stage1_n
        self._stage1_nu = stage1_nu
        self._stage2_nu = stage2_nu
        self._stage3_n = stage3_n
        self._stage3_nu = stage3_nu

        self._num_of_stages = 3
        self._stages = [Stage() for _ in range(self._num_of_stages)]
        self._stages[0].handlers = [Handler(stage1_nu) for _ in range(stage1_n)]
        self._stages[1].handlers = [Handler(stage2_nu)]
        self._stages[2].handlers = [Handler(stage3_nu) for _ in range(stage3_n)]

        self._new_customer_time = random.expovariate(self._lambd)
        self._curr_time = 0
        self._simulation_time = simulation_time

        self._handled_customers = []

    def simulate(self) -> None:
        while self._curr_time < self._simulation_time:
            event = self._get_next_event()
            self._update_state(event)
        self._calculate_statistics()

    def get_result(self):
        return self._statistics

    def _get_next_event(self) -> Event:
        event = Event(EventType.NEW_CUSTOMER, self._new_customer_time)

        for j in range(len(self._stages)):
            stage = self._stages[j]
            for i in range(len(stage.handlers)):
                h = stage.handlers[i]
                if h.is_active():
                    if event.get_time() > h.get_next_event_time():
                        event.set_time(h.get_next_event_time())
                        event.set_event_type(EventType.CUSTOMER_HANDLED)
                        event.set_stage(j)
                        event.set_handler(i)
        return event

    def _update_state(self, event: Event) -> None:
        self._update_time(event.get_time())
        if event.get_event_type() == EventType.NEW_CUSTOMER:
            self._stages[0].queue.append(Customer(self._num_of_stages))
            self._new_customer_time = self._curr_time + random.expovariate(self._lambd)
        elif event.get_event_type() == EventType.CUSTOMER_HANDLED:
            self._process_customer_handled(event)
        elif event.get_event_type() == EventType.UNKNOWN:
            print("Unreachable!")
            assert False

        self._fill_handlers()

    def _update_time(self, new_time: int) -> None:
        offset = new_time - self._curr_time
        for i in range(len(self._stages)):
            s = self._stages[i]
            num_of_active_handlers = 0
            for h in s.handlers:
                if h.is_active():
                    h.get_customer().processing_times[i] += offset
                    num_of_active_handlers += 1
            for customer in s.queue:
                customer.queue_times[i] += offset

            s.L_queue_stat.append((offset, len(s.queue)))
            s.L_obs_stat.append((offset, num_of_active_handlers))
            s.L_smo_stat.append((offset, len(s.queue) + num_of_active_handlers))

        self._curr_time = new_time

    def _process_customer_handled(self, event: Event) -> None:
        stage_num = event.get_stage()
        handler_num = event.get_handler()
        stage = self._stages[stage_num]
        handler = stage.handlers[handler_num]

        if stage_num == self._num_of_stages - 1:
            self._handled_customers.append(handler.get_customer())
        else:
            next_stage = self._stages[stage_num + 1]
            next_stage.queue.append(handler.get_customer())

        handler.finish_handle()

    def _fill_handlers(self) -> None:
        for s in self._stages:
            for h in s.handlers:
                if not h.is_active():
                    if s.queue:
                        h.start_handle(s.queue[0], self._curr_time)
                        s.queue.pop(0)
                    else:
                        break

    def _calculate_statistics(self) -> None:
        self._statistics = Statistics(self._num_of_stages)
        self._calculate_load_times()
        self._calculate_average_queue_times()
        self._calculate_t_smo()
        self._statistics.total_load_time = sum(self._statistics.load_times)
        self._statistics.total_average_queue_time = sum(self._statistics.average_queue_times)
        self._calculate_load_coeffs()
        self.calc_L_queues()
        self.calc_L_obs()
        self.calc_L_smo()



    def _calculate_load_times(self):
        for c in self._handled_customers:
            for i in range(self._num_of_stages):
                self._statistics.load_times[i] += c.processing_times[i]

    def _calculate_average_queue_times(self):
        for c in self._handled_customers:
            for i in range(self._num_of_stages):
                self._statistics.average_queue_times[i] += c.queue_times[i]

        for i in range(self._num_of_stages):
            self._statistics.average_queue_times[i] /= len(self._handled_customers)

    def _calculate_t_smo(self):
        for c in self._handled_customers:
            for i in range(self._num_of_stages):
                self._statistics.t_smo[i] += c.queue_times[i] + c.processing_times[i]

        for i in range(self._num_of_stages):
            self._statistics.t_smo[i] /= len(self._handled_customers)

    def _calculate_load_coeffs(self):
        for i in range(self._num_of_stages):
            self._statistics.load_coeffs[i] = self._statistics.load_times[i] / (self._simulation_time * len(self._stages[i].handlers))
            self._statistics.load_coeffs[i] *= len(self._stages[i].handlers)

    def calc_L_queues(self):
        for i in range(self._num_of_stages):
            stage = self._stages[i]
            self._statistics.L_queue[i] = self.calc_L(stage.L_queue_stat)

    def calc_L_obs(self):
        for i in range(self._num_of_stages):
            stage = self._stages[i]
            self._statistics.L_obs[i] = self.calc_L(stage.L_obs_stat)

    def calc_L_smo(self):
        for i in range(self._num_of_stages):
            stage = self._stages[i]
            self._statistics.L_smo[i] = self.calc_L(stage.L_smo_stat)

    def calc_L(self, L_stat) -> float:
        sum = 0
        for (time, count) in L_stat:
            sum += time * count
        return sum / self._simulation_time



# Найти:
# Время простоя и работы обработчиков
# A - среднее число заявок, обслуживаемых в СМО в единицу времени (абсолютная пропускная способность СМО)
# L_smo - среднее число заявок, находящихся в СМО
# L_queue - среднее число заявок, находящихся в очереди
# L_obs - среднее число заявок, находящихся на обслуживани

class Statistics:
    def __init__(self, num_of_stages: int):
        self.load_times = [0 for _ in range(num_of_stages)]
        self.total_load_time = sum(self.load_times)
        self.average_queue_times = [0 for _ in range(num_of_stages)]
        self.total_average_queue_time = sum(self.average_queue_times)
        self.load_coeffs = [0. for _ in range(num_of_stages)]
        self.L_queue = [0. for _ in range(num_of_stages)]
        self.L_obs = [0. for _ in range(num_of_stages)]
        self.L_smo = [0. for _ in range(num_of_stages)]
        self.t_smo = [0. for _ in range(num_of_stages)]


def simulation_solution() -> None:
    print("simulation_solution:")
    lambd = 45/60  # человека в минуту
    stage1_n = 4
    stage1_nu = 1 / 5  # человека в минуту

    stage2_nu = 1  # человека в минуту

    stage3_n = 3
    stage3_nu = 1  # человека в минуту

    simulation_time = 1000 * 60

    simulation = Simulation(lambd, stage1_n, stage1_nu, stage2_nu, stage3_n, stage3_nu, simulation_time)
    simulation.simulate()
    statistics = simulation.get_result()

    print("statistics.total_load_time: ", statistics.total_load_time)
    print("statistics.total_average_queue_time: ", statistics.total_average_queue_time)

    print(statistics.load_times[0] / (simulation_time * stage1_n))
    print(statistics.load_times[1] / (simulation_time))
    print(statistics.load_times[2] / (simulation_time * stage3_n))
    print(statistics.total_load_time / (simulation_time * (stage1_n + 1 + stage3_n)))

    sum = 0
    for c in simulation._handled_customers:
        sum += c.processing_times[0]

    sum /= len(simulation._handled_customers)
    print("SUm: ", sum)

    num_of_stages = 3
    for i in range(num_of_stages):
        print("Stage " + str(i))
        print("Load coeff: ", statistics.load_coeffs[i])
        print("L_queue: ", statistics.L_queue[i])
        print("L_obs: ", statistics.L_obs[i])
        print("L_smo: ", statistics.L_smo[i])
        print("t_smo: ", statistics.t_smo[i])
