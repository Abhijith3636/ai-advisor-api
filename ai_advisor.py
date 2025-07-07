import datetime
from ml_investment_predictor import predict_instrument



instrument_metadata = {
    "PPF": {
        "risk": "Low",
        "lock_in": "15 years",
        "liquidity": "Low",
        "tax_benefits": "Yes (Sec 80C)",
        "expected_return": "7% p.a."
    },
    "Debt Mutual Fund": {
        "risk": "Medium",
        "lock_in": "No lock-in",
        "liquidity": "High",
        "tax_benefits": "Partial (LTCG after 3 years)",
        "expected_return": "6–8% p.a."
    },
    "Equity Mutual Fund": {
        "risk": "High",
        "lock_in": "No lock-in",
        "liquidity": "High",
        "tax_benefits": "No",
        "expected_return": "10–12% p.a."
    },
    "ELSS Mutual Fund": {
        "risk": "High",
        "lock_in": "3 years",
        "liquidity": "Medium",
        "tax_benefits": "Yes (Sec 80C)",
        "expected_return": "10–12% p.a."
    },
    "Bank FD": {
        "risk": "Low",
        "lock_in": "1–5 years",
        "liquidity": "Medium",
        "tax_benefits": "Interest taxable",
        "expected_return": "6–7% p.a."
    },
    "Post Office RD": {
        "risk": "Low",
        "lock_in": "5 years",
        "liquidity": "Medium",
        "tax_benefits": "No",
        "expected_return": "6.5% p.a."
    },
    "Sovereign Gold Bonds": {
        "risk": "Medium",
        "lock_in": "5–8 years",
        "liquidity": "Low",
        "tax_benefits": "Interest taxable",
        "expected_return": "6.5–7.5% p.a."
    },
    "ULIP": {
        "risk": "Medium",
        "lock_in": "5 years",
        "liquidity": "Low",
        "tax_benefits": "Yes (Sec 80C)",
        "expected_return": "6–10% p.a."
    },
    "NPS": {
        "risk": "Medium",
        "lock_in": "Until retirement",
        "liquidity": "Low",
        "tax_benefits": "Yes (Sec 80C + 80CCD)",
        "expected_return": "8–10% p.a."
    },
    "Real Estate Investment": {
        "risk": "Medium",
        "lock_in": "5–10+ years",
        "liquidity": "Low",
        "tax_benefits": "Property capital gains",
        "expected_return": "Varies"
    },
    "REITs": {
        "risk": "Medium",
        "lock_in": "3+ years",
        "liquidity": "Medium",
        "tax_benefits": "No",
        "expected_return": "7–9% p.a."
    },
    "Gold ETF": {
        "risk": "Medium",
        "lock_in": "No lock-in",
        "liquidity": "High",
        "tax_benefits": "LTCG tax on gains",
        "expected_return": "6–8% p.a."
    },
    "Index Fund": {
        "risk": "High",
        "lock_in": "No lock-in",
        "liquidity": "High",
        "tax_benefits": "LTCG applicable",
        "expected_return": "10–12% p.a."
    },
    "Stocks": {
        "risk": "Very High",
        "lock_in": "No lock-in",
        "liquidity": "High",
        "tax_benefits": "LTCG/STCG",
        "expected_return": "12–18% p.a."
    },
    "Crypto": {
        "risk": "Very High",
        "lock_in": "No lock-in",
        "liquidity": "High",
        "tax_benefits": "30% flat tax in India",
        "expected_return": "Highly volatile"
    },
    "Fixed Maturity Plan": {
        "risk": "Low to Medium",
        "lock_in": "3–5 years",
        "liquidity": "Low",
        "tax_benefits": "Post 3 years – LTCG",
        "expected_return": "6–7.5% p.a."
    }
}



