---
name: godisnji-porez-na-dohodak-gradjana
description: Calculate and review Serbian annual personal income tax filings on PP GPDG for any tax year. Use when you need to determine the applicable non-taxable threshold, six-times threshold, personal allowance, dependent allowance, under-40 deduction, tax credit, annual tax due, or filing steps on ePorezi based on official current-year sources.
metadata:
  short-description: Calculate Serbian PP GPDG annual tax
---

# Godisnji Porez na Dohodak Gradjana

Use this skill for Serbian `PP GPDG` annual personal income tax calculations and filing review.

This skill is year-sensitive. Always resolve the target tax year explicitly and browse official sources before calculating.

Prefer the bundled script for arithmetic once the current-year parameters are known:

- `scripts/compute_pp_gpdg.py`

Read `references/official-sources.md` when you need the official source map, search patterns, or a checklist of inputs.

## What this skill does

It helps you:

- identify which calendar year is being taxed and which filing year applies;
- find the current official threshold and allowance amounts;
- map source documents into PP GPDG-style calculation buckets;
- calculate annual tax under the current Serbian structure;
- review a prefilled ePorezi return and explain why it differs from raw certificates;
- outline how to submit and pay through ePorezi.

## Source policy

Use primary sources only:

- Poreska uprava (`purs.gov.rs`)
- ePorezi (`eporezi.purs.gov.rs`)
- Republicki zavod za statistiku (`stat.gov.rs` or `publikacije.stat.gov.rs`)
- the relevant law text only when the annual guide is not enough

Do not rely on blogs or calculators for final numbers.

## Workflow

1. Fix the time frame.

- identify the tax year, for example `<tax-year>`
- identify the filing year, for example `<filing-year>`
- use explicit dates in the explanation

2. Resolve the official annual parameters for that tax year.

At minimum verify:

- annual non-taxable amount
- six-times average annual salary threshold for the 15% bracket
- taxpayer allowance
- dependent allowance per family member
- 50% cap on total personal allowances
- under-40 additional deduction, if applicable for that tax year
- filing deadline and payment deadline

3. Collect raw inputs.

Typical sources:

- `PPP-PO` certificates
- prefilled `PP GPDG` return on ePorezi
- foreign tax certificates
- evidence of refund of overpaid social contributions
- self-assessed income records

4. Prefer the prefilled ePorezi return as the filing surface if it exists.

If raw documents and the prefilled return differ, explain the difference before changing anything. Do not blindly sum certificate lines into the return without checking how the income was classified by Poreska uprava.

5. Compute in this order.

- annual income items after deduction of paid tax and contributions
- add refund of overpaid contributions if applicable
- apply under-40 additional deduction only to eligible income groups and only if the taxpayer was under 40 on `31.12.` of the tax year
- subtract the annual non-taxable amount
- apply taxpayer and dependent allowances, capped at 50% of `3.12`
- split the remaining base into:
  - up to six-times average annual salary at 10%
  - excess above that at 15%
- subtract tax credit if applicable, capped by law

6. Watch the edge cases.

- age is tested on `31.12.` of the tax year
- dependent allowances cannot be duplicated across taxpayers
- the personal allowance cap can make extra dependents irrelevant in practice
- portal fields are in dinars without decimals
- ePorezi arithmetic may truncate fractional dinars rather than round up; prefer portal numbers if you already have them

7. Explain filing steps only after the arithmetic is clear.

Typical path:

- open `PP GPDG` on ePorezi
- verify or correct data
- sign and submit
- pay once the return is recorded and payment details are available

## Script usage

Prepare a JSON file with the current-year parameters and annualized income items, then run:

```bash
python3 scripts/compute_pp_gpdg.py --input examples/rounded-example.json
```

Use the script only after confirming the current-year legal structure still matches the assumptions in the script.

The bundled example file uses rounded, obviously illustrative figures and is safe to publish:

- `examples/rounded-example.json`

## Output expectations

Leave the user with:

- the resolved official threshold and allowance values for the target tax year;
- a step-by-step tax calculation;
- any assumptions or unresolved discrepancies;
- the filing deadline and how to submit through ePorezi.
