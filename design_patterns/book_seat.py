from abc import ABC, abstractmethod
from enum import Enum
import threading
from dataclasses import dataclass

# 1. Enums for State Management
class SeatStatus(Enum):
    AVAILABLE = 1
    BOOKED = 2

# 2. Core Entity: Represents an Individual Seat
@dataclass
class Seat:
    seat_no: int
    status: SeatStatus = SeatStatus.AVAILABLE

# 3. Strategy Pattern Interface & Implementations
class SeatAllocationStrategy(ABC):
    @abstractmethod
    def allocate(self, seats: list[Seat], num_tickets: int) -> list[int] | None:
        """Returns a list of seat indices to book, or None if allocation fails."""
        pass

class ContiguousSlidingWindow(SeatAllocationStrategy):
    """Finds the first available consecutive block of seats."""
    def allocate(self, seats: list[Seat], num_tickets: int) -> list[int] | None:
        consecutive_count = 0
        start_idx = 0

        for i, seat in enumerate(seats):
            if seat.status == SeatStatus.AVAILABLE:
                consecutive_count += 1
                if consecutive_count == num_tickets:
                    return list(range(start_idx, i + 1))
            else:
                consecutive_count = 0
                start_idx = i + 1
        return None

class NextAvailableScattered(SeatAllocationStrategy):
    """Finds any available seats, even if they aren't next to each other."""
    def allocate(self, seats: list[Seat], num_tickets: int) -> list[int] | None:
        available_indices = [i for i, seat in enumerate(seats) if seat.status == SeatStatus.AVAILABLE]
        if len(available_indices) >= num_tickets:
            return available_indices[:num_tickets]
        return None

# 4. Structural Component: Row-level management
class Row:
    def __init__(self, row_label: str, num_seats: int):
        self.row_label = row_label
        self.seats = [Seat(i + 1) for i in range(num_seats)]
        # CRITICAL FIX: Changed to RLock to prevent self-deadlock during double acquisition
        self.lock = threading.RLock() 

    def book_seats(self, seat_indices: list[int]) -> bool:
        """Atomic booking action protected by the row's reentrant lock."""
        with self.lock:
            # Check-and-Act safety check
            if any(self.seats[idx].status != SeatStatus.AVAILABLE for idx in seat_indices):
                return False
            
            # Commit booking state
            for idx in seat_indices:
                self.seats[idx].status = SeatStatus.BOOKED
            return True

# 5. Orchestrator Component: The Seating Layout Manager
class SeatingShowManager:
    def __init__(self, total_rows: int, seats_per_row: int, allocation_strategy: SeatAllocationStrategy):
        self.rows = {chr(65 + i): Row(chr(65 + i), seats_per_row) for i in range(total_rows)}
        self.strategy = allocation_strategy  # Dynamic Strategy Injection

    def book_tickets(self, num_tickets: int) -> str | None:
        """Scans the theater rows applying the injected allocation strategy."""
        for label, row in self.rows.items():
            with row.lock:
                # Delegate the searching algorithm to the strategy
                seat_indices = self.strategy.allocate(row.seats, num_tickets)
                
                if seat_indices is not None:
                    if row.book_seats(seat_indices):
                        seat_numbers = [row.seats[idx].seat_no for idx in seat_indices]
                        return f"Successfully booked row {label}, seats: {seat_numbers}"
                        
        return "Booking Failed: Insufficient seats matching your criteria."

# --- Concurrency Simulation Testing ---
def simulate_user_booking(manager: SeatingShowManager, num_tickets: int, user_name: str):
    result = manager.book_tickets(num_tickets)
    print(f"[{user_name}]: {result}")

if __name__ == "__main__":
    print("--- Initializing Movie Seating Manager with Strategy Pattern ---")
    
    # We can inject whichever algorithm we want right here
    contiguous_strategy = ContiguousSlidingWindow()
    show_manager = SeatingShowManager(total_rows=3, seats_per_row=6, allocation_strategy=contiguous_strategy)

    threads = []
    for i in range(4):
        t = threading.Thread(
            target=simulate_user_booking, 
            args=(show_manager, 13, f"User_{i+1}")
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()