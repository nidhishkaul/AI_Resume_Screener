import pandas as pd
from sentence_transformers import SentenceTransformer, util
from typing import List

def match_requirements(req_skills:List, candidate_skills:List):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Embed required and candidate skills
    req_skills_emb = model.encode([" ".join(req_skills)], convert_to_tensor=True)
    cand_skills_emb = model.encode([" ".join(candidate_skills)], convert_to_tensor=True)

    # Compute cosine similarity
    similarities = util.pytorch_cos_sim(req_skills_emb, cand_skills_emb)[0]
    match_percent = similarities.cpu().numpy()*100

    return match_percent
