# Import libraries
import matplotlib.pyplot as plt # Visualisation
import pandas as pd # Data manipulation and analysis
from faicons import icon_svg # Icons
import datetime # Manipulate date time

# Import data from shared.py
from shared import app_dir, df
# Shiny modules
from shiny import reactive
from shiny.express import input, render, ui
# Time series forecasting
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
        #  Value boxes for the sum of unit price, sales volume and sales value
        with ui.layout_columns(fill=False):
            with ui.value_box(showcase=icon_svg("coins")):
                "Sum of Unit price"
                @render.text
                def sum_unit_price():
                    """
                    Calculate the sum of unit price

                    Args
                    ----
                    None

                    Returns
                    -------
                    formatted_unit_price_total (float): Total sum of unit price
                    """
                    total_unit_price = filtered_df()['Unit_Price'].sum().round(1)
                    # Formatting the total_unit_price with commas
                    formatted_unit_price_total = f"{total_unit_price:,}"
                    return formatted_unit_price_total
                
            with ui.value_box(showcase=icon_svg("scale-balanced")):
                "Sum of Sales Volume"

                @render.text
                def sum_sales_volume():
                    """
                    Calculate the sum of sales volume

                    Args
                    ----
                    None

                    Returns
                    -------
                    formatted_total_sales_volume (float): Total sum of unit price
                    """
                    # Summing the 'Sales_Volume(KG_LTRS)' column and rounding to 1 decimal place
                    total_sales_volume = round(filtered_df()['Sales_Volume(KG_LTRS)'].sum(), 1)
                    # Formatting the total_sales_volume with commas and adding ' kg/L' suffix
                    formatted_total_sales_volume = f"{total_sales_volume:,} kg/L"
                    return formatted_total_sales_volume

            with ui.value_box(showcase=icon_svg("vault")):
                "Sum of Sales Value"

                @render.text
                def sum_sales_value():
                    """
                    Calculate the sum of sales value

                    Args
                    ----
                    None

                    Returns
                    -------
                    formatted_total_sales_value (float): Total sum of unit price
                    """
                    
                    # Summing the 'Sales_Value' column and rounding to 1 decimal place
                    total_sales_value = filtered_df()['Sales_Value'].sum().round(1)

                    # Formatting the total_sales_value with commas
                    formatted_total_sales_value = f"{total_sales_value:,}"
                    return formatted_total_sales_value

        # Plot on monthly sales over time        
        with ui.layout_columns(fill=False):
             with ui.card():
                "Monthly sales"
                @render.plot
                def plot_sales():
                    """
                    Plot monthly sales

                    Args
                    ----
                    None

                    Returns
                    -------
                    fig (plot): Monthly sales over time
                    """
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
                """
                Forecast sales value                                     

                Args
                ----
                None

                Returns
                -------
                fig (plot): Forecast sales value plot
                """
                df_sales = filtered_df().loc[:, ["Sales_Value"]]
                # Aggregate sales data by month
                monthly_sales = df_sales.resample('ME').sum()
                # Build and fit the model
                model = ExponentialSmoothing(
                    monthly_sales['Sales_Value'], seasonal='add', seasonal_periods=4).fit()

                # Forecast for the next 12 months
                forecast = model.forecast(steps=12)

                # Plot the forecast
                plt.figure(figsize=(12, 6))
                fig = plt.plot(monthly_sales.index,
                            monthly_sales['Sales_Value'], marker='o', label='Observed')
                future_dates = [monthly_sales.index.max() + pd.DateOffset(months=i)
                                for i in range(1, 13)]
                forecast_df = pd.DataFrame(
                    {'Date': future_dates, 'Sales_Value': forecast})
                plt.plot(forecast_df['Date'], forecast_df['Sales_Value'],
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
            # Mean of unit price
            with ui.value_box(showcase=icon_svg("coins")):
                "Mean of Unit price"

                @render.text
                def mean_unit_price():
                    """
                    Calculate the mean of unit price

                    Args
                    ----
                    None

                    Returns
                    -------
                    (float): Mean unit price
                    """
                    return f"{filtered_df()['Unit_Price'].mean().round(1):,}"
            
            # Mean of sales volume
            with ui.value_box(showcase=icon_svg("scale-balanced")):
                "Mean of Sales Volume"

                @render.text
                def mean_sales_volume():
                    """
                    Calculate the mean sales volume

                    Args
                    ----
                    None

                    Returns
                    -------
                    (float): Mean sales volume
                    """

                    return f"{round(filtered_df()['Sales_Volume(KG_LTRS)'].mean(), 1):,} kg/L"
            
            # Mean of sales value
            with ui.value_box(showcase=icon_svg("vault")):
                "Mean of Sales Value"

                @render.text
                def mean_sales_value():
                    """
                    Calculate the mean sales value

                    Args
                    ----
                    None

                    Returns
                    -------
                    (float): Mean sales value
                    """
                    return f"{filtered_df()['Sales_Value'].mean().round(1):,}"
                
        with ui.layout_columns(fill=False):
            with ui.card():
                "Bar chart for categorical variables"
                @render.plot
                def plot_cat():
                    """
                    Plot categorical variables

                    Args
                    -----
                    None

                    Returns
                    --------
                    fig (plot): Bar graphs for categorical variables
                    """
                    # List of columns to exclude
                    exclude_columns = ["Category", "Segment", "Item Name", "City", "Pack_Size"]

                    # Filter the columns
                    columns_to_plot = [col for col in df.select_dtypes("object") if col not in exclude_columns]

                    fig, ax = plt.subplots(2, 2, figsize=(9, 5))

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
                """
                Return dataframe
                """
                return filtered_df()    

# Sidebar: Filter controls
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
    ui.input_action_button("filter", "Filter") # Filter
    ui.input_action_button("reset", "Reset") # Reset

 
# Embed chatbot
ui.HTML(
    """
      <script>
        window.embeddedChatbotConfig = {
        chatbotId: "-kIW47h9_yEb8wZj6DlG4",
        domain: "www.chatbase.co"}
      </script>
        <script
        src="https://www.chatbase.co/embed.min.js"
        chatbotId="-kIW47h9_yEb8wZj6DlG4"
        domain="www.chatbase.co"
        defer>
        </script>
    """
)

# CSS stylesheet
ui.include_css(app_dir / "styles.css")

# Reactive data
@reactive.calc
@reactive.event(input.filter, ignore_none=False)
def filtered_df():
    """
    Reactively calculate the dataset output

    Args
    ----
    None

    Returns
    -------
    filt_df (dataframe): Unfiltered or filtered dataframe
    """
    df["Date"] = pd.to_datetime(df["Period"], errors="coerce")
    df.set_index("Date", inplace=True)
    start, end = input.date()
    filt_df = df[start:end]
    df_city = filt_df["City"].isin(input.city())
    df_channel = filt_df["Channel"].isin(input.channel())
    df_manufacture = filt_df["Manufacturer"].isin(input.manufacturer())
    df_pack_size = filt_df["Pack_Size"].isin(input.pack_size())
    df_packaging = filt_df["Packaging"].isin(input.packaging())
    return filt_df[df_city & df_channel & df_manufacture & df_pack_size & df_packaging].drop(columns=["Period"])

@reactive.effect
@reactive.event(input.reset)
def _():
    """
    Reset filters
    """
    ui.update_date_range("date", start=start, end=end)
    ui.update_checkbox_group("city", selected=["Abidjan", "Bouake"])
    ui.update_checkbox_group("channel", selected=[
                             "Groceries", "Open_Market", "Boutique"])
    ui.update_checkbox_group("manufacturer", 
                             selected=['CAPRA', 'GOYMEN FOODS', 'DOUBA', 'PAGANINI', 'PANZANI',
                                        'PASTA DOUBA', 'MR COOK', 'TAT MAKARNACILIK SANAYI VE TICARET AS',
                                        'REINE', 'MOULIN MODERNE', 'AVOS GROUP', 'OBA MAKARNA'])
    ui.update_checkbox_group("pack_size", selected=[
                             '200G', '500G', '4540G', '475G', '250G', '450G'])
    ui.update_checkbox_group("packaging", selected=['SACHET', 'BAG'])
