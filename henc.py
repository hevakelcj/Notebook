#!/usr/bin/env python

import os
import base64

tmp_dir = '/tmp/henc/'

tmp_file_1 = tmp_dir + 'tmpfile-1'
tmp_file_2 = tmp_dir + 'tmpfile-2'

def make_tmp_dir():
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir, 0700)

class HEnc:
    _openssl_template = 'openssl enc -%s -in "%s" -out "%s" -k "%s"'

    # Encode or decode file
    # \param enc_dec only can be 'e' or 'd'
    # \param src_filename
    # \param des_filename
    # \param passwd
    # \param cipher
    @staticmethod
    def openssl_enc_dec(enc_dec, src_filename, des_filename, passwd, cipher):
        command = HEnc._openssl_template % (enc_dec, src_filename, des_filename, passwd)
        if cipher != '':
            command += ' -' + cipher
        #print(command)
        os.system(command)

    def __init__(self):
        self._ciphers_sequeue = 'camellia256|seed-cfb|aes256|blowfish|rc4|cast-cbc|des-ecb|base64'
        self._passwd = ''

        make_tmp_dir()

    def SetPasswd(self, passwd):
        self._passwd = passwd
        pass

    @staticmethod
    def gen_key(passwd):
        key = passwd 
        while len(key) < 64:
            key = base64.b64encode(key).strip('=')
        return key 

    def GetCipherAndKeyList(self):
        ciphers = self._ciphers_sequeue.split('|')
        tbl = []
        for cipher in ciphers:
            cipher = cipher.strip()
            key = HEnc.gen_key(cipher + self._passwd)
            tbl.append((cipher, key))
        return tbl

    def Encode(self, src_filename, des_filename):
        cipher_key = self.GetCipherAndKeyList()
        tmp_filename_src = tmp_file_1 
        tmp_filename_des = tmp_file_2
        os.system('cp "%s" "%s"' % (src_filename, tmp_filename_src))
        for (cipher, key) in cipher_key:
            HEnc.openssl_enc_dec('e', tmp_filename_src, tmp_filename_des, key, cipher)
            os.system('mv "%s" "%s"' % (tmp_filename_des, tmp_filename_src))
        os.system('mv "%s" "%s"' % (tmp_filename_src, des_filename))

    def Decode(self, src_filename, des_filename):
        cipher_key = self.GetCipherAndKeyList()
        cipher_key.reverse()
        tmp_filename_src = tmp_file_1
        tmp_filename_des = tmp_file_2
        os.system('cp "%s" "%s"' % (src_filename, tmp_filename_src))
        for (cipher, key) in cipher_key:
            HEnc.openssl_enc_dec('d', tmp_filename_src, tmp_filename_des, key, cipher)
            os.system('mv "%s" "%s"' % (tmp_filename_des, tmp_filename_src))
        os.system('mv "%s" "%s"' % (tmp_filename_src, des_filename))

#-----------------------------------------------------------------------------------------------
def test():
    print('===test===')
    context = 'Hello'
    passwd = 'abc'
    f = open('test.txt', 'w')
    f.write(context)
    f.close()

    henc = HEnc()
    henc.SetPasswd(passwd)
    henc.Encode('test.txt', 'test.enc')
    os.unlink('test.txt')
    henc.Decode('test.enc', 'test.txt')
    os.unlink('test.enc')
    f = open('test.txt', 'r')
    context_now = f.read()
    f.close()

    if context == context_now:
        print('Pass')
    else:
        print('Fail')
    print('===done===')

if __name__ == '__main__':
    test()
