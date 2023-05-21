# Origin description
Программа показывает погоду по текущим GPS координатам. Координаты берутся
из программы `whereami`, которая работает (и работает отлично!) на компьютерах
Mac. [О whereami](https://github.com/robmathers/WhereAmI).

Получение погоды по координатам происходит в сервисе
[OpenWeather](https://openweathermap.org/api).

Для запуска используйте python 3.10 (внешние библиотеки не требуются для работы
приложения), в `config.py` проставьте API ключ для доступа к OpenWeather и 
запустите:


```bash
./weather
```

Файл `weather` — исполнимый файл с python кодом, его можно открыть посмотреть.

Данный материал подготовлен в качестве примера к [видео](https://www.youtube.com/watch?v=dKxiHlZvULQ) и [книге
«Типизированный Python»](https://t.me/t0digital/151).

### Original repository link
> https://github.com/alexey-goloburdin/weather.git

Author: Alexey Goloburdin

## Changes

I have realised weather colorising and icons.
[![2023-05-21-18-53-15.png](https://i.postimg.cc/Vk4w6JGn/2023-05-21-18-53-15.png)](https://postimg.cc/nXsgShth)

I have made color depend on temperature. In general there is 7 colors. Additionally i have added weather icons, depends on weather conditions: rain, drizzle, snow, cloudy, clear and thunderstorm.
Added oportunity to display weather in Celsius and Farenheit scale. 

All of colors and weather condition icons will be shown below.

Application still use:
```bash
whereami
```
for GPS-coords fetching. 

## Plans / Ideas

1) Make command / flags system for select language and units scale;
2) Add extended model to display wind conditions and other additional features;
3) Make weather forecast.

## All of colors and conditions below:
[![2023-05-21-18-18-28.png](https://i.postimg.cc/rsWMgc1J/2023-05-21-18-18-28.png)](https://postimg.cc/SYyBNBt2)
