from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum
import threading

class SeatStatus(Enum):
    AVAILABLE = 1
    BOOKED = 2

@dataclass
class Seat:
    seat_no : int
    status = SeatStatus.AVAILABLE
    
class Row:
    def __init__(self, row_label, no_of_seats):
        self.row_label = row_label
        self.seats = [Seat(i + 1) for i in range(no_of_seats)]
        self.lock = threading.RLock() 
    
    def book_seats(self, seats_to_book):
        if any(self.seats[idx].status != SeatStatus.AVAILABLE for idx in seats_to_book):
            return False
        for idx in seats_to_book:
            self.seats[idx].status = SeatStatus.BOOKED
        return True
    
class SeatAllocationStrategy(ABC):
    @abstractmethod
    def allocate(self, seats: list[Seat], num_tickets: int) -> list[int] | None:
        """Returns a list of seat indices to book, or None if allocation fails."""
        pass

class ContiguousSlidingWindow(SeatAllocationStrategy):
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
    def allocate(self, seats: list[Seat], num_tickets: int) -> list[int] | None:
        available_indices = [i for i, seat in enumerate(seats) if seat.status == SeatStatus.AVAILABLE]
        if len(available_indices) >= num_tickets:
            return available_indices[:num_tickets]
        return None

class SeatingOrchestrator:
    def __init__(self, total_rows, seats_per_row, allocation_strategy):
        self.rows = {chr(65 + i): Row(chr(65 + i), seats_per_row) for i in range(total_rows)}
        self.strategy = allocation_strategy
        
    def book_tickets(self, no_of_people):
        for label, row in self.rows.items():
            with row.lock:
                seat_indices = self.strategy.allocate(row.seats, no_of_people)
                
                if seat_indices is not None:
                    if row.book_seats(seat_indices):
                        seat_numbers = [row.seats[idx].seat_no for idx in seat_indices]
                        return f"Successfully booked row {label}, seats: {seat_numbers}"
                        
        return "Booking Failed: Insufficient seats matching your criteria."

def simulate_user_booking(orchestrator : SeatingOrchestrator, no_of_tickets, user_name):
    result = orchestrator.book_tickets(no_of_tickets)
    print(f"[{user_name}]: {result}")
    
contiguous_strategy = ContiguousSlidingWindow()
show_manager = SeatingOrchestrator(total_rows=3, seats_per_row=6, allocation_strategy=contiguous_strategy)


result = show_manager.book_tickets(3)
print(result)
# threads = []

# for i in range(4):
#     t = threading.Thread(
#         target = simulate_user_booking,
#         args = (show_manager, 2, "godwin")
#     )
#     threads.append(t)
#     t.start()

# for t in threads:
#     t.join()


