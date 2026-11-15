from controller.utils import *
from controller.packages import *

app = FastAPI()

class MediaItem(BaseModel):
    title: str
    url: str
    gnero: str

@app.get("/")
def read_root():
    return {"status": "server backend running in successful the Ubuntu via SSH and Docker!"}

@app.get("/verify-volume")
def verify_volume():
    exists = os.path.exists(VOLUME_PATH)
    return {
        "volume": VOLUME_PATH,
        "avaible": exists
    }

@app.post("/medias/")
def create_midia(item: MediaItem):
    '''
    Receives a media item validate by pydantic and saves it in a JSON file inside the Docker
    volume (/data).
    '''
    try:
        # 1. Transformate a object for dicionary (serialization in memory)
        item_dict = item.model_dump()

        # 2. Learning the actualy state by amarzening persisty
        data_existing = []
        if os.path.exists(ARCHIVE_DATA):
            with open(ARCHIVE_DATA, "r", encoding="utf-8") as archive:
                try:
                    # The intepretor lear a stream for bytes in disco e reconstroi the list in python
                    data_existing = json.load(archive)
                except json.JSONDecodeError:
                    # Tratamento para archive corrompido empty (evita crash for API)
                    data_existing = []

        # 3. Mutarion structure the data in RAM
        data_existing.append(item_dict)

        # 4. Read atomic by disc (Mode "w" sobscreve o archive in the list actualyzate)
        with open(ARCHIVE_DATA, "w", encoding="utf-8") as archive:
            json.dump(data_existing, archive, ensure_ascii=False, indent=4)

        return {
            "status": "success",
            "menssage": f"The media '{item.title}' was successfully persisted",
            "save_data": item_dict
        }

    except Exception as e:
        # Capture for excecion low level (read permission, I/O error)
        raise HTTPException(
            status_code=500,
            detail=f"Erro critico de I/O ao processar o archive a data: {str(e)}"
        )
