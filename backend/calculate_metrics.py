from typing import Dict, Union
import nltk
from textblob import TextBlob
import re
import sacrebleu


# Ensure you have downloaded necessary NLTK data
nltk.download('punkt')

# Define evaluation criteria
CRITERIA = [
    "relevance",
    "accuracy",
    "coherence",
    "completeness",
    "creativity",
    "tone",
    "alignment_with_intent"
]

# Example weights for each criterion
WEIGHTS = {
    "relevance": 0.2,
    "accuracy": 0.2,
    "coherence": 0.1,
    "completeness": 0.2,
    "creativity": 0.1,
    "tone": 0.1,
    "alignment_with_intent": 0.1
}

def evaluate_response(response: str, expected_output: str) -> Dict[str, Union[float, Dict[str, float]]]:
    """
    Evaluate the LLM response based on defined criteria.

    Parameters:
    - response: The LLM-generated response to evaluate.
    - expected_output: The expected or ideal output for comparison.

    Returns:
    - A dictionary with scores for each criterion and an overall score.
    """

    scores = {criterion: 0.0 for criterion in CRITERIA}

    # Relevance: Check how relevant the response is to the input query.
    scores["relevance"] = evaluate_relevance(response, expected_output)

    # Accuracy: Assess the factual correctness of the response.
    scores["accuracy"] = evaluate_accuracy(response, expected_output)

    # Coherence: Evaluate logical flow and consistency within the response.
    scores["coherence"] = evaluate_coherence(response)

    # Completeness: Determine if the response is thorough and covers the topic.
    scores["completeness"] = evaluate_completeness(response, expected_output)

    # Creativity: Assess originality and innovation in the response.
    scores["creativity"] = evaluate_creativity(response)

    # Tone: Ensure the response maintains an appropriate tone for the context.
    scores["tone"] = evaluate_tone(response, expected_output)

    # Alignment with Intent: Check if the response aligns with the user's intent.
    scores["alignment_with_intent"] = evaluate_alignment(response, expected_output)

    # Calculate the weighted overall score
    overall_score = sum(scores[criterion] * WEIGHTS[criterion] for criterion in CRITERIA)

    return {
        "scores": scores,
        "overall_score": overall_score
    }

def evaluate_relevance(response: str, expected_output: str) -> float:
    """
    Evaluate the relevance of the response compared to the expected output.
    A simple approach using BLEU score to measure similarity.
    """
    
    # Calculate the BLEU score
    score = sacrebleu.sentence_bleu(response, [expected_output]).score
    
    # Normalizing the score to a 0-1 range
    return score / 100

def evaluate_accuracy(response: str, expected_output: str) -> float:
    """
    Evaluate the accuracy of the response based on keyword matching.
    This is a simplified approach; consider more advanced methods for complex needs.
    """
    response_tokens = set(nltk.word_tokenize(response.lower()))
    expected_tokens = set(nltk.word_tokenize(expected_output.lower()))
    
    matching_tokens = response_tokens.intersection(expected_tokens)
    accuracy_score = len(matching_tokens) / len(expected_tokens) if expected_tokens else 0
    return accuracy_score

def evaluate_coherence(response: str) -> float:
    """
    Evaluate the coherence of the response.
    We assume coherence if sentences are logically connected.
    """
    sentences = nltk.sent_tokenize(response)
    
    # Assume each sentence should be related in some way; simple check
    coherence_score = sum(1 for i in range(len(sentences) - 1) if sentences[i] in sentences[i+1]) / max(len(sentences) - 1, 1)
    return coherence_score


def evaluate_completeness(response: str, expected_output: str) -> float:
    """
    Evaluate if the response is complete by comparing length and coverage.
    """
    response_length = len(response.split())
    expected_length = len(expected_output.split())
    
    completeness_score = min(response_length / expected_length, 1.0)
    return completeness_score

def evaluate_creativity(response: str) -> float:
    """
    Evaluate creativity by checking for uncommon phrases or word usage.
    """
    uncommon_words = len([word for word in response.split() if len(word) > 7])  # Example of using complex words
    creativity_score = uncommon_words / len(response.split()) if response else 0
    return creativity_score

def evaluate_tone(response: str, expected_output: str) -> float:
    """
    Evaluate if the tone is consistent with the expected output.
    """
    response_blob = TextBlob(response)
    expected_blob = TextBlob(expected_output)
    
    tone_difference = abs(response_blob.sentiment.polarity - expected_blob.sentiment.polarity)
    tone_score = max(1 - tone_difference, 0)
    return tone_score

def evaluate_alignment(response: str, expected_output: str) -> float:
    """
    Evaluate alignment by checking for key phrases related to the intent.
    """
    key_phrases = re.findall(r'\b\w+\b', expected_output)
    alignment_score = sum(1 for phrase in key_phrases if phrase in response) / len(key_phrases) if key_phrases else 0
    return alignment_score


if __name__ == "__main__":
    response = "This is a sample response from the LLM."
    expected_output = "This is what I expected from the LLM."

    evaluation_result = evaluate_response(response, expected_output)

    print("Evaluation Scores:", evaluation_result["scores"])
    print("Overall Score:", evaluation_result["overall_score"])
