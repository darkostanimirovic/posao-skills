# posao-skills

Public collection of practical Codex skills for people who run a Serbian `DOO` or work as `preduzetnik`.

The goal of this repository is to collect reusable skills for recurring admin, tax, payment, and document workflows that show up around running a small business in Serbia.

Current focus:

- generating `IPS QR` payment codes
- calculating `PP GPDG` annual personal income tax

Planned additions:

- invoice creation
- salary change documents
- vacation decisions and related HR/admin paperwork
- other recurring company obligations and templates

## Current skills

### `ips-qr-kod-generator`

Generates and validates Serbian `NBS IPS QR` payment codes from payment details.

Why this is useful:

- instead of typing payment fields into a banking app
- or copying values line by line
- you generate an IPS QR code once and just scan it

What it includes:

- normalization of payment data
- validation against the NBS IPS QR validator
- PNG QR generation
- example input JSON

Location:

- `skills/ips-qr-kod-generator/`

### `godisnji-porez-na-dohodak-gradjana`

Helps calculate and review Serbian `PP GPDG` annual personal income tax filings for any tax year.

What it includes:

- calculation workflow for annual tax
- guidance on where to find official yearly thresholds and allowances
- handling for personal allowance, dependents, under-40 deduction, and tax credit
- example input JSON with rounded illustrative values

Location:

- `skills/godisnji-porez-na-dohodak-gradjana/`

## How to use

This repo does not need installation as an app or package. The intended workflow is simple:

1. Download or clone the repository.
2. Open the `skills/` directory.
3. Copy the whole skill folder you want into your local Codex skills location.

Examples:

- copy one skill folder only
- copy all folders from `skills/`
- keep this repo as a source repo and selectively sync from it later

If you use Codex locally, a common target is `~/.codex/skills/`, but any local skill location you use is fine.

## Clone option

```bash
git clone https://github.com/darkostanimirovic/posao-skills.git
cd posao-skills
```

Then copy the skill folders you want from `./skills/`.

## Download ZIP option

1. Open `https://github.com/darkostanimirovic/posao-skills`
2. Click `Code`
3. Click `Download ZIP`
4. Extract the archive
5. Copy the desired folders from `skills/` into your local skills location

## Notes

- The example values in this repository are anonymous and illustrative.
- Year-sensitive tax calculations should always be checked against current official Serbian sources before use.
- The included scripts are helpers; the relevant `SKILL.md` files explain when and how to use them.
