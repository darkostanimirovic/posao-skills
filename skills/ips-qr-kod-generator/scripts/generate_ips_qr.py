#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.error
import urllib.request
from decimal import Decimal, InvalidOperation
from pathlib import Path


CYR_TO_LAT = {
    "А": "A", "а": "a",
    "Б": "B", "б": "b",
    "В": "V", "в": "v",
    "Г": "G", "г": "g",
    "Д": "D", "д": "d",
    "Ђ": "Dj", "ђ": "dj",
    "Е": "E", "е": "e",
    "Ж": "Z", "ж": "z",
    "З": "Z", "з": "z",
    "И": "I", "и": "i",
    "Ј": "J", "ј": "j",
    "К": "K", "к": "k",
    "Л": "L", "л": "l",
    "Љ": "Lj", "љ": "lj",
    "М": "M", "м": "m",
    "Н": "N", "н": "n",
    "Њ": "Nj", "њ": "nj",
    "О": "O", "о": "o",
    "П": "P", "п": "p",
    "Р": "R", "р": "r",
    "С": "S", "с": "s",
    "Т": "T", "т": "t",
    "Ћ": "C", "ћ": "c",
    "У": "U", "у": "u",
    "Ф": "F", "ф": "f",
    "Х": "H", "х": "h",
    "Ц": "C", "ц": "c",
    "Ч": "C", "ч": "c",
    "Џ": "Dz", "џ": "dz",
    "Ш": "S", "ш": "s",
}


def parse_args():
    parser = argparse.ArgumentParser(description="Generate and validate an NBS IPS QR code.")
    parser.add_argument("--json", help="Path to JSON file with QR fields.")
    parser.add_argument("--account")
    parser.add_argument("--recipient")
    parser.add_argument("--amount")
    parser.add_argument("--payment-code")
    parser.add_argument("--purpose")
    parser.add_argument("--model")
    parser.add_argument("--reference")
    parser.add_argument("--ro", help="Full RO value. If omitted, it is built from --model and --reference.")
    parser.add_argument("--payer")
    parser.add_argument("--output-prefix", required=True)
    parser.add_argument("--size", type=int, default=600)
    parser.add_argument("--lang", default="sr_RS")
    parser.add_argument("--skip-upload-validate", action="store_true")
    parser.add_argument("--no-auto-latinize", action="store_true")
    return parser.parse_args()


def load_payload(args):
    if args.json:
        data = json.loads(Path(args.json).read_text(encoding="utf-8"))
    else:
        data = {
            "R": args.account,
            "N": args.recipient,
            "I": args.amount,
            "SF": args.payment_code,
            "S": args.purpose,
            "P": args.payer,
        }
        if args.ro:
            data["RO"] = args.ro
        elif args.model or args.reference:
            if not (args.model and args.reference):
                raise SystemExit("Both --model and --reference are required when --ro is omitted.")
            data["RO"] = f"{clean_reference(args.model)}{clean_reference(args.reference)}"
    data.setdefault("K", "PR")
    data.setdefault("V", "01")
    data.setdefault("C", "1")
    return data


def clean_reference(value):
    if value is None:
        return None
    return "".join(ch for ch in str(value).strip() if ch.isalnum())


def normalize_account(value):
    if not value:
        raise SystemExit("Recipient account is required.")
    raw = str(value).strip()
    digits = "".join(ch for ch in raw if ch.isdigit())
    if len(digits) == 18:
        return digits
    parts = [part for part in raw.replace(" ", "").split("-") if part]
    if len(parts) == 3 and all(part.isdigit() for part in parts):
        bank, body, control = parts
        if len(bank) > 3 or len(control) > 2 or len(body) > 13:
            raise SystemExit(f"Cannot normalize account: {value}")
        return f"{int(bank):03d}{int(body):013d}{int(control):02d}"
    raise SystemExit(f"Recipient account must normalize to 18 digits: {value}")


def normalize_amount(value):
    if value is None:
        raise SystemExit("Amount is required.")
    raw = str(value).strip().replace("RSD", "").replace(" ", "")
    if "," in raw and "." in raw:
        last_comma = raw.rfind(",")
        last_dot = raw.rfind(".")
        if last_comma > last_dot:
            raw = raw.replace(".", "").replace(",", ".")
        else:
            raw = raw.replace(",", "")
    elif "," in raw:
        raw = raw.replace(".", "").replace(",", ".")
    try:
        amount = Decimal(raw)
    except InvalidOperation as exc:
        raise SystemExit(f"Invalid amount: {value}") from exc
    if amount < 0:
        raise SystemExit("Amount cannot be negative.")
    return f"RSD{amount.quantize(Decimal('0.01'))}".replace(".", ",")


