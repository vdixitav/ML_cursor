# Save / load artifacts

from dataclasses import dataclass,asdict
from pathlib import Path
from datetime import datetime
from typing import Any, Dict
import json
import pickle

# Base directory where all artifacts are stored
ARTIFACTS_DIR=Path("output")
ARTIFACTS_DIR.mkdir(exist_ok=True)

def _utc_now()-> str:
    return datetime.utcnow().isoformat()


@dataclass
class ArtifactMeta:
    """
Metadata attached to every artifact for trust & audit. 

   """
    
    name: str
    step: str
    created_at: str
    description: str
    artifact_type: str


@dataclass
class Artifact:
    """
Represents a saved artifact with metadata. 

   """
    
    meta: ArtifactMeta
    path: Path


def save_json(
        name: str,
        payload: Dict[str, Any],
        step: str,
        description: str,

)  -> Artifact:
    """
    save a JSON artifact with embedded metadata.
    """ 

    path= ARTIFACTS_DIR/name 

    meta= ArtifactMeta(
        name=name,
        step=step,
        created_at=_utc_now(),
        description=description,
        artifact_type="json"
    )

    wrapped={
        "meta": asdict(meta),
        "data": payload
    }

    with open(path,'w',encoding="utf-8") as f:
        json.dump(wrapped,f,indent=2)

    return Artifact(meta=meta,path=path)

def save_pickle(
        name: str,
        obj: Any,
        step: str,
        description: str,
) -> Artifact:
    """
Save a Python object (model / pipeline) as pickle.
    Metadata is stored separately for safety.    """

    path= ARTIFACTS_DIR/name 

    meta= ArtifactMeta(
        name=name,
        step=step,
        created_at=_utc_now(),
        description=description,
        artifact_type="pickle"
    )

    

    with open(path,'wb') as f:
        pickle.dump(obj,f)

    meta_path = ARTIFACTS_DIR / f"{name}.meta.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(asdict(meta), f, indent=2)    

    return Artifact(meta=meta,path=path)


def save_markdown(
        name: str,
        content: str,
        step: str,
        description: str, 
) -> Artifact:
    """
    Save a markdown artifact (EDA report, model card, etc.).
    """
    path = ARTIFACTS_DIR / name

    meta = ArtifactMeta(
        name=name,
        step=step,
        created_at=_utc_now(),
        description=description,
        artifact_type="markdown"
    )

    path.write_text(content, encoding="utf-8")

    meta_path = ARTIFACTS_DIR / f"{name}.meta.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(asdict(meta), f, indent=2)

    return Artifact(meta=meta, path=path)
    
    

