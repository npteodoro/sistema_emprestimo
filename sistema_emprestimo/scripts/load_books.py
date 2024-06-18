from library.models import Book
import csv

def run():
    with open('../recomendacao/books_data.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        Book.objects.all().delete()

        for row in reader:
            bookID, title, authors, average_rating = row
            print(f"bookID={bookID}, title={title}, authors={authors}, average_rating={average_rating}")

            film = Book(title=title,
                        author=authors,
                        rating=average_rating)
            film.save()
