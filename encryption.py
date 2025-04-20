from cryptography.fernet import Fernet
import hashlib
import base64


def gen_file(password):
    '''
    Generates a file to store the passwords in.

    Params:
        password: the master password (or PIN) used for authentication and encryption.

    Returns:
        Void
    '''
    file = open("passwords","w")
    file.write(base64.b64encode(hashlib.sha512(password.encode('utf-8')).digest()).decode("utf-8"))
    file.write('\n')
    key = base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest())
    file.write(Fernet(key).encrypt("0".encode('utf-8')).decode('utf-8'))
    file.write('\n')
    file.write(Fernet(key).encrypt("".encode('utf-8')).decode('utf-8'))
    file.write('\n')
    file.write(Fernet(key).encrypt("dummy entry".encode('utf-8')).decode('utf-8'))
    file.write('\n')
    file.close()

def read_services(password):
    '''
    Reads all of the tites / services stored in the passwords file with their info descriptions, indexed by ID

    Params:
        password: the master password (or PIN) used for authentication and encryption.
    
    Returns:
        (servs[1:],info[1:]): a tuple containing the service names and their info, indexed by ID, 
            excluding dummy entries. 
    '''
    file = open("passwords","r")
    pwfile = file.readlines()
    file.close()
    if base64.b64encode(hashlib.sha512(password.encode('utf-8')).digest()).decode("utf-8") == pwfile[0][:-1]:
        key = base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest())
        #serv_count = int(Fernet(key).decrypt(pwfile[1][:-1].encode('utf-8')).decode('utf-8'))
        servs = Fernet(key).decrypt(pwfile[2][:-1].encode('utf-8')).decode('utf-8').split(",")
        info = Fernet(key).decrypt(pwfile[3][:-1].encode('utf-8')).decode('utf-8').split("\t\n\t")
        return (servs[1:],info[1:])

def add_service(password,service,serv_name,serv_pass,info='\n'):
    '''
    Adds a service to the passwords file
    Params:
        password: the master password (or PIN) used for authentication and encryption.
        service: name of the service, or custon title of entry
        serv_name: the username to be used for login
        serv_pass: the password used for login on this specific service
        info: a short blurb to be viewd with the service name\
            Optional, default: "\n"

    Returns:
        Void
        

    '''
    file = open("passwords","r")
    pwfile = file.readlines()
    file.close()
    if base64.b64encode(hashlib.sha512(password.encode('utf-8')).digest()).decode("utf-8") == pwfile[0][:-1]:
        key = base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest())
        serv_count = int(Fernet(key).decrypt(pwfile[1][:-1].encode('utf-8')).decode('utf-8'))
        servs = Fernet(key).decrypt(pwfile[2][:-1].encode('utf-8')).decode('utf-8').split(",")
        infos = Fernet(key).decrypt(pwfile[3][:-1].encode('utf-8')).decode('utf-8').split("\t\n\t")
        servs.append(service)
        infos.append(info)
        pwfile.append(f"{base64.b64encode(hashlib.sha512(service.encode('utf-8')).digest()).decode("utf-8")}\n")
        pwfile.append(f"{Fernet(key).encrypt(serv_name.encode('utf-8')).decode('utf-8')}\n")
        pwfile.append(f"{Fernet(key).encrypt(serv_pass.encode('utf-8')).decode('utf-8')}\n")
        servs_txt = ",".join(servs)
        info_txt = "\t\n\t".join(infos)
        pwfile[1] = f"{Fernet(key).encrypt(str(len(servs)).encode('utf-8')).decode('utf-8')}\n"
        pwfile[2] = f"{Fernet(key).encrypt(servs_txt.encode('utf-8')).decode('utf-8')}\n"
        pwfile[3] = f"{Fernet(key).encrypt(info_txt.encode('utf-8')).decode('utf-8')}\n"
        file = open("passwords","w")
        for line in pwfile:
            file.write(line)
        file.close()

def remove_service(password,id):
    '''
    Removes a service from the passwords file

    Params:
        password: the master password (or PIN) used for authentication and encryption.
        id: the sequential ID of the entry being removed. 

    Returns:
        Void

    '''
    file = open("passwords","r")
    pwfile = file.readlines()
    file.close()
    if base64.b64encode(hashlib.sha512(password.encode('utf-8')).digest()).decode("utf-8") == pwfile[0][:-1]:
        key = base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest())
        serv_count = int(Fernet(key).decrypt(pwfile[1][:-1].encode('utf-8')).decode('utf-8'))
        servs = Fernet(key).decrypt(pwfile[2][:-1].encode('utf-8')).decode('utf-8').split(",")
        infos = Fernet(key).decrypt(pwfile[3][:-1].encode('utf-8')).decode('utf-8').split("\t\n\t")
        del servs[id]
        del infos [id]
        for i in range(0,3):
            del pwfile [4 + id * 3 + i]

        servs_txt = ",".join(servs)
        info_txt = "\t\n\t".join(infos)
        pwfile[1] = f"{Fernet(key).encrypt(str(len(servs)).encode('utf-8')).decode('utf-8')}\n"
        pwfile[2] = f"{Fernet(key).encrypt(servs_txt.encode('utf-8')).decode('utf-8')}\n"
        pwfile[3] = f"{Fernet(key).encrypt(info_txt.encode('utf-8')).decode('utf-8')}\n"
        file = open("passwords","w")
        for line in pwfile:
            file.write(line)
        file.close()

def read_data_by_service(password,service):
    '''
    Reads the encrypted data from the password file, given the service name

    Params:
        password: the master password (or PIN) used for authentication and encryption.
        service: the name of the service whos data is being requested.

    Returns:
        data: a list containg all of the entries under the given service name, in list format:
            [<service name (string)>, <username (string)>, <password (string)>]

    '''
    file = open("passwords","r")
    pwfile = file.readlines()
    file.close()
    if base64.b64encode(hashlib.sha512(password.encode('utf-8')).digest()).decode("utf-8") == pwfile[0][:-1]:
        key = base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest())
        #serv_count = int(Fernet(key).decrypt(pwfile[1][:-1].encode('utf-8')).decode('utf-8'))
        servs = Fernet(key).decrypt(pwfile[2][:-1].encode('utf-8')).decode('utf-8').split(",")
        data = []
        for i in range(1,len(servs)):
            if servs[i] == service:
                dat_ent = [service,
                Fernet(key).decrypt(pwfile[1 + i * 3 + 1][:-1].encode('utf-8')).decode('utf-8'),
                Fernet(key).decrypt(pwfile[1 + i * 3 + 2][:-1].encode('utf-8')).decode('utf-8')]
                data.append(dat_ent)
        return data

def read_data_by_ID(password,id):
    '''
    Reads the encrypted data from the password file, given the sequential ID 

    Params:
        password: the master password (or PIN) used for authentication and encryption.
        id: the sequential ID of the entry being removed. 

    Returns:
        data_ent: a single entry of data from the entry specified by id, in the format of:
            [<service name (string)>, <username (string)>, <password (string)>]

    '''
    file = open("passwords","r")
    pwfile = file.readlines()
    file.close()
    if base64.b64encode(hashlib.sha512(password.encode('utf-8')).digest()).decode("utf-8") == pwfile[0][:-1]:
        key = base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest())
        #serv_count = int(Fernet(key).decrypt(pwfile[1][:-1].encode('utf-8')).decode('utf-8'))
        servs = Fernet(key).decrypt(pwfile[2][:-1].encode('utf-8')).decode('utf-8').split(",")
        dat_ent = [servs[id],
        Fernet(key).decrypt(pwfile[4 + id * 3 + 1][:-1].encode('utf-8')).decode('utf-8'),
        Fernet(key).decrypt(pwfile[4 + id * 3 + 2][:-1].encode('utf-8')).decode('utf-8')]
        return dat_ent