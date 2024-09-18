# Load necessary libraries 
# install.packages("dplyr")
# install.packages("broom")

# Import required libraries
library(dplyr)       # For data manipulation
library(broom)       # For tidy output of regression results

# 1. Input the Data Manually
# Here I manually input the yearly data for electricity prices (EUR/MWh) 
# and investments in renewable energy sources (RES) (million EUR).

data <- data.frame(
  Electricity_Price = c(50.79, 37.99, 65.76, 38.85, 44.49, 51.12, 42.60, 37.78, 
                        32.76, 31.83, 28.98, 34.19, 44.47, 37.67, 30.47, 95.18),
  Investment_in_RES = c(13950, 13620, 17720, 23600, 27890, 26120, 22470, 16480, 
                        16400, 13930, 15320, 15940, 13830, 10630, 11750, 36600)
)

# 2. Perform Linear Regression
# Run a linear regression with electricity price as the independent variable (predictor)
# and investments in RES as the dependent variable (outcome).

model <- lm(Investment_in_RES ~ Electricity_Price, data = data)

# 3. Summary of the Regression Model
# This provides an overview of the regression, including R-squared, coefficients, 
# p-values, and other statistical metrics.

summary(model)

# 4. Extract Key Results
# Extract and print important results such as R-squared, Adjusted R-squared, 
# the regression coefficients, and p-values.

r_squared <- summary(model)$r.squared
adj_r_squared <- summary(model)$adj.r.squared
coefficients <- summary(model)$coefficients

# Print Key Results
cat("R-Squared:", r_squared, "\n")
cat("Adjusted R-Squared:", adj_r_squared, "\n")
cat("Intercept (baseline investment):", coefficients[1, 1], "\n")
cat("Coefficient for Electricity Price:", coefficients[2, 1], "\n")
cat("P-Value for Electricity Price:", coefficients[2, 4], "\n")
