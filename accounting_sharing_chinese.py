def profit_sharing_system():
    print("=" * 50)
    print("利潤分帳系統")
    print("=" * 50)
    
    # 輸入基本資訊
    try:
        revenue = float(input("請輸入營業額: "))
        cost = float(input("請輸入成本: "))
        num_people = int(input("請輸入拆帳人數: "))
        
        # 計算利潤
        profit = revenue - cost
        
        if profit <= 0:
            print(f"\n利潤為 {profit}，沒有利潤可分帳。")
            return
        
        print(f"\n營業額: {revenue}")
        print(f"成本: {cost}")
        print(f"利潤: {profit}")
        print(f"拆帳人數: {num_people}")
        
        # 輸入參與分帳的人名
        people = []
        for i in range(num_people):
            name = input(f"\n請輸入第 {i+1} 個人的名稱: ").strip()
            if not name:
                name = f"人員{i+1}"
            people.append(name)
        
        # 輸入分帳比例
        print(f"\n請為以下人員輸入分帳比例（總和應為100%）：")
        
        percentages = []
        total_percentage = 0
        
        for i, person in enumerate(people):
            while True:
                try:
                    percentage = float(input(f"{person} 的分帳比例 (%): "))
                    if percentage < 0:
                        print("比例不能為負數，請重新輸入。")
                        continue
                    
                    percentages.append(percentage)
                    total_percentage += percentage
                    break
                except ValueError:
                    print("請輸入有效的數字。")
        
        # 檢查比例總和是否為100%
        if abs(total_percentage - 100) > 0.01:  # 允許微小誤差
            print(f"\n注意：分帳比例總和為 {total_percentage}%，不等於100%。")
            adjust_choice = input("是否要自動調整比例為100%？(y/n): ").lower()
            
            if adjust_choice == 'y':
                # 按比例調整
                if total_percentage > 0:
                    adjustment_factor = 100 / total_percentage
                    percentages = [p * adjustment_factor for p in percentages]
                    total_percentage = 100
                    print("比例已自動調整。")
                else:
                    print("錯誤：總比例為0，無法調整。")
                    return
            else:
                print("請重新執行並輸入正確的比例。")
                return
        
        # 計算分帳結果
        print("\n" + "=" * 50)
        print("分帳結果")
        print("=" * 50)
        
        sharing_results = []
        for i, (person, percentage) in enumerate(zip(people, percentages)):
            share_amount = profit * (percentage / 100)
            sharing_results.append({
                "name": person,
                "percentage": percentage,
                "amount": share_amount
            })
        
        # 顯示分帳結果
        print(f"總利潤: {profit:.2f}")
        print("-" * 50)
        
        total_allocated = 0
        for i, result in enumerate(sharing_results):
            print(f"{i+1}. {result['name']}:")
            print(f"   分帳比例: {result['percentage']:.2f}%")
            print(f"   分帳金額: {result['amount']:.2f}")
            total_allocated += result['amount']
        
        print("-" * 50)
        print(f"已分配總額: {total_allocated:.2f}")
        
        # 檢查是否有剩餘利潤（由於四捨五入可能產生微小差異）
        remaining = profit - total_allocated
        if abs(remaining) > 0.01:
            print(f"未分配金額（四捨五入差異）: {remaining:.2f}")
        
        # 可選：保存結果到檔案
        save_choice = input("\n是否要將分帳結果保存到檔案？(y/n): ").lower()
        if save_choice == 'y':
            save_to_file(revenue, cost, profit, sharing_results)
            print("結果已保存到 profit_sharing_results.txt")
    
    except ValueError:
        print("輸入錯誤，請確保輸入的是有效數字。")
    except Exception as e:
        print(f"發生錯誤: {e}")

def save_to_file(revenue, cost, profit, sharing_results):
    """將分帳結果保存到檔案"""
    with open("profit_sharing_results.txt", "w", encoding="utf-8") as f:
        f.write("=" * 50 + "\n")
        f.write("利潤分帳結果\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"營業額: {revenue:.2f}\n")
        f.write(f"成本: {cost:.2f}\n")
        f.write(f"利潤: {profit:.2f}\n")
        f.write(f"參與分帳人數: {len(sharing_results)}\n\n")
        f.write("分帳詳情:\n")
        f.write("-" * 50 + "\n")
        
        for i, result in enumerate(sharing_results):
            f.write(f"{i+1}. {result['name']}:\n")
            f.write(f"   分帳比例: {result['percentage']:.2f}%\n")
            f.write(f"   分帳金額: {result['amount']:.2f}\n")
        
        f.write("-" * 50 + "\n")
        total_allocated = sum(result['amount'] for result in sharing_results)
        f.write(f"已分配總額: {total_allocated:.2f}\n")
        remaining = profit - total_allocated
        if abs(remaining) > 0.01:
            f.write(f"未分配金額（四捨五入差異）: {remaining:.2f}\n")
        
        f.write(f"\n記錄時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

if __name__ == "__main__":
    from datetime import datetime
    profit_sharing_system()
