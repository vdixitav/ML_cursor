# Allowed ML actions only


"""

Policy layer to restrict actions to agents are allows to perform.
this file is CRITICAL for production safety.
All agents and LangCgain tools must go throght this policy.
"""

class PolicyViolation(Exception):
    pass

# Explicit allowlist of ML-safe actions

ALLOWD_ACTIONS={
    # DATA
    "load_data",
    'profile_data',
    'run_eda',
    'build_proprocess_pipeline',
    'train_model',
    'eveluate_model',
    'explain_model',
    'export_artifacts',



}

def enforce(action: str) ->None:
    """
    Enforce ML-only policy.

    Parameters

    actions: str

       Name of the action an agent wants to perform.

    Raises

    PlocyViolation
       If the actions is not explicitly allowd.   
    
    """

    if action not in ALLOWD_ACTIONS:
        raise PolicyViolation(
            f"Action '{action}' is not allowd in ML-only agent system."
    )

