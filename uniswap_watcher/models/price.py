class Price:
    def __init__(self, token_1: str, token_2: str, amount: float, time: str):
        self.token_1 = token_1
        self.token_2 = token_2
        self.amount = amount
        self.time = time

    def to_dict(self):
        return {
            "token_1": self.token_1,
            "token_2": self.token_2,
            "amount": self.amount,
            "time": self.time
        }
