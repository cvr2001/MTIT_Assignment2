from models import Booking

class BookingMockDataService:
    def __init__(self):
        self.bookings = [
            Booking(id=1, movie="Avatar", theater="Hall A", seats=2),
            Booking(id=2, movie="Avengers", theater="Hall B", seats=4),
            Booking(id=3, movie="Inception", theater="Hall C", seats=1),
        ]
        self.next_id = 4

    # Get all bookings
    def get_all_bookings(self):
        return self.bookings

    # Get booking by ID
    def get_booking_by_id(self, booking_id: int):
        return next((b for b in self.bookings if b.id == booking_id), None)

    # Add booking
    def add_booking(self, booking_data):
        data = booking_data.model_dump()
        data.pop("id", None)  # Prevent ID override
        new_booking = Booking(id=self.next_id, **data)
        self.bookings.append(new_booking)
        self.next_id += 1
        return new_booking

    # Update booking
    def update_booking(self, booking_id: int, booking_data):
        booking = self.get_booking_by_id(booking_id)
        if booking:
            update_data = booking_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(booking, key, value)
            return booking
        return None

    # Delete booking
    def delete_booking(self, booking_id: int):
        booking = self.get_booking_by_id(booking_id)
        if booking:
            self.bookings.remove(booking)
            return True
        return False