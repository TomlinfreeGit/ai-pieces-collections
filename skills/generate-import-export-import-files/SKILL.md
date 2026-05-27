---
name: generate-import-export-import-files
description: Generate import JSON files for import-export features, including complex and edge-case datasets with multi-level inheritance, composition datatype constraints, cross-entity references, and intentionally invalid variants for test coverage. Use this whenever the user asks for import files, test fixtures, sample import payloads, migration datasets, or import validation cases.
---

# Generate Import-Export Import Files

Use this skill to create high-quality import JSON payloads for import/export testing.

## What This Skill Produces

- Valid import files for happy-path tests.
- Complex import files with deep type hierarchies and cross references.
- Negative-case import files with deliberate violations for validation tests.
- Small, medium, or large datasets depending on requested scope.

## Input Contract

Collect and confirm these inputs before generating files:

- Target schema sections required by the user: `versionInfo`, `attributeTypes`, `entityTypes`, `referenceTypes`, `references`, `relationTypes`.
- Required concepts: `asset`, `aspect`, and any other concept used in the environment.
- Complexity level: `basic`, `complex`, or `stress`.
- Case style: `valid only`, `invalid only`, or `mixed`.
- Determinism preference: stable anchors and names across runs, or fresh anchors every run.

If the user does not specify, default to:

- Include all top-level sections.
- Complexity = `complex`.
- Case style = `mixed`.
- Determinism = stable anchors.

## Generation Rules

1. Start from a valid envelope.
2. Build a consistent anchor map before writing payload sections.
3. Generate `attributeTypes` first, then `entityTypes`, then other sections.
4. For `composition` datatype, always include a valid `$constraint` object and ensure the referenced type exists unless generating a negative case.
5. Do not emit empty constraint objects (`{}`). For datatypes without effective constraints, emit `$constraint: null`.
6. For inheritance chains (`$base`), make parent/ancestor relationships explicit and intentional.
7. Keep references coherent by default: every UUID-like value should resolve to a known type anchor unless the case intentionally tests unresolved references.
8. Preserve import realism: include mixed naming patterns and sparse metadata where useful.
9. When producing invalid cases, isolate one primary failure per file unless the user explicitly asks for multi-failure files.
10. Apply a dedicated namespace prefix for generated type names by default (for example `ImportRunA.`) to reduce collisions with existing types in the target environment.

## Backend Hard Constraints

These constraints are mandatory because the backend validates them strictly.

- Type name (`$name`) must follow the type naming rule:
	- Length `1..255`.
	- Dot-separated with at least two segments.
	- Each segment must start with letter or underscore.
	- Segment characters allowed: letters, digits, underscore, hyphen.
	- Do not start user-defined type names with `anchor.`.
- Datatype enum must be supported exactly.
- Behavior enum must be supported exactly.
- Constraint semantics:
	- `composition` requires a valid anchor constraint object.
	- For datatypes without active constraints, prefer `$constraint: null`.
	- Never emit empty constraint object `{}`.
	- If composition owner is an aspect, avoid asset-target constraint concept.

## Required Consistency Checks

Before finalizing output, self-check:

- Every required top-level field exists.
- Each `$anchor` is unique inside its section.
- `composition` constraints resolve correctly (`$concept`, `$type`, `$abstraction`) for valid cases.
- All `$base` references resolve for valid cases.
- Property references inside `entityTypes` resolve to defined `attributeTypes` anchors for valid cases.
- Every `attributeTypes[*].$datatype` value is from supported enum values only:
	- `aggregation`, `bigstring`, `bool`, `composition`, `enum`, `flags`, `float32`, `float64`, `int16`, `int32`, `int64`, `int8`, `localizedstring`, `raw`, `string`, `timespan`, `timestamp`, `uint16`, `uint32`, `uint64`, `uint8`, `uuid`.
- Every `attributeTypes[*].$behavior` value is from supported enum values only:
	- `constant`, `dynamic`, `readonly`.
- Non-composition datatypes must not carry empty object constraints (`{}`). Use `null` when no concrete constraint is required.
- JSON is syntactically valid.

## Preflight Checklist (Before Returning Output)

Run these checks before final output:

- `attributeTypes[*].$name` and `entityTypes[*].$name` pass type naming rule.
- `attributeTypes[*].$datatype` values are all in supported enum set.
- `attributeTypes[*].$behavior` values are all in supported enum set.
- Non-composition entries do not contain empty object constraints.
- Composition entries contain `$abstraction`, `$concept`, `$type`.
- All referenced anchors (`$base`, composition `$constraint.$type`, entity attribute links) resolve.
- Prefer a consistent namespace prefix on generated names to avoid DB collision risk.

## Complex Case Patterns

Use the patterns below when the user asks for complex coverage:

