def assert_borrows(response, borrows, borrow_in_page=True):
    for borrow in borrows:
        if borrow_in_page:
            assert bytes(borrow.book, encoding='UTF8') in response.data
        else:
            assert not bytes(borrow.book, encoding='UTF8') in response.data
