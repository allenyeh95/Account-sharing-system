from datetime import datetime

def profit_sharing_system():
    print("=" * 50)
    print("Profit Sharing System")
    print("=" * 50)
    
    # Input basic information
    try:
        revenue = float(input("Please enter total revenue: "))
        cost = float(input("Please enter total costs: "))
        num_people = int(input("Please enter number of participants: "))
        
        # Calculate profit
        profit = revenue - cost
        
        if profit <= 0:
            print(f"\nProfit is {profit}. There is no profit to distribute.")
            return
        
        print(f"\nRevenue: {revenue}")
        print(f"Cost: {cost}")
        print(f"Profit: {profit}")
        print(f"Number of participants: {num_people}")
        
        # Input names of participants
        people = []
        for i in range(num_people):
            name = input(f"\nEnter name for person {i+1}: ").strip()
            if not name:
                name = f"Person {i+1}"
            people.append(name)
        
        # Input sharing percentages
        print(f"\nPlease enter the sharing percentage for each person (Total should be 100%):")
        
        percentages = []
        total_percentage = 0
        
        for i, person in enumerate(people):
            while True:
                try:
                    percentage = float(input(f"Percentage for {person} (%): "))
                    if percentage < 0:
                        print("Percentage cannot be negative. Please try again.")
                        continue
                    
                    percentages.append(percentage)
                    total_percentage += percentage
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
        
        # Check if total is 100%
        if abs(total_percentage - 100) > 0.01:  # Allow for small rounding errors
            print(f"\nNotice: Total percentage is {total_percentage}%, which is not 100%.")
            adjust_choice = input("Would you like to auto-adjust percentages to 100%? (y/n): ").lower()
            
            if adjust_choice == 'y':
                # Pro-rata adjustment
                if total_percentage > 0:
                    adjustment_factor = 100 / total_percentage
                    percentages = [p * adjustment_factor for p in percentages]
                    total_percentage = 100
                    print("Percentages have been adjusted.")
                else:
                    print("Error: Total percentage is 0. Cannot adjust.")
                    return
            else:
                print("Please restart and enter the correct proportions.")
                return
        
        # Calculate results
        print("\n" + "=" * 50)
        print("Sharing Results")
        print("=" * 50)
        
        sharing_results = []
        for i, (person, percentage) in enumerate(zip(people, percentages)):
            share_amount = profit * (percentage / 100)
            sharing_results.append({
                "name": person,
                "percentage": percentage,
                "amount": share_amount
            })
        
        # Display results
        print(f"Total Profit: {profit:.2f}")
        print("-" * 50)
        
        total_allocated = 0
        for i, result in enumerate(sharing_results):
            print(f"{i+1}. {result['name']}:")
            print(f"   Share Percentage: {result['percentage']:.2f}%")
            print(f"   Share Amount: {result['amount']:.2f}")
            total_allocated += result['amount']
        
        print("-" * 50)
        print(f"Total Allocated: {total_allocated:.2f}")
        
        # Check for rounding differences
        remaining = profit - total_allocated
        if abs(remaining) > 0.01:
            print(f"Unallocated amount (rounding diff): {remaining:.2f}")
        
        # Optional: Save to file
        save_choice = input("\nWould you like to save the results to a file? (y/n): ").lower()
        if save_choice == 'y':
            save_to_file(revenue, cost, profit, sharing_results)
            print("Results saved to profit_sharing_results.txt")
    
    except ValueError:
        print("Input error: Please ensure you are entering valid numbers.")
    except Exception as e:
        print(f"An error occurred: {e}")

def save_to_file(revenue, cost, profit, sharing_results):
    """Saves the sharing results to a text file"""
    with open("profit_sharing_results.txt", "w", encoding="utf-8") as f:
        f.write("=" * 50 + "\n")
        f.write("Profit Sharing Results\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Revenue: {revenue:.2f}\n")
        f.write(f"Cost: {cost:.2f}\n")
        f.write(f"Total Profit: {profit:.2f}\n")
        f.write(f"Participants: {len(sharing_results)}\n\n")
        f.write("Breakdown:\n")
        f.write("-" * 50 + "\n")
        
        for i, result in enumerate(sharing_results):
            f.write(f"{i+1}. {result['name']}:\n")
            f.write(f"   Percentage: {result['percentage']:.2f}%\n")
            f.write(f"   Amount: {result['amount']:.2f}\n")
        
        f.write("-" * 50 + "\n")
        total_allocated = sum(result['amount'] for result in sharing_results)
        f.write(f"Total Allocated: {total_allocated:.2f}\n")
        remaining = profit - total_allocated
        if abs(remaining) > 0.01:
            f.write(f"Rounding Difference: {remaining:.2f}\n")
        
        f.write(f"\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

if __name__ == "__main__":
    profit_sharing_system()