- Deep inheritance tree: base -> level2 -> level3 -> level4.
- Composition to aspect: asset attribute type with `$datatype: composition` pointing to an `aspect` type.
- Fan-out references: one attribute type reused by multiple entities.
- Duplicate name conflict case: same `$name` with different anchors.
- Broken base case: entity with nonexistent `$base`.
- Broken composition case: composition `$constraint.$type` pointing to missing anchor.
- Mixed valid/invalid pack: one valid file plus N focused invalid files.

For detailed scenario templates, read:

- `references/case-catalog.md`

## Output Format

When creating files, return:

1. A short summary table of generated files and their intent.
2. Exact file paths.
3. The JSON content for each generated file.

If the user asks for direct file creation in workspace, create files under a user-specified folder.
If no folder is provided, default to `spec/import-cases/`.

## Naming Convention

Use descriptive file names:

- `import-valid-complex.json`
- `import-invalid-missing-base.json`
- `import-invalid-composition-missing-type.json`
- `import-mixed-pack-index.md` (optional manifest)

## Prompt Handling Strategy

When user intent is underspecified:

- Ask at most 3 short clarification questions only if needed.
- Otherwise proceed with sensible defaults and state the assumptions.

When user provides a sample payload:

- Preserve its structural conventions.
- Extend it with requested complexity while keeping it internally consistent.

## Output Example

Use only the following valid example as the reference output shape:

