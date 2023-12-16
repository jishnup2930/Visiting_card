import mock
import requests
from hr import generate_one_vcard,generate_one_qrcode,handle_initdb,HRException

def test_generate_vcard(): 
    data = generate_one_vcard('John','Bob','Junior Engineer','johnbob@example.com','55454616545')
    assert data == f"""
            BEGIN:VCARD
            VERSION:2.1
            N:John;Bob
            FN:Bob John
            ORG:Authors, Inc.
            TITLE:Junior Engineer
            TEL;WORK;VOICE:55454616545
            ADR;WORK:;;100 Flat Grape Dr.;Fresno;CA;95555;United States of America
            EMAIL;PREF;INTERNET:johnbob@example.com
            REV:20150922T195243Z
            END:VCARD"""
            

def test_generate_qrcode():
    lname, fname, designation, email, phone = 'John','Bob','Junior Engineer','johnbob@example.com','55454616545'

    expected_url = requests.get(f'https://chart.googleapis.com/chart?cht=qr&chs=250x250&chl={lname, fname, designation, email, phone}')
    expected_qr_content = expected_url.content

    generated_qr = generate_one_qrcode(lname, fname, designation, email, phone)

    assert generated_qr == expected_qr_content


def test_handle_initdb():
        args = mock.Mock()
        args.dbname = 'hr'


