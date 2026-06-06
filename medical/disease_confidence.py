from collections import defaultdict
import numpy as np

def disease_confidence(ids, scores, all_chunks):
    disease_scores = defaultdict(list)

    for i, idx in enumerate(ids[0]):
        disease = all_chunks[idx]["metadata"]["disease"]
        disease_scores[disease].append(scores[0][i])
    final_scores = {
        disease: np.mean(vals)
        for disease, vals in disease_scores.items()
    }

    return sorted(final_scores.items(), key=lambda x: x[1], reverse=True)

