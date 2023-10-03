#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import smtplib
#import mimetypes
#import email.mime.application
#from email.mime.multipart import MIMEMultipart
#from email.mime.text import MIMEText
#from email.mime.base import MIMEBase
#from email import encoders
import subprocess
import time

#Limpa a lixeira antes do backup
def limpa_lixo():
    limpeza = 'rm -rf /dados/lixeira/*'
    subprocess.call(limpeza ,shell=True)
    print("\nLixeira limpa com sucesso...")

#Essa função gera um banner com a hora inicial do Backup
def inicio(horaInicio):

    inicio = '''
 ===========================================================================
||  ____          _____ _  ___    _ _____    _____   _____                   ||
|| |  _ \   /\   / ____| |/ / |  | |  __ \  |  __ \ / ____|                  ||
|| | |_) | /  \ | |    | ' /| |  | | |__) | | |__) | (___  _   _ _ __   ___  ||
|| |  _ < / /\ \| |    |  < | |  | |  ___/  |  _  / \___ \| | | | '_ \ / __| ||
|| | |_) / ____ \ |____| . \| |__| | |      | | \ \ ____) | |_| | | | | (__  ||
|| |____/_/    \_\_____|_|\_ \____/|_|      |_|  \_\_____/ \__, |_| |_|\___| ||
||                                                          __/ |            ||
||                                                         |___/             ||
||                    BACKUP DIFERENCIAL DO FILESERVER                       ||
  ===========================================================================
  ===========================================================================
                BACKUP DIFERENCIAL DO FILESERVER INICIADO ÀS %s

''' % horaInicio
    return inicio

#Termino e calculos
def termino(diaInicio, horaInicio, pathdestino_remoto_vpn_dados,pathdestino_remoto_vpn_home, pathdestino_remoto_lan_dados,pathdestino_remoto_lan_home, pathdestino_local_dados,pathdestino_local_home, pathlog, backup, backup1):
    hoje = (time.strftime("%d-%m-%Y"))
    horaFinal   = time.strftime('%H:%M:%S')
    backup = backup.replace('tar cvf', '')
    backup1 = backup1.replace('tar cvf', '')
    final = '''
  ==========================================================================================================
                            BACKUP DIFF ATUALIZADO
                HORA INICIAL:    %s  -  %s
                HORA FINAL  :    %s  -  %s
                LOG FILE    :    %s
                BAK FILE VPN:    %s
                BAK FILE VPN:    %s
                BAK FILE LAN:    %s
                BAK FILE LAN:    %s
                BAK FILE LOCAL : %s
                BAK FILE LOCAL : %s
  ==========================================================================================================
    ''' % (diaInicio, horaInicio, hoje, horaFinal, pathlog, pathdestino_remoto_lan_dados,pathdestino_remoto_lan_home,pathdestino_remoto_vpn_dados,pathdestino_remoto_vpn_home,pathdestino_local_dados,pathdestino_local_home)
    return final


#ESSA FUNÇÃO DESMONTA O HD DE BACKUP POR SEGURANÇA.
#DESCOMENTE A LINHA desmonta_hd() DENTRO DE backupfull() PARA UTILIZÁ-LA
def desmonta_hd(disk):
    try:
        umount = 'umount %s' % disk
        subprocess.call(umount, shell=True)
        return True
    except:
        return False


#CONSTROI OS LOGS DO SISTEMA - Aqui selecionamos o nome do backup e o arquivo de logs que iremos criar.
def geralog():
    date = (time.strftime("%Y-%m-%d"))              #
    logfile     = '%s-backup-diff.txt' % date       # Cria o arquivo de Log
    pathlog     = '/var/log/backup/%s' % logfile    # Arquivo de log
    return pathlog


