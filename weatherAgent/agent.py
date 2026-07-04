SYSTEM_PROMT = """
you need to use chain of thought techniqe
START | PLAN | OUTPUT | TOOL 

you can also call a tool if require

Availavble tools
    - get_wather(city: str): Take city name as input and give the output

example1:
    what is weather in malda
    def get_weather(city):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    res = requests.get(url)
    if res.status_code == "200":
        return f"The weather in {city} is {res.text}"
    return f"something went wonrg"





"""