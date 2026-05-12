# NBS IPS QR reference

Use this only when you need exact field behavior or troubleshooting detail.

## Primary sources

- NBS IPS generator and validator site: `https://ips.nbs.rs/`
- NBS generator API guide:
  - `https://nbs.rs/QRcode/api/qr/v1/gen/{size}`
  - `https://nbs.rs/QRcode/api/qr/v1/generate/{size}`
- NBS validator API guide:
  - `https://nbs.rs/QRcode/api/qr/v1/validate`
  - `https://nbs.rs/QRcode/api/qr/v1/upload`
- NBS recommendations PDF for textual payloads:
  - `https://ips.nbs.rs/PDF/pdfPreporukeValidacijaLat.pdf`

## Field rules

- `K:PR` for payment order QR
- `V:01`
- `C:1` for UTF-8
- `R` is recipient account and must be exactly 18 digits with no separators
- `N` is recipient name
- `I` is amount with currency prefix and decimal comma, for example `RSD1025,12`
- `P` is optional payer info
- `SF` is payment code
- `S` is payment purpose
- `RO` is reference credit data; in practice use `model` immediately followed by the reference number, for example `97163220000111111111000`

## Common failure cases

- trailing newline at the end of the text payload
- trailing `|`
- account not normalized to 18 digits
- `I` uses decimal point instead of decimal comma
- optional fields included with empty values
- unsupported characters in `N`, `S`, or `P`

## Recommended troubleshooting order

1. Validate the plain text payload with `validate`
2. Fix payload errors until the validator returns `OK`
3. Generate the PNG with `gen` or `generate`
4. Validate the generated image with `upload`

## Account normalization

If the input account is given with dashes in the usual Serbian form, normalize it to:

- first segment: 3 digits
- middle segment: left-pad to 13 digits
- final control segment: 2 digits

Example:

- `840-955845-10` -> `840000000095584510`
- `165-55-74` -> `165000000000005574`

## Practical note

If the NBS validator rejects Cyrillic recipient or purpose text, prefer Latin and regenerate. Treat the validator as the source of truth for the final payload.
