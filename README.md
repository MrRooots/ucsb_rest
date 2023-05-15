# ucsb_rest

Deployment: `docker-compose -f docker-compose.yml up -d --build`

Payload format:
`
POST:
{
  "merge": int { 1 | 0 }  <- If merge == 0 -> Rewrite __whole__ table
  "currencies": {
    "CURRENCY_NAME": {
      "ANOTHER_CURRENCY_NAME": EXCHANGE_RATE,
      ...
    }
  }
}
`
