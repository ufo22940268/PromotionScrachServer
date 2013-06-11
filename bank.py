class Bank():
    """docstring for Bank"""
    def __init__(self):
        #These are the only things we need to fetch.
        self.url = "";
        self.title = "";

        self.name = "";
        self.fetchTime = "";
	self.accepted = 0;

    def __str__(self):
        return "url:" + self.url + "\ttitle:" + self.title + "\tname:" + self.name;

