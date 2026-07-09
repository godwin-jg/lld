from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount : float) -> bool:
        pass
    @abstractmethod
    def work(self):
        pass

class StripProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print("Connecting to Stript to charge payment...")
        return True
    
class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f"Redirecting to PayPal token authorization for ${amount}...")
        return True