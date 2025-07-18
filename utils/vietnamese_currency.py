def convert_number_to_vietnamese(number):
    units = ["", "nghìn", "triệu", "tỷ"]
    
    def read_three_digits(num):
        chu_so = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
        hundred = num // 100
        ten = (num % 100) // 10
        unit = num % 10
        result = ""
        if hundred > 0:
            result += chu_so[hundred] + " trăm"
            if ten == 0 and unit > 0:
                result += " linh"
        if ten > 1:
            result += " " + chu_so[ten] + " mươi"
            if unit == 1:
                result += " mốt"
            elif unit == 5:
                result += " lăm"
            elif unit > 0:
                result += " " + chu_so[unit]
        elif ten == 1:
            result += " mười"
            if unit == 5:
                result += " lăm"
            elif unit > 0:
                result += " " + chu_so[unit]
        elif ten == 0 and unit > 0:
            result += " " + chu_so[unit]
        return result.strip()

    parts = []
    i = 0
    while number > 0:
        n = number % 1000
        if n != 0:
            prefix = read_three_digits(n)
            if units[i]:
                prefix += " " + units[i]
            parts.insert(0, prefix)
        number //= 1000
        i += 1

    return " ".join(parts).capitalize() + " đồng"
