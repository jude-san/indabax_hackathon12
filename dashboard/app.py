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
    ui.date_select(
        "date"
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

with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Unit price")

        @reactive.calc
        def sum_unit_price():
            return round(df["Unit_Price"].sum(), 1)

    with ui.card(full_screen=True):
        ui.card_header("Sales Volume")

        @reactive.calc
        def sum_sales_volume():
            return round(df["Sales_Volume(KG_LTRS)"].sum(), 1)
        
    with ui.card(full_screen=True):
        ui.card_header("Sales Value")

        @reactive.calc
        def sum_sales_value():
            return round(df["Sales_Value"].sum(), 1)


# with ui.layout_column_wrap(fill=False):
#     with ui.value_box(showcase=icon_svg("earlybirds")):
#         "Number of penguins"

#         @render.text
#         def count():
#             return filtered_df().shape[0]

#     with ui.value_box(showcase=icon_svg("ruler-horizontal")):
#         "Average bill length"

#         @render.text
#         def bill_length():
#             return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

#     with ui.value_box(showcase=icon_svg("ruler-vertical")):
#         "Average bill depth"

#         @render.text
#         def bill_depth():
#             return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"





ui.include_css(app_dir / "styles.css")


# @reactive.calc
# def filtered_df():
#     filt_df = df[df["species"].isin(input.species())]
#     filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
#     return filt_df
