
class Initialisation:
    """ 
    inistialisation of the app 
        - import a data from rapid-api 
    """

    RAPID_KEY ="f2b69e8ab2mshc6b37f3259eace5p104495jsnc2a8ef50efc6"
    URL ="https://parazun-amazon-data.p.rapidapi.com/search/"
    HEADERS = {
            'x-rapidapi-host': "parazun-amazon-data.p.rapidapi.com",
            'x-rapidapi-key': RAPID_KEY
            }
    LIST_PAYS = list_pays = ['FR']
    NBR_PAGES = 2 
    COULEUR = ['#D56149','#49B5D5','yellow','green']#,'gray','pink','orange'] 
    


    def __init__(self):
        # configuration 
        self.rapid_key = self.RAPID_KEY
        self.url = self.URL  
        self.headers =  self.HEADERS   
        self.list_pays = self.LIST_PAYS
        self.nbr_pages = self.NBR_PAGES
        self.couleurs = self.COULEUR 
        




