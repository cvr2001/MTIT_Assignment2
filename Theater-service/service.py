from data_service import TheaterMockDataService

class TheaterService:
    def __init__(self):
        self.data_service = TheaterMockDataService()

    def get_all(self):
        return self.data_service.get_all_theaters()

    def get_by_id(self, theater_id: int):
        return self.data_service.get_theater_by_id(theater_id)

    def create(self, theater_data):
        return self.data_service.add_theater(theater_data)

    def update(self, theater_id: int, theater_data):
        return self.data_service.update_theater(theater_id, theater_data)

    def delete(self, theater_id: int):
        return self.data_service.delete_theater(theater_id)