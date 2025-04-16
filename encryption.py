from cryptography.fernet import Fernet
import hashlib
import base64


def gen_file(password):
    """
    Generate a new password file with the master password hash and empty service list.
    
    Args:
        password (str): The master password for the password manager
    
    This function creates a file with:
    - Line 1: Hashed master password (SHA-512, base64 encoded)
    - Line 2: Encrypted count of services (initially "0")
    - Line 3: Encrypted list of services (initially empty)
    """
    file = open("passwords", "w")
    # Write the hashed master password (SHA-512)
    file.write(base64.b64encode(hashlib.sha512(password.encode('utf-8')).digest()).decode("utf-8"))
    file.write('\n')
    
    # Generate encryption key from the password (SHA-256)
    key = base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest())
    
    # Write encrypted service count (starting with "0")
    file.write(Fernet(key).encrypt("0".encode('utf-8')).decode('utf-8'))
    file.write('\n')
    
    # Write encrypted service list (starting empty)
    file.write(Fernet(key).encrypt("".encode('utf-8')).decode('utf-8'))
    file.write('\n')
    file.close()


def read_services(password):
    """
    Read the list of services from the password file.
    
    Args:
        password (str): The master password for the password manager
        
    Returns:
        list: List of service names, or None if the password is incorrect
        
    This function verifies the master password and returns all stored service names.
    """
    file = open("passwords", "r")
    pwfile = file.readlines()
    file.close()
    
    # Verify the master password by comparing hashes
    if base64.b64encode(hashlib.sha512(password.encode('utf-8')).digest()).decode("utf-8") == pwfile[0][:-1]:
        # Generate encryption key from the password
        key = base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest())
        
        # Decrypt the service list and split by comma
        # Note: Line commenting out service count calculation as it's not used in this function
        #serv_count = int(Fernet(key).decrypt(pwfile[1][:-1].encode('utf-8')).decode('utf-8'))
        servs = Fernet(key).decrypt(pwfile[2][:-1].encode('utf-8')).decode('utf-8').split(",")
        
        # Return all services except the first empty element (from splitting an initially empty string)
        return servs[1:]


def add_service(password, service, serv_name, serv_pass):
    """
    Add a new service entry to the password file.
    
    Args:
        password (str): The master password for the password manager
        service (str): Unique identifier for the service
        serv_name (str): Display name of the service
        serv_pass (str): Password for the service
        
    This function adds a new service with its credentials to the password file if
    the master password is correct.
    """
    file = open("passwords", "r")
    pwfile = file.readlines()
    file.close()
    
    # Verify the master password by comparing hashes
    if base64.b64encode(hashlib.sha512(password.encode('utf-8')).digest()).decode("utf-8") == pwfile[0][:-1]:
        # Generate encryption key from the password
        key = base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest())
        
        # Decrypt the current service count
        serv_count = int(Fernet(key).decrypt(pwfile[1][:-1].encode('utf-8')).decode('utf-8'))
        
        # Decrypt the service list and add the new service
        servs = Fernet(key).decrypt(pwfile[2][:-1].encode('utf-8')).decode('utf-8').split(",")
        servs.append(service)
        
        # Add new service data: service hash, encrypted name, and encrypted password
        pwfile.append(f"{base64.b64encode(hashlib.sha512(service.encode('utf-8')).digest()).decode("utf-8")}\n")
        pwfile.append(f"{Fernet(key).encrypt(serv_name.encode('utf-8')).decode('utf-8')}\n")
        pwfile.append(f"{Fernet(key).encrypt(serv_pass.encode('utf-8')).decode('utf-8')}\n")
        
        # Update the service list and count in the file
        servs_txt = ",".join(servs)
        pwfile[1] = f"{Fernet(key).encrypt(str(len(servs)).encode('utf-8')).decode('utf-8')}\n"
        pwfile[2] = f"{Fernet(key).encrypt(servs_txt.encode('utf-8')).decode('utf-8')}\n"
        
        # Write the updated file
        file = open("passwords", "w")
        for line in pwfile:
            file.write(line)
        file.close()
            

def read_data(password, service):
    """
    Read the credentials for a specific service.
    
    Args:
        password (str): The master password for the password manager
        service (str): The service identifier to look up
        
    Returns:
        list: List of lists containing [service, name, password] for matching services,
              or None if the master password is incorrect
              
    This function searches for and returns credentials for the specified service.
    """
    file = open("passwords", "r")
    pwfile = file.readlines()
    file.close()
    
    # Verify the master password by comparing hashes
    if base64.b64encode(hashlib.sha512(password.encode('utf-8')).digest()).decode("utf-8") == pwfile[0][:-1]:
        # Generate encryption key from the password
        key = base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest())
        
        # Decrypt the service list
        # Note: Line commenting out service count calculation as it's not used in this function
        #serv_count = int(Fernet(key).decrypt(pwfile[1][:-1].encode('utf-8')).decode('utf-8'))
        servs = Fernet(key).decrypt(pwfile[2][:-1].encode('utf-8')).decode('utf-8').split(",")
        
        # Find and collect data for the requested service
        data = []
        for i in range(1, len(servs)):
            if servs[i] == service:
                dat_ent = [
                    service,
                    Fernet(key).decrypt(pwfile[i * 3 + 1][:-1].encode('utf-8')).decode('utf-8'),
                    Fernet(key).decrypt(pwfile[i * 3 + 2][:-1].encode('utf-8')).decode('utf-8')
                ]
                data.append(dat_ent)
        return data