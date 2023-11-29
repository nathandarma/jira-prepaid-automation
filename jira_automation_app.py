import streamlit as st
import pandas as pd

def create_epic_name(product, offer, go_live_date, end_date):
    epic_name = f"Offer | Pre-Paid | {product} - {offer} | {go_live_date} - {end_date}"
    return epic_name

def create_story_ticket(name, overview, label, due_date, team, additional_info=None):
    ticket = {
        "Name": name,
        "Description": overview,
        "Label": label,
        "Due Date": due_date,
        "Team": team,
    }
    if additional_info:
        ticket.update(additional_info)
    return ticket

def generate_csv(epic_name, overview):
    tickets = [
        create_story_ticket("Offer | " + epic_name, overview, "Trading", go_live_date, "DIGITAL Partner Agency Model"),
        create_story_ticket("Copy | " + epic_name, overview, "Trading", go_live_date - pd.DateOffset(weeks=4), "DIGITAL Partner Agency Model"),
        # ... (similarly create other tickets)
    ]

    df = pd.DataFrame(tickets)
    csv_content = df.to_csv(index=False)

    with open("jira_bulk_upload.csv", "w") as csv_file:
        csv_file.write(csv_content)

def main():
    st.title("Jira Automation with Streamlit")

    product = st.text_input("Product")
    offer = st.text_input("Offer")
    overview = st.text_area("Overview")
    go_live_date = st.date_input("Go-Live Date")
    end_date = st.date_input("End Date")

    if st.button("Submit"):
        epic_name = create_epic_name(product, offer, go_live_date, end_date)
        generate_csv(epic_name, overview)
        st.success("CSV created successfully!")

    if st.button("Download"):
        st.markdown("### Download CSV")
        with open("jira_bulk_upload.csv", "rb") as file:
            st.download_button(label="Click to Download", data=file, key="download_button")

if __name__ == "__main__":
    main()
