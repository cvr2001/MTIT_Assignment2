from models import Show

class ShowMockDataService:
    def __init__(self):
        self.shows = [
            Show(id=1, movie_id=1, theater_id=1, start_time="2026-03-25 10:00 AM"),
            Show(id=2, movie_id=2, theater_id=2, start_time="2026-03-25 01:30 PM"),
            Show(id=3, movie_id=1, theater_id=3, start_time="2026-03-25 06:00 PM"),
        ]
        self.next_id = 4

    def get_all_shows(self):
        return self.shows

    def get_show_by_id(self, show_id: int):
        return next((s for s in self.shows if s.id == show_id), None)

    def add_show(self, show_data):
        data = show_data.model_dump()
        data.pop("id", None)  # Prevent ID override
        new_show = Show(id=self.next_id, **data)
        self.shows.append(new_show)
        self.next_id += 1
        return new_show

    def update_show(self, show_id: int, show_data):
        show = self.get_show_by_id(show_id)
        if show:
            update_data = show_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(show, key, value)
            return show
        return None

    def delete_show(self, show_id: int):
        show = self.get_show_by_id(show_id)
        if show:
            self.shows.remove(show)
            return True
        return False