# ----------------- ADVISOR ENGINE ------------------
def generate_advice(user, goals, investments, insurance):
    advice = []

    salary = user["salary"]
    expenses = user.get("expenses", 0)
    monthly_savings = salary - expenses
    total_required_saving = 0
    affordable_goals = 0

    if not investments and not insurance:
        advice.append({
            "category": "System Alert",
            "priority": "High",
            "message": "🔰 You haven't started investing or bought any insurance. Begin by saving at least 10–20% of your income. Then explore simple low-risk investments and basic insurance to protect your finances."
            })

    if monthly_savings <= 0:
        savings_rate = 0
        priority = "High"
        msg = "Your expenses exceed your income. Reduce spending or increase earnings to start saving."
    else:
        savings_rate = (monthly_savings / salary) * 100
        if savings_rate < 10:
            priority = "High"
            msg = f"Your savings rate is just {savings_rate:.1f}%. Try to reduce expenses or increase income to save at least 20% of your salary."
        elif savings_rate < 20:
            priority = "Medium"
            msg = f"Your savings rate is {savings_rate:.1f}%. Consider trimming discretionary expenses to reach a healthier target of 20%."
        elif savings_rate < 35:
            priority = "Low"
            msg = f"Good! Your savings rate is {savings_rate:.1f}%. Keep maintaining or improving this trend."
        else:
            priority = "Low"
            msg = f"Excellent! Your savings rate is {savings_rate:.1f}%. You're building wealth at a great pace."

    advice.append({"category": "Cash Flow", "priority": priority, "message": msg})

    if salary < 10000:
        advice.insert(0, {
            "category": "System Alert",
            "priority": "High",
            "message": "⚠️ Your current financial situation is unstable. Consider speaking to a financial advisor before investing."
        })
    
    insurance_types = {ins["type"]: ins["coverage"] for ins in insurance}
    age = user["age"]
    annual_salary = salary * 12

    recommended_health_cover = 300000 if age < 30 else 500000 if age <= 45 else 700000
    health_coverage = insurance_types.get("Health Insurance", 0)

    multiplier = 8 if salary < 30000 else 10 if salary <= 70000 else 12
    recommended_term_cover = annual_salary * multiplier
    term_coverage = insurance_types.get("Term Life Insurance", 0)

    # ---------------- Emergency Fund Intelligence ---------------- #
    emergency_multiplier = 3  # base recommendation

    # Increase multiplier if underinsured
    if health_coverage < recommended_health_cover:
        emergency_multiplier += 0.5
    if term_coverage < recommended_term_cover:
        emergency_multiplier += 0.5

    # Increase if self-employed or has dependents
    if user.get("job_type", "").lower() == "self-employed":
        emergency_multiplier += 1
    if user.get("dependents", 0) > 0:
        emergency_multiplier += 0.5

    emergency_target = round(salary * emergency_multiplier)

    if user["savings"] < emergency_target:
        advice.append({
            "category": "Emergency Fund",
            "priority": "High",
            "message": (
                f"Increase your emergency fund to at least ₹{emergency_target:,} "
                f"(based on {emergency_multiplier:.1f}× monthly salary, adjusted for insurance and dependents)."
            )
        })
    else:
        advice.append({
            "category": "Emergency Fund",
            "priority": "Low",
            "message": (
                f"✅ Your emergency fund of ₹{user['savings']:,} meets the recommended "
                f"{emergency_multiplier:.1f}× salary buffer. Great job!"
            )
        })


    # Investment Diversification
    unique_instruments = set(i["instrument_name"] for i in investments)
    if len(unique_instruments) < 2:
        advice.append({
            "category": "Investment",
            "priority": "Medium",
            "message": "Consider diversifying your investments into more categories."
        })
    else:
        advice.append({
            "category": "Investment",
            "priority": "Low",
            "message": "Your investments are well-diversified."
        })

    # Investment Allocation Analysis
    from collections import defaultdict

    

# Exclude Insurance from general investments
    filtered_investments = [inv for inv in investments if inv["instrument_name"] != "Insurance"]

