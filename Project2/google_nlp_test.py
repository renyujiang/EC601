from google.cloud import language_v1
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./ec602-project-2-382ab4aae677.json"

client = language_v1.LanguageServiceClient()

# generate test text
text = "This is BU EC601 Project2's homework."
document = language_v1.Document(
    content=text, type_=language_v1.Document.Type.PLAIN_TEXT
)

# Sentiment analysis
sentiment = client.analyze_sentiment(
    request={"document": document}
).document_sentiment

# Entities analysis
entities = client.analyze_entities(
    request={"document": document}
)

print("Sentiment analysis:\n","Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))

print("Entities analysis:\n",entities)

print("\n\n\n")
# Iterate the server response
for i in entities.entities:
    print(i.name,"\n",i.type_,"\n",i.salience,"\n",i.mentions,"\n")