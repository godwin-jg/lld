from dataclasses import dataclass
from abc import ABC, abstractmethod
# class Item:
#     def __init__(self, name: str, price: float):
#         self.name = name
#         self.price = price

@dataclass
class Item:
    name: str
    price: float
    
class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, current_total: float) -> float:
        """Calculates and returns the updated total after discount."""
        pass

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage 
        
    def apply_discount(self, current_total: float) -> float:
        return current_total * (1 - self.percentage / 100)

class FlatDiscount(DiscountStrategy):
    def __init__(self, amount: float):
        self.amount = amount 
        
    def apply_discount(self, current_total: float) -> float:
        return max(0.0, current_total - self.amount)

class BuyOneGetOneFreeDiscount(DiscountStrategy):
    def __init__(self, target_item_name: str):
        self.target_item_name = target_item_name

    def apply_discount(self, items: list[Item], current_total: float) -> float:
        target_items = [item for item in items if item.name == self.target_item_name]
        count = len(target_items)
        
        if count < 2:
            return current_total
            
        free_pairs = count // 2
        item_price = target_items[0].price
        total_discount = free_pairs * item_price
        
        return max(0.0, current_total - total_discount)

class ShoppingCart:
    def __init__(self):
        self._items : list[Item] = []
        self._discounts : list[DiscountStrategy] = []
    
    def add_item(self, item: Item) -> None:
        self._items.append(item)
    
    def apply_coupon(self, discount: DiscountStrategy) -> None:
        self._discounts.append(discount)
        
    def calculate_subtotal(self) -> float:
        return sum(item.price for item in self._items)
    
    def calculate_final_total(self) -> float:
        total = self.calculate_subtotal()
        
        for discount in self._discounts:
            total = discount.apply_discount(total)
            
        return round(total, 2)
        

cart = ShoppingCart()
cart.add_item(Item("Wireless Mouse", 50.0))
cart.add_item(Item("Mechanical Keyboard", 120.0))

print(f"Subtotal: ${cart.calculate_subtotal()}")  # $170.0

cart.apply_coupon(BuyOneGetOneFreeDiscount("Wireless Mouse"))
cart.apply_coupon(FlatDiscount(20.0))       # $170 - $20 = $150
cart.apply_coupon(PercentageDiscount(10.0)) # $150 - 10% = $135

print(f"Final Checkout Total: ${cart.calculate_final_total()}") # Output: $135.0
# add_item
# remove_item

# Discount,
# Item,
# Coupon
# calculate_subtotal
# cauculate_total