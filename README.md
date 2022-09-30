## ground

This is a simple CRUD Rest API based FastApi & PostgresSql

- Create (idempotent method)
- Get By ID
- Get All (retrive csv file)
- Update
- Delete

## start

```
    docker-compose up
```

## test 
- Create: `PUT http://localhost:8000/api/v1/users`. 
  Simple payload: `{
    "email": "xstest2@gmail.com",
    "description": "test new insert"
}`
- Get By ID: `GET http://localhost:8000/api/v1/users/{userId}`
- Get All (retrive csv file): `GET http://localhost:8000/api/v1/users`
- Update: `PUT http://localhost:8000/api/v1/users/{userId}`
  Simple payload: `{
    "email": "xstest2@gmail.com",
    "description": "test new insert"
}`
- Delete: `DELETE http://localhost:8000/api/v1/users/{userId}`
  
- also can use Postman from `test.postman_collection.json`