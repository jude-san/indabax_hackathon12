# Juderic Retail Dashboard

## Instruction to install anaconda

You need to have anaconda installed to proceed with the following steps.
This will ensure you can create and activate a conda environment. Alternatively, you can create a virtual environment with a familiar tool.

Follow the link below to install Anaconda.

[Anaconda](https://www.anaconda.com/download/)

## Create a conda environment

**Replace [preferred_name] with the preferred name of your environment**

```bash
conda create -n preferred_name
```

## Activate environment

```bash
conda activate preferred_name
```

## Install dependencies

```bash
pip install -r requirements.txt
```

OR install the packages below using pip. For example, pip install shiny

### Packages

- faicons
- shiny
- matplotlib
- pandas
- datetime
- statsmodels
- openpyxl

## Run shiny app on the command line

```bash
shiny run app.py
```

Please ensure you are in the directory of app.py when you run the above command
