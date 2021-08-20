class InsufficientPoints(Exception):
    def __init__(self, payer, payer_points, amount):
        self.message = f"Payer: '{payer}'. Payer Points: '{payer_points}'. Amount to be Added: '{amount}'"
        super().__init__(self.message)

class InsufficientBalance(Exception):
    def __init__(self, balance, amount):
        self.message = f"Current Point Balance '{balance}'. Amount to be Redeemed: '{amount}'"
        super().__init__(self.message)
