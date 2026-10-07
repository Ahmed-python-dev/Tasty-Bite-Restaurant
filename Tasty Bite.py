import json
restaurant_name = "Tasty Bite"
order_id = 1

def load_orders():
    try:
        with open("orders.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
orders = load_orders()
if orders:
    order_id = max(order[0] for order in orders) + 1
def save_orders():
    with open("orders.json", "w") as file:
        json.dump(orders, file)
print("Restaurant:" , restaurant_name)
print("---------------------------------------------")
menu= {"Burger":100,"pizza":150,"pasta":120,"chicken":180,"cola":30}

print("Welcome to" , restaurant_name)
def show_menu() :
    for item in menu:
        print(item, menu[item])
show_menu()
def calculate_total(order,menu):
    total = 0
    for item, quantity in order:
        total += menu[item] * quantity
    return total
def calculate_discount(total, discount_rate):
    discount = total * discount_rate
    return discount
def print_invoice(customer_name, phone, order_id, order, menu, discount, final_total):
    print("your order: ")
    print("customer: ", customer_name)
    print("phone: ", phone)
    print("order id: ", order_id)
    for item, quantity in order:
        print(item, "Quantity:", quantity, "Price:", menu[item], "Subtotal:", menu[item] * quantity)
    print("Discount:", discount)
    print("Final Total:", final_total)
def search_order(orders, search_id):
    found = False
    for order in orders:
        order_id, customer_name, phone, order_items, final_total = order
        if order_id == search_id:
            print("Order found")
            print("Customer:", customer_name)
            print("Phone:", phone)
            print("Final total:", final_total)
            found = True
            return
    if not found:
        print("Order not found")
def edit_order(orders, edit_id):
    for order in orders:
        order_id, customer_name, phone, order_items, final_total = order
        if order_id == edit_id:
            print("Order found")
            print("Order items:")
            for item, quantity in order_items:
                print(item, "Quantity:", quantity)
            edit_item = input("Enter item to edit: ")
            for menu_item in menu:
                if menu_item.lower() == edit_item.lower():
                    edit_item = menu_item
                    break
                
         
            if edit_item in menu:
                try:
                    new_quantity = int(input("Enter new quantity: "))
                    if new_quantity <= 0:
                        print("Quantity must be greater than 0")
                        return
                except ValueError:
                    print("Please enter a number")
                    return
                   
                    
                else:
                    for i, (item_name, quantity) in enumerate(order_items):
                        if item_name == edit_item:
                            order_items[i] = (item_name, new_quantity)
                            new_total = calculate_total(order_items, menu)
                            new_discount = calculate_discount(new_total, 0.10)
                            new_final_total = new_total - new_discount
                            orders[orders.index(order)] = (order_id, customer_name, phone, order_items, new_final_total)
                            save_orders()
                            print("Order updated")
                            print("New Final Total:", new_final_total)
                            print_invoice(customer_name, phone, order_id, order_items, menu,new_discount, new_final_total)
                            return
                            
                            
                           
                    print("Item not found in this order")
                    
            else:
                print("Item not found in menu")
                return
    print("Order not found")        
def delete_order(orders, delete_id):
    for order in orders:
        order_id, customer_name, phone, order_items, final_total = order
        if order_id == delete_id:
            orders.remove(order)
            save_orders()
            print("Order deleted")
            return
    print("Order not found")       
def calculate_daily_sales(orders):
    daily_sales = 0
    for order in orders:
        order_id, customer_name, phone, order_items, final_total = order
        daily_sales += final_total
    return daily_sales
def count_orders(orders):
    total_orders = 0
    for order in orders:
        total_orders += 1
    return total_orders
def calculate_item_sales(orders):
    item_sales = {}
    for order in orders:
        order_id, customer_name, phone, order_items, final_total = order
        for item, quantity in order_items:
            if item in item_sales:
                item_sales[item] += quantity
            else:
                item_sales[item] = quantity
    return item_sales
def get_most_sold_item(item_sales):
    if not item_sales:
        return None
    most_sold_item = max(item_sales, key=item_sales.get)
    
    return most_sold_item
def take_order():
    customer_name = input("enter your name : ")
    phone = input("enter phone: ")
    order = []
    more = "yes"
    while more == "yes":
        item = input("enter your order : ")
        for menu_item in menu:
            if menu_item.lower() == item.lower():
                item = menu_item
                break
        if item in menu:
            try:
                quantity = int(input("enter quantity: "))
                if quantity <= 0:
                    print("quantity must be greater than 0")
                    continue
                order.append((item, quantity))
            except ValueError:
                    
                continue
        else:
            print("Item not found")
        more = input("Do you want to add another item : ").lower()
   
    return customer_name, phone, order
def process_order(order, menu):
    total = calculate_total(order, menu)
    discount_rate = 0.10
    discount = calculate_discount(total, discount_rate)
    final_total = total - discount
    return total, discount, final_total
def main_menu():
    print("1. New Order")
    print("2. Search Order")
    print("3. Delete Order")
    print("4. Edit Order")
    print("5. Sales Report")
    print("6. Exit")
    choice = input("Choose an option: ")
    return choice    
def main():
    global order_id
    
    while True:
        choice = main_menu()
        if choice == "1":
            customer_name, phone, order = take_order()
            if not order:
                print("Order must contain at least one item")
                continue
            total, discount, final_total = process_order(order, menu)
            print_invoice(customer_name, phone, order_id, order, menu, discount, final_total)
            orders.append((order_id, customer_name, phone, order, final_total))
            save_orders()
            order_id += 1
        elif choice == "2":
            try:
                search_id = int(input("enter order id to search : "))
                search_order(orders, search_id)
            except ValueError:
                print("Please enter a number")
        elif choice == "3":
            try:
                delete_id = int(input("enter order id to delete : "))
                delete_order(orders, delete_id)
            except ValueError:
                print("Please enter a number")
        elif choice == "4":
            try:
                edit_id = int(input("enter order id to edit : "))
                edit_order(orders, edit_id)
            except ValueError:
                print("Please enter a number")
        elif choice == "5":
            daily_sales = calculate_daily_sales(orders)
            total_orders = count_orders(orders)
            item_sales = calculate_item_sales(orders)
            print("Daily Sales:", daily_sales)
            print("Total orders:", total_orders)
            most_sold_item = get_most_sold_item(item_sales)
            print("Most sold item:", most_sold_item)
            if most_sold_item:
                print("Quantity sold:", item_sales[most_sold_item])
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")                    
    
main()        

     
   