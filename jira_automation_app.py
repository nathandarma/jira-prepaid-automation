import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def create_story_ticket(name, description, labels, due_date, team):
    ticket = {
        "Name": name,
        "Description": description,
        "Labels": labels,
        "Due Date": due_date,
        "Team": team,
    }
    return ticket

def generate_csv(epic_name, overview, go_live_date, end_date, epic_link):
    # Convert dates to the format expected by Jira (dd/MMM/yy h:mm a)
    go_live_date_str = go_live_date.strftime("%d/%b/%y %I:%M %p")
    end_date_str = end_date.strftime("%d/%b/%y %I:%M %p")

    # Mapping of team names to team IDs
    team_id_mapping = {
        "DIGITAL Partner Agency Model": "7944",
        "DIGITAL AEM Specialists": "4550",
        "DIGITAL Agora Shop and Robotics": "3741",
        "DIGITAL Search": "4577",
    }

    # Create Story tickets
    tickets = [
        create_story_ticket("Offer | " + epic_name, overview, "Trading", go_live_date_str, "DIGITAL Partner Agency Model"),
        create_story_ticket("Copy | " + epic_name, overview, "Trading", (go_live_date - timedelta(weeks=4)).strftime("%d/%b/%y %I:%M %p"), "DIGITAL Partner Agency Model"),
        create_story_ticket("VD | " + epic_name, overview, "Trading", (go_live_date - timedelta(weeks=4)).strftime("%d/%b/%y %I:%M %p"), "DIGITAL Partner Agency Model"),
        create_story_ticket("Legal | " + epic_name, overview, "Trading", (go_live_date - timedelta(weeks=2)).strftime("%d/%b/%y %I:%M %p"), "DIGITAL Partner Agency Model"),
        create_story_ticket("AEM | " + epic_name, overview, ["Trading", "Not-Ready"], (go_live_date - timedelta(days=3)).strftime("%d/%b/%y %I:%M %p"), "DIGITAL AEM Specialists"),
        create_story_ticket("AEM Removal | " + epic_name, overview, ["Trading", "Not-Ready"], end_date_str, "DIGITAL AEM Specialists"),
        create_story_ticket("Agora | " + epic_name, overview + "\nRemember to complete and attach Agora config form: https://swimplify.co/projects/telstra/telstra-promos-form/", ["Trading", "AgoraGTM"], (go_live_date - timedelta(days=3)).strftime("%d/%b/%y %I:%M %p"), "DIGITAL Agora Shop and Robotics"),
        create_story_ticket("T+ | " + epic_name, overview + "\nRemember to engage BOH via https://confluence.tools.telstra.com/display/CSB/02.+Engagement+Form", ["Trading", "AgoraGTM", "Loyalty"], (go_live_date - timedelta(days=3)).strftime("%d/%b/%y %I:%M %p"), "DIGITAL Agora Shop and Robotics"),
        create_story_ticket("SEO | " + epic_name, overview, ["Trading", "SEO"], (go_live_date - timedelta(days=3)).strftime("%d/%b/%y %I:%M %p"), "DIGITAL Search"),
        create_story_ticket("SEM | " + epic_name, overview, ["Trading", "SEM"], (go_live_date - timedelta(days=3)).strftime("%d/%b/%y %I:%M %p"), "DIGITAL Search"),
        create_story_ticket("Pre-Release Review | " + epic_name, overview, "Trading", (go_live_date - timedelta(days=2)).strftime("%d/%b/%y %I:%M %p"), "DIGITAL Partner Agency Model"),
    ]

    df = pd.DataFrame(tickets)
    df["Issue Type"] = "Story"  # Add "Issue Type" column and assign "Story" to all entries
    df["Epic Link"] = epic_link
    df = df.rename(columns={"Name": "Summary", "Team": "Team ID"})  # Rename columns
    csv_content = df.to_csv(index=False)

    csv_file_name = f"{epic_name.replace(' ', '_')}.csv"  # Remove spaces and use as the file name

    with open(csv_file_name, "w") as csv_file:
        csv_file.write(csv_content)

    return csv_file_name

def main():
    st.title("Batch Creation of Pre-Paid Trading Tickets")

    # Prompt user for input
    product = st.text_input("Product")
    offer = st.text_input("Offer")
    overview = st.text_area("Overview", type='default')
    go_live_date = st.date_input("Go-Live Date")
    end_date = st.date_input("End Date")
    epic_link = st.text_input("Epic Link (DCAEG code)")

    # Button to trigger actions
    if st.button("Submit"):
        epic_name = f"Offer | Pre-Paid | {product} - {offer} | {go_live_date.strftime('%d %b %y')} - {end_date.strftime('%d %b %y')}"
        epic_name = epic_name.replace("/", "-")  # Replace '/' with '-' in the date part
        epic_name = epic_name.replace(" ", "_")  # Replace spaces with '_' in the epic name

        # Create Epic and Story tickets
        epic_csv = generate_csv(epic_name, overview, go_live_date, end_date, epic_link)

        # Display download section
        st.subheader("Click to Download")
        st.markdown(f"Download your CSV file [here](sandbox:/mnt/data/{epic_csv})", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
