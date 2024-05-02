import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=['date'])

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.plot(df.index, df['value'], color='red')
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    df_bar = df_bar.groupby(['year', 'month'], sort=False).mean()
    # print(df_bar.groupby('year').count()) # missing 4 months from 2016
    # print(df_bar)
    df_bar = df_bar.reset_index()
    missing_data = {
        "year": [2016, 2016, 2016, 2016],
        "month": ['January', 'February', 'March', 'April'],
        "value": [0, 0, 0, 0]
    }
    df_bar = pd.concat((pd.DataFrame(missing_data), df_bar))
    # print(df_bar)
    # Draw bar plot
    fig, ax = plt.subplots(figsize=(8, 6))
    # ax.plot(df_bar.index, df_bar['value'])
    graph = sns.barplot(data=df_bar, x="year", y="value", hue="month")
    ax.set_title("Daily freeCodeCamp Forum Average Page Views per Month")
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    graph.legend_.set_title("Months")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done! (almost))
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    # personal fix
    df_box['month'] = [d.strftime('%b').capitalize() for d in df_box.date]
    # df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1, 2, figsize=(16,6))
    ax[0].set_title("Year-wise Box Plot (Trend)")
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel("Page Views")
    sns.boxplot(data=df_box, x="year", y="value", ax=ax[0])

    ax[1].set_title("Month-wise Box Plot (Seasonality)")
    ax[1].set_xlabel("Month")
    ax[1].set_ylabel("Page Views")
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sns.boxplot(data=df_box, x="month", y="value", ax=ax[1], order=month_order)
    # print(df_box)

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

def main() -> None:
    draw_line_plot()
    draw_bar_plot()
    draw_box_plot()

if __name__ == "__main__":
    main()