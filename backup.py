import paramiko
import subprocess
import argparse
import os
from zipfile import ZipFile
from datetime import date


# Configurações de conexão
host = "192.168.0.160"  
username = "root"
password = "123"


def ssh_connect():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, username=username, password=password)
        print("Conectado ao ESXi com sucesso.")
        return client
    except Exception as e:
        print(f"Erro ao conectar ao ESXi: {e}")
        return None

def export_vm_with_ovftool(esxi_host, username, password, vm_name, destination_path, ovftool_dir):
    try:
        os.chdir(ovftool_dir)
        
        command = [
            "ovftool",
            f"vi://{username}:{password}@{esxi_host}/{vm_name}",
            destination_path
        ]
        data_atual = date.today()

        
        print(f"Exportando a VM '{vm_name}' para '{destination_path}'...")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        for line in process.stdout:
            print(line, end="") #PROGRESSO
        
        process.wait()
        
        if process.returncode == 0:
            print(f"Exportação concluída com sucesso: {destination_path}")
        else:
            stderr_output = process.stderr.read()
            print(f"Erro durante a exportação: {stderr_output}")

        with ZipFile(f"C:/backupVm/{vm_name}-{data_atual}.zip", 'w') as zip_object:
        	zip_object.write(destination_path)

        os.remove(destination_path)

    except Exception as e:
        print(f"Erro ao executar o OVF Tool: {e}")

def run_command(ssh_client, command):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    if error:
        print(f"Erro ao executar comando: {error}")
    return output

def list_vms(ssh_client):
    command = "vim-cmd vmsvc/getallvms"
    output = run_command(ssh_client, command)
    vms = []
    if output:
        lines = output.splitlines()
        for line in lines[1:]:  # Ignora o cabeçalho
            parts = line.split()
            vm_id = parts[0]
            vm_name = parts[1]
            vms.append((vm_id, vm_name))

    print("Listando VMs...")
    for vm_id, vm_name in vms:
        print(f"VM ID: {vm_id}, Nome: {vm_name}")        

def power_on_vm(ssh_client, vmid):
    command = f"vim-cmd vmsvc/power.on vmid"
    print(f"Ligando a VM '{vmid}'...")
    output = run_command(ssh_client, command)

def power_off_vm(ssh_client, vm_id):
    command = f"vim-cmd vmsvc/power.off {vm_id}"
    output = run_command(ssh_client, command)
    if "Powered off" in output or not output:
        print(f"VM com ID {vm_id} desligada com sucesso.")
    else:
        print(f"Erro ao desligar a VM com ID {vm_id}: {output}")


def main():
    ovftool_dir = "C:/Program Files/VMware/VMware OVF Tool"

    
    # Conectar ao ESXi
    print("Conectando... \n")
    ssh_client = ssh_connect()
    if not ssh_client:
        return

    vms = {'pfsense_backup' : 8, 'mysql8' : 17}


    for vm_name, vm_id  in vms.items():
    	print(f"Iniciando backup de: {vm_name}")
    	power_off_vm(ssh_client, vm_id)
    	export_vm_with_ovftool(host, username, password, vm_name, f"C:/backupVm/{vm_name}.ova", ovftool_dir)
    	power_on_vm(ssh_client, vm_id)


    # Fechar a conexão SSH
    ssh_client.close()

if __name__ == "__main__":
	if os.path.isdir('C:/backupVm'):
		pass
	else:
		os.mkdir('C:/backupVm')
	parser = argparse.ArgumentParser(description="Script BACKUP VM")
	parser.add_argument('--list', action='store_true', help="Lista as VMs disponíveis")
	parser.add_argument('--exec', action='store_true', help="Executa BACKUP")
	args = parser.parse_args()
	if args.exec:
   		main()
	if args.list:
		client = ssh_connect()
		list_vms(client)
	else:
		print("Nenhum comando passado. \n Use --list para listar as VMs. \n Use --exec para fazer o backup")
    
