import numpy as np

# Define input data
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

# Weights
dsr_weight = 0.4
rc_weight = 0.3
gc_weight = 0.3

# Sophisticated price calculation function with the chosen DSR weight
def calculate_price_sophisticated(demand, supply, redispatch_costs, generation_costs):
    # Demand/Supply Ratio
    dsr = demand / supply
    
    # Normalize redispatch and generation costs (handling single value or dictionary)
    if isinstance(redispatch_costs, dict):
        normalized_rc = redispatch_costs / np.mean(list(redispatch_costs.values()))  # Normalize across zones
        normalized_gc = generation_costs / np.mean(list(generation_costs.values()))  # Normalize across zones
    else:
        normalized_rc = 1  # No need to normalize single value (acts as its own mean)
        normalized_gc = 1  # No need to normalize single value (acts as its own mean)
    
    # Calculate the final price using weighted sum
    price = (dsr_weight * dsr + rc_weight * normalized_rc + gc_weight * normalized_gc) * 100  # Scaling factor
    
    return price

# Calculate prices using the sophisticated model with DSR weight of 0.4
prices_sophisticated = {
    "1-zone": calculate_price_sophisticated(demand["1-zone"], supply["1-zone"], redispatch_costs["1-zone"], generation_costs["1-zone"]),
    "2-zone": {
        "North": calculate_price_sophisticated(demand["2-zone"]["North"], supply["2-zone"]["North"], redispatch_costs["2-zone"]["North"], generation_costs["2-zone"]["North"]),
        "South": calculate_price_sophisticated(demand["2-zone"]["South"], supply["2-zone"]["South"], redispatch_costs["2-zone"]["South"], generation_costs["2-zone"]["South"])
    },
    "4-zone": {
        "North East": calculate_price_sophisticated(demand["4-zone"]["North East"], supply["4-zone"]["North East"], redispatch_costs["4-zone"]["North East"], generation_costs["4-zone"]["North East"]),
        "North West": calculate_price_sophisticated(demand["4-zone"]["North West"], supply["4-zone"]["North West"], redispatch_costs["4-zone"]["North West"], generation_costs["4-zone"]["North West"]),
        "South East": calculate_price_sophisticated(demand["4-zone"]["South East"], supply["4-zone"]["South East"], redispatch_costs["4-zone"]["South East"], generation_costs["4-zone"]["South East"]),
        "South West": calculate_price_sophisticated(demand["4-zone"]["South West"], supply["4-zone"]["South West"], redispatch_costs["4-zone"]["South West"], generation_costs["4-zone"]["South West"])
    }
}

# Print the results
print("Sophisticated Simulated Electricity Prices for 2030 with DSR Weight 0.4:")
print(f"1-zone: {prices_sophisticated['1-zone']:.2f} EUR/MWh")
print(f"2-zone North: {prices_sophisticated['2-zone']['North']:.2f} EUR/MWh")
print(f"2-zone South: {prices_sophisticated['2-zone']['South']:.2f} EUR/MWh")
print(f"4-zone North East: {prices_sophisticated['4-zone']['North East']:.2f} EUR/MWh")
print(f"4-zone North West: {prices_sophisticated['4-zone']['North West']:.2f} EUR/MWh")
print(f"4-zone South East: {prices_sophisticated['4-zone']['South East']:.2f} EUR/MWh")
print(f"4-zone South West: {prices_sophisticated['4-zone']['South West']:.2f} EUR/MWh")
