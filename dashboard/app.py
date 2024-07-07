import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from faicons import icon_svg
import datetime

# Import data from shared.py
from shared import app_dir, df
from shiny import reactive
from shiny.express import input, render, ui
from functools import partial
from shiny.ui import page_navbar
from api import API_KEY
import openai

# Openai
openai.api_key = API_KEY

def get_response(query):
    response = openai.completions.create(
        prompt=query,
        model="gpt-3.5-turbo-instruct",
        stream=True,
        max_tokens=150
    )
    return  response.choices[0].text_strip()

start = datetime.date(2021, 1, 1)
end = datetime.date(2022, 12, 1)

with ui.sidebar(title="Filter controls"):
    # Date selector
    ui.input_date_range(
        "date",
        "Date range",
        start=start,
        end=end,
        min=start,
        max=end,
        width="100"
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
        "Channels",
        ["Groceries", "Open_Market", "Boutique"],
        selected=["Groceries", "Open_Market", "Boutique"]
    )
    
    # Query box
    ui.input_text("query", "Enter your query")
    
    # Button
    ui.input_action_button("submit", "Submit")

ui.page_opts(title="Juderic Retail Dashboard", fillable=True
             )

with ui.layout_columns(fill=False):
    with ui.value_box(showcase=icon_svg("coins")):
        "Unit price"

        @render.text
        def sum_unit_price():
            return filtered_df()["Unit_Price"].sum().round(1)

    with ui.value_box(showcase=icon_svg("scale-balanced")):
        "Sales Volume"

        @render.text
        def sum_sales_volume():
            return f"{round(filtered_df()['Sales_Volume(KG_LTRS)'].sum(), 1)} kg/L"
        
    with ui.value_box(showcase=icon_svg("vault")):
        "Sales Value"

        @render.text
        def sum_sales_value():
            return filtered_df()["Sales_Value"].sum().round(1)

with ui.layout_columns():
    with ui.card():
        "Monthly sales"
        @render.plot
        def plot_sales():
            # Remove rows with invalid dates
            df_sales = filtered_df().loc[:, ["Sales_Value"]]
            # Aggregate sales data by month
            monthly_sales = df_sales.resample('ME').sum()

            # Plot the time series data
            fig = plt.figure(figsize=(12, 6))
            plt.plot(monthly_sales.index,
                    monthly_sales['Sales_Value'], marker='o')
            plt.title('Monthly Sales Value Over Time')
            plt.xlabel('Date')
            plt.ylabel('Sales Value')
            plt.grid(True)
            return fig
    with ui.card():
        "Chatbot response"
        @render.text
        def response():
            user_query = input.query()
            if user_query:
                chatgpt_response = get_response(user_query)
                return f"Response {chatgpt_response}"
            else:
                return "Please enter a query"
        
                

ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
    df["Date"] = pd.to_datetime(df["Period"], errors="coerce")
    df.set_index("Date", inplace=True)
    start, end = input.date()
    filt_df = df[start:end]
    filt_df = filt_df[filt_df["City"].isin(input.city())]
    filt_df = filt_df[filt_df["Channel"].isin(input.channel())]
    return filt_df
