# Import libraries
import matplotlib.pyplot as plt
import pandas as pd
from faicons import icon_svg
import datetime

# Import data from shared.py
from shared import app_dir, df
from shiny import reactive
from shiny.express import input, render, ui
from shiny.ui import page_navbar
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Start and end dates
start = datetime.date(2021, 1, 1)
end = datetime.date(2022, 12, 1)

# Title page
ui.h1("Juderic Retail Dashboard")

# Navigation tabs
with ui.navset_tab(id="home"):
    # Home tab
    with ui.nav_panel("Home"):
        #  Value boxes
        with ui.layout_columns(fill=False):
            with ui.value_box(showcase=icon_svg("coins")):
                "Sum of Unit price"
                @render.text
                def sum_unit_price():
                    total_unit_price = filtered_df()['Unit_Price'].sum().round(1)
                    # Formatting the total_unit_price with commas
                    formatted_total = f"{total_unit_price:,}"
                    return formatted_total
                
            with ui.value_box(showcase=icon_svg("scale-balanced")):
                "Sum of Sales Volume"

                @render.text
                def sum_sales_volume():
                    # Summing the 'Sales_Volume(KG_LTRS)' column and rounding to 1 decimal place
                    total_sales_volume = round(filtered_df()['Sales_Volume(KG_LTRS)'].sum(), 1)
                    # Formatting the total_sales_volume with commas and adding ' kg/L' suffix
                    formatted_total_sales_volume = f"{total_sales_volume:,} kg/L"
                    return formatted_total_sales_volume

            with ui.value_box(showcase=icon_svg("vault")):
                "Sum of Sales Value"

                @render.text
                def sum_sales_value():
                    # Summing the 'Sales_Value' column and rounding to 1 decimal place
                    total_sales_value = filtered_df()['Sales_Value'].sum().round(1)

                    # Formatting the total_sales_value with commas
                    formatted_total_sales_value = f"{total_sales_value:,}"
                    return formatted_total_sales_value
                
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
                
    # Sales forecast tab           
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
    
    # Descriptive tab       
    with ui.nav_panel("Descriptives"):
        #  Value boxes
        with ui.layout_columns(fill=False):
            with ui.value_box(showcase=icon_svg("coins")):
                "Mean of Unit price"

                @render.text
                def mean_unit_price():
                    res = f"{filtered_df()["Unit_Price"].mean().round(1):,}"
                    return res

            with ui.value_box(showcase=icon_svg("scale-balanced")):
                "Mean of Sales Volume"

                @render.text
                def mean_sales_volume():
                    return f"{round(filtered_df()['Sales_Volume(KG_LTRS)'].mean(), 1):,} kg/L"

            with ui.value_box(showcase=icon_svg("vault")):
                "Mean of Sales Value"

                @render.text
                def mean_sales_value():
                    return f"{filtered_df()["Sales_Value"].mean().round(1):,}"
                
        with ui.layout_columns(fill=False):
            with ui.card():
                "Bar chart for categorical variables"
                @render.plot
                def plot_cat():
                    
                    # List of columns to exclude
                    exclude_columns = ["Category", "Segment", "Item Name", "City", "Pack_Size"]

                    # Filter the columns
                    columns_to_plot = [col for col in df.select_dtypes("object") if col not in exclude_columns]

                    fig, ax = plt.subplots(2, 2, figsize=(14, 6))

                    # Flatten the axes array
                    ax = ax.flatten()

                    index = 0
                    for i in columns_to_plot:
                        filtered_df()[i].value_counts().sort_values().plot(kind="barh", ax=ax[index])
                        index += 1
                        # Adjust layout to prevent overlap
                        plt.tight_layout()
                    return fig

    # Dataset tab                           
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
    
    # Buttons
    ui.input_action_button("filter", "Filter")
    ui.input_action_button("reset", "Reset")

          
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
    df_manufacture = filt_df["Manufacturer"].isin(input.manufacturer())
    df_pack_size = filt_df["Pack_Size"].isin(input.pack_size())
    df_packaging = filt_df["Packaging"].isin(input.packaging())
    return filt_df[df_city & df_channel & df_manufacture & df_pack_size & df_packaging]

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
