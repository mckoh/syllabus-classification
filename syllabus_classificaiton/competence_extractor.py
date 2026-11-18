from pydantic import BaseModel
from ollama import chat, embeddings

from .constant import CONTEXT_SIZE
from .constant import EXTRACT_TEMPERATURE, EXTRACTION_PROMPT
from .constant import LANG_MODEL, EMBED_MODEL


class Extraction(BaseModel):
    course_name: str
    competences: list[str]

def extract(text: str) -> Extraction:
    resp = chat(
        model=LANG_MODEL,
        messages=[
            {"role": "system", "content": EXTRACTION_PROMPT},
            {"role": "user", "content": text},
        ],
        format=Extraction.model_json_schema(),
        options={
            "temperature": EXTRACT_TEMPERATURE,
            "num_ctx": CONTEXT_SIZE
        },
    )
    return Extraction.model_validate_json(resp.message.content)