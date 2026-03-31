from data_service import ShowMockDataService

class ShowService:
    def __init__(self):
        self.data_service = ShowMockDataService()

    def get_all(self):
        return self.data_service.get_all_shows()

    def get_by_id(self, show_id: int):
        return self.data_service.get_show_by_id(show_id)

    def create(self, show_data):
        return self.data_service.add_show(show_data)

    def update(self, show_id: int, show_data):
        return self.data_service.update_show(show_id, show_data)

    def delete(self, show_id: int):
        return self.data_service.delete_show(show_id)