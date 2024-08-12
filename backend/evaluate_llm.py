import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir)))

from calculate_metrics import evaluate_response
from src.core.config import get_qa_chain


def average(numbers):
    if len(numbers) == 0:
        return 0  # Handle empty list case
    return sum(numbers) / len(numbers)

def evaluate_chatbot(chatbot):
    """Function to evaluate the chatbot"""

    # TODO: Need to update more questions
    test_data = [
        {"input": "How Is Apollo Data Sourced and Collected?", "expected_output": """
         Apollo collects and verifies data against multiple data sources to identify the best source of truth. There are 4 main ways in which Apollo collects data:
Data contributor network: Apollo has a strong database thanks to its large network of over 2 million data contributors that share information about their business contacts with Apollo in the course of using Apollo services. This means that Apollo can run verification checks against connected inboxes and CRMs.
Engagement suite: Apollo's powerful engagement tools enable it to track email replies and bounces to collect and verify valid emails against invalid ones.
Public data crawling: Apollo has proprietary algorithms that regularly crawl the web at scale, parse public-facing websites, and build a web-wide index of people and company data.
Third-party data providers: Apollo processes over 270 million records monthly from carefully vetted third-party data providers. These partnerships help to complement Apollo's already highly accurate and ever-growing database with additional high-quality verified data.
At Apollo, data isn't single-sourced. The combination of its multiple data sources, proprietary algorithms, and data network of over 2 million contributors allow Apollo to provide the best-in-class data coverage and quality.
"""},
        {"input": "How Does Apollo's Data Compare to Others?", "expected_output": """
         Apollo consistently expands and refines its database to offer you the most accessible, trustworthy B2B data. To identify the best source of truth, Apollo collects and verifies data against multiple data sources as well as via its:
Network of over 2 million data contributors.
Email engagement tools.
Verified third-party data providers.
Crawling of public data sources.
Compared to other B2B databases, Apollo offers over 65+ data attribute filters so you can find and reach your entire target market.
         """},
    ]

    final_scores = []
    for item in test_data:
        print(f"testing input: {item['input']}")
        response = chatbot(item['input'])['result']
        evaluation_result = evaluate_response(response, item['expected_output'])
        final_scores.append(evaluation_result['overall_score'])

    return average(final_scores)
    

qa = get_qa_chain()
result = evaluate_chatbot(qa)
print("Result of chatbot evaluation")
print(result)