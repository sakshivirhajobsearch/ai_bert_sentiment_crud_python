from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="BERT Sentiment CRUD API")

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/sentiments/", response_model=schemas.SentimentResponse)
def create_sentiment(sentiment: schemas.SentimentCreate, db: Session = Depends(get_db)):
    return crud.create_sentiment(db, sentiment)

@app.get("/sentiments/", response_model=list[schemas.SentimentResponse])
def read_sentiments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_sentiments(db, skip=skip, limit=limit)

@app.get("/sentiments/{sentiment_id}", response_model=schemas.SentimentResponse)
def read_sentiment(sentiment_id: int, db: Session = Depends(get_db)):
    db_sentiment = crud.get_sentiment(db, sentiment_id)
    if db_sentiment is None:
        raise HTTPException(status_code=404, detail="Sentiment not found")
    return db_sentiment

@app.put("/sentiments/{sentiment_id}", response_model=schemas.SentimentResponse)
def update_sentiment(sentiment_id: int, sentiment: schemas.SentimentUpdate, db: Session = Depends(get_db)):
    updated = crud.update_sentiment(db, sentiment_id, sentiment)
    if updated is None:
        raise HTTPException(status_code=404, detail="Sentiment not found")
    return updated

@app.delete("/sentiments/{sentiment_id}")
def delete_sentiment(sentiment_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_sentiment(db, sentiment_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Sentiment not found")
    return {"message": "Sentiment deleted successfully"}
