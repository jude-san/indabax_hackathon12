# Import libraries
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from faicons import icon_svg
import datetime

# Import data from shared.py
from shared import app_dir, df
import shiny
from shiny import reactive
from shiny.express import input, render, ui
from functools import partial
from shiny.ui import page_navbar
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Start and end dates
start = datetime.date(2021, 1, 1)
end = datetime.date(2022, 12, 1)

# Title page
ui.page_opts(title="Juderic Retail Dashboard", fillable=True)

with ui.navset_tab(id="home"):
    with ui.nav_panel("Home"):
        #  Value boxes
        with ui.layout_columns(fill=False):
            with ui.value_box(showcase=icon_svg("coins")):
                "Unit price"

                @render.text
                def sum_unit_price():
                    res = f"{filtered_df()["Unit_Price"].sum().round(1):,}"
                    return res

            with ui.value_box(showcase=icon_svg("scale-balanced")):
                "Sales Volume"

                @render.text
                def sum_sales_volume():
                    return f"{round(filtered_df()['Sales_Volume(KG_LTRS)'].sum(), 1):,} kg/L"

            with ui.value_box(showcase=icon_svg("vault")):
                "Sales Value"

                @render.text
                def sum_sales_value():
                    return f"{filtered_df()["Sales_Value"].sum().round(1):,}"
                
        with ui.layout_columns(fill=False):
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
                
    with ui.nav_panel("Sales forecast"):
        with ui.card():
            "Forecast sales"
            @render.plot
            def forecast_sales():
                # Remove rows with invalid dates
                df_sales = filtered_df().loc[:, ["Sales_Value"]]
                # Aggregate sales data by month
                monthly_sales = df_sales.resample('ME').sum()
                # Build and fit the model
                model = ExponentialSmoothing(
                    monthly_sales['Sales_Value'], seasonal='add', seasonal_periods=12).fit()

                # Forecast for the next 12 months
                forecast = model.forecast(steps=12)

                # Plot the forecast
                plt.figure(figsize=(12, 6))
                fig = plt.plot(monthly_sales.index,
                            monthly_sales['Sales_Value'], marker='o', label='Observed')
                future_dates = [monthly_sales.index.max() + pd.DateOffset(months=i)
                                for i in range(1, 13)]
                forecast_df = pd.DataFrame(
                    {'Period': future_dates, 'Sales_Value': forecast})
                plt.plot(forecast_df['Period'], forecast_df['Sales_Value'],
                        marker='o', linestyle='--', label='Forecasted')
                plt.title('Sales Value Forecast')
                plt.xlabel('Date')
                plt.ylabel('Sales Value')
                plt.legend()
                plt.grid(True)
                return fig
    with ui.nav_panel("Dataset"):
        with ui.card():
            "Dataset"
            @render.data_frame
            def dataframe():
                return filtered_df()    

# # Sidebar: Filter controls
with ui.sidebar(title="Filter controls", open="desktop"):
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
    
    # Manufacturer selector
    ui.input_checkbox_group(
        "manufacturer",
        "Manufacturer",
        ['CAPRA', 'GOYMEN FOODS', 'DOUBA', 'PAGANINI', 'PANZANI',
         'PASTA DOUBA', 'MR COOK', 'TAT MAKARNACILIK SANAYI VE TICARET AS',
         'REINE', 'MOULIN MODERNE', 'AVOS GROUP', 'OBA MAKARNA'],
        selected=['CAPRA', 'GOYMEN FOODS', 'DOUBA', 'PAGANINI', 'PANZANI',
                  'PASTA DOUBA', 'MR COOK', 'TAT MAKARNACILIK SANAYI VE TICARET AS',
                  'REINE', 'MOULIN MODERNE', 'AVOS GROUP', 'OBA MAKARNA']
    )
    
    # Pack size selector
    ui.input_checkbox_group(
        "pack_size",
        "Pack size",
        ['200G', '500G', '4540G', '475G', '250G', '450G'],
        selected=['200G', '500G', '4540G', '475G', '250G', '450G']
    )
    
    # Packaging selector
    ui.input_checkbox_group(
        "packaging",
        "Packaging",
        ['SACHET', 'BAG'],
        selected=['SACHET', 'BAG']
    )
    
    # Button
    ui.input_action_button("filter", "Filter")

          
# CSS stylesheet
ui.include_css(app_dir / "styles.css")

# Reactive data
@reactive.calc
@reactive.event(input.filter, ignore_none=False)
def filtered_df():
    df["Date"] = pd.to_datetime(df["Period"], errors="coerce")
    df.set_index("Date", inplace=True)
    start, end = input.date()
    filt_df = df[start:end]
    df_city = filt_df["City"].isin(input.city())
    df_channel = filt_df["Channel"].isin(input.channel())
    return filt_df[df_city & df_channel]

# Embed chatbot
ui.HTML(
    """
      <script>
        window.embeddedChatbotConfig = {
        chatbotId: "AgzYXakqXm0hdtC4cNzAn",
        domain: "www.chatbase.co"}
      </script>
        <script
        src="https://www.chatbase.co/embed.min.js"
        chatbotId="AgzYXakqXm0hdtC4cNzAn"
        domain="www.chatbase.co"
        defer>
        </script>
    """
)
