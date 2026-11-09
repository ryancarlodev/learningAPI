# Usa a imagem Python3.12
FROM python:3.12-slim

# Define o diretorio de trabalho
WORKDIR /app

# Instala as dependencias do sistema
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Copia arquivos de requisistos
COPY requirements.txt .

# Instala dependecias do app (FastAPI e Uvicorn)
RUN pip install --no-cache-dir -r requirements.txt

# Copia tudo para dentro do container 
COPY . .

# Expoe a porta 8000 para acessarmos a API
EXPOSE 8000

# Comando para rodar a aplicacao quando o container iniciar
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]