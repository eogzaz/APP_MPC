def Date_to_julian(d):
    year, month, day_with_fraction = d.split()
    year = int(year)
    month = int(month)
    day_with_fraction = float(day_with_fraction)

    day = int(day_with_fraction)
    fraction_of_day = day_with_fraction - day

    if month <= 2:
        year -= 1
        month += 12

    A = year // 100
    B = 2 - A + A // 4

    jd = int(365.25 * (year + 4716)) \
       + int(30.6001 * (month + 1)) \
         + day + B - 1524.5 + fraction_of_day


    return jd#int(jd)+.5

def Date_to_julian_N(d):
  return int(Date_to_julian(d))+.5