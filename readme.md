## Learning about PostgreSQL and GCP
This project is the flask server which interacts with a PostgreSQL database hosted on Google App Engine which stores books and authors.
- there are endpoints which allow for CREATE and READ functionality out of CRUD
- this project is not currently live on the server (I've been working locally lately)
- I am building this to learn the concepts necessary to build a product for StudyBuddies (which helps professors create study groups in classes)
- Since this is a learning project with a small team, I am not using GitHub best practices, but I would with a larger team (3+ developers)

## Design Decisions
PostgreSQL > MySQL because more active development, better community  
GCP > AWS because GCP has a nicer UI and is easier to use  
SQLAlchemy has a rich ORM methodology which will make development easier in the long run

## Endpoints
**Base url**:   
localhost:8080/api/v1  
thermal-apricot-305315.uk.r.appspot.com/api/v1

**Get All Books**  
GET /resources/books/all

**Add author**  
POST /people/authors/add
```
{
    "author_first_name": "Michael",
    "author_last_name": "Scott"
}
```
**Add Book**  
POST /resources/books/add
```
{
    "title": "This is a Title",
    "first_sentence": "This is the first sentence",
    "published": 2008,
    "author_first_name": "Michael",
    "author_last_name": "Scott"
}
```

**Get Books from author**  
POST /resources/author_books
- In progress
```
{
    "author_first_name": "Michael",
    "author_last_name": "Scott"
}
```
