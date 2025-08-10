from sqlalchemy.orm import Session
from . import models, schemas
from .sentiment import analyze_sentiment

def create_sentiment(db: Session, sentiment_data: schemas.SentimentCreate):
    sentiment_label = analyze_sentiment(sentiment_data.text)
    db_sentiment = models.SentimentRecord(text=sentiment_data.text, sentiment=sentiment_label)
    db.add(db_sentiment)
    db.commit()
    db.refresh(db_sentiment)
    return db_sentiment

def get_sentiments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.SentimentRecord).offset(skip).limit(limit).all()

def get_sentiment(db: Session, sentiment_id: int):
    return db.query(models.SentimentRecord).filter(models.SentimentRecord.id == sentiment_id).first()

def update_sentiment(db: Session, sentiment_id: int, sentiment_data: schemas.SentimentUpdate):
    sentiment_record = get_sentiment(db, sentiment_id)
    if sentiment_record:
        sentiment_record.text = sentiment_data.text
        sentiment_record.sentiment = analyze_sentiment(sentiment_data.text)
        db.commit()
        db.refresh(sentiment_record)
    return sentiment_record

def delete_sentiment(db: Session, sentiment_id: int):
    sentiment_record = get_sentiment(db, sentiment_id)
    if sentiment_record:
        db.delete(sentiment_record)
        db.commit()
    return sentiment_record
