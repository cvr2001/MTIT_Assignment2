from data_service import MovieMockDataService

class MovieService:
    def __init__(self):
        self.data_service = MovieMockDataService()

    def get_all(self):
        return self.data_service.get_all_movies()

    def get_by_id(self, movie_id: int):
        return self.data_service.get_movie_by_id(movie_id)

    def create(self, movie_data):
        return self.data_service.add_movie(movie_data)

    def update(self, movie_id: int, movie_data):
        return self.data_service.update_movie(movie_id, movie_data)

    def delete(self, movie_id: int):
        return self.data_service.delete_movie(movie_id)