import qrcode
import random
import string
import paramiko
from PIL import Image


def generate_password(length):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Configurações do SSH
ssh_host = 'exemplo.com'  # Insira o endereço do host SSH
ssh_port = 22  # Porta SSH padrão
ssh_username = 'seu_usuario'  # Insira o nome de usuário para SSH
ssh_password = 'sua_senha'  # Insira a senha para SSH

# Gerar uma senha aleatória
new_password = generate_password(10)

# Comandos SSH
ssh_commands = [
    'config wireless-controller vap',
    'edit SSID-TSAG-GUEST',
    'setpassphrase "{}"'.format(new_password),
    'end'
]

# Conexão SSH e execução dos comandos
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ssh_host, port=ssh_port, username=ssh_username, password=ssh_password)
    
    for command in ssh_commands:
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        if output:
            print(output)
        
        if error:
            print(error)

    ssh.close()
    print('Comandos executados com sucesso!')
except paramiko.AuthenticationException:
    print('Falha na autenticação SSH')
except paramiko.SSHException as ssh_exception:
    print('Erro de conexão SSH:', str(ssh_exception))


def generate_custom_wifi_qrcode(ssid, password, security_type, filename):
    wifi_data = f"WIFI:T:{security_type};S:{ssid};P:{password};;"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(wifi_data)
    qr.make(fit=True)
    qr_code = qr.make_image(fill_color="black", back_color="white")

    # Personalização do QR Code
    qr_code = qr_code.convert("RGB")
    qr_code = qr_code.resize((500, 500))  # Altere o tamanho conforme necessário
    qr_code = add_logo(qr_code, "./logo.png")  # Adicione um logotipo (opcional)
    qr_code = customize_colors(qr_code, fill_color=(0, 71, 171), back_color=(255, 255, 255))  # Personalize as cores (opcional)
    qr_code.save(filename)
    print("QR Code gerado com sucesso!")

def add_logo(qr_code, logo_filename):
    logo = Image.open(logo_filename)
    logo_width, logo_height = logo.size
    qr_code_width, qr_code_height = qr_code.size
    logo_max_size = int(qr_code_width / 4)

    if logo_width > logo_max_size or logo_height > logo_max_size:
        logo = logo.resize((logo_max_size, logo_max_size))

    logo_width, logo_height = logo.size
    logo_position = ((qr_code_width - logo_width) // 2, (qr_code_height - logo_height) // 2)
    qr_code.paste(logo, logo_position)

    return qr_code

def customize_colors(qr_code, fill_color, back_color):
    qr_code = qr_code.convert("RGBA")

    data = qr_code.getdata()

    new_data = []
    for item in data:
        if item[:3] == (255, 255, 255):
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append((fill_color[0], fill_color[1], fill_color[2], 255))

    qr_code.putdata(new_data)
    qr_code = qr_code.convert("RGB")

    return qr_code

# Exemplo de uso
ssid = "ANTONIO 2.4G"
password = "14091991"
security_type = "WPA"  # Pode ser "WEP", "WPA", "WPA2" ou "nopass"
filename = "custom_wifi_qrcode.png"

generate_custom_wifi_qrcode(ssid, password, security_type, filename)


import subprocess

# Variáveis de configuração
storage_account = "nome-da-conta-de-armazenamento"
container_name = "nome-do-container"
image_file = "qcrode.png"
new_image_path = "caminho-da-nova-imagem.png"

# Comando para remover a imagem, se existir
remove_command = f"az storage blob delete --account-name {storage_account} --container-name {container_name} --name {image_file}"
subprocess.run(remove_command, shell=True)

# Comando para fazer o upload da nova imagem
upload_command = f"az storage blob upload --account-name {storage_account} --container-name {container_name} --type block --name {image_file} --type page --file {new_image_path}"
subprocess.run(upload_command, shell=True)