{\rtf1\ansi\ansicpg1252\cocoartf2759
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import pandas as pd\
import matplotlib.pyplot as plt\
from matplotlib.animation import FuncAnimation\
from matplotlib.offsetbox import OffsetImage, AnnotationBbox\
from matplotlib.patches import Rectangle\
from IPython.display import Video\
import matplotlib.dates as mdates\
\
# Load your data\
df = pd.read_excel("/Users/adamjannetti/Desktop/Data2.xlsx")\
df['Date'] = pd.to_datetime(df['Date'])  # Ensure Date is in datetime format\
\
# Initialize the plot with black background\
fig, ax1 = plt.subplots(figsize=(12, 6), dpi=150, facecolor='black')\
ax1.set_facecolor("black")\
ax2 = ax1.twinx()\
ax2.set_facecolor("black")\
\
# Set titles and labels with additional padding\
fig.suptitle("Bitcoin (BTC) Price vs. Hash Rate", fontsize=20, y=0.92, color="white", fontweight="bold")\
ax1.set_xlabel('Date', fontsize=14, color="white", fontweight="bold", labelpad=15)\
ax1.set_ylabel('Bitcoin (BTC) Price ($)', color='white', fontsize=14, fontweight="bold", labelpad=15)\
ax2.set_ylabel('Hash Rate (TH/s)', color='white', fontsize=14, fontweight="bold", labelpad=15)\
\
# Adjust layout to ensure equal spacing for both Y-axis labels\
plt.subplots_adjust(left=0.15, right=0.85, top=0.8)\
\
# Custom formatter for BTC price axis to show 1 decimal place for values < $1\
def btc_price_formatter(x, _):\
    if x < 1:\
        return f'$\{x:.1f\}'\
    else:\
        return f'$\{x:,.0f\}'\
\
# Apply custom formatter to BTC price Y-axis only\
ax1.yaxis.set_major_formatter(plt.FuncFormatter(btc_price_formatter))\
ax1.tick_params(axis='y', labelcolor='white', labelsize=12, width=2)\
ax2.tick_params(axis='y', labelcolor='white', labelsize=12, width=2)\
ax1.tick_params(axis='x', labelsize=12, colors="white", width=2)\
\
# Set the date format for the X-axis\
ax1.xaxis.set_major_locator(mdates.YearLocator())\
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))\
\
# Format the y-axis for Hash Rate with commas\
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'\{x:,.0f\}'))\
\
# Load and set up the watermark image behind the line series\
image_path = "/Users/adamjannetti/Desktop/TephraLogoBlack.jpg"\
image = plt.imread(image_path)\
imagebox = OffsetImage(image, zoom=0.5, alpha=0.4)\
ab = AnnotationBbox(imagebox, (0.5, 0.5), frameon=False, xycoords='axes fraction', zorder=0)\
\
# Add the watermark image to the plot with lower zorder\
ax1.add_artist(ab)\
\
# Add a white rectangle to define the chart area\
rect = Rectangle(\
    (0, 0), 1, 1,\
    transform=ax1.transAxes,\
    color="white", alpha=0.1, zorder=0\
)\
ax1.add_patch(rect)\
\
# Initialization function for FuncAnimation with blank starting frame\
def init():\
    ax1.set_xlim(df['Date'].iloc[0], df['Date'].iloc[0] + pd.DateOffset(days=30))\
    ax1.set_ylim(0, df['BTC_Price'].max() * 1.1)\
    ax2.set_ylim(0, df['Hash_Rate'].max() * 1.1)\
    line1.set_data([], [])\
    line2.set_data([], [])\
    return line1, line2\
\
# Update function to animate the plot with fixed lower limits and dynamic upper limits for both x and y axes\
def update(frame):\
    x = df['Date'][:frame + 1]\
    y1 = df['BTC_Price'][:frame + 1]\
    y2 = df['Hash_Rate'][:frame + 1]\
\
    line1.set_data(x, y1)\
    line2.set_data(x, y2)\
\
    # Keep the left x-axis limit fixed and expand the right limit dynamically\
    left_limit = df['Date'].iloc[0]\
    right_limit = x.iloc[-1] if len(x) > 1 else x.iloc[0] + pd.Timedelta(days=1)\
    ax1.set_xlim(left_limit, right_limit)\
\
    # Keep the lower y-axis limits fixed at zero and expand the upper limits dynamically\
    upper_limit_y1 = max(y1) * 1.1\
    upper_limit_y2 = max(y2) * 1.1\
    ax1.set_ylim(0, upper_limit_y1)\
    ax2.set_ylim(0, upper_limit_y2)\
\
    return line1, line2\
\
# Plot lines with higher zorder to ensure they are on top of the watermark\
line1, = ax1.plot([], [], color='#ff5500', label='Bitcoin (BTC) Price', zorder=2)\
line2, = ax2.plot([], [], color='white', label='Hash Rate', zorder=2)\
\
# Add legend in white font above the chart\
legend = fig.legend(\
    loc="upper center", \
    bbox_to_anchor=(0.5, 0.88), \
    ncol=2, \
    fontsize=12, \
    frameon=False,\
    labelcolor='white', \
    prop=\{'weight': 'bold', 'size': 12\}\
)\
\
# Create animation with the full length of the DataFrame\
ani = FuncAnimation(fig, update, frames=len(df), init_func=init, blit=True)\
\
# Display the final frame as a static image\
x = df['Date']\
y1 = df['BTC_Price']\
y2 = df['Hash_Rate']\
ax1.plot(x, y1, color='#ff5500')\
ax2.plot(x, y2, color='white')\
plt.show()\
\
# Save the animation as an MP4 video\
ani.save("/Users/adamjannetti/Desktop/Bitcoin_HashRate_Animation.mp4", writer="ffmpeg", fps=260)}