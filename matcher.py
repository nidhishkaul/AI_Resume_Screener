from database import client
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from typing import List

def match_requirements(req_skills:List):
    model = SentenceTransformer("alvperez/skill-sim-model")

    # Load resume data from MongoDB
    collection = client["Resume_Database"]["Resume_Collection"]
    df = pd.DataFrame(list(collection.find()))

    # Embed required skills
    req_skills_emb = model.encode([" ".join(req_skills)], convert_to_tensor=True)

    # Convert skill lists to strings
    resume_skill_docs = [" ".join(skills) for skills in df["skills"]]
    df_skills_emb = model.encode(resume_skill_docs, convert_to_tensor=True)

    # Compute cosine similarity
    similarities = util.pytorch_cos_sim(req_skills_emb, df_skills_emb)[0]
    df["Match_Percent"] = similarities.cpu().numpy()

    return df