```json
{
    "versionInfo": {
        "dbVersion": 4,
        "backendVersion": "v2.4.0-rc.0-72-gcd6a95a5-dirty"
    },
    "attributeTypes": [
        {
            "$anchor": "baa4c61c-6986-41b2-89bd-17e1d4980899",
            "$name": "My.AttributeType.EnergyAspectRef",
            "$displayname": {},
            "$base": null,
            "$behavior": "dynamic",
            "$nullable": true,
            "$datatype": "composition",
            "$array": false,
            "$minimum": 0,
            "$maximum": 0,
            "$unit": "",
            "$constraint": {
                "$abstraction": "instance",
                "$concept": "aspect",
                "$type": "d0110588-4c52-426c-95c0-a0b69b920114"
            },
            "$metadata": {}
        }
    ],
    "entityTypes": [
        {
            "$concept": "asset",
            "$anchor": "a0dcb3c2-7ac5-43aa-b42f-33b9b0094405",
            "$name": "My.AssetType.Conveyor",
            "$displayname": {},
            "$base": "0ad068b1-b1a2-420a-9907-3c03c2784e90",
            "$metadata": {},
            "runningState": "29931149-ff77-4da6-bec6-7ce3ddfdef96",
            "speed": "7069a47e-180b-4bbe-bf46-eb658cc2bcba",
            "temperature": "12cdf442-21f6-45f3-a569-1a103d8a3382",
            "$_basePath": [
                {
                    "$anchor": "0ad068b1-b1a2-420a-9907-3c03c2784e90",
                    "$concept": "asset",
                    "$abstraction": "type",
                    "$name": "anchor.asset-base",
                    "$displayname": {}
                }
            ]
        },
        {
            "$concept": "asset",
            "$anchor": "e95a3851-cc79-4822-ae6d-412e69ff3e80",
            "$name": "My.AssetType.Gateway",
            "$displayname": {},
            "$base": "0ad068b1-b1a2-420a-9907-3c03c2784e90",
            "$metadata": {},
            "$_basePath": [
                {
                    "$anchor": "0ad068b1-b1a2-420a-9907-3c03c2784e90",
                    "$concept": "asset",
                    "$abstraction": "type",
                    "$name": "anchor.asset-base",
                    "$displayname": {}
                }
            ]
        },
        {
            "$concept": "asset",
            "$anchor": "31ad1180-29ef-4fef-b9f3-acd2b7caafcc",
            "$name": "My.AssetType.Line",
            "$displayname": {},
            "$base": "0ad068b1-b1a2-420a-9907-3c03c2784e90",
            "$metadata": {},
            "actualOutput": "3c398ed4-c279-42ab-9c80-c4f7f18ab8b9",
            "lineStatus": "a9e33f8a-3d37-40da-87f1-250adfc280e1",
            "plannedOutput": "3c398ed4-c279-42ab-9c80-c4f7f18ab8b9",
            "$_basePath": [
                {
                    "$anchor": "0ad068b1-b1a2-420a-9907-3c03c2784e90",
                    "$concept": "asset",
                    "$abstraction": "type",
                    "$name": "anchor.asset-base",
                    "$displayname": {}
                }
            ]
        },
        {
            "$concept": "aspect",
            "$anchor": "d0110588-4c52-426c-95c0-a0b69b920114",
            "$name": "MY.AspectType.Energy",
            "$displayname": {},
            "$base": "39880264-3da8-4b76-9811-a0187c1d2909",
            "$metadata": {},
            "currentPower": "12cdf442-21f6-45f3-a569-1a103d8a3382",
            "dailyEnergy": "12cdf442-21f6-45f3-a569-1a103d8a3382",
            "monthlyEnergy": "12cdf442-21f6-45f3-a569-1a103d8a3382"
        },
        {
            "$concept": "asset",
            "$anchor": "e5605d1f-06e3-4c3d-9339-dc710e8130cd",
            "$name": "My.AssetType.Motor",
            "$displayname": {},
            "$base": "0ad068b1-b1a2-420a-9907-3c03c2784e90",
            "$metadata": {},
            "EnergyAspectRef": "baa4c61c-6986-41b2-89bd-17e1d4980899",
            "$_basePath": [
                {
                    "$anchor": "0ad068b1-b1a2-420a-9907-3c03c2784e90",
                    "$concept": "asset",
                    "$abstraction": "type",
                    "$name": "anchor.asset-base",
                    "$displayname": {}
                }
            ]
        },
        {
            "$concept": "asset",
            "$anchor": "961cff5b-4830-4002-b367-c13c67feab68",
            "$name": "My.AssetType.Robot",
            "$displayname": {},
            "$base": "0ad068b1-b1a2-420a-9907-3c03c2784e90",
            "$metadata": {},
            "alarmState": "29931149-ff77-4da6-bec6-7ce3ddfdef96",
            "cycleTime": "29931149-ff77-4da6-bec6-7ce3ddfdef96",
            "mode": "a9e33f8a-3d37-40da-87f1-250adfc280e1",
            "$_basePath": [
                {
                    "$anchor": "0ad068b1-b1a2-420a-9907-3c03c2784e90",
                    "$concept": "asset",
                    "$abstraction": "type",
                    "$name": "anchor.asset-base",
                    "$displayname": {}
                }
            ]
        },
        {
            "$concept": "asset",
            "$anchor": "0f653145-2575-4012-94b2-99259dddadec",
            "$name": "MY.AssetType.Robot.Core_battery",
            "$displayname": {},
            "$base": "961cff5b-4830-4002-b367-c13c67feab68",
            "$metadata": {},
            "build_date": "754610f5-84bc-48fe-8ae2-8ea0cac89b02",
            "expire_date": "754610f5-84bc-48fe-8ae2-8ea0cac89b02",
            "service_duration": "f0e6a44d-41b1-4855-9fbc-a88b61bd9d0f",
            "$_basePath": [
                {
                    "$anchor": "0ad068b1-b1a2-420a-9907-3c03c2784e90",
                    "$concept": "asset",
                    "$abstraction": "type",
                    "$name": "anchor.asset-base",
                    "$displayname": {}
                },
                {
                    "$anchor": "961cff5b-4830-4002-b367-c13c67feab68",
                    "$concept": "asset",
                    "$abstraction": "type",
                    "$name": "My.AssetType.Robot",
                    "$displayname": {}
                }
            ]
        },
        {
            "$concept": "asset",
            "$anchor": "012ccc66-a9f4-4a1d-95f6-992d8a5995f8",
            "$name": "My.AssetType.Sensor",
            "$displayname": {},
            "$base": "0ad068b1-b1a2-420a-9907-3c03c2784e90",
            "$metadata": {},
            "$_basePath": [
                {
                    "$anchor": "0ad068b1-b1a2-420a-9907-3c03c2784e90",
                    "$concept": "asset",
                    "$abstraction": "type",
                    "$name": "anchor.asset-base",
                    "$displayname": {}
                }
            ]
        },
        {
            "$concept": "asset",
            "$anchor": "3fc2c7af-59e5-43b5-90e6-b2effbcf9e9d",
            "$name": "My.Third",
            "$displayname": {},
            "$base": "0f653145-2575-4012-94b2-99259dddadec",
            "$metadata": {},
            "$_basePath": [
                {
                    "$anchor": "0ad068b1-b1a2-420a-9907-3c03c2784e90",
                    "$concept": "asset",
                    "$abstraction": "type",
                    "$name": "anchor.asset-base",
                    "$displayname": {}
                },
                {
                    "$anchor": "961cff5b-4830-4002-b367-c13c67feab68",
                    "$concept": "asset",
                    "$abstraction": "type",
                    "$name": "My.AssetType.Robot",
                    "$displayname": {}
                },
                {
                    "$anchor": "0f653145-2575-4012-94b2-99259dddadec",
                    "$concept": "asset",
                    "$abstraction": "type",
                    "$name": "MY.AssetType.Robot.Core_battery",
                    "$displayname": {}
                }
            ]
        }
    ],
    "referenceTypes": [],
    "references": [],
    "relationTypes": []
}
```
