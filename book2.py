from typing import Optional
from fastapi import FastAPI, Body, Path
from pydantic import BaseModel, Field #add validation to each object

app = FastAPI()

class Book():
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: str

    def __init__(self, id, title, author, description, rating, published_date):
      self.id = id
      self.title = title
      self.author = author
      self.description = description
      self.rating = rating  
      self.published_date = published_date


class BookRequest(BaseModel):
   id: Optional[int] = None
   title: str = Field(min_length=3)
   author: str = Field(min_length=1)
   description: str = Field(min_length=1, max_length=100)
   rating: int = Field(gt=-1, lt=6)
   published_date: str

   model_config = {
      "json_schema_extra": {
         "example":{
         "title" : "A new book",
         "author" : "coding with smriti",
         "description" : "A new description of a book",
         "rating":5
      }
      }
   }
        

BOOKS = [
   Book(1, 'Computer Science', 'Smriti Dubey', 'A very nice book', 5, "01-01-2000"),
   Book(2, 'Kubernetes', 'Richa Dubey', 'decent book', 2, "01-01-2001"),
   Book(3, 'Docker', 'Srishti Dubey', 'nice ', 4, "01-01-2001"),
   Book(4, 'Github Actions', 'Ranu Dubey', 'good', 5, "01-01-2010"),
   Book(5, 'Linux', 'Poonam Dubey', 'exellent', 1, "01-01-2100")
]

@app.get('/books')
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}") #get book by id
async def read_book(book_id: int):
   for book in BOOKS:
    if book.id == book_id:
      return book

@app.get("/books_by_rating")
async def read_book_by_rating(book_rating : int):
   books_to_return = []
   for book in BOOKS:
      if book.rating == book_rating:
         books_to_return.append(book)
   return books_to_return

@app.post("/create-book")
async def create_book(book_request: BookRequest): #put the raw JSON body of the request into the variable book_request
  new_book = Book(**book_request.model_dump())
  BOOKS.append(find_book_id(new_book))

@app.put("/books/update_book")
async def update_book (book: BookRequest):
   for i in range (len(BOOKS)):
      if BOOKS[i].id == book.id:
         BOOKS[i] = book


@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt = 0)):
   for i in range (len(BOOKS)):
      BOOKS.pop(i)
      break

@app.get("/books/by_date/{published_date}")   
async def published_date_books(published_date: str):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


def find_book_id(book: Book):
   if len(BOOKS) > 0:
      book.id = BOOKS[-1].id+1  #BOOKS[-1] last book in the dict
   else:
      book.id = 1
   return book
   