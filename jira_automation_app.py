import streamlit as st
import pandas as pd

def create_epic_name(product, offer, go_live_date, end_date):
    epic_name = f"Offer | Pre-Paid | {product} - {offer} | {go_live_date.strftime('%d %b %y')} - {end_date.strftime('%d %b %y')}"
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

def generate_csv(epic_name, overview, go_live_date, end_date):
    tickets = [
        create_story_ticket("Offer | " + epic_name, overview, "Trading", go_live_date, "DIGITAL Partner Agency Model"),
        create_story_ticket("Copy | " + epic_name, overview, "Trading", go_live_date - pd.DateOffset(weeks=4), "DIGITAL Partner Agency Model"),
        create_story_ticket("VD | " + epic_name, overview, "Trading", go_live_date - pd.DateOffset(weeks=4), "DIGITAL Partner Agency Model"),
        create_story_ticket("Legal | " + epic_name, overview, "Trading", go_live_date - pd.DateOffset(weeks=2), "DIGITAL Partner Agency Model"),
        create_story_ticket("AEM | " + epic_name, overview, "Trading", go_live_date - pd.DateOffset(days=3), "DIGITAL AEM Specialists", additional_info={"Label": ["Trading", "Not-Ready"], "Component": "T.com AEM Production"}),
        create_story_ticket("AEM Removal | " + epic_name, overview, "Trading", end_date, "DIGITAL AEM Specialists", additional_info={"Label": ["Trading", "Not-Ready"], "Component": "T.com AEM Production"}),
        create_story_ticket("Agora | " + epic_name, overview + "\nRemember to complete and attach Agora config form: https://swimplify.co/projects/telstra/telstra-promos-form/", "Trading", go_live_date - pd.DateOffset(days=3), "DIGITAL Agora Shop and Robotics", additional_info={"Label": ["Trading", "AgoraGTM"], "Component": "Shop"}),
        create_story_ticket("T+ | " + epic_name, overview + "\nRemember to engage BOH via https://confluence.tools.telstra.com/display/CSB/02.+Engagement+Form", "Trading", go_live_date - pd.DateOffset(days=3), "DIGITAL Agora Shop and Robotics", additional_info={"Label": ["Trading", "AgoraGTM", "Loyalty"], "Component": "Shop"}),
        create_story_ticket("SEO | " + epic_name, overview, "Trading", go_live_date - pd.DateOffset(days=3), "DIGITAL Search", additional_info={"Label": ["Trading", "SEO"], "Component": "Search (SEO/SEM)"}),
        create_story_ticket("SEM | " + epic_name, overview, "Trading", go_live_date - pd.DateOffset(days=3), "DIGITAL Search", additional_info={"Label": ["Trading", "SEM"], "Component": "Search (SEO/SEM)"}),
        create_story_ticket("Pre-Release Review | " + epic_name, overview, "Trading", go_live_date - pd.DateOffset(days=2), "DIGITAL Partner Agency Model"),
    ]

    df = pd.DataFrame(tickets)
    csv_content = df.to_csv(index=False)

    csv_file_name = f"{epic_name.replace(' ', '_')}.csv"  # Remove spaces and use as the file name

    with open(csv_file_name, "w") as csv_file:
        csv_file.write(csv_content)

    return csv_file_name

def main():
    st.title("Batch Creation of Pre-Paid Trading Tickets")

    product = st.text_input("Product")
    offer = st.text_input("Offer")
    overview = st.text_input("Overview", type='textarea')
    go_live_date = st.date_input("Go-Live Date")
    end_date = st.date_input("End Date")

    submit_clicked = st.button("Submit")

    if submit_clicked:
        epic_name = create_epic_name(product, offer, go_live_date, end_date)
        csv_file_name = generate_csv(epic_name, overview, go_live_date, end_date)
        st.success("CSV created successfully!")

    if submit_clicked:
        # Display the "Download CSV" heading and button only if the "Submit" button has been clicked
        st.markdown("### Download CSV")
        with open(csv_file_name, "rb") as file:
            st.download_button(label="Click to Download", data=file, key="download_button", file_name=csv_file_name)

if __name__ == "__main__":
    main()
