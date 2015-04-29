#!/usr/bin/env python
#coding = gbk

'''
This python script is use for encrypting our secret text file.
It depends on openssl.

File    : notebook.py 
Author  : Chunjun Li <hevakelcj@gmail.com>
Date    : 2014-12-01

[2014-12-01 V1.0] create and first commit.
[2014-12-21 V1.1] add "decode" operation
'''

import sys
import os
import getpass
import henc

#===============================================================================
usage_template = '''\
Usage: %s create|read|write|decode|chpwd notename\
'''

#===============================================================================
def enc_file(txt_filename, enc_filename, passwd):
    if not os.path.exists(txt_filename):
        pass
    e = henc.HEnc()
    e.SetPasswd(passwd)
    e.Encode(txt_filename, enc_filename)
    del e

def dec_file(enc_filename, txt_filename, passwd):
    if not os.path.exists(enc_filename):
        pass
    e = henc.HEnc()
    e.SetPasswd(passwd)
    e.Decode(enc_filename, txt_filename)
    del e

#===============================================================================
tmp_dir = '/tmp/notebook/'

def make_tmp_dir():
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir, 0700)

def get_txt_filename(notename):
    return tmp_dir + notename + '.txt' 

def get_enc_filename(notename):
    return notename + '.enc' 

def get_passwd():
    return getpass.getpass('Enter password: ')

def get_new_passwd():
    while True:
        passwd = getpass.getpass('Enter new password: ')
        if passwd == getpass.getpass('  Confirm password: '):
            break
        print('WARN: verify failure!')
    return passwd

def ask_yes_or_no(prompt, default_yes):
    if default_yes:
        while True:
            answer = raw_input(prompt + ' [yes]/no: ')
            if answer == '' or answer == 'yes':
                return True
            elif answer == 'no':
                return False
    else:
        while True:
            answer = raw_input(prompt + ' yes/[no]: ')
            if answer == '' or answer == 'no':
                return False
            elif answer == 'yes':
                return True

#===============================================================================
def create_notebook(notename):
    txt_filename = get_txt_filename(notename)
    enc_filename = get_enc_filename(notename)

    if os.path.exists(enc_filename) and \
       not ask_yes_or_no('Notebook exists! Need overwrite?', False):
        return

    passwd = get_new_passwd()
    os.system('touch "%s"; vi "%s"' % (txt_filename, txt_filename))
    enc_file(txt_filename, enc_filename, passwd)
    os.unlink(txt_filename)

def open_notebook(notename, is_save):
    txt_filename = get_txt_filename(notename)
    enc_filename = get_enc_filename(notename)

    if not os.path.exists(enc_filename):
        print('ERROR: %s doesn\'t exist!' % enc_filename)
        return

    passwd = get_passwd()
    dec_file(enc_filename, txt_filename, passwd)
    if is_save:
        os.system('vi "%s"' % txt_filename)
        if ask_yes_or_no('Is need save this modifiction?', True):
            enc_file(txt_filename, enc_filename, passwd)
            print('Saved.')
        else:
            print('Cancel.')
    else:
        os.system('vi -R "%s"' % txt_filename)

    os.unlink(txt_filename)
 
def read_notebook(notename):
    open_notebook(notename, False)

def write_notebook(notename):
    open_notebook(notename, True)

def change_passwd(notename):
    txt_filename = get_txt_filename(notename)
    enc_filename = get_enc_filename(notename)

    if not os.path.exists(enc_filename):
        print('ERROR: %s doesn\'t exist!' % enc_filename)
        return

    old_passwd = get_passwd()
    dec_file(enc_filename, txt_filename, old_passwd)
    os.system('vi "%s"' % txt_filename)
    if ask_yes_or_no('Are you really want change password?', False):
        new_passwd = get_new_passwd()
        enc_file(txt_filename, enc_filename, new_passwd)
        print('Done.')
    else:
        print('Cancel.')
    os.unlink(txt_filename)

def decode_notebook(notename):
    txt_filename = get_txt_filename(notename)
    enc_filename = get_enc_filename(notename)

    if not os.path.exists(enc_filename):
        print('ERROR: %s doesn\'t exist!' % enc_filename)
        return

    passwd = get_passwd()
    dec_file(enc_filename, txt_filename, passwd)
    pass

#===============================================================================
def notebook(operate, notename):
    switch_operate = {'create':create_notebook,\
                      'read'  :read_notebook,\
                      'write' :write_notebook,\
                      'decode':decode_notebook,\
                      'chpwd' :change_passwd}
    try:
        make_tmp_dir()
        switch_operate[operate](notename)
    except KeyError:
        print('ERROR: operate should be "%s".' % '|'.join(switch_operate.keys()))

#===============================================================================
def display_usage():
    print(usage)

#===============================================================================
def test_enc_dec_file():
    print('test_enc_dec_file')
    txt_filename = 'test.txt'
    enc_filename = 'test.enc'
    context = 'Hello'
    passwd = '1234567890'

    f = open(txt_filename, 'w')
    f.write(context)
    f.close()

    enc_file(txt_filename, enc_filename, passwd)
    if not os.path.exists(enc_filename):
        print('TEST ERROR: %s not exist.' % enc_filename)
        return;
    os.unlink(txt_filename)
    dec_file(enc_filename, txt_filename, passwd)
    if not os.path.exists(txt_filename):
        print('TEST ERROR: %s not exist.' % txt_filename)
        return;

    f = open(txt_filename, 'r')
    context_dec = f.read()
    f.close()

    if context == context_dec:
        print('Pass')
    else:
        print('Fail')

    os.unlink(txt_filename)
    os.unlink(enc_filename)

    print('done')

def test_yes_or_no():
    print(ask_yes_or_no('Default Yes', True))
    print(ask_yes_or_no('Default No', False))
    pass

def test():
    test_enc_dec_file()
    test_yes_or_no()
    #TODO

#===============================================================================
if __name__ == '__main__':
    usage = usage_template % sys.argv[0]
    try:
        if len(sys.argv) == 2 and sys.argv[1] == 'test':
            test()
        elif len(sys.argv) == 3:
            notebook(sys.argv[1], sys.argv[2])
        else:
            print('ERROR: argv is not enough')
            display_usage()
    except KeyboardInterrupt:
        print('\nUser interrupt.')
