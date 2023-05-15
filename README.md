# ucsb_rest

Deployment: `docker-compose -f docker-compose.yml up -d --build`

Access: `127.0.0.1:800`

Payload example:
POST:
`http://127.0.0.1:8000/database`
```json
{
  "merge": 1
  "currencies": {
    "FROM_CURRENCY_NAME": {
      "TO_CURRENCY_NAME": 0.01,
      "TO_CURRENCY_NAME_1": 12
    },
    "FROM_CURRENCY_NAME_1": {
      "TO_CURRENCY_NAME_2": 15,
      "TO_CURRENCY_NAME_3": 35,
      "TO_CURRENCY_NAME_4": 15.21
    }
  }
}
````

GET:
`http://127.0.0.1:8000/convert?from=RUB&to=USD&amount=25`
