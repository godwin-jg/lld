from abc import ABC, abstractmethod

# ==========================================
# STEP 1: DEFINE THE PRODUCT INTERFACES
# ==========================================

class Burger(ABC):
    """The Burger Interface."""
    @abstractmethod
    def get_description(self) -> str:
        pass


class Drink(ABC):
    """The Drink Interface."""
    @abstractmethod
    def get_description(self) -> str:
        pass


# ==========================================
# STEP 2: IMPLEMENT CONCRETE PRODUCTS
# ==========================================

# --- New York Products ---
class NYCStyleBurger(Burger):
    def get_description(self) -> str:
        return "Classic Smash Burger with local NY cheddar cheese. 🧀"


class NYCCraftSoda(Drink):
    def get_description(self) -> str:
        return "Artisanal Brooklyn Root Beer."


# --- Texas Products ---
class TexasStyleBurger(Burger):
    def get_description(self) -> str:
        return "Thick hickory-smoked BBQ Beef Burger with Texas toast. 🤠"


class TexasSweetTea(Drink):
    def get_description(self) -> str:
        return "Southern Style Sweet Iced Tea (Extra Sweet!)."


# ==========================================
# STEP 3: DEFINE THE CREATOR (BASE STORE)
# ==========================================

class FranchiseStore(ABC):
    """
    The Corporate HQ class. It defines the workflow but 
    leaves the actual product creation to its subclasses.
    """
    
    # These are the Factory Methods. Subclasses MUST implement these.
    @abstractmethod
    def create_burger(self) -> Burger:
        pass

    @abstractmethod
    def create_drink(self) -> Drink:
        pass

    def serve_combo_meal(self) -> None:
        """
        Core business logic. Notice it relies completely on the 
        factory methods to get the items, without knowing 
        the exact concrete classes.
        """
        burger = self.create_burger()
        drink = self.create_drink()
        
        print("--- Assembling Franchise Combo Meal ---")
        print(f"Main:  {burger.get_description()}")
        print(f"Drink: {drink.get_description()}")
        print("Meal served successfully!\n")


# ==========================================
# STEP 4: IMPLEMENT CONCRETE CREATORS (LOCATIONS)
# ==========================================

class NewYorkFranchise(FranchiseStore):
    """New York location knows how to make NY items."""
    def create_burger(self) -> Burger:
        return NYCStyleBurger()

    def create_drink(self) -> Drink:
        return NYCCraftSoda()


class TexasFranchise(FranchiseStore):
    """Texas location knows how to make Texas items."""
    def create_burger(self) -> Burger:
        return TexasStyleBurger()

    def create_drink(self) -> Drink:
        return TexasSweetTea()


# ==========================================
# STEP 5: CLIENT CODE & RUNTIME EXECUTION
# ==========================================

def order_food(store: FranchiseStore):
    """
    The client code only works with the FranchiseStore interface.
    It has no idea if it's dealing with NY or Texas.
    """
    store.serve_combo_meal()


if __name__ == "__main__":
    print("=== Walked into the New York Store ===")
    ny_store = NewYorkFranchise()
    order_food(ny_store)
    
    print("=== Walked into the Texas Store ===")
    tx_store = TexasFranchise()
    order_food(tx_store)