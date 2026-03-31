from models import Movie

class MovieMockDataService:
    def __init__(self):
        self.movies = [
            Movie(id=1, title="Avatar", director="James Cameron", genre="Sci-Fi", duration_minutes=162, language="English"),
            Movie(id=2, title="Your Name", director="Makoto Shinkai", genre="Anime/Romance", duration_minutes=106, language="Japanese"),
            Movie(id=3, title="Inception", director="Christopher Nolan", genre="Thriller", duration_minutes=148, language="English"),
        ]
        self.next_id = 4

    # Get all movies
    def get_all_movies(self):
        return self.movies

    # Get movie by ID
    def get_movie_by_id(self, movie_id: int):
        return next((m for m in self.movies if m.id == movie_id), None)

    # Add new movie
    def add_movie(self, movie_data):
        data = movie_data.model_dump()
        data.pop("id", None)  # Prevent ID override
        new_movie = Movie(id=self.next_id, **data)
        self.movies.append(new_movie)
        self.next_id += 1
        return new_movie

    # Update movie
    def update_movie(self, movie_id: int, movie_data):
        movie = self.get_movie_by_id(movie_id)
        if movie:
            update_data = movie_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(movie, key, value)
            return movie
        return None

    # Delete movie
    def delete_movie(self, movie_id: int):
        movie = self.get_movie_by_id(movie_id)
        if movie:
            self.movies.remove(movie)
            return True
        return False