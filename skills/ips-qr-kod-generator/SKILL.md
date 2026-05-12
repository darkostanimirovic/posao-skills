---
name: ips-qr-kod-generator
description: Generate and validate NBS IPS QR payment codes for Serbia from payment slips, tax orders, government payment instructions, utility bills, or ad hoc payment data. Use when you need to normalize account/model/reference fields, produce a valid IPS text payload, generate PNG QR files, or troubleshoot why an IPS QR is rejected by the NBS validator.
metadata:
  short-description: Generate and validate NBS IPS QR codes
---

# IPS QR Kod Generator

Use this skill for Serbian IPS QR payment codes based on the NBS specification.

Prefer the bundled script for deterministic generation and validation:

- `scripts/generate_ips_qr.py`

Read `references/nbs-ips-qr.md` only when you need the exact field rules, API endpoints, or troubleshooting notes.

## What this skill does

It helps you:

- turn payment instructions into a valid IPS text string;
- normalize a Serbian payment account into the required 18-digit form;
- combine `model` and `poziv na broj` into `RO`;
- generate a PNG QR code via the NBS API;
- validate both the text payload and the generated image with the NBS validator;
- debug common failures such as bad formatting, trailing newline characters, or unsupported characters in text fields.

## Workflow

1. Collect the payment fields.

Required minimum for a `PR` payment QR:

- recipient account
- recipient name
- amount in RSD
- payment code

Common optional fields:

- payment purpose
- reference credit number (`RO`)
- payer data (`P`)

2. Normalize the data before generating.

- `K` is `PR`
- `V` is `01`
- `C` is `1`
- `R` must be exactly 18 digits
- `I` must look like `RSD12000,00`
- `RO` must be the concatenation of `model` and `poziv na broj`, for example `97` + `1632200001111111111000`
- never leave a trailing `|` or newline at the end of the text payload
- omit optional tags entirely when empty

3. Validate the text payload with the NBS validator before trusting it.

The validator is authoritative. If it rejects the payload, fix that first and only then generate the PNG.

4. Generate the PNG and validate the image upload as a final check.

This catches cases where the text is valid but the generated artifact is not what you expect.

## Script usage

Generate from explicit fields:

```bash
python3 scripts/generate_ips_qr.py \
  --account 840-955845-10 \
  --recipient "Primer Primaoca Uplate DOO" \
  --amount 12000.00 \
  --payment-code 253 \
  --purpose "UPLATA PRIMER" \
  --model 97 \
  --reference 1632200001111111111000 \
  --output-prefix ./out/ips-qr-primer
```

Generate from JSON:

```bash
python3 scripts/generate_ips_qr.py \
  --json examples/payment-example.json \
  --output-prefix ./out/ips-qr-primer
```

The script writes:

- `<prefix>.txt` with the IPS text payload
- `<prefix>.png` with the QR image

It validates both by default and exits non-zero if validation fails.

The bundled example file uses clearly fictitious, rounded values and is safe to publish:

- `examples/payment-example.json`

## Character set rule

Use the NBS validator result, not assumptions, to decide whether text is acceptable.

If `N`, `S`, or `P` is rejected because of characters, prefer Latin text. The bundled script can auto-transliterate Serbian Cyrillic text fields to Latin and re-validate.

## When to inspect manually

Inspect the payload manually when:

- the bank app rejects a QR that NBS accepts;
- the payer gave a human-formatted account with dashes or spaces;
- the instruction contains both `model` and `poziv na broj`, and you need to confirm how they combine into `RO`;
- the purpose or recipient text contains characters outside plain Latin letters, digits, and common punctuation.

## Output expectations

Leave the user with:

- the final `.txt` IPS payload;
- the final `.png` QR file;
- a short note on whether the NBS validator returned `OK`;
- any normalization you applied, especially account padding, `RO` construction, or text transliteration.
