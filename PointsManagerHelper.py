import heapq
from collections import defaultdict
from datetime import datetime
from typing import List

from PointsManagerExceptions import InsufficientBalance, InsufficientPoints

class PointManager():
    def __init__(self):
        self.PAYER_TOTALS = defaultdict(int)
        self.AVAILABLE_TRANSACTIONS = [] # This will be list for HEAPQ functions
        self.TRANSACTIONS_HISTORY = []

    def _add_to_payer_amount(self, payer:str, amount:int) -> None:
        self.PAYER_TOTALS[payer] += amount

    def _add_to_transaction_history(self, payer:str, amount:int, timestamp: datetime) -> None:
        entry = dict(payer=payer, points=amount, timestamp=str(timestamp))
        self.TRANSACTIONS_HISTORY.append(entry)

    def _add_to_available_transactions(self, payer:str, amount:int, timestamp: datetime) -> None:
        heapq.heappush(self.AVAILABLE_TRANSACTIONS,
                       [str(timestamp), payer, amount]
                       )
    def _get_balance_total(self) -> int:
        return sum(self.PAYER_TOTALS.values())

    def _payer_points_sufficient(self, payer:str, amount:int) -> bool:
        payer_total = self.PAYER_TOTALS[payer]
        processed = payer_total + amount
        return True if processed > 0 else False

    def _total_balance_sufficient(self, amount:int) -> bool:
        processed = self._get_balance_total() - amount
        return True if processed >= 0 else False

    def _redeem_points_logic(self, amount:int):
        """
        The most complicated function, so here is a breakdown:
        1. Does user have enough points in total, if not then don't proceed
        2. Start with the payer that is at the earliest date, that hasn't been spent
           this is determined by a Priority queue, sorted by timestamp. Each item is the points given
           at that time NOT total points available for the payer
        3. Iterate through until we have met the amount
        4. For loop
            - Does top payer have an amount available LESS than the amount we need to give?
              if so, then we can safely use up all of those values and modify whats left to calculate and
              remove from priority queue.
            - if amount available is MORE than amount we want to spend, then we only need to take a part of
              that payer's amount at that time and don't pop out out of priority queue.
            - For both outcomes, we then tally up that payers amount for this transaction
            - Continue looping through until amount to be redeemed is met. This will just be handled by while
              loop, and the amount that is remaing to be redeemed, which is being changed after each loop and transaction
        """
        transactions = defaultdict(int)
        remaining_amount = amount

        while remaining_amount > 0 and self.AVAILABLE_TRANSACTIONS:
            top_of_heap = self.AVAILABLE_TRANSACTIONS[0]
            timestamp, payer, available = top_of_heap
            applied = 0
            if available <= remaining_amount:
                heapq.heappop(self.AVAILABLE_TRANSACTIONS)
                applied = available
            elif available > remaining_amount:
                applied = remaining_amount
                top_of_heap[2] -= remaining_amount
            transactions[payer] -= applied
            remaining_amount -= applied
        return transactions

    def _update_after_redeem_points(self, transactions: List[dict]) -> None:
        current_time = str(datetime.now())
        for payer, points in transactions.items():
            self._add_to_transaction_history(payer, points, current_time)
            self._add_to_payer_amount(payer, points)

    def add_points(self, payer:str, amount:int, timestamp: datetime) -> None:
        if amount < 0 and not self._payer_points_sufficient(payer, amount):
            raise InsufficientPoints(payer, self.PAYER_TOTALS[payer], amount)
        else:
            self._add_to_payer_amount(payer, amount)
            self._add_to_transaction_history(payer, amount, str(datetime.now()))
            self._add_to_available_transactions(payer,amount, timestamp)

    def redeem_points(self, amount):
        if not self._total_balance_sufficient(amount):
            raise InsufficientBalance(self._get_balance_total(), amount)
        transactions = self._redeem_points_logic(amount)
        self._update_after_redeem_points(transactions)
        return dict(transactions)

    def get_balance_detailed(self):
        if not dict(self.PAYER_TOTALS):
            return dict(message="No Balance")
        else:
            return dict(self.PAYER_TOTALS)
