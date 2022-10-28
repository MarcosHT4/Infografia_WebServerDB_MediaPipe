import io
import json
from unittest import result
import cv2
from fastapi import FastAPI, File, UploadFile, Depends
from starlette.responses import StreamingResponse
from predictor import SelfiePredictor
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI(title="Servicio web de eliminacion de fondo")

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def format_result(result):
    result_format = []
    for item in result:
        result_format.append({"id": item['id'], "landmarks": item['landmarks']})
            
     
    final_result = []
    for item in result_format:
        final_item = json.dumps(item)
        final_result.append(final_item)
    landmark_list = []
    for item in final_result:
        landmark_list.append(json.loads(item))
    for item in landmark_list:
        item['landmarks'] = json.loads(item['landmarks'])

     
    return landmark_list if len(landmark_list)>1 else (landmark_list[0] if len(landmark_list)==1 else [])

    



@app.post("/selfie")
def selfie_segmentation(
    bg_r: int = 0, 
    bg_g: int = 0, 
    bg_b: int = 0, 
    image_file: UploadFile = File(...)
    ):
    predictor = SelfiePredictor(bg_color=(bg_r, bg_g, bg_b))
    output = predictor.predict_file(image_file.file)
    res, img_png = cv2.imencode(".png", output)
    return StreamingResponse(io.BytesIO(img_png.tobytes()), media_type="image/png")

@app.get("/saludo")
def saludo(nombre: str, edad: int):
    return {"mensaje": f"Buenas! soy {nombre} y tengo {edad} años"}

@app.get("/esqueletocompleto")
def esqueleto_completo(db:Session = Depends(get_db)): 
    result_dict = [u.__dict__ for u in db.query(models.PoseLandmark).all()] 
    list_landmarks = format_result(result_dict) 
    return list_landmarks 

@app.get("/esqueletocompleto/{id}") 
def esqueleto_completo_id(id: int, db:Session = Depends(get_db)): 
    result_dict = [u.__dict__ for u in db.query(models.PoseLandmark).filter(models.PoseLandmark.id == id).all()] 
    list_landmarks = format_result(result_dict)
    print(list_landmarks)
    return list_landmarks 

@app.delete("/esqueletocompleto/{id}")
def delete_esqueleto_completo_id(id: int, db:Session = Depends(get_db)):
    db.query(models.PoseLandmark).filter(models.PoseLandmark.id == id).delete()
    db.commit()
    return {"mensaje": f"Se ha eliminado el esqueleto con id {id}"}    

    

@app.post("/esqueleto")
def esqueleto(image_file: UploadFile = File(...), db:Session = Depends(get_db)): #Reemplazar
    predictor = SelfiePredictor()
    output, t_points = predictor.predict_skeleton(image_file.file)
    json_t_points = json.dumps(t_points)
    print(json_t_points)

    res, img_png = cv2.imencode(".png", output)
    pose_landmark_model = models.PoseLandmark()
    pose_landmark_model.landmarks = json_t_points
    db.add(pose_landmark_model)
    db.commit()
    
    return StreamingResponse(io.BytesIO(img_png.tobytes()), media_type="image/png")
