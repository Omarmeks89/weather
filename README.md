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

Link on original repository below.

> https://github.com/alexey-goloburdin/weather.git

Author: Alexey Goloburdin

## Changes

I have realised weather colorising and icons.

[![header.png](https://i.postimg.cc/YSH72JwG/header.png)](https://postimg.cc/mP8J8pkB)

I have made color depend on temperature. In general there is 7 colors. Additionally i have added weather icons, depends on weather conditions: rain, drizzle, snow, cloudy, clear and thunderstorm.
Added oportunity to display weather in Celsius and Farenheit scale. 

All of colors and weather condition icons will be shown below.

Application still use:
```bash
whereami
```
for GPS-coords fetching. I have a little throubles with `whereami` on Ubuntu - 
so for Linux app use:
```bash
whereami -r
```
Note, that now app can not choose exact OS - this will be fixet a bit later.

## Plans / Ideas

1) Make command / flags system for select language and units scale;
2) Add extended model to display wind conditions and other additional features;
3) Make weather forecast.
4) Make GPS-fetcher depend on exact OS.

## All of colors and conditions below:

[![w1.png](https://i.postimg.cc/vT1ktzsw/w1.png)](https://postimg.cc/8fSZ1LcZ)
[![wf1.png](https://i.postimg.cc/XXSHc6L9/wf1.png)](https://postimg.cc/7J9nwcpL)
[![w2.png](https://i.postimg.cc/YCkkM574/w2.png)](https://postimg.cc/GHM6jSHr)
[![wf2.png](https://i.postimg.cc/4NRRQDm8/wf2.png)](https://postimg.cc/Wt8y2fmr)
[![w3.png](https://i.postimg.cc/SR03V9NX/w3.png)](https://postimg.cc/xJR61cmY)
[![wf3.png](https://i.postimg.cc/QMHz3mF9/wf3.png)](https://postimg.cc/d7c6R8mw)
