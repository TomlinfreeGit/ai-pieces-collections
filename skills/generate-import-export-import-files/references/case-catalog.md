# Import Case Catalog

Use this catalog to generate targeted import files.

## Valid Cases

### V1 - Complex Hierarchy With Composition

- Includes `attributeTypes` with `composition` datatype.
- Composition constraint points to an existing `aspect` entity type.
- Includes deep `$base` inheritance chain (3+ levels).
- Includes shared attribute references across multiple entities.

### V2 - Broad Reuse Graph

- One attribute type is reused by many entity types.
- Multiple assets inherit from the same base.
- No unresolved references.

### V3 - Large Stress Valid Dataset

- 50+ entities with mixed inheritance depths.
- 30+ attribute types including scalar and composition types.
- Cross references remain valid.

## Invalid Cases

### I1 - Missing Base

- At least one `entityTypes[*].$base` points to a missing anchor.
- Keep all other references valid to isolate the failure.

### I2 - Missing Composition Target

- `attributeTypes[*].$datatype` is `composition`.
- `attributeTypes[*].$constraint.$type` points to a missing aspect type anchor.

### I3 - Duplicate Name Collision

- Two entity types share the same `$name` with different anchors.
- Useful for uniqueness/conflict validation behavior.

### I4 - Dangling Attribute Reference

- An entity property points to an unknown attribute type anchor.

### I5 - Multi-Failure Stress Invalid Dataset

- Combines several failures in one file.
- Use only when user explicitly asks for combined failures.

## Suggested Default Pack

- `import-valid-complex.json` from V1.
- `import-invalid-missing-base.json` from I1.
- `import-invalid-composition-missing-type.json` from I2.
- `import-invalid-dangling-attribute-ref.json` from I4.

## Generation Checklist

- Ensure JSON syntax validity.
- Ensure anchors are UUID-like strings.
- Keep one principal fault per invalid file unless requested otherwise.
- Keep section ordering stable for readability:
  - `versionInfo`
  - `attributeTypes`
  - `entityTypes`
  - `referenceTypes`
  - `references`
  - `relationTypes`
