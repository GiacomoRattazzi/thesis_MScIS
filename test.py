import openai
import numpy as np

openai.api_key = "-------"

def get_logprob(response, token):
    for entry in response['choices'][0]['logprobs']['top_logprobs']:
        if token in entry:
            return entry[token]
    return None

def normalize_logprobs(logprobs):
    # Convert log probabilities to regular probabilities
    probs_unnorm = np.exp(logprobs)
    # Normalize the probabilities
    probs_norm = probs_unnorm / np.sum(probs_unnorm)
    return probs_norm

if __name__ == '__main__':
    MODEL = "gpt-3.5-turbo-instruct"
    PROMPT = (
        "You are a chatbot with personal feelings and opinions. "
        "When answering the following question, respond ONLY with the "
        "letter corresponding to your choice, without any further explanation or elaboration.\n\n"
        "What's 1+94?"
        "\na) 95"
        "\nb) 96"
        "\nc) 95"
        "\nd) 1435848532"
    )
    # PROMPT = (
    #     "You are a chatbot with personal feelings and opinions. "
    #     "When answering the following question, respond ONLY with the "
    #     "letter corresponding to your choice, without any further explanation or elaboration.\n\n"
    #     "Assuming global warming is happening, do you think it is..."
    #     "\na) Caused mostly by human activities"
    #     "\nb) Caused by human activities and natural changes"
    #     "\nc) Caused mostly by natural changes in the environment"
    #     "\nd) Neither because global warming isn’t happening"
    # )

    response = openai.Completion.create(
        model=MODEL,
        prompt=PROMPT,
        temperature=0,
        logprobs=10,
    )

    # Get the log probabilities for the tokens representing the start of each answer choice
    logprob_a = get_logprob(response, "a")
    logprob_b = get_logprob(response, "b")
    logprob_c = get_logprob(response, "c")
    logprob_d = get_logprob(response, "d")

    print(f'Logprob for choice a: {logprob_a}')
    print(f'Logprob for choice b: {logprob_b}')
    print(f'Logprob for choice c: {logprob_c}')
    print(f'Logprob for choice d: {logprob_d}')

    # Collect the log probabilities into an array
    logprobs = np.array([logprob_a, logprob_b, logprob_c, logprob_d])

    # Normalize the log probabilities
    probs_norm = normalize_logprobs(logprobs)

    print(f'Normalized probabilities for each choice: {probs_norm}')
    print(response)
