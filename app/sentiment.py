from transformers import pipeline

# Load BERT sentiment analysis model only once at startup
sentiment_pipeline = pipeline(
    task="sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_sentiment(text: str) -> str:
    """
    Analyze the sentiment of the given text using the preloaded BERT model.

    Returns:
        str: Sentiment label and confidence score, e.g., 'POSITIVE (0.98)'
    """
    result = sentiment_pipeline(text)[0]
    label = result["label"].capitalize()  # Make 'POSITIVE' → 'Positive'
    score = round(result["score"], 2)
    return f"{label} ({score})"
