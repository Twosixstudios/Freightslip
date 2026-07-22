from dataclasses import dataclass


@dataclass
class ProfitabilityResult:
    loaded_miles: float
    deadhead_miles: float
    total_miles: float
    gross_pay: float
    true_rpm: float
    fuel_cost: float
    maintenance_cost: float
    total_expenses: float
    net_profit: float
    net_rpm: float
    status: str
    status_emoji: str


def calculate_profitability(
    gross_pay: float,
    loaded_miles: float,
    deadhead_miles: float = 50.0,
    diesel_price: float = 3.85,
    truck_mpg: float = 6.5,
    maintenance_cost_per_mile: float = 0.15,
    tolls_misc: float = 0.0,
) -> ProfitabilityResult:
    """Calculates true trip metrics, net profit, and real rate-per-mile (RPM).

    Decoupled logic — ready to import into Fleet Scout or FastAPI backends.
    """
    safe_loaded = float(loaded_miles or 0.0)
    safe_pay = float(gross_pay or 0.0)
    total_miles = safe_loaded + float(deadhead_miles or 0.0)

    if total_miles <= 0:
        return ProfitabilityResult(
            loaded_miles=0,
            deadhead_miles=0,
            total_miles=0,
            gross_pay=safe_pay,
            true_rpm=0.0,
            fuel_cost=0.0,
            maintenance_cost=0.0,
            total_expenses=0.0,
            net_profit=0.0,
            net_rpm=0.0,
            status="NO DATA",
            status_emoji="⚪",
        )

    # Core Financial Calculations
    true_rpm = safe_pay / total_miles if total_miles > 0 else 0.0
    fuel_cost = (
        (total_miles / truck_mpg) * diesel_price if truck_mpg > 0 else 0.0
    )
    maintenance_cost = total_miles * maintenance_cost_per_mile
    total_expenses = fuel_cost + maintenance_cost + float(tolls_misc or 0.0)
    net_profit = safe_pay - total_expenses
    net_rpm = net_profit / total_miles

    # Decision Engine Thresholds
    if net_rpm >= 1.20:
        status = "HIGH PROFITABILITY — RECOMMENDED"
        status_emoji = "�"
    elif net_rpm >= 0.75:
        status = "MARGINAL PROFIT — PROCEED WITH CAUTION"
        status_emoji = "�"
    else:
        status = "LOW PROFIT / LOSS — AVOID OR RE-NEGOTIATE"
        status_emoji = "�"

    return ProfitabilityResult(
        loaded_miles=safe_loaded,
        deadhead_miles=deadhead_miles,
        total_miles=total_miles,
        gross_pay=safe_pay,
        true_rpm=true_rpm,
        fuel_cost=fuel_cost,
        maintenance_cost=maintenance_cost,
        total_expenses=total_expenses,
        net_profit=net_profit,
        net_rpm=net_rpm,
        status=status,
        status_emoji=status_emoji,
    )