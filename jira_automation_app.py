import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def create_story_ticket(name, overview, label, due_date, team, epic_link, additional_info=None):
    team_id_mapping = {
        "DIGITAL Partner Agency Model": "7944",
        "DIGITAL AEM Specialists": "4550",
        "DIGITAL Agora Shop and Robotics": "3741",
        "DIGITAL Search": "4577",
    }

    ticket = {
        "Summary": name,
        "Description": overview,
        "Label": label,
        "Due Date": due_date,
        "Team": {"id": team_id_mapping.get(team, ""), "name": team},  # Include both ID and name
        "Epic Link": epic_link,
    }
    if additional_info:
        ticket.update(additional_info)
    return ticket

def generate_csv(epic_name, overview, go_live_date, end_date, epic_link):
    # Convert dates to the format expected by Jira (yyyy-MM-dd)
    go_live_date_str = go_live_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Mapping of team names to team IDs
    team_id_mapping = {
        "DIGITAL Partner Agency Model": "7944",
        "DIGITAL AEM Specialists": "4550",
        "DIGITAL Agora Shop and Robotics": "3741",
        "DIGITAL Search": "4577",
    }

    tickets = [
        create_story_ticket("Offer | " + epic_name, overview, "Trading", go_live_date_str, "DIGITAL Partner Agency Model", epic_link, additional_info={"Team ID": team_id_mapping["DIGITAL Partner Agency Model"]}),
        create_story_ticket("Copy | " + epic_name, overview, "Trading", (go_live_date - pd.DateOffset(weeks=4)).strftime("%Y-%m-%d"), "DIGITAL Partner Agency Model", epic_link, additional_info={"Team ID": team_id_mapping["DIGITAL Partner Agency Model"]}),
        create_story_ticket("VD | " + epic_name, overview, "Trading", (go_live_date - pd.DateOffset(weeks=4)).strftime("%Y-%m-%d"), "DIGITAL Partner Agency Model", epic_link, additional_info={"Team ID": team_id_mapping["DIGITAL Partner Agency Model"]}),
        create_story_ticket("Legal | " + epic_name, overview, "Trading", (go_live_date - pd.DateOffset(weeks=2)).strftime("%Y-%m-%d"), "DIGITAL Partner Agency Model", epic_link, additional_info={"Team ID": team_id_mapping["DIGITAL Partner Agency Model"]}),
        create_story_ticket("AEM | " + epic_name, overview, "Trading", (go_live_date - pd.DateOffset(days=3)).strftime("%Y-%m-%d"), "DIGITAL AEM Specialists", epic_link, additional_info={"Label": ["Trading", "Not-Ready"], "Component": "T.com AEM Production", "Team ID": team_id_mapping["DIGITAL AEM Specialists"]}),
        create_story_ticket("AEM Removal | " + epic_name, overview, "Trading", end_date_str, "DIGITAL AEM Specialists", epic_link, additional_info={"Label": ["Trading", "Not-Ready"], "Component": "T.com AEM Production", "Team ID": team_id_mapping["DIGITAL AEM Specialists"]}),
        create_story_ticket("Agora | " + epic_name, overview + "\nRemember to complete and attach Agora config form: https://swimplify.co/projects/telstra/telstra-promos-form/", "Trading", (go_live_date - pd.DateOffset(days=3)).strftime("%Y-%m-%d"), "DIGITAL Agora Shop and Robotics", epic_link, additional_info={"Label": ["Trading", "AgoraGTM"], "Component": "Shop", "Team ID": team_id_mapping["DIGITAL Agora Shop and Robotics"]}),
        create_story_ticket("T+ | " + epic_name, overview + "\nRemember to engage BOH via https://confluence.tools.telstra.com/display/CSB/02.+Engagement+Form", "Trading", (go_live_date - pd.DateOffset(days=3)).strftime("%Y-%m-%d"), "DIGITAL Agora Shop and Robotics", epic_link, additional_info={"Label": ["Trading", "AgoraGTM", "Loyalty"], "Component": "Shop", "Team ID": team_id_mapping["DIGITAL Agora Shop and Robotics"]}),
        create_story_ticket("SEO | " + epic_name, overview, "Trading", (go_live_date - pd.DateOffset(days=3)).strftime("%Y-%m-%d"), "DIGITAL Search", epic_link, additional_info={"Label": ["Trading", "SEO"], "Component": "Search (SEO/SEM)", "Team ID": team_id_mapping["DIGITAL Search"]}),
        create_story_ticket("SEM | " + epic_name, overview, "Trading", (go_live_date - pd.DateOffset(days=3)).strftime("%Y-%m-%d"), "DIGITAL Search", epic_link, additional_info={"Label": ["Trading", "SEM"], "Component": "Search (SEO/SEM)", "Team ID": team_id_mapping["DIGITAL Search"]}),
        create_story_ticket("Pre-Release Review | " + epic_name, overview, "Trading", (go_live_date - pd.DateOffset(days=2)).strftime("%Y-%m-%d"), "DIGITAL Partner Agency Model", epic_link, additional_info={"Team ID": team_id_mapping["DIGITAL Partner Agency Model"]}),
    ]

    df = pd.DataFrame(tickets)
    df["Issue Type"] = "Story"  # Add "Issue Type" column and assign "Story" to all entries
    df = df.rename(columns={"Team": "Team Name", "Team ID": "Team"})
    csv_content = df.to_csv(index=False)

    csv_file_name = f"{epic_name.replace(' ', '_')}.csv"  # Remove spaces and use as the file name

    with open(csv_file_name, "w") as csv_file:
        csv_file.write(csv_content)

    return csv_file_name

def main():
    st.title("Batch Creation of Pre-Paid Trading Tickets")

    product = st.text_input("Product")
    offer = st.text_input("Offer")
    overview = st.text_area("Overview", height=100)
    go_live_date = st.date_input("Go-Live Date")
    end_date = st.date_input("End Date")
    epic_link = st.text_input("Epic Link (DCAEG code)")

    if st.button("Submit"):
        epic_name = f"Offer | Pre-Paid | {product} - {offer} | {go_live_date.strftime('%d %b %y')} - {end_date.strftime('%d %b %y')}"
        epic_csv = generate_csv(epic_name, overview, go_live_date, end_date, epic_link)
        st.markdown(f"### Click to Download\n[Download CSV]({epic_csv})")

if __name__ == "__main__":
    main()
