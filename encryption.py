from cryptography.fernet import Fernet
import hashlib
import base64


def gen_file(password):
    file = open("passwords","w")
    file.write(base64.b64encode(hashlib.sha512(password.encode('utf-8')).digest()).decode("utf-8"))
    file.write('\n')
    key = base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest())
    file.write(Fernet(key).encrypt("0".encode('utf-8')).decode('utf-8'))
    file.write('\n')
    file.write(Fernet(key).encrypt("".encode('utf-8')).decode('utf-8'))
    file.write('\n')
    file.close()

def read_services(password):
    file = open("passwords","r")
    pwfile = file.readlines()
    file.close()
    if base64.b64encode(hashlib.sha512(password.encode('utf-8')).digest()).decode("utf-8") == pwfile[0][:-1]:
        key = base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest())
        #serv_count = int(Fernet(key).decrypt(pwfile[1][:-1].encode('utf-8')).decode('utf-8'))
        servs = Fernet(key).decrypt(pwfile[2][:-1].encode('utf-8')).decode('utf-8').split(",")
        return servs[1:]

def add_service(password,service,serv_name,serv_pass):
    file = open("passwords","r")
    pwfile = file.readlines()
    file.close()
    if base64.b64encode(hashlib.sha512(password.encode('utf-8')).digest()).decode("utf-8") == pwfile[0][:-1]:
        key = base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest())
        serv_count = int(Fernet(key).decrypt(pwfile[1][:-1].encode('utf-8')).decode('utf-8'))
        servs = Fernet(key).decrypt(pwfile[2][:-1].encode('utf-8')).decode('utf-8').split(",")
        servs.append(service)
        pwfile.append(f"{base64.b64encode(hashlib.sha512(service.encode('utf-8')).digest()).decode("utf-8")}\n")
        pwfile.append(f"{Fernet(key).encrypt(serv_name.encode('utf-8')).decode('utf-8')}\n")
        pwfile.append(f"{Fernet(key).encrypt(serv_pass.encode('utf-8')).decode('utf-8')}\n")
        servs_txt = ",".join(servs)
        pwfile[1] = f"{Fernet(key).encrypt(str(len(servs)).encode('utf-8')).decode('utf-8')}\n"
        pwfile[2] = f"{Fernet(key).encrypt(servs_txt.encode('utf-8')).decode('utf-8')}\n"
        file = open("passwords","w")
        for line in pwfile:
            file.write(line)
        file.close()
            
def read_data(password,service):
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
                Fernet(key).decrypt(pwfile[i * 3 + 1][:-1].encode('utf-8')).decode('utf-8'),
                Fernet(key).decrypt(pwfile[i * 3 + 2][:-1].encode('utf-8')).decode('utf-8')]
                data.append(dat_ent)
        return data

