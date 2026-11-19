"""Unit tests for src/wallet_affordability.py -> can_afford(balance_cents, price_cents).

Requirement reference: Digital Wallet specification, sections 2 and 3.2.
Test data was derived with equivalence partitioning and boundary value analysis.
"""
import pytest

from src.wallet_affordability import can_afford

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
# SECTION 1: VALID INPUTS  (spec 3.2, requirements 1 and 2)
# What it tests: can_afford() returns True when balance >= price and False when
# balance < price, around the boundary where balance == price. The result must
# be the real bool True/False, not the integers 1/0 (spec 3.2 "Output").
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "balance_cents, price_cents, expected",
    [
        # Boundary + 1: balance is one cent more than the price -> affordable.
        pytest.param(501, 500, True, id="balance-one-cent-above-price"),
        # Boundary: balance equals price. Spec says >= so this is affordable.
        pytest.param(500, 500, True, id="balance-equal-to-price"),
        # Boundary - 1: balance is one cent short -> not affordable.
        pytest.param(499, 500, False, id="balance-one-cent-below-price"),
        # Empty wallet cannot pay a positive price.
        pytest.param(0, 1, False, id="zero-balance-positive-price"),
        # A zero price is always affordable.
        pytest.param(500, 0, True, id="positive-balance-zero-price"),
        # Spec: a zero price is affordable even when the balance is zero.
        pytest.param(0, 0, True, id="zero-balance-zero-price"),
    ],
)
def test_valid_inputs_return_expected_boolean(balance_cents, price_cents, expected):
    # Arrange: inputs come from the parameters above
    # Act: call the function under test
    result = can_afford(balance_cents, price_cents)
    # Assert: `is` checks for the exact True/False object. `==` would wrongly
    # accept 1 or 0, because 1 == True and 0 == False in Python.
    assert result is expected


# ---------------------------------------------------------------------------
# SECTION 2: INVALID VALUES -> ValueError  (spec 2 rule 4; spec 3.2 constraints)
# What it tests: the arguments ARE ints but negative. Both balance_cents and
# price_cents must be nonnegative, so the function must raise ValueError.
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "balance_cents, price_cents",
    [
        # Lower boundary - 1 of balance (price is valid).
        pytest.param(-1, 0, id="negative-balance"),
        # Lower boundary - 1 of price (balance is valid).
        pytest.param(500, -1, id="negative-price"),
        # Both arguments are out of range.
        pytest.param(-1, -1, id="negative-balance-and-price"),
    ],
)
def test_negative_value_raises_value_error(balance_cents, price_cents):
    # Act + Assert: the call must raise ValueError, otherwise the test fails
    with pytest.raises(ValueError):
        can_afford(balance_cents, price_cents)


# ---------------------------------------------------------------------------
# SECTION 3: INVALID TYPES -> TypeError  (spec 2 rules 2 and 3)
# What it tests: if an argument is not a plain int (float, str, None, bool),
# the function must raise TypeError. One test checks balance_cents and one
# checks price_cents, with the other argument kept valid, so a failure points
# to the exact parameter that is not being validated.
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("bad_balance", INVALID_TYPES)
def test_invalid_balance_type_raises_type_error(bad_balance):
    # balance_cents has the wrong type; price_cents (1) is valid
    with pytest.raises(TypeError):
        can_afford(bad_balance, 1)


@pytest.mark.parametrize("bad_price", INVALID_TYPES)
def test_invalid_price_type_raises_type_error(bad_price):
    # price_cents has the wrong type; balance_cents (500) is valid
    with pytest.raises(TypeError):
        can_afford(500, bad_price)