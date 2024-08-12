import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the CSV file path
csv_file = 'work_data.csv'

# Initialize the CSV file with headers if it doesn't exist
if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=["Date", "Project Name", "Hours Worked", "Work Details", "Extra Remarks"])
    df.to_csv(csv_file, index=False)

# Set the page title
st.set_page_config(page_title="Daily Work Log", page_icon=":calendar:")
# Streamlit App
st.title("Work Log Entry")

# State variables to reset form inputs
if 'submitted' not in st.session_state:
    st.session_state.submitted = False


# Input Fields
with st.form("work_form"):
    date = st.date_input("Date")
    project_name = st.text_input("Project Name")
    hours_worked = st.number_input("Hours Worked", min_value=0.0, format="%.2f")
    work_details = st.text_area("Work Details")
    extra_remarks = st.text_area("Extra Remarks (Optional)")
    
    # Save button
    submitted = st.form_submit_button("Save")
    
    if submitted:
        # Append the data to CSV
        new_data = pd.DataFrame({
            "Date": [date],
            "Project Name": [project_name],
            "Hours Worked": [hours_worked],
            "Work Details": [work_details],
            "Extra Remarks": [extra_remarks],
        })
        df = pd.read_csv(csv_file)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(csv_file, index=False)
        st.success("Data saved successfully!")
        
        # Reset input fields by clearing the session state
        st.session_state.submitted = True
        st.session_state.date = None
        st.session_state.project_name = ""
        st.session_state.hours_worked = 0.0
        st.session_state.work_details = ""
        st.session_state.extra_remarks = ""

# Display the saved data
st.subheader("Daily Work Log")
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
    
    if not df.empty:
 
        # Sort the data by the Date column in ascending order
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values(by='Date', ascending=True)
        
        #Display the data in a table
        edited_df = st.data_editor(df, use_container_width=True)
        
        if st.button("Update Data"):
            edited_df.to_csv(csv_file, index=False)
            st.success("Data updated successfully!")

        # Graph #1
        # Plotting the graph to show the total time spent on each project
        st.subheader("Total Time Spent on Each Project")
        project_time = df.groupby("Project Name")["Hours Worked"].sum()
        
        if not project_time.empty:
            fig, ax = plt.subplots()
            project_time.plot(kind='barh', ax=ax)
            ax.set_xlabel("Hours Worked")
            ax.set_ylabel("Projects")
            ax.set_title("Total Time Spent on Each Project")
            
            # Add total value on top of each bar
            for index, value in enumerate(project_time):
                ax.text(value, index, f'{value:.2f}', va='center')
            
            st.pyplot(fig)
        else:
            st.write("No project data available to display the graph.")
        
        # Graph #2    
        # Plotting the graph to show the total time spent on each day
        st.subheader("Total Time Spent on Each Day")
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d-%m-%Y')  # Format dates to dd-mm-YYYY
        day_time = df.groupby("Date")["Hours Worked"].sum()
        
        if not day_time.empty:
            fig, ax = plt.subplots()
            day_time.plot(kind='barh', ax=ax)
            ax.set_xlabel("Hours Worked")
            ax.set_ylabel("Date")
            ax.set_title("Total Time Spent on Each Day")
            
            # Add total value on top of each bar
            for index, value in enumerate(day_time):
                ax.text(value, index, f'{value:.2f}', va='center')
            st.pyplot(fig)
            
        else:
            st.write("No data available to display the graph.")
            
        # Graph #3
        # Plotting the graph to show the total time spent on each project on each day
        st.subheader("Total Time Spent on Each Project on Each Day")
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d-%m-%Y')  # Format dates to dd-mm-YYYY
        project_day_time = df.groupby(["Date", "Project Name"])["Hours Worked"].sum().unstack()
        
        if not project_day_time.empty:
            fig, ax = plt.subplots()
            project_day_time.plot(kind='barh', stacked=True, ax=ax)  # Create a stacked bar chart
            ax.set_xlabel("Hours Worked")
            ax.set_ylabel("Date")
            ax.set_title("Total Time Spent on Each Project on Each Day")
            st.pyplot(fig)
            
        else:
            st.write("No data available to display the graph.")
            
        
        # Graph #4
        # Plotting the graph to show the date & hours of a specific project 
        st.subheader("Filter Projects")
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d-%m-%Y')  # Format dates to dd-mm-YYYY
        project_names = df['Project Name'].unique().tolist()
        selected_project = st.selectbox("Select Project", project_names)     
        # st.write("Selected Project:", selected_project)
        
        filtered_df = df[df['Project Name'] == selected_project]
        
        st.write(filtered_df)
        # if not filtered_df.empty:
        #     # Set the Date column as the index
        #     filtered_df.set_index('Date', inplace=True)
            
        #     # Plot the graph
        #     fig, ax = plt.subplots()
        #     bars = filtered_df['Hours Worked'].plot(kind='bar', ax=ax)
            
        #     ax.set_xlabel("Date")
        #     ax.set_ylabel("Hours Worked")
        #     ax.set_title(f"Total Hours Worked on {selected_project}")
        #     ax.set_xticklabels(filtered_df.index, rotation=45)  # Rotate date labels for better visibility
            
        #     # Add total value on top of each bar
        #     for bar in bars.patches:
        #         ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{bar.get_height():.2f}', ha='center', va='bottom')
            
        #     st.pyplot(fig)
        # else:
        #     st.write("No data available to display the graph.")
        
        if not filtered_df.empty:
            # Set the Date column as the index
            filtered_df.set_index('Date', inplace=True)
            
            # Plot the graph with dates on the y-axis and hours on the x-axis
            fig, ax = plt.subplots()
            bars = filtered_df['Hours Worked'].plot(kind='barh', ax=ax)
            
            ax.set_ylabel("Date")
            ax.set_xlabel("Hours Worked")
            ax.set_title(f"Total Hours Worked on {selected_project}")
            ax.set_yticklabels(filtered_df.index, rotation=0)  # Keep date labels horizontal
            
            # Add total value on top of each bar
            for bar in bars.patches:
                ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.2f}', ha='left', va='center')
            
            st.pyplot(fig)
        else:
            st.write("No data available to display the graph.")
    else:
        st.write("No data available. Please add some entries.")
