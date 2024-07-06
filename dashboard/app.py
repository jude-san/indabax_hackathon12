import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from faicons import icon_svg

# Import data from shared.py
from shared import app_dir, df
from shiny import reactive
from shiny.express import input, render, ui

ui.page_opts(title="Juderic Retail Dashboard", fillable=True)

with ui.sidebar(title="Filter controls"):
    # Date selector
    ui.input_date_range(
        "date",
        "Date range",
        start="2021-01-01",
        end="2022-12-01",
        min="2021-01-01",
        max="2022-12-01",
        width=10
    )
    
    # Cities selector
    ui.input_checkbox_group(
        "city",
        "Cities",
        ["Abidjan", "Bouake"],
        selected=["Abidjan", "Bouake"],
    )
    
    # Channel selector
    ui.input_checkbox_group(
        "channel",
        "Channel",
        ["Groceries", "Open_Market", "Boutique"],
        selected=["Groceries", "Open_Market", "Boutique"]
    )

with ui.layout_columns(fill=False):
    with ui.value_box(showcase=icon_svg("coins")):
        "Unit price"

        @render.text
        def sum_unit_price():
            return round(df["Unit_Price"].sum(), 1)

    with ui.value_box(showcase=icon_svg("scale-balanced")):
        "Sales Volume"

        @render.text
        def sum_sales_volume():
            return f"{round(df['Sales_Volume(KG_LTRS)'].sum(), 1)} kg/L"
        
    with ui.value_box(showcase=icon_svg("vault")):
        "Sales Value"

        @render.text
        def sum_sales_value():
            return round(df["Sales_Value"].sum(), 1)

with ui.layout_columns():
    @render.plot
    def plot_sales():
        # Remove rows with invalid dates
        df_sales = df.loc[:, ["Period", "Sales_Value"]].dropna(subset=["Period"])
        # Set Period as index
        df_sales.set_index("Period", inplace=True)
        # Aggregate sales data by month
        monthly_sales = df_sales.resample('M').sum()

        # Plot the time series data
        fig = plt.figure(figsize=(12, 6))
        plt.plot(monthly_sales.index,
                monthly_sales['Sales_Value'], marker='o')
        plt.title('Monthly Sales Value Over Time')
        plt.xlabel('Date')
        plt.ylabel('Sales Value')
        plt.grid(True)
        return fig
                

ui.include_css(app_dir / "styles.css")


# @reactive.calc
# def filtered_df():
#     filt_df = df[df["species"].isin(input.species())]
#     filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
#     return filt_df
