from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class MediaItem(BaseModel):
    titulo: str
    url: str
    gnero: str

@app.get("/")
def home():
    return {"mensagem": "Servidor backend rodando com sucesso no Ubuntu via SSH e Docker!"}

@app.get("/verificar-volume")
def verificar_volume():
    caminho_volume = "/dados"
    existe = os.path.exists(caminho_volume)
    return {
        "volume_conectado": existe,
        "caminho": caminho_volume,
        "mensagem": "Volume dados_teste mapeado com sucesso!" if existe else "Volume não encontrado."
    }

@app.post("/midias/")
def cadastrar_midia(item: MediaItem):
    return {
        "status": "sucesso",
        "mensagem": f"A mídia '{item.titulo}' do gênero '{item.gnero}' foi recebida para processamento.",
        "url_alvo": item.url
    }