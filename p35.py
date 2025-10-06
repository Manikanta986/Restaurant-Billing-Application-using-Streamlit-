# Restaurant Billing Application using Streamlit!
import streamlit as st
import datetime
import csv
import os

st.title("🍽️ Welcome to Golden Restaurant")

# --- Initialize session state ---
if "Bill" not in st.session_state:
    st.session_state.Bill = {}
if "order_finished" not in st.session_state:
    st.session_state.order_finished = False
if "Tip" not in st.session_state:
    st.session_state.Tip = 0
if "Rating" not in st.session_state:
    st.session_state.Rating = None
if "order_saved" not in st.session_state:
    st.session_state.order_saved = False
if "step" not in st.session_state:
    st.session_state.step = 1
if "payment_mode" not in st.session_state:
    st.session_state.payment_mode = None
if "table_confirmed" not in st.session_state:
    st.session_state.table_confirmed = False  # New flag to confirm table

def reset_app():
    """Reset session state to start new order."""
    st.session_state.Bill = {}
    st.session_state.order_finished = False
    st.session_state.Tip = 0
    st.session_state.Rating = None
    st.session_state.order_saved = False
    st.session_state.payment_mode = None
    st.session_state.step = 1
    st.session_state.table_confirmed = False
    st.success("✅ App reset. You can start a new order now.")

# --- Step 1: Customer Details ---
if st.session_state.step == 1:
    Customers_name = st.text_input("Enter Customer Name:")
    Customer_number = st.text_input("Enter Mobile Number:")

    if st.button("Next ➡️"):
        if not Customers_name or not Customer_number:
            st.warning("Please fill all details.")
        elif not Customer_number.isdigit() or len(Customer_number) != 10:
            st.warning("Invalid Mobile Number! Enter 10 digits.")
        else:
            st.session_state.Customers_name = Customers_name
            st.session_state.Customer_number = Customer_number
            st.session_state.step = 2

# --- Step 2: Dining Option ---
elif st.session_state.step == 2:
    dining_option = st.radio("Choose your option:", ("Dine-in", "Takeaway"))
    st.session_state.dining_option = dining_option

    if dining_option == "Dine-in":
        num_persons = st.number_input("Enter number of persons (1-10):", min_value=1, max_value=10)
        # Assign table based on number of persons
        if num_persons <= 2:
            table_number = 1
        elif num_persons <= 5:
            table_number = 2
        else:
            table_number = 3
        st.session_state.table_number = table_number
        st.info(f"Assigned Table: {table_number}")

        # Show OK button to confirm table
        if st.button("✅ OK"):
            st.session_state.table_confirmed = True
            st.success(f"Table {table_number} confirmed!")
            st.session_state.step = 3  # Move to next step only after confirmation

    else:  # Takeaway option
        if st.button("Next ➡️"):
            st.session_state.step = 3

# --- Step 3: Menu Selection ---
elif st.session_state.step == 3:
    Menus = {
        "Veg": {"Paneer Biryani": 160, "Mushroom Biryani": 170, "Cashew Biryani": 150, "Vegetable Biryani": 180},
        "Non-veg": {"Chicken Biryani": 150, "Hyderabadi Special Biryani": 200, "Frypeice Biryani": 180, "Mutton Biryani": 190, "Fish Biryani": 220},
        "Desserts": {"Double ka Meetha": 60, "Gajar ka Halva": 55, "Gulabjamun": 30, "Rasmalai": 60, "Burfi": 70}
    }

    category = st.selectbox("Select Category:", list(Menus.keys()))
    items_with_price = [f"{item} - ₹{price}" for item, price in Menus[category].items()]
    selected_item = st.selectbox(f"Select item from {category.capitalize()} menu:", items_with_price)

    item_choice = selected_item.split(" - ")[0]
    item_price = Menus[category][item_choice]
    quantity = st.number_input(f"Enter quantity for {item_choice}:", min_value=1, value=1)

    if st.button("Add Item"):
        if item_choice in st.session_state.Bill:
            st.session_state.Bill[item_choice] += quantity
        else:
            st.session_state.Bill[item_choice] = quantity
        st.success(f"{quantity} x {item_choice} (₹{item_price}) added to your order!")

    if st.button("Finish Order ➡️"):
        if not st.session_state.Bill:
            st.warning("Add at least one item to finish the order!")
        else:
            st.session_state.step = 3.5  # go to confirmation step

