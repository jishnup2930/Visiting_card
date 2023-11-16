import os
import requests
from gen_vcard import parse_data,gen_vcard_content,gen_qrcode_content

def test_get_data():
    test_file = "/tmp/sample.csv"
    with open(test_file, 'w') as f:
        f.write('John,Bob,Lawyer,johnbob@example.com,55454616545\n')
    data = parse_data(test_file)
    assert data == [['John','Bob','Lawyer','johnbob@example.com','55454616545']]
    os.unlink(test_file)

def test_vcard_content(): 
    output = gen_vcard_content('John','Bob','Lawyer','johnbob@example.com','55454616545','100 Flat Grape Dr.;Fresno;CA;95555;United States of America')
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

# def test_gen_qrcode():
#     data = [['John','Bob','Lawyer','johnbob@example.com','55454616545']]
#     size = 500
#     gen_qrcode_content(data)
#     assert os.path.exists('./vcards/JohnBob.qr.png')

def test_gen_qrcode_content():
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

    generated_qr = gen_qrcode_content(vcard, size)

    assert generated_qr == expected_qr_content