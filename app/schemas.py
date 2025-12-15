from pydantic import BaseModel 

class BookBase(BaseModel): 
    title: str 
class BookCreate(BookBase): 
    author_id: int 
class Book(BookBase): 
    id: int 
    class Config: 
        orm_mode = True

class AuthorBase(BaseModel): 
    name: str 
class AuthorCreate(AuthorBase): 
    pass 
class Author(AuthorBase): 
    id: int 
    books: list[Book] = [] 
    class Config: 
        orm_mode = True
