import argparse
import csv
import logging
import os
import requests

logger = None

def parse_args():
    parser = argparse.ArgumentParser(prog="gen_vcard.py",
                                     description="Generates employee visiting card and qr code")
    parser.add_argument("file", help="Name of output directory")
    parser.add_argument("-v", "--verbose", help="Print detailed logging", action='store_true', default=False)
    parser.add_argument("-n", "--number", help="Number of vcards to generate", action='store', type=int, default=10)
    parser.add_argument("-qr","--qrcode", help ="Generate QR code only",action ='store_true')
    parser.add_argument("-vc","--vcard", help ="Generate vcard  only",action ='store_true')
    args = parser.parse_args()
    return args
                
def setup_logging(log_level):
    global logger
    logger = logging.getLogger("vcard")
    handler = logging.StreamHandler()
    fhandler = logging.FileHandler("run.log")
    fhandler.setLevel(logging.DEBUG)
    handler.setLevel(log_level)
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(asctime)s | %(filename)s:%(lineno)d | %(message)s"))
    fhandler.setFormatter(logging.Formatter("[%(levelname)s] %(asctime)s | %(filename)s:%(lineno)d | %(message)s"))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(fhandler)
    
def input_data(file):
    data = []
    with open(file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
                data.append(row)
    return data

def vcard_content(data):
    first_name, last_name, title, email, phone_number = data
    data = f"""
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
    return data

def generate_vcards(file,number):
    if not os.path.exists('vcards'):   
        os.mkdir('vcards')
    count = 0
    for data in file:
        count +=1
        first_name, last_name, title, email, phone_number = data

        with open(f'vcards/{first_name}{last_name}.vcf', 'w') as f:
            f.write(vcard_content(data))
            logger.debug("%d Generated vcard for %s ", count ,first_name)
        if count >=number:
            break
    logger.info("Vcard generated succesfully")
 
    
def generate_qrcode(data,number): 
    count = 1
    for row in data:
        vcard_list = vcard_content(row)
        first_name, last_name, title, email, phone_number = row

        qrcode = requests.get(f'https://chart.googleapis.com/chart?cht=qr&chs=500x500&chl={vcard_list}')

        with open(f'vcards/{first_name}{last_name}.qr.png', 'wb') as file:
            file.write(qrcode.content)
            logger.debug("%d Generated QR code for %s ", count ,first_name)
            count +=1
        if count >=number:
            break
    logger.info("QR code generated succesfully")

def main():
    args = parse_args()
    if args.verbose:
        setup_logging(logging.DEBUG)
    else:
        setup_logging(logging.INFO)
    file = args.file
    data = input_data(file)
    if args.qrcode:
        generate_qrcode(data,args.number)
    elif args.vcard:
        generate_vcards(data,args.number)
    else:
        generate_vcards(data,args.number)
        generate_qrcode(data,args.number)

if __name__ == '__main__':
    main()
