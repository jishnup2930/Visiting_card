import csv
import os
import requests

def input_data(file):
    data = []
    with open(file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
                data.append(row)
    return data

def vcard_content(data):
    first_name, last_name, title, email, phone_number = data
    return f"""
BEGIN:VCARD
VERSION:2.1
N: {last_name};{first_name}
FN: {first_name} {last_name}
ORG:Authors, Inc.
TITLE: {title}
TEL;WORK;VOICE: {phone_number}
ADR;WORK: 100 Flat Grape Dr.;Fresno;CA;95555;United States of America
EMAIL;PREF;INTERNET: {email}
REV:20150922T195243Z
END:VCARD
"""

def generate_vcards(file):
    if not os.path.exists('vcards'):
         
        os.mkdir('vcards')
    for data in file:
        first_name, last_name, title, email, phone_number = data

        with open(f'vcards/{first_name}{last_name}.vcf', 'w') as f:
            f.write(vcard_content(data))
        

def generate_qrcode(data): 
        for row in data:
            vcard_list = vcard_content(row)
            first_name, last_name, title, email, phone_number = row

            qrcode = requests.get(f'https://chart.googleapis.com/chart?cht=qr&chs=500x500&chl={vcard_list}')

            with open(f'vcards/{first_name}{last_name}.qr.png', 'wb') as file:
                file.write(qrcode.content)

def main():
    file = './sample_datas/employee.csv'
    data=input_data(file)
    generate_vcards(data)
    generate_qrcode(data)

    print("Visiting cards generated successfully")

if __name__ == '__main__':
    main()
