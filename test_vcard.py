from gen_vcard import generate_vcard
import os

def test_gen_vcard():
    with open('temp.csv', 'w') as file:
        file.write('Acosta, Monica, Lawyer, monic.acost@barnes-stewwart.org, 813.771.3464x71941')
    generate_vcard('temp.csv')
    with open ('vcard/AcostaMonica.vcf','r') as f:
        vcard = f.read()

        assert os.path.exists('vcard/AcostaMonica.vcf')

        expected_output =("""
BEGIN:VCARD
VERSION:2.1
Name: Monica;Acosta
FullName: Acosta Monica
ORG:Authors, Inc.
TITLE: Lawyer
TEL;WORK;VOICE: 813.771.3464x71941
ADR;WORK: 100 Flat Grape Dr.;Fresno;CA;95555;United States of America
EMAIL;PREF;INTERNET: monic.acost@barnes-stewart.org
REV:20150922T195243Z
END:VCARD
""")
    assert vcard == expected_output
