from gen_vcard import generate_vcard

def test_gen_vcard():
    # input_data = [['Acosta', 'Monica', 'Lawyer', 'monic.acost@barnes-stewwart.org', '813.771.3464x71941']]
    with open('temp', 'r') as file:
        reader = csv.reader(file)
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
    actual_output = generate_vcard(reader)
    assert actual_output == expected_output

