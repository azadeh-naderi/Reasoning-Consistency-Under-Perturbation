from .lexical import lexical_perturbations
from .structural import structural_perturbations
from .distractors import distractor_perturbations

def all_perturbations():
    return {
        "lexical": lexical_perturbations,
        "structural": structural_perturbations,
        "distractors": distractor_perturbations
    }
