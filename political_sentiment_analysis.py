import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_path = "/Users/andrew/pamphletai/distilbert-political-analysis"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

def classify(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    if predicted_class == 0:
        return "Republican"
    elif predicted_class == 1:
        return "Democrat"
    else:
        return "Unknown"
while True:
    text1 = input(">")
    if text1 == "":
        break
    print(classify(text1))