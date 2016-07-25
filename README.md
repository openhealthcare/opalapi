opalapi is a Python client for the APIs that [http://opal.openhealthcare.org.uk](OPAL) applications provide.

It is compatible with OPAL applications running on OPAL 0.7.0 or higher.

### Installation:

* Clone this repo
* `pip install -r requirements.txt`

### Authentication

The OPAL API requires that external users pass an API token. You can create these in the Django admin of your
application.

### Usage

```python
from opalapi import Client

c = Client('localhost', '5000', '60f4c45cc0cb0fcc5db6b610f3cee4c36fb52012')
patient = c.get.patient(record_id=1)
print patient.demographics[0]
```
