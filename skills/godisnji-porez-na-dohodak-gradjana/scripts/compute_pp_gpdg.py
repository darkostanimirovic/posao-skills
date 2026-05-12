#!/usr/bin/env python3
import argparse
import json
from decimal import Decimal
from pathlib import Path


def to_decimal(value):
    if value is None:
        return Decimal("0")
    if isinstance(value, (int, float)):
        return Decimal(str(value))
    return Decimal(str(value).replace(",", "."))


def trunc_dinar(value):
    return int(to_decimal(value))


def load_input(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def income_after_tax(item):
    if "after_tax_amount" in item:
        return trunc_dinar(item["after_tax_amount"])
    taxable = trunc_dinar(item.get("taxable_amount", 0))
    tax_and_contrib = trunc_dinar(item.get("tax_and_contrib", 0))
    return taxable - tax_and_contrib


def compute(data):
    thresholds = data["thresholds"]
    incomes = data.get("incomes", [])
    age_on_dec_31 = int(data.get("age_on_dec_31", 999))
    is_under_40 = age_on_dec_31 < 40

    items = []
    total_after_tax = 0
    eligible_under_40_sum = 0
    for raw in incomes:
        after_tax = income_after_tax(raw)
        eligible = bool(raw.get("eligible_for_under_40", False))
        item = {
            "name": raw.get("name", "income"),
            "after_tax_amount": after_tax,
            "eligible_for_under_40": eligible,
        }
        items.append(item)
        total_after_tax += after_tax
        if eligible:
            eligible_under_40_sum += after_tax

    refund_of_contributions = trunc_dinar(data.get("refund_of_contributions", 0))
    annual_nontaxable_amount = trunc_dinar(thresholds["annual_nontaxable_amount"])
    six_x_average_annual_salary = trunc_dinar(thresholds["six_x_average_annual_salary"])
    taxpayer_allowance = trunc_dinar(thresholds["taxpayer_allowance"])
    dependent_allowance = trunc_dinar(thresholds["dependent_allowance"])
    under_40_additional_deduction_limit = trunc_dinar(thresholds.get("under_40_additional_deduction", 0))
    dependents_count = int(data.get("dependents_count", 0))
    tax_credit = trunc_dinar(data.get("tax_credit", 0))

    under_40_deduction = 0
    if is_under_40:
        under_40_deduction = min(eligible_under_40_sum, under_40_additional_deduction_limit)

    total_after_under_40 = total_after_tax + refund_of_contributions - under_40_deduction
    taxable_income_before_allowances = max(0, total_after_under_40 - annual_nontaxable_amount)

    nominal_personal_allowance = taxpayer_allowance + dependents_count * dependent_allowance
    personal_allowance_cap = taxable_income_before_allowances // 2
    personal_allowance = min(nominal_personal_allowance, personal_allowance_cap)

    taxable_base = max(0, taxable_income_before_allowances - personal_allowance)
    lower_base = min(taxable_base, six_x_average_annual_salary)
    upper_base = max(0, taxable_base - lower_base)

    tax_10 = trunc_dinar(Decimal(lower_base) * Decimal("0.10"))
    tax_15 = trunc_dinar(Decimal(upper_base) * Decimal("0.15"))
    annual_tax = tax_10 + tax_15
    max_credit = annual_tax // 2
    applied_tax_credit = min(tax_credit, max_credit)
    final_tax = annual_tax - applied_tax_credit

    return {
        "age_on_dec_31": age_on_dec_31,
        "is_under_40": is_under_40,
        "income_items": items,
        "total_after_tax": total_after_tax,
        "refund_of_contributions": refund_of_contributions,
        "eligible_under_40_sum": eligible_under_40_sum,
        "under_40_deduction": under_40_deduction,
        "total_after_under_40": total_after_under_40,
        "annual_nontaxable_amount": annual_nontaxable_amount,
        "taxable_income_before_allowances": taxable_income_before_allowances,
        "taxpayer_allowance": taxpayer_allowance,
        "dependent_allowance": dependent_allowance,
        "dependents_count": dependents_count,
        "nominal_personal_allowance": nominal_personal_allowance,
        "personal_allowance_cap": personal_allowance_cap,
        "personal_allowance_applied": personal_allowance,
        "taxable_base": taxable_base,
        "six_x_average_annual_salary": six_x_average_annual_salary,
        "lower_base_10_percent": lower_base,
        "upper_base_15_percent": upper_base,
        "tax_10_percent": tax_10,
        "tax_15_percent": tax_15,
        "annual_tax_before_credit": annual_tax,
        "tax_credit_requested": tax_credit,
        "tax_credit_applied": applied_tax_credit,
        "final_annual_tax": final_tax,
    }


def print_summary(result):
    print(f"Age on 31.12: {result['age_on_dec_31']}")
    print(f"Under 40 rule applies: {'yes' if result['is_under_40'] else 'no'}")
    print(f"Total after tax and contributions: {result['total_after_tax']}")
    print(f"Refund of contributions: {result['refund_of_contributions']}")
    print(f"Under-40 deduction applied: {result['under_40_deduction']}")
    print(f"Taxable income before allowances: {result['taxable_income_before_allowances']}")
    print(f"Personal allowance applied: {result['personal_allowance_applied']}")
    print(f"Taxable base: {result['taxable_base']}")
    print(f"Tax at 10%: {result['tax_10_percent']}")
    print(f"Tax at 15%: {result['tax_15_percent']}")
    print(f"Tax credit applied: {result['tax_credit_applied']}")
    print(f"Final annual tax: {result['final_annual_tax']}")
    print()
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Compute Serbian PP GPDG annual tax from resolved parameters.")
    parser.add_argument("--input", required=True, help="Path to JSON input file.")
    args = parser.parse_args()
    result = compute(load_input(args.input))
    print_summary(result)


if __name__ == "__main__":
    main()
