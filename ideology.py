from scraper import sitecontents, querysearch, lengthofsearch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

model_name = "distilbert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def truncate_string(input_string, max_length=1024):
    return input_string[:max_length]

def classify_political_tweets(input_text):
    inputs = tokenizer(input_text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)
    predicted_index = torch.argmax(probabilities, dim=1).item()
    label_mapping = {0: "Republican", 1: "Democrat"}
    predicted_label = label_mapping[predicted_index]
    return predicted_label

def polpredict(n, polinput):
    ARTICLE = (sitecontents(n, polinput)[1])
    TITLE = (sitecontents(n, polinput)[0])
    trunc = truncate_string(ARTICLE)
    input_text = summarizer(trunc, max_length=min(len(trunc), 299), min_length=100, do_sample=False)
    input_text = input_text[0]['summary_text']
    CLASSIFIEDTITLE = classify_political_tweets(TITLE)
    result = classify_political_tweets(input_text)
    print(sitecontents(n, polinput)[3])
    return TITLE, CLASSIFIEDTITLE, input_text, result

def finalpred(n, inp):
    length = lengthofsearch(inp)
    if n > length:
        n = length
    return polpredict(n, inp)