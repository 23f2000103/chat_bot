import pandas as pd
import re

# Load dataset

df = pd.read_csv("data/KCC_Call_Dataset.csv")

# -------------------------------------------------
# STANDARDIZE COLUMN NAMES
# -------------------------------------------------

new_columns = []

for col in df.columns:

    cleaned_col = col.strip().lower()

    new_columns.append(cleaned_col)

df.columns = new_columns

# Rename columns if needed

column_mapping = {
    "question": "questions",
    "answer": "answers"
}

for old_col, new_col in column_mapping.items():

    if old_col in df.columns:
        df.rename(columns={old_col: new_col}, inplace=True)

# -------------------------------------------------
# REMOVE EMPTY ROWS
# -------------------------------------------------

df.dropna(subset=["questions", "answers"], inplace=True)

# -------------------------------------------------
# LOWERCASE NORMALIZATION
# -------------------------------------------------

df["questions"] = df["questions"].astype(str).str.lower()
df["answers"] = df["answers"].astype(str).str.lower()

# -------------------------------------------------
# REMOVE EXTRA SPACES
# -------------------------------------------------

def clean_spaces(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


df["questions"] = df["questions"].apply(clean_spaces)
df["answers"] = df["answers"].apply(clean_spaces)


# -------------------------------------------------
# REMOVE SPECIAL SYMBOLS
# -------------------------------------------------

def remove_symbols(text):

    return re.sub(r"[^a-zA-Z0-9\s]", "", text)


df["questions"] = df["questions"].apply(remove_symbols)
df["answers"] = df["answers"].apply(remove_symbols)

# -------------------------------------------------
# REMOVE VERY SHORT / MEANINGLESS ROWS
# -------------------------------------------------

meaningless_words = [
    "ok",
    "done",
    "yes",
    "no",
    "suggested",
    "explained",
    "answered",
    "gave him in details",
    "given detail infornation",
    "explain detail",
    "explain details"
]

def meaningful(text):

    if len(text.split()) < 3:
        return False

    if text.strip() in meaningless_words:
        return False

    return True


df = df[df["questions"].apply(meaningful)]
df = df[df["answers"].apply(meaningful)]

# -------------------------------------------------
# REMOVE DUPLICATES
# -------------------------------------------------

df = df.groupby("questions")["answers"].apply(list).reset_index()
# -------------------------------------------------
# STANDARDIZE AGRICULTURAL TERMS
# -------------------------------------------------

term_mapping = {
    "paddy": "rice",
    "fungus": "fungal disease",
    "bugs": "pests",
    "insects": "pests"
}


def standardize_terms(text):

    if isinstance(text, list):

        cleaned_list = []

        for item in text:

            for old_term, new_term in term_mapping.items():
                item = item.replace(old_term, new_term)

            cleaned_list.append(item)

        return cleaned_list

    else:

        for old_term, new_term in term_mapping.items():
            text = text.replace(old_term, new_term)

        return text


df["questions"] = df["questions"].apply(standardize_terms)
df["answers"] = df["answers"].apply(standardize_terms)

# -------------------------------------------------
# SAVE CLEANED DATASET
# -------------------------------------------------

df.to_csv("data/cleaned_dataset.csv",index=False)

print("Dataset cleaned successfully")
print(f"Remaining rows: {len(df)}")