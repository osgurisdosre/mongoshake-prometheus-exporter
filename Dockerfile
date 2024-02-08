# Define a imagem base a ser utilizada
FROM python:3.11.4-alpine

# Define o diretório de trabalho no container
WORKDIR /app

# Copia os arquivos necessários para o diretório de trabalho
COPY requirements.txt .
COPY . .

# Instala as dependências necessárias
RUN pip3 install --no-cache-dir -r requirements.txt

# Define o comando a ser executado quando o container for iniciado
CMD ["python3", "src/app.py"]