#CONSTROI O ARQUIVO E PATH DE BACKUP E RETORNA
def gerabackup():
    date = (time.strftime("%Y-%m-%d"))
    # Opções que serão passadas com Rsync. Comentários no inicio do Script :)
    opts    = 'Cravzp'
    exclude = '*.log, *.tmp, .recycle,'              # Define os diretórios e tipos de arquivos que não vão ter backup
    #backupfile  = '%s-backup-full.tar.gz' % date    # Cria o nome do arquivo de Backup
    pathdestino_remoto_vpn_dados = '/media/xterm/d3c124cd-fe44-4485-9ff8-31f7f5603357/dados/'  # Destino onde será gravado o Backup Remoto VPN /dados
    pathdestino_remoto_vpn_home = '/media/xterm/d3c124cd-fe44-4485-9ff8-31f7f5603357/home/'    # Destino onde será gravado o Backup Remoto VPN /dados
    pathdestino_remoto_lan_dados = '/backup/dados/'                                           # Destino onde será gravado o Backup Remoto lan /dados       
    pathdestino_remoto_lan_home = '/backup/home/'                                             # Destino onde será gravado o Backup Remoto lan /home
    pathdestino_local_dados = '/backup/'                                                      # Destino onde será gravado o Backup Local em espelho /dados
    pathdestino_local_home = '/backup/home/'                                                  # Destino onde será gravado o Backup Local em espelho /home
    pathorigem  = '/dados/'                                                                   # pasta que será 'backupeada' /dados
    pathorigem1  = '/home/'                                                                   # pasta que será 'backupeada' /home
    
    #Caso o backup seja na maquina, favor passar os parametros de backup_local
 
    backup_nas  = 'rsync -%s --exclude={%s} --progress %s -e ssh root@10.215.86.1:%s ' % (opts, exclude, pathorigem, pathdestino_remoto_vpn_dados)      # INCREMENTAL   
    backup_nas1 = 'rsync -%s --exclude={%s} --progress %s -e ssh root@10.215.86.1:%s ' % (opts, exclude, pathorigem1, pathdestino_remoto_vpn_home)        # INCREMENTAL
    backup      = 'rsync -%s --exclude={%s} --progress %s -e ssh root@192.168.1.96:%s ' % (opts, exclude, pathorigem, pathdestino_remoto_lan_dados)              # INCREMENTAL
    backup1     = 'rsync -%s --exclude={%s} --progress %s -e ssh root@192.168.1.96:%s ' % (opts, exclude, pathorigem1, pathdestino_remoto_lan_home)              # INCREMENTAL
    backup_local    = 'rsync -%s --exclude={%s} --progress %s %s --delete ' % (opts, exclude, pathorigem, pathdestino_local_dados)                               # ESPELHADO 
    backup1_local   = 'rsync -%s --exclude={%s} --progress %s %s --delete ' % (opts, exclude, pathorigem1, pathdestino_local_home)                               # ESPELHADO
    return backup_nas, backup_nas1, backup_local, backup1_local, backup, backup1, pathdestino_remoto_vpn_dados, pathdestino_remoto_vpn_home, pathdestino_remoto_lan_dados,pathdestino_remoto_lan_home,pathdestino_local_dados,pathdestino_local_home

##FUNCAO QUE ENVIA OS LOGS DE BACKUP PARA O ADMIN
def send_email(pathlog):
   try:
     mailadmin="bruno@terminalx.net.br"
     senduser="bruno@terminalx.net.br"
     copia="ti@exsto.com.br"
     smtp="smtp.hostinger.com.br:587"
     senha="Bmed2007#2020"
     command="/usr/local/bin/sendEmail -f %s -t %s -cc %s -u 'Logs de backup AD-EXSTO' -a %s -s %s -o tls=no -xu %s -xp %s -m 'Seguem logs de backup AD-EXSTO'" % (senduser,mailadmin,copia,pathlog,smtp,mailadmin,senha)
     subprocess.call(command,shell=True)
   # Create a text/plain message
   
     print("\nEmail enviado com sucesso")
   except:
     print("\nErro ao enviar email")

### ABRE CONEXAO COM A VPN ###
def vpn_conect():
   pathovpnfile = '/root/backup_domingos.ovpn'
   conect = 'openvpn --config %s &' % pathovpnfile
   ip_tunel = '10.215.86.1'
   try:
     subprocess.call(conect,shell=True)
     #subprocess.check_output([conect])
     check = 'ping -c 5 %s' %ip_tunel
     subprocess.call(check,shell=True)
     print("Conexão Ok, host responde...")
     return True
   except:
     print("Conexão FAIL...")
     return False   
     
### SINCRONIZA BACKUP NO NAS LOCAL ###
def backup_nas_local(): 

    horaInicio = time.strftime('%H:%M:%S')
    pathlog = geralog()
    backup_nas, backup_nas1, backup_local, backup1_local, backup, backup1, pathdestino_remoto_vpn_dados, pathdestino_remoto_vpn_home, pathdestino_remoto_lan_dados,pathdestino_remoto_lan_home,pathdestino_local_dados,pathdestino_local_home = gerabackup()
    log = ' >> %s' % pathlog
    start = inicio(horaInicio)
      
    x = open(pathlog, 'w')
    x.write(start)
    x.close()

    subprocess.call(backup + log ,shell=True)
    subprocess.call(backup1 + log ,shell=True)

