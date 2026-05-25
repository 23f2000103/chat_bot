import pandas as pd
from utils.text_matcher import similarity

# Load dataset once
dataset = pd.read_csv("data/KCC_Call_Dataset.csv")

def find_similar_question(user_query):

    best_score = 0
    best_match = None

    for _, row in dataset.iterrows():

        dataset_question = str(row["questions"])

        score = similarity(user_query,dataset_question)

        if score > best_score:

            best_score = score

            best_match = {
                "question": dataset_question,
                "answer": row["answers"],
                "score": score
            }

    return best_match