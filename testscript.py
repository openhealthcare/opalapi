"""
Test script for OPAL API
"""
from opalapi import Client

c = Client('localhost', '5000', '60f4c45cc0cb0fcc5db6b610f3cee4c36fb52012')
print 'Getting patient'
patient = c.get.patient(record_id=1)
print 'Printing demographics'
print patient.demographics[0]
print 'Getting demographics independently'
demographics = c.get.demographics(record_id=patient.demographics[0].id)
print 'Printing independent demographics'
print demographics
