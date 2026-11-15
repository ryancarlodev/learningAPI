from controller.utils import *
from controller.packages import *

app = FastAPI()

class MediaItem(BaseModel):
    title: str
    url: str
    gnero: str

@app.get("/")
def read_root():
    return {"status": "Backend running successfully on Ubuntu via SSH and Docker!"}

@app.get("/verify-volume")
def verify_volume():
    exists = os.path.exists(VOLUME_PATH)
    return {
        "volume": VOLUME_PATH,
        "available": exists
    }

@app.post("/medias/")
def create_midia(item: MediaItem):
    '''
    Receives a media item validatd by Pydantic and saves it in a JSON file inside the Docker
    volume (/dados).
    '''
    try:
        # 1. Convert an object to a dictionary (serialization in memory)
        item_dict = item.model_dump()

        # 2. Checking the current state of persistent storage
        data_existing = []

        if os.path.exists(ARCHIVE_DATA):
            with open(ARCHIVE_DATA, "r", encoding="utf-8") as archive:
                try:
                    # The interpreter reads a stream of bytes from disk and rebuilds the list in Python
                    data_existing = json.load(archive)
                except json.JSONDecodeError:
                    # Handling for corrupted or empty files (prevents API crashes)
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
