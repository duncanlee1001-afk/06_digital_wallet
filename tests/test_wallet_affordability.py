"""Unit tests for src/wallet_affordability.py -> can_afford(balance_cents, price_cents).

Requirement reference: Digital Wallet specification, sections 2 and 3.2.
Test data was derived with equivalence partitioning and boundary value analysis.
"""
import pytest

from src.wallet_affordability import can_afford

# bool is a subclass of int in Python but the specification (section 2, rule 2)
# says booleans are not valid integers, so they must be rejected too.
INVALID_TYPES = [
    pytest.param(1.5, id="float"),
    pytest.param(1.0, id="whole-number-float"),
    pytest.param("1", id="str"),
    pytest.param(None, id="none"),
    pytest.param(True, id="bool-true"),
    pytest.param(False, id="bool-false"),
]


# --- Valid inputs (spec 3.2, requirements 1 and 2; output must be a real bool)
@pytest.mark.parametrize(
    "balance_cents, price_cents, expected",
    [
        pytest.param(501, 500, True, id="balance-one-cent-above-price"),
        pytest.param(500, 500, True, id="balance-equal-to-price"),
        pytest.param(499, 500, False, id="balance-one-cent-below-price"),
        pytest.param(0, 1, False, id="zero-balance-positive-price"),
        pytest.param(500, 0, True, id="positive-balance-zero-price"),
        pytest.param(0, 0, True, id="zero-balance-zero-price"),
    ],
)
def test_valid_inputs_return_expected_boolean(balance_cents, price_cents, expected):
    # Arrange: inputs come from the parameters above
    # Act
    result = can_afford(balance_cents, price_cents)
    # Assert: `is` makes sure we get the real True/False, not 1/0
    assert result is expected


# --- Invalid values -> ValueError (spec 2 rule 4; spec 3.2 constraints) -----
@pytest.mark.parametrize(
    "balance_cents, price_cents",
    [
        pytest.param(-1, 0, id="negative-balance"),
        pytest.param(500, -1, id="negative-price"),
        pytest.param(-1, -1, id="negative-balance-and-price"),
    ],
)
def test_negative_value_raises_value_error(balance_cents, price_cents):
    with pytest.raises(ValueError):
        can_afford(balance_cents, price_cents)


# --- Invalid types -> TypeError (spec 2 rules 2 and 3) -----------------------
@pytest.mark.parametrize("bad_balance", INVALID_TYPES)
def test_invalid_balance_type_raises_type_error(bad_balance):
    with pytest.raises(TypeError):
        can_afford(bad_balance, 1)


@pytest.mark.parametrize("bad_price", INVALID_TYPES)
def test_invalid_price_type_raises_type_error(bad_price):
    with pytest.raises(TypeError):
        can_afford(500, bad_price)
