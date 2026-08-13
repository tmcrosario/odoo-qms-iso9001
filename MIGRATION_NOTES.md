# Migration Notes — odoo-qms-iso9001 (→ 19.0)

Module: `qms` (ISO 9001 Quality Management System).

## Context

This repo's `19.0` branch is the **team's own complete upstream migration**
(`upstream/19.0` == `origin/19.0`, tip `848260d`), which migrates the module through the
full `14 → 15 → 16 → 17 → 18 → 19` chain. An earlier automated migration pass in this
workspace had been based on a **stale local `14.0`** and was superseded; the local
`19.0` branch was reset to the team's upstream. This document covers a **small
fix-on-top pass** applied to that current upstream code — it does **not** recreate the
migration from scratch and does **not** discard any team work.

Per the operator's decision for this round: **no OCA pre-commit tooling and no
reformatting** were added (to avoid a large formatting-noise diff over the team's
branch); only the residual deprecations below were fixed.

## Residual deprecations fixed (on top of upstream/19.0)

### Models

- **`_check_recursion()` → `_has_cycle()`** (renamed/removed in 18.0, with **inverted
  semantics**) in `qms/models/finding_origin.py` and `qms/models/weakness_cause.py`. The
  old helper returned `True` when the hierarchy was _valid_; the 18.0+ `_has_cycle()`
  returns `True` when a cycle _exists_. Both `@api.constrains("parent_id")` methods were
  rewritten from `if not super()._check_recursion(): raise ...` to
  `if self._has_cycle(): raise ...`, preserving the original "reject recursive cycles"
  behaviour, and renamed to `_check_parent_recursion` (a plain constraint name, no
  longer shadowing a framework method that no longer exists).

### Views

- `qms/views/finding_views.xml`: converted the 3 remaining `attrs="{...}"` (removed in
  17.0) to direct attribute expressions:
  - `attrs="{'readonly':[('state','not in',['pending'])]}"` →
    `readonly="state not in ['pending']"`
  - `attrs="{'invisible':[('state','not in',['open','done'])]}"` →
    `invisible="state not in ['open','done']"`
  - `attrs="{'readonly':[('state','not in',['open'])]}"` →
    `readonly="state not in ['open']"`

  **Note:** all three were inside a **commented-out block** (the disabled "Plan Review"
  / "Effectiveness Review" groups, lines ~129–146). They are dead code and were harmless
  as-is; they were converted purely so the block is 19.0-correct if it is ever
  re-enabled. No live view node was affected.

## Already correct in the team's 19.0 (verified, no change needed)

- `version` is `19.0.1.0.0`; `<tree>`→`<list>` and `view_mode` tree→list are all done;
  no `name_get`, `fields_view_get`, `xmlid_to_res_id`, `_translate`, `view_type`,
  `t-esc`, `tree_view_ref`, `except_orm`, `@api.one/@api.multi`, or bare
  `_cr/_uid/_context` remain.
- Security: no `category_id`-on-`res.groups` legacy pattern is present in the current
  code (the team restructured security); nothing to migrate to `res.groups.privilege`
  here.

## Removed dependencies

- None.

## Dependencies to verify before push

- None specific to this pass (the team manifest is self-contained on `base`).

## Autosave / onchange → constrains conversions

- None. The recursion invariants are in `@api.constrains` (now using `_has_cycle()`); no
  exception-raising `@api.onchange` exists.

## Items left for human review

- The 3 converted `attrs` live in a commented-out block — confirm whether that "Plan
  Review / Effectiveness Review" feature is meant to be re-enabled at all (out of scope
  here).

## Tooling

- Intentionally **not** added this round (operator decision). The other 9 repos in this
  batch carry the OCA 19.0 pre-commit stack; if consistency is later desired here, it
  can be added as a separate `[ADD]` commit.

## Translations

- Translation regeneration deferred to a later stage.
