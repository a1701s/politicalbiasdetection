# politicalbiasdetection
Political Bias detection with NLP, BERT, and GDELT 2.0

Base model was https://huggingface.co/m-newhauser/distilbert-political-tweets, and framework for GDELT access is from alex9smith's GDELT Doc, check them out!

This project can be run by running app.py.

# Process

Here's how it works
1. It uses GDELT 2.0 to find article websites online, in the form of URL, Title, and Author
2. Once it has access to the website's URL, it uses BeautifulSoup and urllib to scrape the site for the actual news text and title
3. It then pushes the article through a BERT summarizer, shrinking down the text but still keeping the important points
4. Finally it ranks both the title and website summary with the finetuned political analysis model.

# Potential Improvements

1. Summarizer may affect the end product - Fixed: Summarizer does not affect quotes as much, so simply ramp up importance of quotes to fix the offset in the political detection model

# Output

Output will look something like this:

https://www.bendbulletin.com/nation/trump-pleads-not-guilty-to-34-charges-admonished-by-judge/article_941248f4-c3c9-52c0-a8e1-707d30ee6569.html
('Trump pleads not guilty to 34 charges; admonished by judge | Nation | bendbulletin.com', 'Democrat', 'Donald Trump is the only ex-president ever to be charged with a crime. He is accused of falsifying business records in a hush money investigation. The indictment centers on allegations that Trump falsified internal business records at his private company. The arraignment in a Manhattan courtroom was a stunning — and humbling — spectacle for the former president, putting him face-to-face with prosecutors who bluntly accused him of criminal conduct and setting the stage for a possible criminal trial in the city where he became a celebrity.', 'Democrat')

With the format ('<Title>', '<Political Leaning>', '<Summarized Article>', '<Political Leaning>').

The end goal of this project was to allow me to easily create datasets that I can use for further projects.
