import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def read_files_from_folder(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as file:
                documents.append(file.read().strip())
    return documents

def sample_analyze_sentiment():
    endpoint = os.environ["AZURE_LANGUAGE_ENDPOINT"]
    key = os.environ["AZURE_LANGUAGE_KEY"]
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    
    input_folder = "inputs"
    documents = read_files_from_folder(input_folder)
    
    if not documents:
        print("No text files found in the 'inputs' folder.")
        return
    
    result = text_analytics_client.analyze_sentiment(documents, show_opinion_mining=True)
    docs = [doc for doc in result if not doc.is_error]

    print("Sentiment Analysis Results:")
    for idx, doc in enumerate(docs):
        print(f"Document {idx + 1}: {doc.sentiment} (Confidence: {doc.confidence_scores})")

    positive_reviews = [doc for doc in docs if doc.sentiment == 'positive' and doc.confidence_scores.positive >= 0.9]

    print("\nFinal Positive Reviews:")
    for idx, review in enumerate(positive_reviews):
        print(f"Positive Review {idx + 1}:")
        for sentence in review.sentences:
            print(f"  {sentence.text} (Sentiment: {sentence.sentiment})")

if __name__ == "__main__":
    sample_analyze_sentiment()
