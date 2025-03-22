from app.repositories.mark import MarkRepository


class MarkService:
    def __init__(self, mark_repository):
        
        self.mark_repository = mark_repository