class CreditSystem:
    DENOMINATIONS = [(5, 18), (2, 7), (1, 3)]  # (dollars, credits)

    def __init__(self):
        self.balance = 0

    def purchase(self, dollars: int) -> int:
        """Add credits for the given dollar amount. Returns new balance."""
        if dollars <= 0:
            raise ValueError("Dollar amount must be positive.")
        remaining = dollars
        for denomination, credits in self.DENOMINATIONS:
            while remaining >= denomination:
                self.balance += credits
                remaining -= denomination
        return self.balance

    def spend(self, amount: int = 1) -> bool:
        """Deduct credits. Returns False if insufficient balance."""
        if self.balance < amount:
            return False
        self.balance -= amount
        return True