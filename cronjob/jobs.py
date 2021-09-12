from book.models import Book, Author


def test_job():
    return


def create_book_job(num_books, author_name, kwarg1=2, kwarg2=3):
    author = Author.objects.create(name='Ramses')

    Book.objects.create()
