from pydantic import BaseModel, Field
from typing import Literal


class ExtractedCompetence(BaseModel):
    evidence: str = Field(
        description="Exaktes, wörtliches Zitat aus der Kursbeschreibung als Beleg."
    )
    match_type: Literal["direct", "indirect"] = Field(
        description="Wurde die Kompetenz explizit ('direct') oder implizit ('indirect') genannt?"
    )
    name: str = Field(
        description="Exakter Name der Kompetenz aus dem JSON-Kompetenzrahmen."
    )


class Extraction(BaseModel):
    course_name: str = Field(description="Titel des Kurses aus der Beschreibung.")
    competences: list[ExtractedCompetence] = Field(
        default_factory=list,
        description="Liste der nachweislich abgedeckten Kompetenzen."
    )