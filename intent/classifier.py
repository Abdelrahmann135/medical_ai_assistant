from app.resources import intent_classifier

def classify_intent(query, labels):
    """Classify the intent of the query."""
    classifier = intent_classifier()
    result = classifier(query, labels)
    return result





