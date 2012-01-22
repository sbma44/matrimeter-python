import scraper, scrapelib, json, re, math

class NextbusScraper(scraper.Scraper):    
    """Scraper for WMATA Nextbus info"""
    def __init__(self, wmata_api_key, stop_id, direction_text=None, route_id=None):
        super(NextbusScraper, self).__init__()
        self.wmata_api_key = wmata_api_key
        self.stop_id = stop_id
        self.direction_text = direction_text
        self.route_id = route_id
        self.scraper = scrapelib.Scraper()
        
    def scale_minutes(self, mins):
        # TODO: transform result into appropriate scale to account for display's non-linearity
        return int(math.floor((mins / 60.0) * 255)) # for now, scale linearly to an hour
        
    def run(self):
        self._run()
        results = json.loads(self.scraper.urlopen('http://api.wmata.com/NextBusService.svc/json/JPredictions?StopID=%s&api_key=%s' % (self.stop_id, self.wmata_api_key)))
        matching_results = []
        for r in results['Predictions']:
            
            # filter out results that don't match the route_id or direction_text (if specified)
            if self.route_id is not None:
                if re.search(self.route_id, r['RouteID']) is None:
                    continue
            if self.direction_text is not None:
                if re.search(self.direction_text, r['DirectionText']) is None:
                    continue
            matching_results.append(r)
        
        matching_results.sort(key=lambda x: int(x['Minutes']))        
        minutes_until_bus = int(matching_results[0]['Minutes'])
        
        return (self.scale_minutes(minutes_until_bus), ((minutes_until_bus * 60) / 2) )
        
            
                

    
    
        