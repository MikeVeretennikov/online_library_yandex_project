import requests

def test_get_all_books():
    print(requests.get("http://127.0.0.1:5000/api/books"))


def test_post_book_correct():
    print(requests.post("http://127.0.0.1:5000/api/books", json={
        "title": "test_api",
        "author": "test_api",
        "type_of_fiction_id": 1,
        "genre_id": 1,
        "publish_year":1000,
        "path_to_file": "test"
    }).content)
    

def test_post_book_not_correct():
    print(requests.post("http://127.0.0.1:5000/api/books", json={
        "title": "test_api",
        "type_of_fiction_id": 1,
        "genre_id": 1,
        "publish_year":1000,
        "path_to_file": "test"
    }).content)    
    
    
def test_get_genre_books():
    print(requests.get("http://127.0.0.1:5000/api/genre_books/1").content)



def test_get_author_books():
    print(requests.get("http://127.0.0.1:5000/api/author_books/Л.Н. Толстой").content)
    


test_get_all_books()
test_get_genre_books()
test_post_book_correct()
test_post_book_not_correct()
test_get_author_books()