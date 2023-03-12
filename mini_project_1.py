# %%
import pandas as pd
import numpy as np
bookings = pd.read_csv('bookings.csv', sep = ';')

# %%
## информация об исходном датафрейме
bookings.shape
bookings.info()
#bookings_head = bookings.head(7)

# %%
## функция, переименовывающая название столбца
def modify_column(name):
    new_name = name.replace(' ', '_').lower()
    return new_name
## переименовывание столбцов
bookings = bookings.rename(columns = modify_column)

# %%
## число успешных бронирований по каждой стране
bookings.query('is_canceled == 0').country.value_counts()

# %%
## среднее число ночей в отеле City Hotel = 2.98
mean_city_hotel = round(bookings.query("hotel == 'City Hotel'").stays_total_nights.mean(), 2)
## среднее число ночей в отеле Resort Hotel = 4.32
mean_resort_hotel = round(bookings.query("hotel == 'Resort Hotel'").stays_total_nights.mean(), 2)
print(mean_resort_hotel, mean_city_hotel)

# %%
## число случаев овербукинга: когда полученный тип номера отличается от забронированного
bookings.query('assigned_room_type != reserved_room_type').shape

# %%
## самое большое число бронирований в 2016 году приходится на октябрь
book_2016 = bookings.query('arrival_date_year == 2016')
book_2016.groupby(by = 'arrival_date_month', as_index = False).agg({'is_canceled' : 'count'}).sort_values(
    by = 'is_canceled', ascending = False)

## самое большое число бронирований в 2017 году приходится на май
book_2017 = bookings.query('arrival_date_year == 2017')
book_2017.groupby(by = 'arrival_date_month', as_index = False).agg({'is_canceled' : 'count'}).sort_values(
    by = 'is_canceled', ascending = False)

# %%
## в каком месяце чаще всего отменяли бронь City Hotel
hotel = bookings.query("hotel == 'City Hotel' and is_canceled == 1")
hh = hotel.groupby(by = 'arrival_date_year', as_index = False)['arrival_date_month'].value_counts()
hh.sort_values(by = 'count', ascending = False)

# %%
## среднее число взрослых, малышей и детей
print(bookings.adults.mean(), bookings.babies.mean(), bookings.children.mean())

# %%
## создание общего столбца, учитывающего количество детей и подсчет их среднего числа для разного типа отелей
bookings['total_kids'] = bookings['babies'] + bookings['children']
print(round(bookings.query("hotel == 'City Hotel'").total_kids.mean(), 2))
print(round(bookings.query("hotel == 'Resort Hotel'").total_kids.mean(), 2))

# %%
## создание нового логического столбца - есть детей / нет детей
## вычисление метрики churn rate - оттока клиентов, в зависимости от has_kids 
bookings['has_kids'] = np.where(bookings['total_kids'] >= 1, True, False)
## имеют детей - 9332
bookings.query('has_kids == True').shape
## имеют детей и отменили бронь - 3259. 35.0% 
bookings.query('has_kids == True and is_canceled == 1').shape
## не имеют детей - 110058
bookings.query('has_kids == False').shape
## не имеют детей и отменили бронь - 40965. 37.0%
bookings.query('has_kids == False and is_canceled == 1').shape

round(3259 / 9332, 2)
round(40965 / 110058, 2)


