import simpy
import random

class ServiceCenterSimulation:
    def __init__(self, num_servers, arrival_rate, service_time, capacity, duration):
        self.env = simpy.Environment()
        self.server = simpy.Resource(self.env, capacity=num_servers)
        self.arrival_rate = arrival_rate
        self.service_time = service_time
        self.capacity = capacity
        self.duration = duration
        
        # Metrics storage
        self.wait_times = []
        self.timestamps = []
        self.queue_lengths = []
        self.lost_customers = 0
        self.total_arrivals = 0

    def service_process(self, arrival_time):
        """Logic for serving a single customer."""
        with self.server.request() as req:
            yield req
            # Record wait time
            wait = self.env.now - arrival_time
            self.wait_times.append(wait)
            self.timestamps.append(self.env.now)
            
            # Simulate service duration
            yield self.env.timeout(random.expovariate(1.0 / self.service_time))

    def arrival_generator(self):
        """Generates customers and handles queue capacity (balking)."""
        inter_arrival = 60.0 / self.arrival_rate
        
        while True:
            yield self.env.timeout(random.expovariate(1.0 / inter_arrival))
            self.total_arrivals += 1
            
            # Record queue length for analytics
            current_queue = len(self.server.queue)
            self.queue_lengths.append(current_queue)

            # Capacity Check (Balking Logic)
            if self.server.count + current_queue >= self.capacity:
                self.lost_customers += 1
            else:
                self.env.process(self.service_process(self.env.now))

    def run(self):
        """Executes the simulation."""
        self.env.process(self.arrival_generator())
        self.env.run(until=self.duration)
        
        return {
            "wait_times": self.wait_times,
            "timestamps": self.timestamps,
            "lost_customers": self.lost_customers,
            "total_arrivals": self.total_arrivals,
            "queue_lengths": self.queue_lengths
        }