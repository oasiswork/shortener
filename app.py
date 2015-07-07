import os
import bottle
from bottle import request, abort, response, HTTPResponse
from requests import get
from requests.exceptions import HTTPError
from urllib.parse import quote

app = bottle.app()

# Custom decorator for CORS
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors 


@app.route('/', method=['OPTIONS', 'GET'])
@enable_cors
def get_short_url():
    authorized_ips = os.environ.get('AUTHORIZED_IPS').split(',')
    authorized_origins = os.environ.get('AUTHORIZED_ORIGINS').split(',')
    api_key = os.environ.get('BITLY_KEY')

    if (request.headers.get('X-Forwarded-For') in authorized_ips) or (request.headers.get('Origin') in authorized_origins):
        try:
            r = get('https://api-ssl.bitly.com/v3/shorten?access_token=' + api_key + '&format=txt&longUrl=' + quote(request.query.url))
            r.raise_for_status()
            return r.text
        except HTTPError as e:
            return HTTPResponse(status=r.status_code, body=r.text)
    else:
        abort(401, 'Sorry, access denied. Get your own shortener ;)')

app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)), debug=False, server='cherrypy')
