# Official source map for PP GPDG

Use this file when you need to resolve current-year thresholds, filing rules, or missing inputs.

## Primary sources by purpose

### 1. Poreska uprava annual guide

Search for the annual guide PDF for the target tax year on `purs.gov.rs`.

Good search patterns:

- `site:purs.gov.rs godisnji porez na dohodak gradjana <tax-year> pdf`
- `site:purs.gov.rs godisnji porez na dohodak gradjana <filing-year> pdf`
- `site:purs.gov.rs postavljene unapred popunjene prijave za godisnji porez na dohodak gradjana`

This guide usually contains:

- annual non-taxable amount
- average annual salary used for the tax
- six-times threshold
- taxpayer allowance amount
- dependent allowance amount
- under-40 deduction amount
- filing and payment deadline
- examples of PP GPDG calculation

### 2. Republicki zavod za statistiku

Use `stat.gov.rs` or `publikacije.stat.gov.rs` to verify the average annual salary for the tax year.

Good search patterns:

- `site:publikacije.stat.gov.rs prosecne zarade po zaposlenom decembar <tax-year>`
- `site:stat.gov.rs prosecna godisnja zarada <tax-year>`

### 3. ePorezi filing instructions

Use these when the user needs the practical filing path, login method, or return status behavior.

Check:

- `https://eporezi.purs.gov.rs/`
- Poreska uprava ePorezi portal pages
- Poreska uprava user guides for login and submission

## Input checklist

Before calculating, gather:

- taxpayer birth date
- number of dependents actually claimed by this taxpayer
- PPP-PO certificates and similar annual proofs
- any foreign income and foreign tax paid
- any refund of overpaid social contributions
- prefilled PP GPDG if available
- whether there is a tax credit claim under the current rules

## Recommended calculation model

Use these resolved parameters as explicit inputs:

- `annual_nontaxable_amount`
- `six_x_average_annual_salary`
- `taxpayer_allowance`
- `dependent_allowance`
- `under_40_additional_deduction`
- `dependents_count`
- `tax_credit`

For income items, prefer one of these forms:

- `after_tax_amount`
- or `taxable_amount` and `tax_and_contrib`

Also track whether each item is eligible for the under-40 deduction.

## Important nuances

- The return surface can be more authoritative than a single certificate because Poreska uprava may classify income differently.
- If the taxpayer is over 40, the under-40 additional deduction is zero even if some income categories would otherwise qualify.
- The total personal allowance can never exceed 50% of `3.12`.
- Additional dependent allowances can be legally present but practically irrelevant when the 50% cap already binds.
- If `3.12` is zero after threshold and allowed deductions, there may be no filing obligation; verify against the current Poreska uprava guide.

## Filing notes

For each target year, verify:

- exact filing deadline
- whether prefilled returns were posted
- allowed login methods for ePorezi
- whether payment details appear only after the return reaches recorded status
