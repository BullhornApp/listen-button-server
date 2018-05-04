# Listen Button Server

REST backend server for [Listen Button Widget](https://github.com/BullhornApp/listen-button-widget)

## Getting Started

We use Flask and the [CarrierX Python Bindings](https://github.com/carrierx/carrierx-python) to
create a simple web service that utilizes both Mediator and FlexML application endpoints within the
same call-flow.  We also demonstrate passing small amounts of data between services using custom
SIP headers.

By changing the FlexML returned, you can fully customize the call-flow to suit your application
requirements.

## Prerequisites

* Python 3.4+
* CarrierX account credentials
* One phone number routed to a FlexML endpoint.  This number will only be used internally.
* Pool of phone numbers routed to a Mediator endpoint.  We recommend at least 10 numbers.
* RELAY_SIP_HEADERS must be enabled on your FlexML trunk by customer service.

## Installing

* Clone repository and install requirements

```
git clone https://github.com/BullhornApp/listen-button-server.git
cd listen-button-server
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```
* Modify app/site_settings.py.template and save as app/site_settings.py
* Set the FlexML URL on the DID assigned to the FlexML endpoint to the location you will be running
this service.
* Run the application in development mode as ./app/ws.py or in production mode using uWSGI.  An
example systemd unit file is included in the etc/ directory.

## Making a request

```
curl http://localhost:8080/create -H 'Content-type: application/json' -X POST \
  --data-binary '{"url":"http://example.com/path/to/media.mp3"}'
```

## License

Code licensed under the MIT License: http://opensource.org/licenses/MIT
