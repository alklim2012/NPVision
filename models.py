import numpy as np
import pandas as pd

def grade_tonnage_curve(cutoff, curve=None):
    if curve is not None:
        nearest = curve.iloc[(curve['Cutoff'] - cutoff).abs().argsort()[:1]]
        return float(nearest['Tonnage']), float(nearest['Grade'])
    else:
        a = 500
        b = 0.7
        tonnage = a * (cutoff ** -b)
        grade = max(1.5 - cutoff * 0.5, 0.2)
        return tonnage, grade

def estimate_capex(prod):
    return 1000 + 150 * prod

def estimate_schedule(capex, years):
    return [capex / 2 if t < 2 else 0 for t in range(int(np.ceil(years)))]

def calculate_npv(tonnage, grade, price, recovery, opex, prod, discount):
    metal = tonnage * grade / 100
    revenue = metal * recovery / 100 * price
    years = tonnage / prod
    cash = (revenue - opex * tonnage) / years
    capex = estimate_capex(prod)
    schedule = estimate_schedule(capex, years)
    flows = [cash] * int(np.ceil(years))
    npv = sum([(flows[t] - schedule[t]) / ((1 + discount / 100) ** (t + 1)) for t in range(len(flows))])
    return npv, years, capex

def generate_scenarios(params):
    cutoffs = np.round(np.arange(params["cutoff_range"][0], params["cutoff_range"][1] + 0.01, 0.1), 2)
    prods = np.round(np.arange(params["prod_range"][0], params["prod_range"][1] + 0.01, 0.5), 2)
    records = []
    for cutoff in cutoffs:
        for prod in prods:
            npvs, years, capexes = [], [], []
            for _ in range(50):
                price = np.random.normal(params["price"], params["price_std"])
                rec = np.random.normal(params["recovery"], params["recovery_std"])
                tonnage, grade = grade_tonnage_curve(cutoff, params["user_curve"])
                npv, life, capex = calculate_npv(tonnage, grade, price, rec, params["opex"], prod, params["discount_rate"])
                npvs.append(npv)
                years.append(life)
                capexes.append(capex)
            records.append({
                "Cutoff": cutoff,
                "Production": prod,
                "Avg NPV": np.mean(npvs),
                "Avg Life": np.mean(years),
                "CAPEX": np.mean(capexes)
            })
    return pd.DataFrame(records)
