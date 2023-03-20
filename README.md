
<h1 align="center">
  Stock Market API Service
  <br>
</h1>


<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
    <a href="#considerations">Considerations</a> •
</p>


## Key Features

* Register a new user
* Log in to generate a token
* Ask for company stock information with token

## How To Use

- Register

```bash
curl --location 'https://market-stock.herokuapp.com/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "stefania",
    "lastname": "arias",
    "email": "sarias@gmail.com",
    "password": "12345678"
}'
```

- Log in 

```bash
curl --location 'http://market-stock.herokuapp.com/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "sarias@gmail.com",
    "password": "12345678"
}'
```

Use the access token to authenticate it has a 24hs lifetime.

```bash
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3OTk1NjU2MiwiaWF0IjoxNjc5MzUxNzYyLCJqdGkiOiJlN2MzZjk0NWFlNjc0MjEzYjg2ODJmODk1NDM3MjhiMSIsInVzZXJfaWQiOjJ9.RJIv8lY8VuM5KkIZobkNX1pcJQtYjajWecOdFmnnd_c",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc5NDM4MTYyLCJpYXQiOjE2NzkzNTE3NjIsImp0aSI6IjBmZDVhY2ZmMDJhOTQzNjViYmMzOGUxMmQ3MmZjN2QzIiwidXNlcl9pZCI6Mn0.KCcMHvdL_YbrJR2m6AeTxAb6YyVgoGOTjDtyFD4tAQo",
    "lifetime": "86400 sec"
}
```

- Ask company stock information

Add stock symbol as query param .../?symbol=META
Use Bearer token authentication

```bash
curl --location 'https://market-stock.herokuapp.com/stock/?symbol=META' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc5NDM4MTYyLCJpYXQiOjE2NzkzNTE3NjIsImp0aSI6IjBmZDVhY2ZmMDJhOTQzNjViYmMzOGUxMmQ3MmZjN2QzIiwidXNlcl9pZCI6Mn0.KCcMHvdL_YbrJR2m6AeTxAb6YyVgoGOTjDtyFD4tAQo' \
--data ''
```

## Considerations

- API throttling: 10/min for anonymous and authenticated users
- Log: drf-api-logger, you can see the logs connecting to the database
