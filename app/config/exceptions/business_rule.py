class BusinessRuleException(Exception):
    def __init__(self, detail="Bad request"):
        self.detail = detail
        super().__init__(self.detail)
