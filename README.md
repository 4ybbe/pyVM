<h1 align="center" id="title">pyVM - backup</h1>

<h2>Dependencias</h2>

<p>1. OVFTool</p>

```
https://developer.broadcom.com/tools/open-virtualization-format-ovf-tool/latest
```

<p>2. Python</p>

```
pip3 install -r requirements
```

<br>
<h2>Setup</h2>
<p>1. VMWare variaveis</p>

```
10 # host = "192.168.0.10"  
11 # username = "root"
12 # password = "123"
```

<p>2. OVFTools variaveis</p>

```
99 # ovftool_dir = "C:/Program Files/VMware/VMware OVF Too"  
```

<p>3. VMWare VM'S</p>

```
108 # vms = {'pfsense_backup' : 8, 'mysql8' : 17}
```

<br>
<h2>Uso</h2>

Lista Maquinas
```
$ python backup --list
```

Executa Backup
```
$ python backup --exec
```