# Include both investment and insurance amounts
    total_investment = (
        sum(inv["amount"] for inv in filtered_investments) +
        sum(ins.get("amount", 0) for ins in insurance)
    )

    if total_investment == 0:
        advice.append({
            "category": "Investment",
            "priority": "High",
            "message": "⚠️ You have no investments yet. Start investing a portion of your savings to build long-term wealth."
        })
    else:
    

        category_allocation = defaultdict(float)

        # Add investment amounts
        for inv in filtered_investments:
            category_allocation[inv["instrument_name"]] += inv["amount"]

        # ✅ Add insurance as a separate category
        category_allocation["Insurance"] += sum(ins.get("amount", 0) for ins in insurance)
        

        allocation_summary = []
        over_concentrated = False
        for name, amt in category_allocation.items():
            percent = (amt / total_investment) * 100
            allocation_summary.append(f"• {name}: {percent:.1f}%")
            if percent > 70:
                over_concentrated = True

        if over_concentrated:
            advice.append({
                "category": "Investment",
                "priority": "Medium",
                "message": (
                    f"⚠️ Your investments are highly concentrated.\n"
                    f"🔍 Allocation:\n" + "\n".join(allocation_summary) +
                    "\n💡 Consider diversifying further to manage risk."
                )
            })
        else:
            advice.append({
                "category": "Investment",
                "priority": "Low",
                "message": (
                    f"✅ Your investment spread looks balanced.\n"
                    f"🔍 Allocation:\n" + "\n".join(allocation_summary)
                )
            })
        
    # Asset Class Exposure Summary
        asset_classes = {
            "Debt": ["Bank FD", "Debt Mutual Fund"],
            "Equity": ["Equity Mutual Fund", "ELSS Mutual Fund", "Stocks"],
            "Hybrid": ["PPF", "ULIP", "NPS"],
            "Alternative": ["Sovereign Gold Bonds", "Real Estate Investment"]
        }

        class_totals = defaultdict(float)
        for inv in investments:
            for category, names in asset_classes.items():
                if inv["instrument_name"] in names:
                    class_totals[category] += inv["amount"]
                    break

        asset_summary = []
        for cat, amt in class_totals.items():
            percent = (amt / total_investment) * 100
            asset_summary.append(f"• {cat}: {percent:.1f}%")

        dominant_asset = max(class_totals, key=class_totals.get) if class_totals else "None"
        advice.append({
            "category": "Investment",
            "priority": "Medium" if dominant_asset == "Debt" else "Low",
            "message": (
                f"📊 Asset Class Exposure:\n" + "\n".join(asset_summary) +
                f"\n💡 Dominant class: {dominant_asset}. "
                + ("Consider adding equity instruments for long-term growth." if dominant_asset == "Debt" else "Your asset allocation looks reasonable.")
            )
        })


    # Goal Planning (ML + Explanation)
    current_year = datetime.datetime.now().year
    for goal in goals:
        years_left = goal["target_year"] - current_year
        if years_left <= 0:
            advice.append({
                "category": "Goals",
                "priority": "High",
                "message": f"Review goal '{goal['name']}' – the target year has passed."
            })
            continue

        remaining_amount = goal["amount"] - goal.get("saved_amount", 0)
        monthly_saving_needed = remaining_amount / (years_left * 12)
        total_required_saving += monthly_saving_needed

        ml_based_instrument, ml_confidence = predict_instrument({
            "age": user["age"],
            "salary": user["salary"],
            "savings": user["savings"],
            "risk_profile": "High",
            "goal": goal["name"],
            "goal_amount": goal["amount"],
            "years_to_goal": years_left
        })

        metadata = instrument_metadata.get(ml_based_instrument, {})
        expected_return_rate = 0.07
        fv = monthly_saving_needed * (((1 + expected_return_rate / 12) ** (years_left * 12) - 1) / (expected_return_rate / 12)) * (1 + expected_return_rate / 12)

        if monthly_saving_needed > salary:
            realistic_goal = (monthly_savings * years_left * 12) + goal.get("saved_amount", 0)
            msg = (
                f"📌 Goal: {goal['name']}\n"
                f"❗ Required monthly saving (₹{monthly_saving_needed:,.0f}) is more than your entire income (₹{salary:,}).\n"
                f"💡 This goal is not feasible currently. Consider reducing the goal amount or extending the timeline.\n"
                f"🔄 Based on your current savings, you could aim for a goal of ₹{realistic_goal:,.0f} instead."
            )
            priority = "High"
        elif monthly_saving_needed > monthly_savings:
            msg = (
                f"📌 Goal: {goal['name']}\n"
                f"❗ Required savings (₹{monthly_saving_needed:,.0f}/month) exceeds your current monthly savings (₹{monthly_savings:,.0f}).\n"
                f"💡 Consider reducing the goal amount or extending the timeline."
            )
            priority = "High"
        else:
            affordable_goals += 1
            msg = (
                f"📌 Goal: {goal['name']}\n"
                f"🎯 Recommended Instrument: {ml_based_instrument}\n"
                f"🤖 Confidence: {ml_confidence:.1f}%\n"
                f"💰 Monthly Saving Required: ₹{monthly_saving_needed:,.0f} for {years_left} years\n"
                f"📊 Projected Value: ₹{fv:,.0f}\n"
                f"📈 Expected Return Rate: {metadata.get('expected_return', '7% p.a.')}\n"
                f"🔍 {ml_based_instrument} Overview:\n"
                f"• Risk: {metadata.get('risk', 'N/A')}\n"
                f"• Lock-in: {metadata.get('lock_in', 'N/A')}\n"
                f"• Liquidity: {metadata.get('liquidity', 'N/A')}\n"
                f"• Tax Benefits: {metadata.get('tax_benefits', 'N/A')}"
            )
            priority = "Medium"

        advice.append({
            "category": "Goals",
            "priority": priority,
            "message": msg
        })

    if total_required_saving > monthly_savings:
        if affordable_goals == 1:
            suggestion = "You can comfortably handle only 1 of your financial goals at this time."
        elif affordable_goals == 0:
            suggestion = "Your current income does not support any of your financial goals. Start with emergency savings."
        else:
            suggestion = f"You can afford {affordable_goals} goals. Consider prioritizing the most important one."

        advice.insert(1, {
            "category": "Goals",
            "priority": "High",
            "message": (
                f"❗ Your total required savings for all goals is ₹{total_required_saving:,.0f}/month, "
                f"but your actual monthly savings is only ₹{monthly_savings:,.0f}.\n"
                f"💡 Suggestion: {suggestion}"
            )
        })

    # Insurance Check
    insurance_types = {ins["type"]: ins["coverage"] for ins in insurance}
    age = user["age"]
    annual_salary = salary * 12

    recommended_health_cover = 300000 if age < 30 else 500000 if age <= 45 else 700000
    health_coverage = insurance_types.get("Health Insurance", 0)
    if health_coverage <= 0:
        advice.append({
            "category": "Risk",
            "priority": "High",
            "message": "❌ You do not have health insurance. Please consider buying health coverage to protect your finances from medical emergencies."
        })
    elif health_coverage < recommended_health_cover:
        advice.append({
            "category": "Risk",
            "priority": "Medium",
            "message": f"Your health insurance (₹{health_coverage:,}) is below the recommended ₹{recommended_health_cover:,} for your age ({age}). Consider increasing it."
        })

    multiplier = 8 if salary < 30000 else 10 if salary <= 70000 else 12
    recommended_term_cover = annual_salary * multiplier
    term_coverage = insurance_types.get("Term Life Insurance", 0)
    if term_coverage <= 0:
        advice.append({
            "category": "Risk",
            "priority": "High",
            "message": "❌ You lack term life insurance. Consider a plan to protect your family’s income in case of emergencies."
        })
    elif term_coverage < recommended_term_cover:
        advice.append({
            "category": "Risk",
            "priority": "Medium",
            "message": f"Your term insurance (₹{term_coverage:,}) is below the recommended ₹{recommended_term_cover:,} based on your salary ({salary}/month). Consider increasing it."
        })
    
     #----------------- Step 3: Smarter Insurance Advice ----------------- #
    is_retirement_planned = any("retire" in g["name"].lower() for g in goals)
    large_goals = [g for g in goals if g["amount"] >= 2000000]

    if is_retirement_planned and age > 40 and health_coverage < 500000:
        advice.append({
            "category": "Risk",
            "priority": "High",
            "message": "🛡️ Planning for retirement? Ensure your health insurance is ₹500,000 or more to cover rising medical costs."
        })

    if large_goals and term_coverage < recommended_term_cover:
        advice.append({
            "category": "Risk",
            "priority": "High",
            "message": f"📌 You have major financial goals like '{large_goals[0]['name']}'. Consider increasing term life cover beyond ₹{recommended_term_cover:,}."
        })

    return advice



# ----------------- RUN SCRIPT ------------------
if __name__ == "__main__":
    result = {
        "user": user,
        "goals": goals,
        "monthly_savings": user["salary"] - user["expenses"],
        "advice": generate_advice(user, goals, investments, insurance)
    }

    print("\n📊 AI Advisor Summary\n")
    print(f"👤 User: {result['user']['name']}")
    print(f"💰 Monthly Savings: ₹{result['monthly_savings']:,}\n")
    

    for idx, item in enumerate(result["advice"], 1):
        print(f"{idx}. [{item['category']}] ({item['priority']}) - {item['message']}")
