import csv

def generate_vcard(file):
    with open(file, 'r') as file:
        reader = csv.reader(file)

        for row in reader:
            first_name, last_name, title, email, phone_number = row

            with open(f'/home/jishnu/employee/vcard/{first_name}{last_name}.vcf', 'w') as f:
                f.write(f"""
BEGIN:VCARD
VERSION:2.1
Name: {last_name};{first_name}
FullName: {first_name} {last_name}
ORG:Authors, Inc.
TITLE: {title}
TEL;WORK;VOICE: {phone_number}
ADR;WORK: 100 Flat Grape Dr.;Fresno;CA;95555;United States of America
EMAIL;PREF;INTERNET: {email}
REV:20150922T195243Z
END:VCARD
""")

def main():
    file = 'employee.csv'
    generate_vcard(file)
    print("vcards generated successfully")

if __name__ == '__main__':
    main()
