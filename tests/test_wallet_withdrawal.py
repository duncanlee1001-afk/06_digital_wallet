"""Unit tests for src/wallet_withdrawal.py -> withdraw(balance_cents, amount_cents).

Requirement reference: Digital Wallet specification, sections 2 and 3.1.
Test data was derived with equivalence partitioning and boundary value analysis.
"""
import pytest

from src.wallet_withdrawal import withdraw

# Shared test data for the TypeError tests.
# Each value is NOT a plain int, so the function must reject it with TypeError.
# bool is a subclass of int in Python, but the specification (section 2, rule 2)
# says booleans are not valid integers, so True and False must be rejected too.
INVALID_TYPES = [
    pytest.param(1.5, id="float"),               # decimal number
    pytest.param(1.0, id="whole-number-float"),  # looks like 1 but is a float
    pytest.param("1", id="str"),                 # number written as text
    pytest.param(None, id="none"),               # missing value
    pytest.param(True, id="bool-true"),          # bool must not count as int
    pytest.param(False, id="bool-false"),
]


# ---------------------------------------------------------------------------
# SECTION 1: VALID WITHDRAWALS  (spec 3.1, requirements 1 and 2)
# What it tests: when the inputs are valid, withdraw() returns
# balance - amount as an int, including the edge where the whole balance is
# withdrawn (the result must be 0).
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "balance_cents, amount_cents, expected",
    [
        # Normal case: a typical withdrawal leaves a positive balance.
        pytest.param(500, 200, 300, id="regular-withdrawal"),
        # Lower boundary of amount: the smallest allowed withdrawal (1 cent).
        pytest.param(500, 1, 499, id="minimum-positive-amount"),
        # Upper boundary - 1: one cent less than the balance, 1 cent left over.
        pytest.param(500, 499, 1, id="one-cent-below-balance"),
        # Upper boundary: amount equals balance. Spec says this is allowed and returns 0.
        pytest.param(500, 500, 0, id="exact-balance-returns-zero"),
        # Smallest possible balance that can be fully withdrawn.
        pytest.param(1, 1, 0, id="smallest-balance-fully-withdrawn"),
        # Very large numbers still work (spec only requires whole integers).
        pytest.param(10**12, 1, 10**12 - 1, id="very-large-balance"),
    ],
)
def test_valid_withdrawal_returns_remaining_balance(balance_cents, amount_cents, expected):
    # Arrange: inputs come from the parameters above
    # Act: call the function under test
    result = withdraw(balance_cents, amount_cents)
    # Assert: correct remaining balance...
    assert result == expected
    # ...and the output is an int number of cents (spec 3.1 "Output")
    assert type(result) is int


# ---------------------------------------------------------------------------
# SECTION 2: INVALID VALUES -> ValueError  (spec 2 rule 4; spec 3.1 requirement 2)
# What it tests: the arguments ARE ints, but the value is outside the permitted
# range (amount must be > 0 and <= balance; balance must be >= 0), so the
# function must raise ValueError.
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "balance_cents, amount_cents",
    [
        # Upper boundary + 1: withdrawing more than the balance.
        pytest.param(500, 501, id="one-cent-above-balance"),
        # Nothing to withdraw from: any positive amount exceeds a zero balance.
        pytest.param(0, 1, id="positive-amount-from-zero-balance"),
        # Lower boundary - 1 of amount: zero is not a positive amount.
        pytest.param(500, 0, id="zero-amount"),
        # Zero amount is still invalid even when the balance is also zero.
        pytest.param(0, 0, id="zero-amount-and-zero-balance"),
        # Negative amount is below the permitted range.
        pytest.param(500, -1, id="negative-amount"),
        # Negative balance is below the permitted range (balance must be nonnegative).
        pytest.param(-1, 1, id="negative-balance"),
    ],
)
def test_invalid_value_raises_value_error(balance_cents, amount_cents):
    # Arrange: inputs come from the parameters above
    # Act + Assert: the call must raise ValueError, otherwise the test fails
    with pytest.raises(ValueError):
        withdraw(balance_cents, amount_cents)


# ---------------------------------------------------------------------------
# SECTION 3: INVALID TYPES -> TypeError  (spec 2 rules 2 and 3)
# What it tests: if an argument is not a plain int (float, str, None, bool),
# the function must raise TypeError. One test checks balance_cents and one
# checks amount_cents, with the other argument kept valid, so a failure points
# to the exact parameter that is not being validated.
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("bad_balance", INVALID_TYPES)
def test_invalid_balance_type_raises_type_error(bad_balance):
    # balance_cents has the wrong type; amount_cents (1) is valid
    with pytest.raises(TypeError):
        withdraw(bad_balance, 1)


@pytest.mark.parametrize("bad_amount", INVALID_TYPES)
def test_invalid_amount_type_raises_type_error(bad_amount):
    # amount_cents has the wrong type; balance_cents (500) is valid
    with pytest.raises(TypeError):
        withdraw(500, bad_amount)