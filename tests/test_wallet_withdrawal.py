import pytest

from src.wallet_withdrawal import withdraw

# Values that are NOT plain ints. bool is a subclass of int in Python but the
# specification (section 2, rule 2) says booleans are not valid integers.
INVALID_TYPES = [
    pytest.param(1.5, id="float"),
    pytest.param(1.0, id="whole-number-float"),
    pytest.param("1", id="str"),
    pytest.param(None, id="none"),
    pytest.param(True, id="bool-true"),
    pytest.param(False, id="bool-false"),
]


# --- Valid withdrawals (spec 3.1, requirements 1 and 2) -------------------
@pytest.mark.parametrize(
    "balance_cents, amount_cents, expected",
    [
        pytest.param(500, 200, 300, id="regular-withdrawal"),
        pytest.param(500, 1, 499, id="minimum-positive-amount"),
        pytest.param(500, 499, 1, id="one-cent-below-balance"),
        pytest.param(500, 500, 0, id="exact-balance-returns-zero"),
        pytest.param(1, 1, 0, id="smallest-balance-fully-withdrawn"),
        pytest.param(10**12, 1, 10**12 - 1, id="very-large-balance"),
    ],
)
def test_valid_withdrawal_returns_remaining_balance(balance_cents, amount_cents, expected):
    # Arrange: inputs come from the parameters above
    # Act
    result = withdraw(balance_cents, amount_cents)
    # Assert
    assert result == expected
    assert type(result) is int  # output must be an integer number of cents


# --- Invalid values -> ValueError (spec 2 rule 4; spec 3.1 requirement 2) -
@pytest.mark.parametrize(
    "balance_cents, amount_cents",
    [
        pytest.param(500, 501, id="one-cent-above-balance"),
        pytest.param(0, 1, id="positive-amount-from-zero-balance"),
        pytest.param(500, 0, id="zero-amount"),
        pytest.param(0, 0, id="zero-amount-and-zero-balance"),
        pytest.param(500, -1, id="negative-amount"),
        pytest.param(-1, 1, id="negative-balance"),
    ],
)
def test_invalid_value_raises_value_error(balance_cents, amount_cents):
    # Arrange: inputs come from the parameters above
    # Act + Assert
    with pytest.raises(ValueError):
        withdraw(balance_cents, amount_cents)


# --- Invalid types -> TypeError (spec 2 rules 2 and 3) ----------------------
@pytest.mark.parametrize("bad_balance", INVALID_TYPES)
def test_invalid_balance_type_raises_type_error(bad_balance):
    with pytest.raises(TypeError):
        withdraw(bad_balance, 1)


@pytest.mark.parametrize("bad_amount", INVALID_TYPES)
def test_invalid_amount_type_raises_type_error(bad_amount):
    with pytest.raises(TypeError):
        withdraw(500, bad_amount)