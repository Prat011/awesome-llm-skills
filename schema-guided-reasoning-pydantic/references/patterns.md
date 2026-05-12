# SGR Patterns Playbook

## Why SGR
Schema-Guided Reasoning turns expert checklists into executable output structures.
This makes reasoning reproducible, auditable, and easier to evaluate.

## 1) Cascade
Purpose: force ordered reasoning steps.

Use when:
- model must not skip intermediate checkpoints,
- final decision quality depends on explicit intermediate state.

Schema shape:
- one object,
- fields declared in reasoning order.

Typical order:
1. context summary
2. focused evaluation
3. final decision

## 2) Routing
Purpose: force explicit path choice.

Use when:
- task has mutually exclusive branches,
- each branch needs different required fields.

Preferred strict shape:
- separate branch containers (provider-safe), or
- discriminated unions if provider supports them.

Branch rules:
- branch id is a single-value `Literal`.
- each branch has its own `code` literal set.

## 3) Cycle
Purpose: force repeated reasoning with bounds.

Use when:
- model must enumerate factors/findings/tool calls,
- count of items must be controlled.

Schema shape:
- list of item model,
- explicit min/max bounds.

## Composition
Real workloads combine patterns:
- Cascade for top-level sequence,
- Routing inside each step,
- Cycle for repeated items.

## Provider-Safe Adaptation
If strict API rejects `oneOf` in array items:
- replace `list[Union[A,B]]` with separate lists `list[A]` and `list[B]`.
- keep branch strictness via branch-local `Literal` fields.

## Anti-Patterns
1. Shared enum + `model_validator` for route admissibility.
2. Missing branch literal lock.
3. Over-constraining schema without preserving reasoning checkpoints.
4. Relying on field descriptions for mandatory behavior — see [`cross-cutting-caveats.md`](cross-cutting-caveats.md).
