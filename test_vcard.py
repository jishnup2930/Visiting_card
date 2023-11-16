import os
from gen_vcard import input_data,generate_vcards,vcard_content,generate_qrcode

def test_get_data():
    test_file = "/tmp/sample.csv"
    with open(test_file, 'w') as f:
        f.write('John,Bob,Lawyer,johnbob@example.com,55454616545\n')
    data = input_data(test_file)
    assert data == [['John','Bob','Lawyer','johnbob@example.com','55454616545']]
    os.unlink(test_file)

def test_vcard_content():
    
    data = 'John','Bob','Lawyer','johnbob@example.com','55454616545'
    output = vcard_content(data)
    assert output == """
BEGIN:VCARD
VERSION:2.1
N: Bob;John
FN: John Bob
ORG:Authors, Inc.
TITLE: Lawyer
TEL;WORK;VOICE: 55454616545
ADR;WORK: 100 Flat Grape Dr.;Fresno;CA;95555;United States of America
EMAIL;PREF;INTERNET: johnbob@example.com
REV:20150922T195243Z
END:VCARD
"""