def transliterate_text(value):
    if value is None:
        return None
    return "".join(CYR_TO_LAT.get(ch, ch) for ch in value)


def normalize_payload(data):
    payload = {
        "K": "PR",
        "V": "01",
        "C": "1",
        "R": normalize_account(data.get("R")),
        "N": str(data.get("N", "")).strip(),
        "I": normalize_amount(data.get("I")),
        "SF": f"{int(str(data.get('SF')).strip()):03d}",
    }
    if not payload["N"]:
        raise SystemExit("Recipient name is required.")
    if data.get("S"):
        payload["S"] = str(data["S"]).strip()
    if data.get("P"):
        payload["P"] = str(data["P"]).strip()
    if data.get("RO"):
        payload["RO"] = clean_reference(data["RO"])
    return payload


def build_text(payload):
    order = ["K", "V", "C", "R", "N", "I", "P", "SF", "S", "RO"]
    parts = []
    for key in order:
        value = payload.get(key)
        if value is None or value == "":
            continue
        parts.append(f"{key}:{value}")
    return "|".join(parts)


def post_text(url, text, lang):
    request = urllib.request.Request(
        f"{url}?lang={lang}",
        data=text.encode("utf-8"),
        headers={"Content-Type": "text/plain; charset=utf-8"},
    )
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def post_json_image(url, payload, lang):
    request = urllib.request.Request(
        f"{url}?lang={lang}",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    with urllib.request.urlopen(request) as response:
        return response.read()


def upload_validate(url, image_path, lang):
    boundary = "----codexipsboundary"
    image_bytes = Path(image_path).read_bytes()
    body = []
    body.append(f"--{boundary}\r\n".encode("ascii"))
    body.append(b'Content-Disposition: form-data; name="file"; filename="ips.png"\r\n')
    body.append(b"Content-Type: image/png\r\n\r\n")
    body.append(image_bytes)
    body.append(f"\r\n--{boundary}--\r\n".encode("ascii"))
    request = urllib.request.Request(
        f"{url}?lang={lang}",
        data=b"".join(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def maybe_auto_latinize(payload, validation, disabled):
    if disabled or validation.get("s", {}).get("code") == 0:
        return payload, validation, False
    errors = " ".join(validation.get("e", []))
    if "Tag N" not in errors and "Tag S" not in errors and "Tag P" not in errors:
        return payload, validation, False
    converted = dict(payload)
    for key in ("N", "S", "P"):
        if key in converted:
            converted[key] = transliterate_text(converted[key])
    text = build_text(converted)
    retried = post_text("https://nbs.rs/QRcode/api/qr/v1/validate", text, "sr_RS")
    if retried.get("s", {}).get("code") == 0:
        return converted, retried, True
    return payload, validation, False


def main():
    args = parse_args()
    payload = normalize_payload(load_payload(args))
    text = build_text(payload)
    try:
        validation = post_text("https://nbs.rs/QRcode/api/qr/v1/validate", text, args.lang)
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"NBS validate HTTP error: {exc.code}") from exc
    payload, validation, latinized = maybe_auto_latinize(payload, validation, args.no_auto_latinize)
    text = build_text(payload)
    if validation.get("s", {}).get("code") != 0:
        print(json.dumps(validation, ensure_ascii=False, indent=2))
        raise SystemExit("NBS text validation failed.")

    png = post_json_image(f"https://nbs.rs/QRcode/api/qr/v1/gen/{args.size}", payload, args.lang)

    prefix = Path(args.output_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    txt_path = prefix.with_suffix(".txt")
    png_path = prefix.with_suffix(".png")
    txt_path.write_text(text, encoding="utf-8")
    png_path.write_bytes(png)

    upload_result = None
    if not args.skip_upload_validate:
        upload_result = upload_validate("https://nbs.rs/QRcode/api/qr/v1/upload", png_path, args.lang)
        if upload_result.get("s", {}).get("code") != 0:
            print(json.dumps(upload_result, ensure_ascii=False, indent=2))
            raise SystemExit("Generated PNG failed NBS upload validation.")

    summary = {
        "text_path": str(txt_path),
        "png_path": str(png_path),
        "validator_code": validation.get("s", {}).get("code"),
        "upload_validator_code": None if upload_result is None else upload_result.get("s", {}).get("code"),
        "auto_latinized_text_fields": latinized,
        "payload": payload,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
