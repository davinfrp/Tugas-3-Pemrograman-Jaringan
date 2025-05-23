import socket
import json
import base64
import logging

server_address = ('0.0.0.0', 7777)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        data_received = ""  # empty string
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except:
        logging.warning("error during data receiving")
        return False

def remote_list():
    command_str = f"LIST"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal menunjukkan")
        return False

def remote_get(filename=""):
    command_str = f"GET {filename}"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        namafile = hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile, 'wb+')
        fp.write(isifile)
        fp.close()
        return True
    else:
        print("Gagal Mengambil")
        return False

def remote_upload(filename, filedata):
    encoded_data = base64.b64encode(filedata).decode()
    command_str = f"UPLOAD {filename} {encoded_data}"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        print(f"File {filename} berhasil diupload.")
    else:
        print("Gagal upload:", hasil['data'])

def remote_delete(filename):
    command_str = f"DELETE {filename}"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        print(f"File {filename} berhasil dihapus.")
    else:
        print("Gagal menghapus:", hasil['data'])
        
if __name__ == '__main__':
    server_address = ('172.16.16.101', 2727)
    remote_list()
    remote_get('donalbebek.jpg')
    # Contoh upload file
    with open('tes.txt', 'rb') as fp:
        filedata = fp.read()
    remote_upload('tes.txt', filedata)
    # Contoh delete file
    remote_delete('donalbebek.jpg')
    remote_list()