#Printa o final e relatório
    diaInicio = (time.strftime("%d-%m-%Y"))
    final = termino(diaInicio, horaInicio, pathdestino_remoto_lan_dados,pathdestino_remoto_lan_home,pathdestino_remoto_vpn_dados,pathdestino_remoto_vpn_home,pathdestino_local_dados,pathdestino_local_home,pathlog,backup,backup1)
    r = open(pathlog, 'r') # Abra o arquivo (leitura)
    conteudo = r.readlines()
    conteudo.append(final)   # insira seu conteúdo
    r = open(pathlog, 'w') # Abre novamente o arquivo (escrita)
    r.writelines(conteudo)    # escreva o conteúdo criado anteriormente nele.
    r.close()
    send_email(pathlog)

### SINCRONIZA BACKUP NO NAS REMOTO ###
def backup_nas_vpn(): 

    #ABRE O TUNEL COM O NAS REMOTO
    vpn_conect()
    
    horaInicio = time.strftime('%H:%M:%S')
    pathlog = geralog()
    backup_nas, backup_nas1, backup_local, backup1_local, backup, backup1, pathdestino_remoto_vpn_dados, pathdestino_remoto_vpn_home, pathdestino_remoto_lan_dados,pathdestino_remoto_lan_home,pathdestino_local_dados,pathdestino_local_home = gerabackup()
    log = ' >> %s' % pathlog
    start = inicio(horaInicio)
      
    x = open(pathlog, 'w')
    x.write(start)
    x.close()

    subprocess.call(backup_nas + log ,shell=True)
    subprocess.call(backup_nas1 + log ,shell=True)

#Printa o final e relatório
    diaInicio = (time.strftime("%d-%m-%Y"))
    final = termino(diaInicio, horaInicio, pathdestino_remoto_lan_dados,pathdestino_remoto_lan_home,pathdestino_remoto_vpn_dados,pathdestino_remoto_vpn_home,pathdestino_local_dados,pathdestino_local_home,pathlog,backup_nas,backup_nas1)
    r = open(pathlog, 'r') # Abra o arquivo (leitura)
    conteudo = r.readlines()
    conteudo.append(final)   # insira seu conteúdo
    r = open(pathlog, 'w') # Abre novamente o arquivo (escrita)
    r.writelines(conteudo)    # escreva o conteúdo criado anteriormente nele.
    r.close()
    send_email(pathlog)
    end_tunel = 'pkill openvpn'
    subprocess.call(end_tunel + log ,shell=True)

#CRIA BACKUP ESPELHO EM HD EXTERNO
def backup_hd_espelho():
    #disk = '/dev/sdb'        #Define onde está a partição que será usada para guardar o backup
    horaInicio = time.strftime('%H:%M:%S')
    pathlog = geralog()
    backup_nas, backup_nas1, backup_local, backup1_local, backup, backup1, pathdestino_remoto_vpn_dados, pathdestino_remoto_vpn_home, pathdestino_remoto_lan_dados,pathdestino_remoto_lan_home,pathdestino_local_dados,pathdestino_local_home = gerabackup()
    log = ' >> %s' % pathlog
    start = inicio(horaInicio)
    
    x = open(pathlog, 'w')
    x.write(start)
    x.close()

    #Monta o hd de backup
   # mount = 'mount '+ disk + ' /backup'
    #subprocess.call(mount, shell=True)
          
    #RODA O BACKUP
    subprocess.call(backup_local + log, shell=True)
    subprocess.call(backup1_local + log, shell=True)
        
    #Printa o final e relatório
    diaInicio = (time.strftime("%d-%m-%Y"))
    final = termino(diaInicio, horaInicio, pathdestino_remoto_lan_dados,pathdestino_remoto_lan_home,pathdestino_remoto_vpn_dados,pathdestino_remoto_vpn_home,pathdestino_local_dados,pathdestino_local_home,pathlog,backup_local,backup1_local)

    r = open(pathlog, 'r') # Abra o arquivo (leitura)
    conteudo = r.readlines()
    conteudo.append(final)   # insira seu conteúdo
    r = open(pathlog, 'w') # Abre novamente o arquivo (escrita)
    r.writelines(conteudo)    # escreva o conteúdo criado anteriormente nele.
    r.close()
    #Descomente essa função para desmontar a partição que será utilizada para armazenar o backup
    #desmonta_hd(disk)
    send_email(pathlog)

##########################################################################MAIN########################################################################
limpa_lixo()
backup_nas_vpn()
backup_hd_espelho()
#backup_nas_local()