import re
from collections import Counter

def tokenize(text):
    return re.findall(r'\b\w+\b|[^\w\s]', text.lower())

def calculate_probability(query_tokens, document_tokens, corpus_tokens, lambda_value):
    doc_len = len(document_tokens)
    corpus_len = len(corpus_tokens)
    
    doc_counter = Counter(document_tokens)
    corpus_counter = Counter(corpus_tokens)
    
    probability = 1
    
    for token in query_tokens:
        p_doc = doc_counter[token] / doc_len if doc_len > 0 else 0
        p_corpus = corpus_counter[token] / corpus_len if corpus_len > 0 else 0
        
        smoothed_prob = lambda_value * p_doc + (1 - lambda_value) * p_corpus
        if smoothed_prob == 0:
            smoothed_prob = 1e-10
        
        probability *= smoothed_prob
    
    return probability

n = int(input().strip())
documents = [input().strip() for _ in range(n)]
query = input().strip()

query_tokens = tokenize(query)
corpus_tokens = [token for doc in documents for token in tokenize(doc)]

lambda_value = 0.5

scores = []
for idx, doc in enumerate(documents):
    document_tokens = tokenize(doc)
    score = calculate_probability(query_tokens, document_tokens, corpus_tokens, lambda_value)
    scores.append((score, idx))

scores.sort(key=lambda x: (-x[0], x[1]))

result = [idx for _, idx in scores]
print(result)