# Integrated Values Surveys Indicators

This repository contains DDF (Data Description Format) formatted data from the European Values Study (EVS) and World Values Survey (WVS), focusing on the Traditional vs. Rational Values (TradAgg) and Survival vs. Self-Expression Values (SurvSAgg) indicators which form the basis of the Inglehart–Welzel Cultural Map.

To get started with DDF and learn how to use the dataset, please read the
[introduction to DDF][1] and [DDFcsv format document][2].

[1]: https://open-numbers.github.io/ddf.html
[2]: https://docs.google.com/document/d/1aynARjsrSgOKsO1dEqboTqANRD1O9u7J_xmxy8m5jW8

## Indicators

This dataset contains two key indicators:

- **TradAgg (Traditional vs. Rational Values)**: Reflects the contrast between societies that emphasize traditional values (deference to authority, religion, national pride) versus those that emphasize secular-rational values.
- **SurvSAgg (Survival vs. Self-Expression Values)**: Reflects the contrast between societies that emphasize economic and physical security versus those that emphasize self-expression, subjective well-being, and quality of life.

## Definition of Indicators

These indicators are derived from factor analysis on several variables in the EVS/WVS longitudinal dataset including:

- A008 Feeling of happiness
- A165 Most people can be trusted
- E018 Future changes: Greater respect for authority
- E025 Political action: signing a petition
- F063 How important is God in your life
- F118 Justifiable: homosexuality
- F120 Justifiable: abortion
- G006 How proud of nationality
- Y002 Post-Materialist index 4-item
- Y003 Autonomy Index

## Unit of Measurement

The indicators are factor scores derived from principal component analysis. They do not have specific units but represent relative positions on each dimension. The scores have been scaled so that:

- **TradAgg**: Higher values indicate more secular-rational values, lower values indicate more traditional values
- **SurvSAgg**: Higher values indicate more self-expression values, lower values indicate more survival values

## Data Source

This dataset is based on the Integrated Values Surveys (IVS) 1981-2022, which combines:

- European Values Study (EVS) Trend File 1981-2017
- World Values Survey (WVS) Trend File 1981-2022

### Citations

When using this data, please cite the original sources:

- EVS (2021): EVS Trend File 1981-2017. GESIS Data Archive, Cologne. ZA7503 Data file Version 3.0.0, [doi:10.4232/1.14021](https://doi.org/10.4232/1.14021)
- Haerpfer, C., Inglehart, R., Moreno, A., Welzel, C., Kizilova, K., Diez-Medrano J., M. Lagos, P. Norris, E. Ponarin & B. Puranen et al. (eds.). 2022. World Values Survey Trend File (1981-2022) Cross-National Data-Set. Madrid, Spain & Vienna, Austria: JD Systems Institute & WVSA Secretariat. Data File Version 4.0.0, [doi:10.14281/18241.27](https://doi.org/10.14281/18241.27)

## Processing Information

The dataset was created by:

1. Starting with the Integrated Values Surveys data
2. Running factor analysis to generate TradAgg and SurvSAgg scores for each country-year combination
3. Converting the resulting data into DDF format

For detailed information on the factor creation process, see the source documentation in the `etl/source` directory.
