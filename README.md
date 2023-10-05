# Backupy - Versão 1.0

**TERMINALX - SOLUÇÕES OPEN SOURCE**  
**Bruno Carvalho - Diretor Tecnológico**  
- Email: bruno@terminalx.net.br  
- WhatsApp: +55 35 984413336  

## Descrição
Este script gera backups do sistema de arquivos em diferentes locais:

- Backup local - HD ou partição local
- Backup em rede local - Em algum compartilhamento de arquivo ou NAS local
- Backup em VPN - Em alguma rede remota via túnel OpenVPN

Requisitos para o funcionamento:
- OpenVpn Ok.
- Rsync Ok.
- Chave ssh compartilhada para acesso sem senha.
- sendEmail script Perl para envio de email (https://github.com/zehm/sendEmail)

Utilizando o programa "rsync"+"OpenVPN"+"SSH", podemos fazer cópias incrementais dos estados das estruturas de diretórios e sincronizar com as atualizações diárias. Além das camadas de segurança do túnel criptografado, ainda temos a conexão segura do SSH.

Após o backup ser feito, um email é enviado ao Sysadmin.

- Para o envio do email, é necessário configurar o servidor SMTP no script e criar os paths caso eles não existam.
