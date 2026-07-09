from abc import ABC, abstractmethod

# class ShippingCalculator:
#     def calculator(self, weight, carrier):
#         if carrier == "FEdex":
#             pass
#         elif carrier == "UPS":
#             return weight * 2.2 + 4.0


class ShippmentStrategy(ABC):
    @abstractmethod
    def calculate_cost(self, weight):
        pass
    

class FedExStrategy(ShippmentStrategy):
    def calculate_cost(self, weight):
        return weight * 2.2 + 5

class UPSStrategy(ShippmentStrategy):
    def calculate_cost(self, weight: float) -> float:
        return weight * 2.2 + 4.0
    

class Order:
    def __init__(self, weight, shipping_strategy):
        self.weight = weight
        self.shipping_strategy = shipping_strategy
    
    def set_shipping_strategy(self, shipping_strategy):
        self.shipping_strategy = shipping_strategy

    def get_total_shipping(self) -> float:
        return self.shipping_strategy.calculate_cost(self.weight)
    
my_order = Order(weight=10.0, shipping_strategy=FedExStrategy())
print(f"FedEx Cost: ${my_order.get_total_shipping()}")  # Output: $30.0

# The customer changes their mind and wants UPS instead
my_order.set_shipping_strategy(UPSStrategy()) # change strategy at runtime without changing the object itself
print(f"UPS Cost: ${my_order.get_total_shipping()}")    # Output: $26.0