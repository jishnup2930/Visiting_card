# from gen_vcard import generate_vcard
# def test_gen_vcard():
#     input_data = [['Acosta', 'Monica', 'Lawyer', 'monic.acost@barnes-stewwart.org', '813.771.3464x71941']]
    
#     expected_output =("""
# BEGIN:VCARD
# VERSION:2.1
# Name: Monica;Acosta
# FullName: Acosta Monica
# ORG:Authors, Inc.
# TITLE: Lawyer
# TEL;WORK;VOICE: 813.771.3464x71941
# ADR;WORK: 100 Flat Grape Dr.;Fresno;CA;95555;United States of America
# EMAIL;PREF;INTERNET: monic.acost@barnes-stewart.org
# REV:20150922T195243Z
# END:VCARD
# """)
#     assert generate_vcard(input_data) == expected_output





from gen_vcard import generate_vcard

def test_gen_vcard():
    input_data = ['Acosta', 'Monica', 'Lawyer', 'monic.acost@barnes-stewwart.org', '813.771.3464x71941']
    
    expected_output = """
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
""".strip()

    # Join the lines of the returned vCard content into a single string
    actual_output = '\n'.join(generate_vcard(input_data).split('\n')).strip()

    assert actual_output == expected_output












# from gen_vcard import generate_vcard

# def test_gen_vcard():
#     input_data = ['Trevino', 'Bryan', 'Gaffer', 'bryan.trevi@waters.info', '373.370.6665x878']

#     # Generate the vCard
#     generate_vcard()

#     # Define the expected output
#     expected_output = f"""
# BEGIN:VCARD
# VERSION:2.1
# Name:Bryan;Trevino
# FullName:Trevino Bryan
# ORG:Authors, Inc.
# TITLE:Gaffer
# TEL;WORK;VOICE:373.370.6665x878
# ADR;WORK:100 Flat Grape Dr.;Fresno;CA;95555;United States of America
# EMAIL;PREF;INTERNET:bryan.trevi@waters.info
# REV:20150922T195243Z
# END:VCARD
# """

#     # Read the generated vCard file
#     with open('/home/jishnu/employee/vcard/BryanTrevino.vcf', 'r') as f:
#         actual_output = f.read()

#     # Remove leading/trailing whitespaces for comparison
#     actual_output = actual_output.strip()
#     expected_output = expected_output.strip()

#     # Compare the actual and expected outputs
#     assert actual_output == expected_output

# # Run the test
# test_gen_vcard()
