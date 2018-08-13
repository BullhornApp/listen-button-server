#!/usr/bin/env python

import base64
from xml.sax.saxutils import escape

from carrierx.client import CoreClient
from carrierx.client import MediatorClient
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from site_settings import *

app = Flask(__name__)
CORS(app)

core = CoreClient(
    username=CORE_USERNAME,
    password=CORE_PASSWORD,
    base_url=CORE_BASE_URL,
)

mediator = MediatorClient(
    username=MEDIATOR_USERNAME,
    password=MEDIATOR_PASSWORD,
    base_url=MEDIATOR_BASE_URL,
)


class RequestException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message

    def to_dict(self):
        return {'detail': self.message}


@app.errorhandler(RequestException)
def handle_request_exception(err):
    response = jsonify(err.to_dict())
    response.status_code = err.status_code
    return response


@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    app.logger.info(data)

    if not data:
        raise RequestException('invalid data encoding')

    if not data.get('url'):
        raise RequestException('url not specified')

    url_b64 = base64.b64encode(str.encode(data['url'])).decode('utf8')

    r = mediator.bindings.create(
        destination_did=FLEXML_DID,
        maximum_ttl=MAXIMUM_TTL,
        wait_origination_did_ttl=WAIT_ORIGINATION_DID_TTL,
        attributes={
            'sip_header_X-Playback-URL': url_b64
        }
    )

    return jsonify({"phonenumber": r.redirect_did})


@app.route('/playback', methods=['POST'])
def playback():
    data = request.get_json()
    app.logger.info(data)

    url = base64.b64decode(data['SipHeader_X-Playback-URL']).decode('utf8')

    if INTRO_PROMPT:
        return '''
                <Response>
                    <Play>{}</Play>
                    <Play streaming="true" timeLimit="7200" errorAction="/error">{}</Play>
                </Response>
                '''.format(INTRO_PROMPT, escape(url))
    else:
        return '''
                <Response>
                    <Play streaming="true" timeLimit="7200" errorAction="/error">{}</Play>
                </Response>
                '''.format(escape(url))


@app.route('/error', methods=['POST'])
def stream_error():
    if ERROR_PROMPT:
        return '''
            <Response>
                <Play>{}</Play>
            </Response>
            '''.format(ERROR_PROMPT)
    else:
        return '''
            <Response>
                <Say voice="woman">A playback error has occurred</Say>
            </Response>
            '''


if __name__ == '__main__':
    app.run(host=HTTP_HOST, port=HTTP_PORT, debug=True)
