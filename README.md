# URL Shortener app

Small app (bottle + CherryPy) to act as a gateway to Bit.ly  
It provides a auth-free shortening service to JS apps.

To avoid abuse, the app will only allow requests to pre-defined source IPs or Origins.

This is designed to run on Heroku with the following env vars :

* AUTHORIZED_IPS: comma-separated IPs without CIDR
* AUTHORIZED_ORIGINS: comma-sparated URLs with http(s)://
* BITLY_KEY: your Bit.ly API Key
