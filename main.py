import os
import csv

#
# Diretório onde o script está localizado
caminho_base = os.path.dirname(os.path.abspath(__file__))

# Mudar para o diretório especificado
os.chdir(caminho_base)

# Verificar o diretório atual
diretorio_atual = os.getcwd()
print(f"Diretório atual: {diretorio_atual}")

# Caminho dos arquivos de modelo e CSV relativos ao script
modelo_ipstatic_path = os.path.join(caminho_base, 'modelo_ipstatic.xml')
modelo_dhcp_path = os.path.join(caminho_base, 'modelo_dhcp.xml')
dados_csv_path = os.path.join(caminho_base, 'dados.csv')

# Verificar se os arquivos existem antes de tentar abrir
for arquivo in [modelo_ipstatic_path, modelo_dhcp_path, dados_csv_path]:
    if not os.path.exists(arquivo):
        raise FileNotFoundError(f"Arquivo não encontrado: {arquivo}")
    else:
        print(f"Arquivo encontrado: {arquivo}")

# Função para substituir placeholders no modelo XML
def preencher_modelo(xml_modelo, ramal, senha, label, dominio, sip_proxy, ip, mask, gateway, dns1, dns2, tzone):
    xml_preenchido = xml_modelo.replace('{{ramal}}', ramal)
    xml_preenchido = xml_preenchido.replace('{{senha}}', senha)
    xml_preenchido = xml_preenchido.replace('{{label}}', label)
    xml_preenchido = xml_preenchido.replace('{{dominio}}', dominio)
    xml_preenchido = xml_preenchido.replace('{{sip_proxy}}', sip_proxy)
    xml_preenchido = xml_preenchido.replace('{{ip}}', ip)
    xml_preenchido = xml_preenchido.replace('{{mask}}', mask)
    xml_preenchido = xml_preenchido.replace('{{gateway}}', gateway)
    xml_preenchido = xml_preenchido.replace('{{dns1}}', dns1)
    xml_preenchido = xml_preenchido.replace('{{dns2}}', dns2)
    xml_preenchido = xml_preenchido.replace('{{tzone}}', tzone)

    
    return xml_preenchido

# Carregar os modelos XML
with open('modelo_ipstatic.xml', 'r') as file:
    modelo__ipstatic_xml = file.read()

with open('modelo_dhcp.xml', 'r') as file:
    modelo_dhcp_xml = file.read()

# Ler os dados do arquivo CSV
with open('dados.csv', newline='') as csvfile:
    leitor = csv.DictReader(csvfile)
    for linha in leitor:
        ramal = linha['ramal']
        senha = linha['senha']
        label = linha['label']
        dominio = linha['dominio']
        sip_proxy = linha['sip_proxy']
        ip = linha['ip']
        mask = linha['mask']
        gateway = linha['gateway']
        dns1 = linha['dns1']
        dns2 = linha['dns2']
        tzone = linha['tzone']

        

        # Escolher o modelo XML com base no valor do campo 'IP'
        if ip.lower() == 'dhcp':
            xml_modelo = modelo_dhcp_xml
        else:
            xml_modelo = modelo__ipstatic_xml

        # Extrair o nome da pasta com base nas primeiras letras antes do primeiro hífen
        nome_pasta = dominio.split('-')[0].lower()  # Extrai a parte antes do primeiro hífen e converte para minúsculas

        # Preencher o modelo XML com os dados atuais
        xml_preenchido = preencher_modelo(xml_modelo, ramal, senha, label, dominio, sip_proxy, ip, mask, gateway, dns1, dns2, tzone)

        # Criar a pasta para o domínio se não existir
        pasta_dominio = os.path.join(caminho_base, nome_pasta, dominio)
        if not os.path.exists(pasta_dominio):
            os.makedirs(pasta_dominio)

        # Salvar o XML preenchido em um novo arquivo dentro da pasta do domínio
        nome_arquivo = os.path.join(pasta_dominio, f'Config-eSpace7910-{ramal}-{ip}-{dominio}.xml')
        with open(nome_arquivo, 'w') as file:
            file.write(xml_preenchido)

        print(f'Arquivo {nome_arquivo} gerado com sucesso.')
