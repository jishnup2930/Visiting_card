import argparse
import csv
import logging
import os
import requests

logger = None

def parse_args():
    parser = argparse.ArgumentParser(prog="gen_vcard.py",
                                     description="Generates employee visiting card and qr code")
    parser.add_argument("ipfile",help='Name of input file')
    parser.add_argument("-v", "--verbose", help="Print detailed logging", action='store_true', default=False)
    parser.add_argument("-n", "--number", help="Number of vcards to generate", action='store', type=int, default=10)
    parser.add_argument("-q","--qrcode", help ="Generate vacrd and QR code ",action ='store_true')
    parser.add_argument("-s","--size", help ="Size of QR code",action ='store',type=int,default=500)
    parser.add_argument("-a","--address",help="To give the address in the vcard",action='store',default='100 Flat Grape Dr.;Fresno;CA;95555;United States of America')
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
    
def parse_data(file):
    data = []
    with open(file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
                data.append(row)
    return data

def gen_vcard_content(first_name, last_name, title, email, phone_number,address):
    vcard = f"""
BEGIN:VCARD
VERSION:2.1
N: {last_name};{first_name}
FN: {first_name} {last_name}
ORG:Authors, Inc.
TITLE: {title}
TEL;WORK;VOICE: {phone_number}
ADR;WORK: {address}
EMAIL;PREF;INTERNET: {email}
REV:20150922T195243Z
END:VCARD
"""
    return vcard

def generate_all_vcards(data,number,address):
    if not os.path.exists('vcards'):   
        os.mkdir('vcards')
    count = 0
    for i in data:
        count +=1
        first_name, last_name, title, email, phone_number = i
        vcard=gen_vcard_content(first_name, last_name, title, email, phone_number,address)

        with open(f'vcards/{first_name}{last_name}.vcf', 'w') as f:
            f.write(vcard)
            logger.debug("%d Generated vcard for %s ", count ,first_name)
        if count >=number:
            break
    logger.info("Vcard generated successfully")

def gen_qrcode_content(vcard,size,address):
    qrcode = requests.get(f'https://chart.googleapis.com/chart?cht=qr&chs={size}x{size}&chl={vcard}')
    qr = qrcode.content 
    return qr
    
def generate_all_qrcode(qr,number,size,address): 
    if not os.path.exists('vcards'):   
        os.mkdir('vcards') 
    count = 0
    for data in qr:
        count +=1
        first_name, last_name, title, email, phone_number = data

        with open(f'vcards/{first_name}{last_name}.qr.png', 'wb') as file:
            file.write(gen_qrcode_content(data,size,address))
            logger.debug("%d Generated QR code for %s ", count ,first_name)
        if count >=number:
            break
    logger.info("QR code generated succesfully")

def main():
    args = parse_args()
    if args.verbose:
        setup_logging(logging.DEBUG)
    else:
        setup_logging(logging.INFO)
    file = args.ipfile
    data = parse_data(file)
    if args.qrcode:
        if args.size:
            generate_all_vcards(data,args.number,args.address)   
            generate_all_qrcode(data,args.number,args.size,args.address)
    else:
        generate_all_vcards(data,args.number,args.address)

if __name__ == '__main__':
    main()
