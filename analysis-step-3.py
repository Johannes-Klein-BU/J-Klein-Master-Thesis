# Redefining the necessary inputs
demand = {
    "1-zone": 745,
    "2-zone": {"North": 261.2, "South": 483.8},
    "4-zone": {"North East": 179.2, "North West": 82.0, "South East": 275.8, "South West": 208.0}
}

supply = {
    "1-zone": 797.5,
    "2-zone": {"North": 429.5, "South": 368.0},
    "4-zone": {"North East": 337.3, "North West": 92.2, "South East": 203.1, "South West": 164.9}
}

redispatch_costs = {
    "1-zone": 3567.8,
    "2-zone": {"North": 1082.1, "South": 2339.7},
    "4-zone": {"North East": 453.5, "North West": 759.4, "South East": 1159.6, "South West": 1076.9}
}

generation_costs = {
    "1-zone": 33507,
    "2-zone": {"North": 18152.6, "South": 15550.3},
    "4-zone": {"North East": 14260.9, "North West": 3899.5, "South East": 8585.4, "South West": 6971.6}
}

base_dsr_weight = 0.4

# Adjusted function to calculate prices based on DSR weight and other inputs
def calculate_prices_with_dsr_weight(dsr_weight, adjusted_demand=None, adjusted_supply=None, adjusted_redispatch=None, adjusted_generation=None):
    if adjusted_demand is None:
        adjusted_demand = demand
    if adjusted_supply is None:
        adjusted_supply = supply
    if adjusted_redispatch is None:
        adjusted_redispatch = redispatch_costs
    if adjusted_generation is None:
        adjusted_generation = generation_costs

    def calculate_price_sophisticated(demand, supply, redispatch_costs, generation_costs):
        # Demand/Supply Ratio
        dsr = demand / supply
        
        # Normalize redispatch and generation costs (handling single value or dictionary)
        if isinstance(redispatch_costs, dict):
            normalized_rc = redispatch_costs / np.mean(list(redispatch_costs.values()))  # Normalize across zones
            normalized_gc = generation_costs / np.mean(list(generation_costs.values()))  # Normalize across zones
        else:
            normalized_rc = 1  # No need to normalize single value
            normalized_gc = 1  # No need to normalize single value
        
        # Weights
        weight_rc = 0.3
        weight_gc = 1 - dsr_weight - weight_rc  # Ensure total weight is 1
        
        # Calculate the final price using weighted sum
        price = (dsr_weight * dsr + weight_rc * normalized_rc + weight_gc * normalized_gc) * 100  # Scaling factor
        
        return price

    # Calculate prices using the sophisticated model with the given DSR weight
    prices_sophisticated = {
        "1-zone": calculate_price_sophisticated(adjusted_demand["1-zone"], adjusted_supply["1-zone"], adjusted_redispatch["1-zone"], adjusted_generation["1-zone"]),
        "2-zone": {
            "North": calculate_price_sophisticated(adjusted_demand["2-zone"]["North"], adjusted_supply["2-zone"]["North"], adjusted_redispatch["2-zone"]["North"], adjusted_generation["2-zone"]["North"]),
            "South": calculate_price_sophisticated(adjusted_demand["2-zone"]["South"], adjusted_supply["2-zone"]["South"], adjusted_redispatch["2-zone"]["South"], adjusted_generation["2-zone"]["South"])
        },
        "4-zone": {
            "North East": calculate_price_sophisticated(adjusted_demand["4-zone"]["North East"], adjusted_supply["4-zone"]["North East"], adjusted_redispatch["4-zone"]["North East"], adjusted_generation["4-zone"]["North East"]),
            "North West": calculate_price_sophisticated(adjusted_demand["4-zone"]["North West"], adjusted_supply["4-zone"]["North West"], adjusted_redispatch["4-zone"]["North West"], adjusted_generation["4-zone"]["North West"]),
            "South East": calculate_price_sophisticated(adjusted_demand["4-zone"]["South East"], adjusted_supply["4-zone"]["South East"], adjusted_redispatch["4-zone"]["South East"], adjusted_generation["4-zone"]["South East"]),
            "South West": calculate_price_sophisticated(adjusted_demand["4-zone"]["South West"], adjusted_supply["4-zone"]["South West"], adjusted_redispatch["4-zone"]["South West"], adjusted_generation["4-zone"]["South West"])
        }
    }
    
    return prices_sophisticated

# Function to adjust a nested dictionary by a certain percentage
def adjust_nested_dict(data, adjustment):
    return {k: (v * (1.1 if adjustment == "increase" else 0.9)) if isinstance(v, (int, float)) else adjust_nested_dict(v, adjustment) for k, v in data.items()}

# Function to adjust a parameter by a certain percentage and recalculate prices
def adjust_and_recalculate(factor, adjustment):
    if factor == "demand":
        adjusted_demand = adjust_nested_dict(demand, adjustment)
        adjusted_supply = supply
        adjusted_redispatch = redispatch_costs
        adjusted_generation = generation_costs
        dsr_weight = base_dsr_weight
    elif factor == "supply":
        adjusted_demand = demand
        adjusted_supply = adjust_nested_dict(supply, adjustment)
        adjusted_redispatch = redispatch_costs
        adjusted_generation = generation_costs
        dsr_weight = base_dsr_weight
    elif factor == "redispatch":
        adjusted_demand = demand
        adjusted_supply = supply
        adjusted_redispatch = adjust_nested_dict(redispatch_costs, adjustment)
        adjusted_generation = generation_costs
        dsr_weight = base_dsr_weight
    elif factor == "generation":
        adjusted_demand = demand
        adjusted_supply = supply
        adjusted_redispatch = redispatch_costs
        adjusted_generation = adjust_nested_dict(generation_costs, adjustment)
        dsr_weight = base_dsr_weight
    elif factor == "dsr_weight":
        adjusted_demand = demand
        adjusted_supply = supply
        adjusted_redispatch = redispatch_costs
        adjusted_generation = generation_costs
        dsr_weight = base_dsr_weight * (1.1 if adjustment == "increase" else 0.9)
    
    return calculate_prices_with_dsr_weight(dsr_weight, adjusted_demand, adjusted_supply, adjusted_redispatch, adjusted_generation)

# Collect results for each variation
sensitivity_results = {}

for factor in ["demand", "supply", "redispatch", "generation", "dsr_weight"]:
    sensitivity_results[f"{factor}_increase"] = adjust_and_recalculate(factor, "increase")
    sensitivity_results[f"{factor}_decrease"] = adjust_and_recalculate(factor, "decrease")

sensitivity_results
