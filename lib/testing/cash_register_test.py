#!/usr/bin/env python3

from cash_register import CashRegister

import io
import sys

class TestCashRegister:
    '''CashRegister in cash_register.py'''

    def reset_register_totals(self):
        self.cash_register.total = 0
        self.cash_register_with_discount.total = 0

    def setup_method(self):
        self.cash_register = CashRegister()
        self.cash_register_with_discount = CashRegister(20)

    def test_discount_attribute(self):
        '''takes one optional argument, a discount, on initialization.'''
        assert self.cash_register.discount == 0
        assert self.cash_register_with_discount.discount == 20

    def test_total_attribute(self):
        '''sets an instance variable total to zero on initialization.'''
        assert self.cash_register.total == 0
        assert self.cash_register_with_discount.total == 0

    def test_items_attribute(self):
        '''sets an instance variable items to an empty list on initialization.'''
        assert self.cash_register.items == []
        assert self.cash_register_with_discount.items == []

    def test_add_item(self):
        '''accepts a title and a price and increases the total.'''
        self.cash_register.add_item(0.98)
        assert self.cash_register.total == 0.98
        self.reset_register_totals()

    def test_add_item_optional_quantity(self):
        '''also accepts an optional quantity.'''
        self.cash_register.add_item(5.00, 3)
        assert self.cash_register.total == 15.00
        self.reset_register_totals()

    def test_add_item_with_multiple_items(self):
        '''doesn't forget about the previous total'''
        self.cash_register.add_item(4.5)
        assert self.cash_register.total == 4.5
        self.cash_register.add_item(5.0)
        assert self.cash_register.total == 9.5
        self.cash_register.add_item(2.50, 2)
        assert self.cash_register.total == 14.5
        self.reset_register_totals()

    def test_apply_discount(self):
        '''applies the discount to the total price.'''
        self.cash_register_with_discount.add_item(1000)
        self.cash_register_with_discount.apply_discount()   
        assert self.cash_register_with_discount.total == 800
        self.reset_register_totals()

    def test_apply_discount_success_message(self):
        '''prints a success message with the updated total'''
        captured_out = io.StringIO()
        sys.stdout = captured_out
        self.cash_register_with_discount.add_item(1000)
        self.cash_register_with_discount.apply_discount()
        sys.stdout = sys.__stdout__
        actual_output = captured_out.getvalue().strip()  # Remove leading/trailing whitespaces
        expected_output = "After the discount, the total comes to $800.00."
        print("Actual Output:", repr(actual_output))  # Print actual output
        print("Expected Output:", repr(expected_output))  # Print expected output
        assert actual_output == expected_output


    def test_apply_discount_reduces_total(self):
        '''reduces the total'''
        self.cash_register_with_discount.add_item(1000)
        self.cash_register_with_discount.apply_discount()
        assert self.cash_register_with_discount.total == 800
        self.reset_register_totals()

    def test_apply_discount_when_no_discount(self):
        '''prints an error message that there is no discount to apply'''
        captured_out = io.StringIO()
        sys.stdout = captured_out
        self.cash_register.apply_discount()
        sys.stdout = sys.__stdout__
        expected_output = "There is no discount to apply.\n"
        assert captured_out.getvalue().strip() == expected_output

    def test_items_list_without_multiples(self):
        '''returns an array containing all items that have been added'''
        new_register = CashRegister()
        new_register.add_item(1.99)
        new_register.add_item(1.76)
        assert new_register.items == [1.99, 1.76]

    def test_items_list_with_multiples(self):
        '''returns an array containing all items that have been added, including multiples'''
        new_register = CashRegister()
        new_register.add_item(1.99, 2)
        new_register.add_item(1.76, 3)
        assert new_register.items == [1.99, 1.99, 1.76, 1.76, 1.76]

    def test_void_last_transaction(self):
        '''subtracts the last item from the total'''
        self.cash_register.add_item(0.99)
        self.cash_register.add_item(1.76)
        self.cash_register.void_last_transaction()
        assert self.cash_register.total == 0.99
        self.reset_register_totals()

    def test_void_last_transaction_with_multiples(self):
        '''returns the total to 0.0 if all items have been removed'''
        self.cash_register.add_item(1.76, 2)
        self.cash_register.void_last_transaction()
        assert self.cash_register.total == 0.0
        assert self.cash_register.items == []
        self.reset_register_totals()
