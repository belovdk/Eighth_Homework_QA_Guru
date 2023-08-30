import pytest
from .models import Product, Cart


@pytest.fixture
def book():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:

    def test_product_check_quantity(self, book):
        assert book.check_quantity(1000)

    def test_product_buy(self, book):
        current_quantity = book.quantity

        book.buy(500)

        assert book.quantity == current_quantity - 500

    def test_product_buy_more_than_available(self, book):
        with pytest.raises(ValueError):
            book.buy(1001)


class TestCart:

    def test_add_product(self, book, cart):
        cart.add_product(book, 1)

        assert cart.products.get(book) == 1

    def test_product_buy(self, book, cart):
        cart.add_product(book, 1)
        cart.buy()

        assert book.quantity == 999
        assert len(cart.products) == 0

    def test_remove_all_products(self, book, cart):
        cart.add_product(book, 1)
        cart.remove_product(book)

        assert len(cart.products) == 0

    def test_remove_more_than_exist_product(self, book, cart):
        cart.add_product(book, 1)
        cart.remove_product(book, 2)

        assert len(cart.products) == 0

    def test_remove_with_no_argument(self, book, cart):
        cart.add_product(book, 1)
        cart.remove_product(book)

        assert len(cart.products) == 0

    def test_get_zero_total_price(self, book, cart):
        assert cart.get_total_price() == 0

    def test_get_total_price(self, book, cart):
        cart.add_product(book, 3)

        assert book.price * 3 == cart.get_total_price()

    def test_clear(self, book, cart):
        cart.add_product(book, 1)

        cart.clear()

        assert len(cart.products) == 0

    def test_buy(self, book, cart):
        cart.add_product(book, 3)

        cart.buy()

        assert len(cart.products) == 0
        assert book.quantity == 997

    def test_buy_more_than_have(self, book, cart):
        cart.add_product(book, 1001)
        with pytest.raises(ValueError):
            cart.buy()
