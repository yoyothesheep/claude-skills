# Living Specification — [Subsystem Name]

*Authoritative living technical specification of this subsystem as it operates **today in production**. No strikethroughs or retired architectures.*

## Subsystem Overview

[What role this subsystem plays in the overall application, key user workflows supported, and core domain invariants.]

## Domain Model & Architecture

- **Primary Module**: `[path/to/module.py]`
- **Key Entities**:
  - `Entity1`: [Role and responsibilities]
  - `Entity2`: [Role and responsibilities]
- **Seams & External Boundaries**:
  - [Seam description and how data crosses it]

## Workflows & Invariants

### 1. [Primary Workflow]
1. [Step 1]
2. [Step 2]
3. [Step 3]

### 2. [Edge Cases & Error Recovery]
- **Case 1**: [Behavior]
- **Case 2**: [Behavior]

## Verification & Testing Strategy

- Unit & integration tests live under `tests/[subsystem]/`.
- Key assertions: [What must be proven deterministically].
