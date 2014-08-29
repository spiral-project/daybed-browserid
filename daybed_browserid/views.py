# -*- coding: utf-8 -*-
import json
import logging
import requests

from browserid.utils import decode_bytes
from cornice import Service
from daybed.tokens import get_hawk_credentials
from daybed.views.errors import forbidden_view
from daybed_browserid.backends.exceptions import UserIdNotFound
from pyramid.httpexceptions import HTTPBadRequest

logger = logging.getLogger(__name__)


bid = Service(name='browserid', path='/tokens/browserid',
              description='Endpoint to get your BID specific token')


@bid.post(permission='post_token')
def post_browserid(request):
    """Get or create a token for this Assertion"""

    db = request.registry.browserid_db

    if 'assertion' in request.POST:
        # Persona login
        assertion = request.POST['assertion']
    elif 'Authorization' in request.headers and \
         request.headers['Authorization'].lower().startswith('browserid'):
        assertion = request.headers['Authorization'].split()[1]
    else:
        return forbidden_view()

    audience = json.loads(decode_bytes(assertion.split('.')[3]))['aud']

    if audience not in request.registry['browserid.audiences']:
        raise HTTPBadRequest('Invalid audience')

    r = requests.post(request.registry['browserid.verifier_url'],
                      data=json.dumps({'assertion': assertion,
                                       'audience': audience}),
                      headers={'Content-Type': 'application/json'})
    if r.status_code == 500:
        raise HTTPBadRequest('An error occured: %s' % r.content)

    data = r.json()
    print data

    if data['issuer'] not in request.registry['browserid.trusted_issuers']:
        raise HTTPBadRequest(
            '%s is not configured as a trusted issuer.' % data['issuer']
        )

    user_id = data['email']

    is_new = False
    try:
        token = db.get_user_token(user_id)
    except UserIdNotFound:
        is_new = True
        token = None

    token, credentials = get_hawk_credentials(token)

    if is_new:
        db.store_user_token(user_id, token)
        request.db.store_token(token, credentials)
        request.response.status = "201 Created"

    return {
        'token': token,
        'credentials': credentials
    }
