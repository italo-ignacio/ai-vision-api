class UnauthorizedException(Exception):
    def __init__(self, detail="Bad credentials"):
        self.detail = detail
        super().__init__(self.detail)
