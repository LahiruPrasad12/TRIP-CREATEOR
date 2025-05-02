import boto3
import uuid
from fastapi import FastAPI, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from models import Trip
from database import get_db, Base, engine
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware


# Initialize
Base.metadata.create_all(bind=engine)
app = FastAPI()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods, or specify ['GET', 'POST', etc.]
    allow_headers=["*"],
)

s3 = boto3.client("s3",
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id= os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)


@app.post("/upload")
async def upload_trip_with_image(
    file: UploadFile = File(...),
    num_of_passengers: int = Form(...),
    amount_per_passenger: float = Form(...),
    from_: str = Form(..., alias="from"),  # use `from_` because `from` is a Python keyword
    to: str = Form(...),
    company_id: int = Form(...),
    route_id: int = Form(...),
    db: Session = Depends(get_db)
):
    # Generate unique filename
    file_ext = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_ext}"

    # Upload to S3
    s3.upload_fileobj(
        file.file,
        os.getenv('AWS_BUCKET'),
        unique_filename,
        ExtraArgs={
            "ACL": "public-read",
            "ContentType": file.content_type
        }
    )

    # Build the public S3 URL
    s3_url = f"{os.getenv('AWS_URL')}/{unique_filename}"

    # Save trip record
    trip = Trip(
        num_of_passengers=num_of_passengers,
        amount_per_passenger=amount_per_passenger,
        from_location= from_,
        to =to,
        company_id=company_id,
        route_id=route_id,
        url=s3_url
    )

    db.add(trip)
    db.commit()
    db.refresh(trip)

    return {"id": trip.id, "url": s3_url}

@app.get("/")
def read_root():
    return {"message": "It works!"}
