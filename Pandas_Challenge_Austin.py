#!/usr/bin/env python
# coding: utf-8

# # PyCity Schools Analysis
# 
# * As a whole, schools with higher budgets, did not yield better test results. By contrast, schools with higher spending 645-675 per student actually underperformed compared to schools with smaller budgets (585 per student).
# 
# * As a whole, smaller and medium sized schools dramatically out-performed large sized schools on passing math performances (89-91% passing vs 67%).
# 
# * As a whole, charter schools out-performed the public district schools across all metrics. However, more analysis will be required to glean if the effect is due to school practices or the fact that charter schools tend to serve smaller student populations per school. 
# ---

# In[1]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset.  
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])


# ## District Summary

# In[2]:


# Calculate the Totals (Schools and Students)
school_count = len(school_data_complete["school_name"].unique())
student_count = school_data_complete["Student ID"].count()

# Calculate the Total Budget
total_budget = school_data["budget"].sum()


# In[3]:


# Calculate the Average Scores
average_math_score = school_data_complete["math_score"].mean()
average_reading_score = school_data_complete["reading_score"].mean()


# In[7]:


# Calculate the Percentage Pass Rates
passing_count_math = school_data_complete[(school_data_complete["math_score"] >= 70)].count()["student_name"]

passing_percentage_math = passing_count_math / float(student_count) * 100

passing_count_reading = school_data_complete[(school_data_complete["reading_score"] >= 70)].count()["student_name"]

passing_percentage_reading = passing_count_reading / float(student_count) * 100

passing_math_reading_count = school_data_complete[(school_data_complete["math_score"] >= 70) 
                                                  & (school_data_complete["reading_score"] >= 70)].count()["student_name"]

overall_passing_rate = passing_math_reading_count /  float(student_count) * 100


# In[11]:


# Minor Data Cleanup
district_summary = pd.DataFrame({"Total Schools": [school_count], 
                                 "Total Students": [student_count], 
                                 "Total Budget": [total_budget],
                                 "Average Math Score": [average_math_score], 
                                 "Average Reading Score": [average_reading_score],
                                 "% Passing Math": [passing_math_percentage],
                                 "% Passing Reading": [passing_reading_percentage],
                                 "% Overall Passing": [overall_passing_rate]})

district_summary = district_summary[["Total Schools", "Total Students", "Total Budget",
                                     "Average Math Score", 
                                     "Average Reading Score",
                                     "% Passing Math",
                                     "% Passing Reading",
                                     "% Overall Passing"]]

# Formatting
district_summary["Total Students"] = district_summary["Total Students"].map("{:,}".format)
district_summary["Total Budget"] = district_summary["Total Budget"].map("${:,.2f}".format)

# Display the DataFrame
district_summary


# ## School Summary

# In[12]:


# Determine the School Type
school_types = school_data.set_index(["school_name"])["type"]
# Calculate the total student count
per_school_counts = school_data_complete["school_name"].value_counts()

# Calculate the total school budget and per capita spending
# per_school_budget = school_data_complete.groupby(["school_name"]).mean()["budget"]
per_school_budget = school_data_complete.groupby(["school_name"]).mean()["budget"]
per_school_capita = per_school_budget / per_school_counts

# Calculate the average test scores
per_school_math = school_data_complete.groupby(["school_name"]).mean()["math_score"]
per_school_reading = school_data_complete.groupby(["school_name"]).mean()["reading_score"
                                                                         ]


# In[14]:


# Get the students who passed math and passed reading by creating separate filtered DataFrames.
school_passing_math = school_data_complete[(school_data_complete["math_score"] >= 70)]
school_passing_reading = school_data_complete[(school_data_complete["reading_score"] >= 70)]
# Get the the students who passed both reading and math in a separate DataFrame.
passing_math_and_reading= school_data_complete[(school_data_complete["reading_score"]>=70)
                                              & (school_data_complete["math_score"]>=70)]


# In[15]:


#  Calculate the Percentage Pass Rates
per_school_passing_math = school_passing_math.groupby(["school_name"]).count()["student_name"] / per_school_counts * 100

per_school_passing_reading = school_passing_reading.groupby(["school_name"]).count()["student_name"] / per_school_counts * 100

overall_passing_rate = passing_math_and_reading.groupby(["school_name"]).count()["student_name"] / per_school_counts * 100


# In[16]:


# Convert to DataFrame
per_school_summary = pd.DataFrame({"School Type": school_types,
                                   "Total Students": per_school_counts,
                                   "Total School Budget": per_school_budget,
                                   "Per Student Budget": per_school_capita,
                                   "Average Math Score": per_school_math,
                                   "Average Reading Score": per_school_reading,
                                   "% Passing Math": per_school_passing_math,
                                   "% Passing Reading": per_school_passing_reading,
                                   "% Overall Passing": overall_passing_rate})

# Minor data wrangling
per_school_summary = per_school_summary[["School Type", "Total Students", "Total School Budget", "Per Student Budget",
                                         "Average Math Score", "Average Reading Score", 
                                         "% Passing Math", "% Passing Reading", 
                                         "% Overall Passing"]]
per_school_summary["Total School Budget"] = per_school_summary["Total School Budget"].map("${:,.2f}".format)
per_school_summary["Per Student Budget"] = per_school_summary["Per Student Budget"].map("${:,.2f}".format)
# Display the DataFrame
per_school_summary


# ## Top Performing Schools (By % Overall Passing)

# In[17]:


# Sort and show top five schools
top_schools = per_school_summary.sort_values(["% Overall Passing"], ascending=False)
top_schools.head(5)


# ## Bottom Performing Schools (By % Overall Passing)

# In[18]:


# Sort and show bottom five schools
bottom_schools = per_school_summary.sort_values(["% Overall Passing"], ascending=True)
bottom_schools.head(5)


# ## Math Scores by Grade

# In[12]:


# Create data series of scores by grade levels using conditionals

# Group each by school name

# Combine series into single DataFrame

# Minor data wrangling

# Display the DataFrame
scores_by_grade


# ## Reading Score by Grade 

# In[13]:


# Create data series of scores by grade levels using conditionals

# Group each by school name

# Combine series into single DataFrame

# Minor data wrangling

# Display the DataFrame
scores_by_grade


# ## Scores by School Spending

# In[14]:


# Establish the bins 


# In[15]:


# Create a copy of the school summary since it has the "Per Student Budget" 
#  This step can be skip but its best to make a copy. 
school_spending_df = per_school_summary


# In[16]:


# Categorize spending based on the bins.

school_spending_df


# In[17]:


#  Calculate averages for the desired columns. 


# In[18]:


# Assemble into DataFrame


# Minor data wrangling


# Display results
spending_summary


# ## Scores by School Size

# In[19]:


# Establish the bins.
size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]


# In[20]:


# Categorize the spending based on the bins

per_school_summary


# In[21]:


# Calculate averages for the desired columns. 


# In[22]:


# Assemble into DataFrame

# Minor data wrangling

# Display results
size_summary


# ## Scores by School Type

# In[23]:


#  Create new series using groupby for"
# Type | Average Math Score | Average Reading Score | % Passing Math | % Passing Reading | % Overall Passing


# In[24]:


# Assemble into DataFrame


# Minor data wrangling


# Display results
type_summary


# In[ ]:




