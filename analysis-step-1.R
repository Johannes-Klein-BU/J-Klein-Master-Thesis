# install.packages("dplyr")
# install.packages("readr")
# install.packages("ggplot2")
# install.packages("broom")    # For tidy regression output

library(dplyr)     # For data manipulation
library(readr)     # For reading data files
library(ggplot2)   # For data visualization (optional)
library(broom)     # For tidying regression results

# Load the electricity prices data
electricity_prices <- read_csv("path_to_electricity_prices.csv")

# Load the RES investment data
res_investments <- read_csv("path_to_res_investments.csv", skip = 4)  # Adjusting to handle extra header rows if necessary

# Convert Date column in electricity prices to year and aggregate by year
electricity_prices <- electricity_prices %>%
  mutate(Year = lubridate::year(Date)) %>%
  group_by(`ISO3 Code`, Year) %>%
  summarize(Average_Price = mean(`Price (EUR/MWhe)`, na.rm = TRUE))

# Reshape the RES investment data for merging
res_investments_long <- res_investments %>%
  select(`Country Code`, `2015`, `2016`, `2017`, `2018`, `2019`, `2020`) %>%
  pivot_longer(cols = starts_with("20"), names_to = "Year", values_to = "Investment") %>%
  mutate(Year = as.numeric(Year))

# Merge the datasets by Country Code and Year
merged_data <- left_join(electricity_prices, res_investments_long, by = c("ISO3 Code" = "Country Code", "Year" = "Year"))

# Filter out rows with missing data
merged_data <- merged_data %>% filter(!is.na(Average_Price) & !is.na(Investment))

# Function to perform regression and correlation for each country
analyze_country <- function(country_code) {
  country_data <- merged_data %>% filter(`ISO3 Code` == country_code)
  if (nrow(country_data) < 2) return(NULL)
  
  # Perform linear regression
  model <- lm(Investment ~ Average_Price, data = country_data)
  summary <- summary(model)
  tidy_model <- tidy(model)
  
  # Perform correlation test
  correlation <- cor.test(country_data$Average_Price, country_data$Investment)
  
  # Compile results
  results <- data.frame(
    Country = country_code,
    R_Squared = summary$r.squared,
    P_Value_Regression = tidy_model$p.value[2],
    Correlation = correlation$estimate,
    P_Value_Correlation = correlation$p.value
  )
  return(results)
}

# Apply analysis to all countries
results <- lapply(unique(merged_data$`ISO3 Code`), analyze_country)
results_df <- bind_rows(results)

# Filter significant results where p-value < 0.05 for both regression and correlation
significant_results <- results_df %>% filter(P_Value_Regression < 0.05 & P_Value_Correlation < 0.05)

# Output significant results
write.csv(significant_results, "significant_countries_analysis.csv", row.names = FALSE)

# Display significant results
print(significant_results)
