# Templates

## A. Cascade Template

```python
from typing import Literal, Annotated
from annotated_types import Ge, Le
from pydantic import BaseModel, ConfigDict

class DecisionCascade(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reasoning_summary: str
    skill_match_score: Annotated[int, Ge(1), Le(10)]
    final_decision: Literal["hire", "hold", "reject"]
```

## B. Routing Template (Provider-Safe Split)

```python
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

class VerdictDistortion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reasoning: str
    dimension: Literal["VERDICT"]
    code: Literal["CLASSIFICATION", "CUTOFF", "ATTRIBUTION", "COMPLETENESS", "LOGIC_AND_OR"]
    materiality: Literal["MATERIAL", "NON_MATERIAL"]
    evidence_refs: list[int] = Field(default_factory=list)

class JustificationDistortion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reasoning: str
    dimension: Literal["JUSTIFICATION"]
    code: Literal[
        "EXISTENCE", "ACCURACY", "CLASSIFICATION", "CUTOFF",
        "ATTRIBUTION", "COMPLETENESS", "LOGIC_AND_OR", "RELEVANCE"
    ]
    materiality: Literal["MATERIAL", "NON_MATERIAL"]
    evidence_refs: list[int] = Field(default_factory=list)

class CriterionDistortions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    verdict_distortions: list[VerdictDistortion] = Field(default_factory=list)
    justification_distortions: list[JustificationDistortion] = Field(default_factory=list)
```

## C. Cycle Template

```python
from typing import Literal, Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict

class RiskFactor(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reasoning: str
    severity: Literal["low", "medium", "high"]

class RiskAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    factors: Annotated[list[RiskFactor], MinLen(2), MaxLen(4)]
```

## D. Combined SGR Template (Cascade + Routing + Cycle)

```python
from typing import Literal, Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict, Field

class VerdictDistortion(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reasoning: str
    dimension: Literal["VERDICT"]
    code: Literal["CLASSIFICATION", "CUTOFF", "ATTRIBUTION", "COMPLETENESS", "LOGIC_AND_OR"]
    materiality: Literal["MATERIAL", "NON_MATERIAL"]
    evidence_refs: list[int] = Field(default_factory=list)

class JustificationDistortion(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reasoning: str
    dimension: Literal["JUSTIFICATION"]
    code: Literal[
        "EXISTENCE", "ACCURACY", "CLASSIFICATION", "CUTOFF",
        "ATTRIBUTION", "COMPLETENESS", "LOGIC_AND_OR", "RELEVANCE"
    ]
    materiality: Literal["MATERIAL", "NON_MATERIAL"]
    evidence_refs: list[int] = Field(default_factory=list)

class CriterionStep(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Cascade order
    reasoning_summary: str
    llm_verdict: Literal["YES", "PARTIAL", "NO", "OK", "NOT_OK", "UNKNOWN"]

    # Routing (split branches)
    verdict_distortions: Annotated[list[VerdictDistortion], MinLen(0), MaxLen(16)]
    justification_distortions: Annotated[list[JustificationDistortion], MinLen(0), MaxLen(16)]

    # Final per-step decision field
    evidence_supported_verdicts: Literal["YES", "PARTIAL_OR_YES", "PARTIAL", "PARTIAL_OR_NO", "NO"]
```
