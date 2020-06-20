import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument("--type", type=str, help="type of payment")
parser.add_argument("--payment", type=int, help="monthly payment")
parser.add_argument("--principal", type=float, help="credit principal")
parser.add_argument("--periods", type=int, help="number of months needed to repay the credit")
parser.add_argument("--interest", type=float, help="percentage of interest")
args = parser.parse_args()


def plural(years, months):
    if years == 0:
        if months == 0:
            return "You almost repay this credit!"
        elif months == 1:
            return "You need 1 month to repay this credit!"
        else:
            return f"You need {months} months to repay this credit!"
    elif years == 1:
        if months == 0:
            return "You need 1 year to repay this credit!"
        elif months == 1:
            return "You need 1 year and 1 month to repay this credit!"
        else:
            return f"You need 1 year and {months} months to repay this credit!"
    else:
        if months == 0:
            return f"You need {years} years to repay this credit!"
        elif months == 1:
            return f"You need {years} years and 1 month to repay this credit!"
        else:
            return f"You need {years} years and {months} months to repay this credit!"


def CalculateCountMonths(principal, payment, interest):
    nominal_interest = (interest / 100) / 12
    count_periods = math.ceil(
        math.log(payment / (payment - nominal_interest * principal), 1 + nominal_interest))
    years = math.floor(count_periods / 12)
    months = count_periods % 12
    print(plural(years, months))
    print(f"\nOverpayment = {(payment * count_periods) - principal}")


def CalculateAnnuityMonthlyPayment(principal, periods, interest):
    nominal_interest = (interest / 100) / 12
    annuity_payment = math.ceil(principal * (nominal_interest * (1 + nominal_interest) ** periods) / (
            ((1 + nominal_interest) ** periods) - 1))
    print(f"Your annuity payment = {annuity_payment}!")


def CalculateCreditPrincipal(payment, periods, interest):
    nominal_interest = (interest / 100) / 12
    credit_principal = payment / ((nominal_interest * ((1 + nominal_interest) ** periods)) / (
            ((1 + nominal_interest) ** periods) - 1))
    print(f"Your credit principal = {credit_principal}!")


def AnnuityPayment(principal, periods, interest):
    nominal_interest = (interest / 100) / 12
    annuity_payment = math.ceil(principal * (nominal_interest * (1 + nominal_interest) ** periods) / (
            ((1 + nominal_interest) ** periods) - 1))
    print(f"\nYour annuity payment = {annuity_payment}!")
    print(f"\nOverpayment = {annuity_payment - principal}")


def DiffPayment(principal, periods, interest):
    nominal_interest = (interest / 100) / 12
    overpayment = 0
    month = 1
    while month <= periods:
        diff_payment = math.ceil(principal / periods + nominal_interest * (
                principal - (principal * (month - 1)) / periods))
        overpayment += diff_payment
        print(f"Month {month}: paid out {diff_payment}\n")
        month += 1
    overpayment -= principal
    print(f"\nOverpayment = {overpayment}")


def Error():
    print("Incorrect parameters")
    exit()


if args.type == "annuity":
    if not args.interest:
        Error()
    elif not args.periods:
        CalculateCountMonths(args.principal, args.payment, args.interest)
    elif not args.payment:
        CalculateAnnuityMonthlyPayment(args.principal, args.periods, args.interest)
    elif not args.principal:
        CalculateCreditPrincipal(args.payment, args.periods, args.interest)
    else:
        AnnuityPayment(args.principal, args.periods, args.interest)
elif args.type == "diff":
    if args.payment or not args.interest:
        Error()
    else:
        DiffPayment(args.principal, args.periods, args.interest)
else:
    Error()
