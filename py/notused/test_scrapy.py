import scrapy

class AthleteSpider(scrapy.InitSpider):
    abc
    name    = "athlete_spider"
    payload = { # populated with login credentials
        "email"    : "ustas06@hotmail.com",
        "password" : "tomgreen"
    }
    allowed_domains = ["strava.com"]
    login_page = 'https://www.strava.com/login'
    start_urls = [
        'http://www.strava.com/athletes/1153632'
        #'http://www.strava.com/athletes/1153634'
    ]

    def init_request(self):
        """This function is called before crawling starts, to authenticate user
        """
        print "In init_request"
        return scrapy.Request(url=self.login_page, callback=self.login)

    def login(self, response):
        """Generate a login request.
        """
        self.payload["utf8"] = \
            response.xpath('//input[@name="utf8"]/@value').extract()[0]
        
        self.payload["authentication_token"] = \
            response.xpath('//input[@name="authenticity_token"]/@value').extract()[0]
        
        print self.payload
        return scrapy.FormRequest.from_response(response,
                                                formdata=self.payload,
                                                callback=self.check_login_response)

    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
           successfully logged in.
        """
        if "Home" in response.title:
            print "Successfully logged in. Let's start crawling!"
            print response.title
            print response.body
            print self.get_cookies()
            #self.initialized() # can start crawling
        else:
            print "Login unsuccessful"
            print response.title
            print response.body
            print self.get_cookies()
            # Something went wrong, we couldn't log in, so nothing happens.

    def parse(self, response):
        """Executed for each URL
        """
        print "in parse"
        print response.body
        return

