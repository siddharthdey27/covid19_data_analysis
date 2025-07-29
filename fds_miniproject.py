import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk
from datetime import datetime

covid_df = pd.read_csv(r'C:\Users\Siddharth\Downloads\covid_19_india.csv')
vaccine_df = pd.read_csv(r'C:\Users\Siddharth\Downloads\covid_vaccine_statewise.csv')

def preprocess_data():
    global covid_df, vaccine_df
    
    columns_to_drop = ["Sno", "Time", "ConfirmedIndianNational", "ConfirmedForeignNational"]
    covid_df.drop(columns=[col for col in columns_to_drop if col in covid_df.columns], inplace=True, axis=1)
    

    covid_df['Date'] = pd.to_datetime(covid_df['Date'], format='%Y-%m-%d')
    covid_df['Active_cases'] = covid_df['Confirmed'] - (covid_df['Cured'] + covid_df['Deaths'])
    

    vaccine_df.rename(columns={'Total Individuals Vaccinated': 'Total'}, inplace=True)
    vaccine_df = vaccine_df[vaccine_df.State != 'India']

preprocess_data()


def plot_active_cases(state=None, start_date=None, end_date=None):
    filtered_df = covid_df
    if state:
        filtered_df = filtered_df[filtered_df['State/UnionTerritory'] == state]
    if start_date:
        filtered_df = filtered_df[filtered_df['Date'] >= start_date]
    if end_date:
        filtered_df = filtered_df[filtered_df['Date'] <= end_date]
    
    plt.figure(figsize=(16, 6))
    sns.histplot(filtered_df['Active_cases'], bins=30, kde=True, color='blue')
    plt.title("Histogram of Active Cases in India", size=25)
    plt.xlabel("Number of Active Cases")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()


def plot_deaths(state=None, start_date=None, end_date=None):
    filtered_df = covid_df
    if state:
        filtered_df = filtered_df[filtered_df['State/UnionTerritory'] == state]
    if start_date:
        filtered_df = filtered_df[filtered_df['Date'] >= start_date]
    if end_date:
        filtered_df = filtered_df[filtered_df['Date'] <= end_date]
        
    death_counts = filtered_df.groupby('State/UnionTerritory')['Deaths'].sum()
    plt.figure(figsize=(10, 10))
    plt.pie(death_counts, labels=death_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title("Distribution of Total Deaths by State", size=25)
    plt.axis('equal') 
    plt.show()


def plot_vaccination(state=None):
    filtered_df = vaccine_df
    if state:
        filtered_df = filtered_df[filtered_df['State'] == state]
    
    
    if not state:

        total_vaccinations = vaccine_df.groupby('State')['Total'].sum()
    else:
        total_vaccinations = filtered_df.groupby('State')['Total'].sum()

    plt.figure(figsize=(10, 10))
    plt.pie(total_vaccinations, labels=total_vaccinations.index, autopct='%1.1f%%', startangle=140)
    plt.title(f"Vaccination Distribution for {state if state else 'All States'}", size=25)
    plt.axis('equal')  
    plt.show()


def display_top_states(criteria):
    if criteria == "Maximum Deaths":
        top_states = covid_df.groupby('State/UnionTerritory')['Deaths'].sum().nlargest(5)
    elif criteria == "Maximum Vaccinations":
        top_states = vaccine_df.groupby('State')['Total'].sum().nlargest(5)
    elif criteria == "Maximum Confirmed":
        top_states = covid_df.groupby('State/UnionTerritory')['Confirmed'].sum().nlargest(5)
    
    top_states_df = top_states.reset_index()
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_states_df, x=top_states_df.columns[0], y=top_states_df.columns[1])
    plt.title(f"Top 5 States by {criteria}", size=25)
    plt.xlabel("States")
    plt.ylabel("Number of People") 
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


class COVID19AnalysisApp:
    def __init__(self, root): 
        self.root = root
        self.root.title("COVID-19 Data Analysis in India")

   
        self.title_label = ttk.Label(root, text="COVID-19 Data Analysis", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

  
        self.state_label = ttk.Label(root, text="Enter State (Leave blank for all states):")
        self.state_label.pack(pady=5)
        self.state_entry = ttk.Entry(root)
        self.state_entry.pack(pady=5)


        self.start_date_label = ttk.Label(root, text="Enter Start Date (YYYY-MM-DD):")
        self.start_date_label.pack(pady=5)
        self.start_date_entry = ttk.Entry(root)
        self.start_date_entry.pack(pady=5)

        
        self.end_date_label = ttk.Label(root, text="Enter End Date (YYYY-MM-DD):")
        self.end_date_label.pack(pady=5)
        self.end_date_entry = ttk.Entry(root)
        self.end_date_entry.pack(pady=5)

        self.graph_type_label = ttk.Label(root, text="Select Graph Type:")
        self.graph_type_label.pack(pady=5)
        self.graph_type_combobox = ttk.Combobox(root, values=[
            "Active Cases Histogram", 
            "Deaths Pie Chart", 
            "Vaccinations Pie Chart",
            "Top 5 States by Maximum Deaths",
            "Top 5 States by Maximum Vaccinations",
            "Top 5 States by Maximum Confirmed"
        ])
        self.graph_type_combobox.pack(pady=5)

        self.show_graph_button = ttk.Button(root, text="Show Graph", command=self.show_graph)
        self.show_graph_button.pack(pady=10)

        self.exit_button = ttk.Button(root, text="Exit", command=root.quit)
        self.exit_button.pack(pady=10)

    def show_graph(self):
        state = self.state_entry.get().strip()
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()
        graph_type = self.graph_type_combobox.get()

        if graph_type == "Active Cases Histogram":
            plot_active_cases(state if state else None, 
                              start_date if start_date else None, 
                              end_date if end_date else None)
        elif graph_type == "Deaths Pie Chart":
            plot_deaths(state if state else None, 
                        start_date if start_date else None, 
                        end_date if end_date else None)
        elif graph_type == "Vaccinations Pie Chart":
            plot_vaccination(state if state else None)
        elif graph_type == "Top 5 States by Maximum Deaths":
            display_top_states("Maximum Deaths")
        elif graph_type == "Top 5 States by Maximum Vaccinations":
            display_top_states("Maximum Vaccinations")
        elif graph_type == "Top 5 States by Maximum Confirmed":
            display_top_states("Maximum Confirmed")

if __name__ == "__main__": 
    root = tk.Tk()
    preprocess_data()  
    app = COVID19AnalysisApp(root)
    root.mainloop()
