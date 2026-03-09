class NotFoundException(Exception):
    def __init__(self, detail="Entity"):
        self.detail = f"{detail} not found"
        super().__init__(self.detail)
