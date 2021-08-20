from datetime import datetime, timedelta
import pytest
from PointsManagerHelper import PointManager, InsufficientPoints, InsufficientBalance

#TODO: Give these tests another look over. Also add FastAPI tests
def test_payer_total_does_not_go_negative():
    mngr = PointManager()
    payer = "DANNON"
    amount = 100
    mngr._add_to_payer_amount(payer, amount)
    assert mngr._payer_points_sufficient(payer, -amount * 2) == False

def test_adding_points_returns_exception_if_insuffecient_points():
    mngr = PointManager()
    payer = "DANNON"
    amount = 100
    mngr._add_to_payer_amount(payer, amount)
    with pytest.raises(InsufficientPoints):
        mngr.add_points(payer, -amount*2, datetime.now())

def test_adding_points_returns_expected_payer_total_for_single_payer_added():
    mngr = PointManager()
    payer = "DANNON"
    amount = 100
    mngr.add_points(payer, amount, str(datetime.now()))
    assert mngr.PAYER_TOTALS.get(payer) == amount

def test_adding_points_returns_expected_payer_total_for_same_payer_added_twice():
    mngr = PointManager()
    payer = "DANNON"
    amount = 100
    mngr.add_points(payer, amount, str(datetime.now()))
    mngr.add_points(payer, amount, str(datetime.now()))
    assert mngr.PAYER_TOTALS.get(payer) == amount * 2

def test_adding_points_returns_expected_transaction_history():
    mngr = PointManager()
    payer = "DANNON"
    amount = 100
    mngr.add_points(payer, amount, str(datetime.now()))
    transaction = mngr.TRANSACTIONS_HISTORY[0]
    assert (payer, amount) == (transaction["payer"], transaction["points"])

def test_that_available_balance_is_in_order():
    mngr = PointManager()
    timestamp_first = datetime.now()
    timestamp_second = datetime.now() + timedelta(days=1)
    timestamp_third = datetime.now() + timedelta(days=2)
    mngr._add_to_available_transactions(payer="DANON", amount=1, timestamp=timestamp_first)
    mngr._add_to_available_transactions(payer="YOPLAIT", amount=12, timestamp=timestamp_second)
    mngr._add_to_available_transactions(payer="Yogurt", amount=124, timestamp=timestamp_third)
    expected_timestamp, *_ = mngr.AVAILABLE_TRANSACTIONS[0]
    assert expected_timestamp == str(timestamp_first)

def test_get_balance_returns_no_balance():
    mngr = PointManager()
    assert mngr.get_balance_detailed() == dict(message="No Balance")

def test_get_balance_returns_expected_balance():
    mngr = PointManager()
    payer = "DANNON"
    amount = 100
    mngr.add_points(payer, amount, datetime.now())
    assert mngr.get_balance_detailed() == {payer:amount}

def test_redeem_points_success_from_single_payer():
    mngr = PointManager()
    payer = "Dannon"
    to_put_in = 100
    to_redeem = 5
    mngr.add_points(payer, to_put_in, str(datetime.now()))
    transactions = mngr.redeem_points(to_redeem)
    assert transactions == {payer:-to_redeem}

def test_redeem_points_success_from_two_payers():
    mngr = PointManager()
    to_redeem = 150
    payer_name_one = "Dannon"
    payer_name_two = "Yoplait"
    payer_one = (payer_name_one, 100, datetime.now())
    payer_two = (payer_name_two, 100, datetime.now() + timedelta(days=1))
    mngr.add_points(*payer_one)
    mngr.add_points(*payer_two)

    transactions = mngr.redeem_points(to_redeem)

    assert transactions == {payer_name_one:-100, payer_name_two:-50}

def test_redeem_points_fail_from_two_payers_but_insuffienct_points():
    mngr = PointManager()
    to_redeem = 300
    payer_name_one = "Dannon"
    payer_name_two = "Yoplait"
    payer_one = (payer_name_one, 100, datetime.now())
    payer_two = (payer_name_two, 100, datetime.now())
    mngr.add_points(*payer_one)
    mngr.add_points(*payer_two)

    with pytest.raises(InsufficientBalance):
        mngr.redeem_points(to_redeem)

def test_redeeming_points_returns_exception_if_insuffecient_balance():
    mngr = PointManager()
    payer = "DANNON"
    amount = 100
    mngr._add_to_payer_amount(payer, amount)
    with pytest.raises(InsufficientBalance):
        mngr.redeem_points(amount*2)

def test_redeem_points_successful_and_only_payers_in_order():
    # mngr = PointManager()
    # to_redeem = 300
    # payer_name_one = "Dannon"
    # payer_name_two = "Yoplait"
    # payer_one = (payer_name_one, 100, datetime.now())
    # payer_two = (payer_name_two, 100, datetime.now())
    # mngr.add_points(*payer_one)
    # mngr.add_points(*payer_two)
    #
    # with pytest.raises(InsufficientBalance):
    #     mngr.redeem_points(to_redeem)
    pass
