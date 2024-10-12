from dataclasses import dataclass

@dataclass
class Website:
    name: str
    url : str
    page_content : str
    organised_page_content : list[dict[str, str|list[float]|list[str]]]
    bets : list[Bet]

    def __init__(self, name, url):
        self.name = name
        self.url = url
    
    def get_page_content()
