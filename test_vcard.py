import os
from gen_vcard import input_data,generate_vcards

def test_get_data():
    test_file = "/tmp/sample.csv"
    with open(test_file, 'w') as f:
        f.write('John,Bob,Lawyer,johnbob@example.com,55454616545\n')
    data = input_data(test_file)
    assert data == [['John','Bob','Lawyer','johnbob@example.com','55454616545']]
    os.unlink(test_file)

def test_generate_vcards():
    data = [['John','Bob','Lawyer','johnbob@example.com','55454616545']]
    generate_vcards(data)
    with open('./vcards/JohnBob.vcf', 'r') as f:
        vcard = f.read()
    assert os.path.exists('./vcards/JohnBob.vcf')
    assert f"""
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
""" in vcard
    os.unlink('./vcards/JohnBob.vcf')