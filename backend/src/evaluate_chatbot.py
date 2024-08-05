import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, '..')))

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from src.core.config import qa

def evaluate_chatbot(chatbot):
    """Function to evaluate the chatbot"""

    # TODO: Need to customize it based on given Knowledgebase
    test_data = [
        {"input": "What is the capital of France? Give me only answer", "expected_output": "Paris"},
        {"input": "Who wrote 'To Kill a Mockingbird'? Give me only answer", "expected_output": "Harper Lee"},
    ]

    y_true = [item['expected_output'] for item in test_data]
    y_pred = [chatbot(item['input'])['result'] for item in test_data]
    print(y_true)
    print(y_pred)
    
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='macro')
    recall = recall_score(y_true, y_pred, average='macro')
    f1 = f1_score(y_true, y_pred, average='macro')
    
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }

metrics = evaluate_chatbot(qa)
print("Result of chatbot evaluation")
print(metrics)