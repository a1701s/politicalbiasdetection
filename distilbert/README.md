---
language:
- en
license: lgpl-3.0
library_name: transformers
tags:
- text-classification
- transformers
- pytorch
- generated_from_keras_callback
metrics:
- accuracy
- f1
datasets:
- m-newhauser/senator-tweets
widget:
- text: "This pandemic has shown us clearly the vulgarity of our healthcare system. Highest costs in the world, yet not enough nurses or doctors. Many millions uninsured, while insurance company profits soar. The struggle continues. Healthcare is a human right. Medicare for all."
  example_title: "Bernie Sanders (D)"
- text: "Team Biden would rather fund the Ayatollah's Death to America regime than allow Americans to produce energy for our own domestic consumption."
  example_title: "Ted Cruz (R)"
---

# distilbert-political-tweets 🗣 🇺🇸

This model is a fine-tuned version of [distilbert-base-uncased](https://huggingface.co/distilbert-base-uncased) on the [m-newhauser/senator-tweets](https://huggingface.co/datasets/m-newhauser/senator-tweets) dataset, which contains all tweets made by United States senators during the first year of the Biden Administration.
It achieves the following results on the evaluation set:
* Accuracy: 0.9076
* F1: 0.9117

## Model description

The goal of this model is to classify short pieces of text as having either Democratic or Republican sentiment. The model was fine-tuned on 99,693 tweets (51.6% Democrat, 48.4% Republican) made by US senators in 2021.

Model accuracy may not hold up on pieces of text longer than a tweet.

### Training hyperparameters

The following hyperparameters were used during training:
- optimizer: Adam
- training_precision: float32
- learning_rate = 5e-5
- num_epochs = 5

### Framework versions

- Transformers 4.16.2
- TensorFlow 2.8.0
- Datasets 1.18.3
- Tokenizers 0.11.6
