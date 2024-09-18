# Full R Code for Regression Analysis of Electricity Prices and RES Investments
# This script performs a linear regression analysis to examine the relationship 
# between electricity prices and investments in renewable energy sources (RES).

# Load necessary libraries (uncomment if not installed)
# install.packages("dplyr")
# install.packages("broom")
# install.packages("readr")

# Import required libraries
library(dplyr)       # For data manipulation
library(broom)       # For tidy output of regression results
library(readr)       # For reading data from CSV

# 1. Load Data from CSV File
# The CSV should contain two columns: 'Electricity_Price' and 'Investment_in_RES'.
# Make sure to replace 'path_to_your_file.csv' with the actual file path to your data.

data <- read_csv("path_to_your_file.csv")

# 2. Perform Linear Regression
# We will run a linear regression with electricity price as the independent variable (predictor)
# and investments in RES as the dependent variable (outcome).

model <- lm(Investment_in_RES ~ Electricity_Price, data = data)

# 3. Summary of the Regression Model
# This provides an overview of the regression, including R-squared, coefficients, 
# p-values, and other statistical metrics.

summary(model)

# 4. Extract Key Results
# We'll extract and print important results such as R-squared, Adjusted R-squared, 
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
