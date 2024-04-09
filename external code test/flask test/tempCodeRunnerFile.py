import matplotlib.pyplot as plt

# Given percentages
percent_gt_01 = 30
percent_lt_minus01 = 40
percent_between_minus01_to_01 = 30

# Labels for the pie chart
labels = ['> 0.1', '< -0.1', '-0.1 to 0.1']

# Percentages
sizes = [percent_gt_01, percent_lt_minus01, percent_between_minus01_to_01]

# Colors for each section
colors = ['#ff9999', '#66b3ff', '#99ff99']

# Explode the first slice (optional)
explode = (0.1, 0, 0)

# Plotting the pie chart
plt.figure(figsize=(8, 6))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, explode=explode)

# Equal aspect ratio ensures that pie is drawn as a circle
plt.axis('equal')

# Title of the pie chart
plt.title('Distribution of Numbers')

# Save the plot as a PDF
plt.savefig('pie_chart.pdf', format='pdf')

# Display the plot
plt.show()
