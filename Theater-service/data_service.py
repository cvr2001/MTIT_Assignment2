from models import Theater

class TheaterMockDataService:
    def __init__(self):
        self.theaters = [
            Theater(id=1, name="Hall A", capacity=150, screen_type="Standard"),
            Theater(id=2, name="IMAX Hall", capacity=250, screen_type="IMAX 3D"),
            Theater(id=3, name="VIP Lounge", capacity=30, screen_type="Standard VIP"),
        ]
        self.next_id = 4

    def get_all_theaters(self):
        return self.theaters

    def get_theater_by_id(self, theater_id: int):
        return next((t for t in self.theaters if t.id == theater_id), None)

    def add_theater(self, theater_data):
        data = theater_data.model_dump()
        data.pop("id", None)  # Prevent ID override
        new_theater = Theater(id=self.next_id, **data)
        self.theaters.append(new_theater)
        self.next_id += 1
        return new_theater

    def update_theater(self, theater_id: int, theater_data):
        theater = self.get_theater_by_id(theater_id)
        if theater:
            update_data = theater_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(theater, key, value)
            return theater
        return None

    def delete_theater(self, theater_id: int):
        theater = self.get_theater_by_id(theater_id)
        if theater:
            self.theaters.remove(theater)
            return True
        return False