# --- Step 3.5: Order Confirmation ---
elif st.session_state.step == 3.5:
    st.header("Confirm Your Order")
    Bill = st.session_state.Bill
    if not Bill:
        st.warning("No items in the order! Go back to add items.")
        if st.button("⬅️ Back to Menu"):
            st.session_state.step = 3
    else:
        total = 0
        prices = {
            **{"Paneer Biryani": 160, "Mushroom Biryani": 170, "Cashew Biryani": 150, "Vegetable Biryani": 180},
            **{"Chicken Biryani": 150, "Hyderabadi Special Biryani": 200, "Frypeice Biryani": 180, "Mutton Biryani": 190, "Fish Biryani": 220},
            **{"Double ka Meetha": 60, "Gajar ka Halva": 55, "Gulabjamun": 30, "Rasmalai": 60, "Burfi": 70}
        }

        for item, qty in Bill.items():
            subtotal = prices[item] * qty
            total += subtotal
            st.write(f"{item}: {qty} x ₹{prices[item]} = ₹{subtotal}")

        st.write(f"**Subtotal:** ₹{total}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirm Order"):
                st.session_state.step = 4
                st.session_state.order_finished = True
        with col2:
            if st.button("⬅️ Edit Order"):
                st.session_state.step = 3

# --- Step 4: Bill Display & Payment ---
elif st.session_state.step == 4 and st.session_state.order_finished:
    Bill = st.session_state.Bill
    st.write("---")
    st.header("Your Bill")

    total = 0
    now = datetime.datetime.now()
    date_time = now.strftime("%d-%m-%Y %I:%M:%S %p")
    st.write(f"**Date & Time:** {date_time}")
    st.write(f"**Customer Name:** {st.session_state.Customers_name}")
    st.write(f"**Mobile Number:** {st.session_state.Customer_number}")
    if st.session_state.dining_option == "Dine-in":
        st.write(f"**Table Number:** {st.session_state.table_number}")

    prices = {
        **{"Paneer Biryani": 160, "Mushroom Biryani": 170, "Cashew Biryani": 150, "Vegetable Biryani": 180},
        **{"Chicken Biryani": 150, "Hyderabadi Special Biryani": 200, "Frypeice Biryani": 180, "Mutton Biryani": 190, "Fish Biryani": 220},
        **{"Double ka Meetha": 60, "Gajar ka Halva": 55, "Gulabjamun": 30, "Rasmalai": 60, "Burfi": 70}
    }

    for item, qty in Bill.items():
        subtotal = prices[item] * qty
        total += subtotal
        st.write(f"{item}: {qty} x ₹{prices[item]} = ₹{subtotal}")

    st.write(f"**Subtotal:** ₹{total}")

    gst = total * 0.05 if total >= 600 else 0
    if gst > 0:
        st.write(f"**GST (5%):** ₹{gst:.2f}")

    total1 = total + gst
    discount = total1 * 0.10 if total1 >= 1000 else 0
    if discount > 0:
        st.write(f"**Discount (10%):** -₹{discount:.2f}")

    if st.session_state.dining_option == "Dine-in":
        tip = st.number_input("Enter Tip Amount (₹):", min_value=0, value=st.session_state.Tip)
        st.session_state.Tip = tip
    else:
        st.session_state.Tip = 0

    final_amount = total + gst + st.session_state.Tip - discount
    st.write(f"**Final Bill: ₹{final_amount}**")

    # --- Payment Mode ---
    st.subheader("Payment Mode")
    st.session_state.payment_mode = st.selectbox("Select Payment Mode:", ["Cash", "UPI", "Card"])

    # --- Feedback / Rating ---
    st.subheader("Feedback / Rating")
    st.session_state.Rating = st.radio(
        "Please rate your experience:",
        options=[1, 2, 3, 4, 5],
        index=None,
        horizontal=True
    )

    if st.button("💾 Save Order"):
        order_details = "; ".join([f"{item}({qty})" for item, qty in Bill.items()])
        file_name = "customers_orders.csv"
        if not os.path.exists(file_name):
            with open(file_name, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Date & Time", "Name", "Mobile", "Items", "Subtotal", "Final Bill", "Tip", "Rating", "Payment Mode"])
        with open(file_name, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                date_time,
                st.session_state.Customers_name,
                st.session_state.Customer_number,
                order_details,
                total,
                final_amount,
                st.session_state.Tip,
                st.session_state.Rating,
                st.session_state.payment_mode
            ])
        st.session_state.order_saved = True
        st.success(f" Customer details saved to customers_orders.csv (Payment: {st.session_state.payment_mode})")

    st.markdown("## Thank you for visiting Golden Restaurant!")
    if st.button(" Done / Next Customer"):
        reset_app()
