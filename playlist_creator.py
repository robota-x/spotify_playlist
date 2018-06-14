def read_credentials(file_name='credentials.txt'):
    with open(file_name, 'r') as f:
        client_id, secret = f.read().splitlines()[:2]
        return {
            'client_id': client_id,
            'secret': secret
        }
        

print(read_credentials())