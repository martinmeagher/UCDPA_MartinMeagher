# Import all modules needed to analyse data
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Assign the filename to the data set to be imported
file = 'vgsales.csv'

# Read the file into a DataFrame
vgsales = pd.read_csv(file, nrows=200, index_col=False)

# Delete any rows with missing data from important columns
vgsales = vgsales.dropna(subset=['Rank', 'Name', 'Platform', 'Genre', 'NA_Sales', 'EU_Sales',
                                 'JP_Sales', 'Other_Sales', 'Global_Sales'])
# Replace any missing values from columns not needed with Nan
vgsales = vgsales.fillna("NaN")

# Add a new column to assign a console name and populate it with nan
vgsales["console"] = np.nan

# Add a label column to make it easier to read graphs when displaying on graphs
vgsales["label"] = vgsales["Name"].str.slice(0, 12)

# Add the rank number to the name to avoid any instances of repeated game names
vgsales["Name"] = vgsales["Rank"].astype(str) + "-" + vgsales["Name"]

# Create a tuple containing the three lists for each of the consoles we are looking to get the top ten sales for
myList = {'nintendo': {"Wii", "WiiU"}, 'xbox': {"XB", "X360", "XOne"}, 'playstation': {"PS", "PS2", "PS3", "PS4"}}

# Create a copy of the structure of the original data frame where data to be displayed will be stored
top10 = vgsales.head(0)


# Function to take out the ten most popular games for a specified set of platform values
def consoleTop10(myList):
    # Filter the original data set with the desired platforms and store in a new data set
    topten = vgsales[vgsales["Platform"].isin(myList[-1])]

    # Sort the filtered dataset by highest global sales in descending order
    topten = topten.sort_values("Global_Sales", ascending=False)

    # Add the console name to the console column so we can use this as a hue for visuals later
    topten.loc[:, "console"] = myList[0]

    # Use only the top ten entries
    return topten.head(10)


# Create a function that will generate the top ten entries for each console from myList
for x in myList.items():
    # Add the top ten entries to the top10 dataset and store them for later analysis
    top10 = top10.append(consoleTop10(x))

# Set the index to the Name column so we can plot a bar chart of the games
top10 = top10.set_index('Name')

# Separate the list into the three different data sets to plot on three different subplots
top10_nintendo = top10[top10['console'] == "nintendo"]
top10_xbox = top10[top10['console'] == "xbox"]
top10_playstation = top10[top10['console'] == "playstation"]

# Create a figure and an array of axes: 3 rows, 1 to display a stacked bar chart
fig, ax = plt.subplots(3, 1, figsize=(12, 6))
plt.subplots_adjust(right=1, top=1, hspace=0.733)

# Plot the Nintendo sales on from around the world as a stacked bar chart
ax[0].bar(top10_nintendo.index, top10_nintendo["NA_Sales"],
          label="North America")
ax[0].bar(top10_nintendo.index, top10_nintendo["EU_Sales"],
          bottom=top10_nintendo["NA_Sales"],
          label="Europe")
ax[0].bar(top10_nintendo.index, top10_nintendo["JP_Sales"],
          bottom=top10_nintendo["NA_Sales"]+top10_nintendo["EU_Sales"],
          label="Japan")
ax[0].bar(top10_nintendo.index, top10_nintendo["Other_Sales"],
          bottom=top10_nintendo["NA_Sales"]+top10_nintendo["EU_Sales"]+top10_nintendo["JP_Sales"],
          label="Rest of the World")

# Plot the Xbox sales on from around the world as a stacked bar chart
ax[1].bar(top10_xbox.index, top10_xbox["NA_Sales"],
          label="North America")
ax[1].bar(top10_xbox.index, top10_xbox["EU_Sales"],
          bottom=top10_xbox["NA_Sales"],
          label="Europe")
ax[1].bar(top10_xbox.index, top10_xbox["JP_Sales"],
          bottom=top10_xbox["NA_Sales"]+top10_xbox["EU_Sales"],
          label="Japan")
ax[1].bar(top10_xbox.index, top10_xbox["Other_Sales"],
          bottom=top10_xbox["NA_Sales"]+top10_xbox["EU_Sales"]+top10_xbox["JP_Sales"],
          label="Rest of the World")

# Plot the Playstation sales on from around the world as a stacked bar chart
ax[2].bar(top10_playstation.index, top10_playstation["NA_Sales"],
          label="North America")
ax[2].bar(top10_playstation.index, top10_playstation["EU_Sales"],
          bottom=top10_playstation["NA_Sales"], label="Europe")
ax[2].bar(top10_playstation.index, top10_playstation["JP_Sales"],
          bottom=top10_playstation["NA_Sales"]+top10_playstation["EU_Sales"],
          label="Japan")
ax[2].bar(top10_playstation.index, top10_playstation["Other_Sales"],
          bottom=top10_playstation["NA_Sales"]+top10_playstation["EU_Sales"]+top10_playstation["JP_Sales"],
          label="Rest of the World")

# Display the legend in the top subplot
ax[0].legend(loc='best', ncol=4)

# Set the X Labels for each graph and rotate at 45 degrees
ax[0].set_xticklabels(top10_nintendo['label'], rotation=45)
ax[1].set_xticklabels(top10_xbox['label'], rotation=45)
ax[2].set_xticklabels(top10_playstation['label'], rotation=45)

# Customise graph to make it easier to read and interpret
ax[0].set(title='No. of Games Sold', xlabel="Nintendo Sales", )
ax[1].set(xlabel="Xbox Sales", ylabel="No. of Games Sold (millions)")
ax[2].set(xlabel="Playstation Sales")
plt.tight_layout()

# Display the graph and save
fig1 = plt.gcf()
plt.show()
fig1.savefig("Console_Sales_Comparison.png", dpi=100)
# Clear the graph to display the next figure
plt.clf()

# Set the palette and colour styles for the graph
sns.set_palette("husl", 3)
sns.set_style("whitegrid")

# Create a count plot to show the genres of the most popular games for each console
sns.countplot(x="Genre", data=top10, hue="console")

# Customise graph to make it easier to read and interpret
plt.title("CountPlot showing Genres of Most Popular Games")
plt.ylabel("No. of Occurrences")
plt.xlabel("Genre")
plt.legend(title='Console', loc='upper left', labels=['Nintendo', 'Xbox', 'Playstation'])

# Display the plot and save
fig2 = plt.gcf()
plt.show()
fig2.savefig("Console_Genres_Comparison.png", dpi=100)
