from langchain_core.tools import tool

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ],
}

@tool
def search_flights(origin: str, destination: str ) -> str: 
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    #1. Tra cu thong tin FLITGHT_DB
    flights = FLIGHTS_DB.get((origin,destination), [])
    #2. Neu khong tra ve thi bao loi
    if not flights:
        return f'Không tìm thấy chuyến bay từ {origin} đến {destination}'

    #3. Format ket qua
    result = f'Danh sach chuyen bay tu {origin} den {destination}:\n'

    for f in flights:
        # Định dạng giá tiền có dấu chấm phân cách
        formatted_price = f"{f['price']:,}".replace(",", ".") + "đ"
        
        result += (f"- {f['airline']} | Khởi hành: {f['departure']} - Đến: {f['arrival']} "
                   f"| Hạng: {f['class']} | Giá: {formatted_price}\n")
    
    return result


@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    #1. Tra cuu hotel HOTEL_DB[city]
    hotels = HOTELS_DB.get(city, [])

    #Neu khong co thong tin
    if not hotels:
        return f'Không tìm thấy khách sạn tại {city}'
    
    #2. Loc theo max_price_per_night
    fillted_hotels = [ h for h in hotels if h['price_per_night'] <= max_price_per_night]

    if not fillted_hotels:
        formatted_max = f"{max_price_per_night:,}".replace(",", ".")
        return f"Không tìm thấy khách sạn tại {city} với giá dưới {formatted_max}đ/đêm. Hãy thử tăng ngân sách."
    
    #3. Xap xep theo rating giam dan
    sorted_hotels = sorted(fillted_hotels, key = lambda x : x['rating'], reverse=True)

    # 4. Format đẹp để trả về cho Agent
    result = f"Danh sách khách sạn tại {city} (Giá tối đa: {max_price_per_night:,}đ):\n".replace(",", ".")

    for h in sorted_hotels:
        price = f"{h['price_per_night']:,}".replace(",", ".")

        stars = "⭐" * h["stars"]
        
        result += (f"- {h['name']} ({stars}) | Khu vực: {h['area']} "
                   f"| Giá: {price}đ/đêm | Rating: {h['rating']}/5\n")
    
    return result


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, cách nhau bởi dấu phẩy, 
      định dạng 'tên_khoản:số_tiền'
    """
    try:
        # 1. Parse chuỗi expenses thành dict {tên: số_tiền}
        expense_dict = {}
        total_expense = 0
        
        # Tách từng khoản chi bằng dấu phẩy
        items = expenses.split(',')
        for item in items:
            if ':' not in item:
                return "Lỗi: Định dạng khoản chi phải là 'tên:số_tiền' (VD: ve_may_bay:1000000)"
            
            name, amount_str = item.split(':')
            # Chuyển đổi số tiền sang kiểu int
            amount = int(amount_str.strip())
            expense_dict[name.strip().replace('_', ' ').capitalize()] = amount
            total_expense += amount

        # 2. Tính số tiền còn lại
        remaining = total_budget - total_expense

        # 3. Format bảng chi tiết
        def fmt(val): return f"{val:,}".replace(",", ".") + "đ"
        
        report = "Bảng chi phí:\n"
        for name, amount in expense_dict.items():
            report += f"- {name}: {fmt(amount)}\n"
        
        report += "---\n"
        report += f"Tổng chi: {fmt(total_expense)}\n"
        report += f"Ngân sách: {fmt(total_budget)}\n"
        report += f"Còn lại: {fmt(remaining)}\n"

        # 4. Kiểm tra nếu âm ngân sách
        if remaining < 0:
            over_amount = abs(remaining)
            report += f"\n Vượt ngân sách {fmt(over_amount)}! Cần điều chỉnh."
            
        return report

    except ValueError:
        return "Lỗi: Số tiền trong chuỗi chi phí phải là con số hợp lệ."
    except Exception as e:
        return f"Lỗi hệ thống khi tính toán: {str(e)}"

