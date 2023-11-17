import os
import requests
from gen_vcard import read_data,generate_vcard_content,generate_qrcode_content

def test_get_data():
    test_file = "/tmp/sample.csv"
    with open(test_file, 'w') as f:
        f.write('John,Bob,Lawyer,johnbob@example.com,55454616545\n')
    data = read_data(test_file)
    assert data == [['John','Bob','Lawyer','johnbob@example.com','55454616545']]
    os.unlink(test_file)

def test_generate_vcard_content(): 
    data = generate_vcard_content('John','Bob','Lawyer','johnbob@example.com','55454616545','100 Flat Grape Dr.;Fresno;CA;95555;United States of America')
    assert data == """
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

def test_generate_qrcode_content():
    size = 500
    vcard = """
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
    expected_url = requests.get(f'https://chart.googleapis.com/chart?cht=qr&chs={size}x{size}&chl={vcard}')
    expected_qr_content = expected_url.content

    generated_qr = generate_qrcode_content(vcard, size)

    assert generated_qr == expected_qr_content