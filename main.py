import os
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


FLIGHTS = [
    {"flight_no": "PK301", "departure": "Karachi", "arrival": "Islamabad", "time": "08:00 AM", "price": 15000},
    {"flight_no": "PK302", "departure": "Karachi", "arrival": "Lahore", "time": "02:00 AM", "price": 16500},
    {"flight_no": "PK303", "departure": "Karachi", "arrival": "Dubai", "time": "06:00 AM", "price": 78000},
    {"flight_no": "PK304", "departure": "Lahore", "arrival": "Islamabad", "time": "06:00 PM", "price": 16000},
    {"flight_no": "PK305", "departure": "Lahore", "arrival": "Karachi", "time": "07:00 PM", "price": 19000},
    {"flight_no": "PK306", "departure": "Lahore", "arrival": "Dubai", "time": "12:10 PM", "price": 86000},
    {"flight_no": "PK307", "departure": "Islamabad", "arrival": "Lahore", "time": "11:00 PM", "price": 16000},
    {"flight_no": "PK308", "departure": "Islamabad", "arrival": "Karachi", "time": "09:00 AM", "price": 19000},
    {"flight_no": "PK309", "departure": "Islamabad", "arrival": "Dubai", "time": "08:00 PM", "price": 96000},
    {"flight_no": "PK310", "departure": "Dubai", "arrival": "Karachi", "time": "10:00 PM", "price": 116000},
    {"flight_no": "PK311", "departure": "Dubai", "arrival": "Lahore", "time": "09:00 PM", "price": 110000},
    {"flight_no": "PK312", "departure": "Dubai", "arrival": "Islamabad", "time": "07:00 AM", "price": 118000},
]


def get_flights(departure, arrival):
    return [f for f in FLIGHTS if f["departure"].lower() == departure.lower() and f["arrival"].lower() == arrival.lower()]


def ai_summarize_flights(flights):
    flight_descriptions = "\n".join(
        [f'{f["flight_no"]}: {f["time"]} - Rs {f["price"]}' for f in flights]
    )
    prompt = f"""
    Here are the available flights:\n{flight_descriptions}
    Summarize these options briefly for a customer booking from a travel app.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return None


def main():
    st.set_page_config(page_title="Flight Booking AI Agent", page_icon="🛫")
    st.title("✈️ AI Flight Booking Assistant")

  
    with st.form("flight_form"):
        departure = st.text_input("Enter Departure City", "Karachi")
        arrival = st.text_input("Enter Arrival City", "Islamabad")
        date = st.date_input("Travel Date")
        submitted = st.form_submit_button("Search Flights")

    if submitted:
        flights = get_flights(departure, arrival)

        if not flights:
            st.error("❌ No flights found for the given route.")
            return

        st.subheader("Available Flights")
        summary = ai_summarize_flights(flights)
        if summary:
            st.markdown(summary)
        else:
            st.warning("⚠️ AI summarization unavailable. Showing raw list:")
            for f in flights:
                st.write(f"{f['flight_no']} - {f['time']} - Rs {f['price']}")

        flight_options = [f"{f['flight_no']} - {f['time']} - Rs {f['price']}" for f in flights]
        selected_flight = st.selectbox("Select a flight to book", flight_options)
        num_tickets = st.number_input("Number of tickets", min_value=1, max_value=10, step=1)

       
        if st.button("Continue to Booking"):
            st.subheader("Passenger Details")
            with st.form("passenger_form"):
                name = st.text_input("Full Name")
                email = st.text_input("Email")
                phone = st.text_input("Phone Number")
                confirm = st.form_submit_button("Confirm Booking")

            if confirm:
                st.success("🎉 Booking Confirmed!")
                st.markdown(f"""
                **Flight:** {selected_flight}  
                **Passenger:** {name}  
                **Tickets:** {num_tickets}  
                📧 A confirmation email has been sent to **{email}**
                """)


if __name__ == "__main__":
    main()
