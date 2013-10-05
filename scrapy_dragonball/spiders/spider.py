from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.log import *
from scrapy_dragonball.settings import *
from scrapy_dragonball.items import *
import urllib, os, re

class RakitanSpider(CrawlSpider):

    name = 'dragonball_spider'
    base_url = "http://www.dragonball-multiverse.com/"
    chapters_url = "en/chapters.html"
    start_urls = [
        base_url + chapters_url
    ]


    image_url = "en/pages/final/"
    filename = "0001"
    extension = ["jpg", "png"]
    my_last_chapter = 0

    # create a directory
    local_save_path = "images/"
    if not os.path.exists(local_save_path):
        os.makedirs(local_save_path)


    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        # HXS to find all chapter
        chapters = hxs.select('//div[@class="cadrelect chapters"]')

        # HXS to find last chapter
        last_chapter = chapters.select('p/a/text()').extract()[-1]
        last_chapter = last_chapter.decode('utf_8')
        # print last_chapter

        # GET MY LAST CHAPTER
        # list all files, and count it
        try:
            directoryListing = os.listdir(self.local_save_path)
            #other code goes here, it iterates through the list of files in the directory
            # print directoryListing
            # sorted(directoryListing)
            # print directoryListing
            if len(directoryListing) > 0:
                text = sorted(directoryListing)[-1]
                text = text.strip()
                text = re.sub('.jpg','',text)
                text = re.sub('.png','',text)
                # text = re.sub('\r','',text)
                self.my_last_chapter = text
                print "Your last chapter = " + str(self.my_last_chapter)
                # print "You have "+ str(len(directoryListing)) + " files"
                # print directoryListing.sort()
            else :
                print "start from 0"
                self.my_last_chapter = 0
        except:
            print("Directory error ")

        # GET ALL IMAGES
        for i in range(int(self.my_last_chapter), int(last_chapter)):
            if i < 10:
                self.filename = "000"+ str(i)
            elif i < 100:
                self.filename = "00"+ str(i)
            elif i < 1000:
                self.filename = "0"+ str(i)

            try:
                x = urllib.urlretrieve(self.base_url + self.image_url + self.filename + "." + self.extension[0], self.local_save_path + self.filename + "." + self.extension[0])
                # print x
                tmp_val = x[1].values()
                # print tmp_val
                # 1329 == 404 error
                if tmp_val[0] == '1329':
                    os.remove(self.local_save_path + self.filename + "." + self.extension[0])
                    print "delete file " + self.local_save_path + self.filename + "." + self.extension[0]
                    y = urllib.urlretrieve(self.base_url + self.image_url + self.filename + "." + self.extension[1], self.local_save_path + self.filename + "." + self.extension[1])
                    # print y
                    tmp_val2 = y[1].values()
                    # print tmp_val2

                    # check again if it's error
                    # delete those 2 file
                    if tmp_val2[0] == '1329':
                        os.remove(self.local_save_path + self.filename + "." + self.extension[1])
                        print "delete file " + self.local_save_path + self.filename + "." + self.extension[1]
                    else:
                        print "Save to " + self.local_save_path + self.filename + "." + self.extension[1]
                else:
                    print "Save to " + self.local_save_path + self.filename + "." + self.extension[0]
            except:
                print "whoops"
                # urllib.urlretrieve(self.base_url + self.image_url + self.filename + "." + self.extension[1], self.local_save_path + self.filename + "." + self.extension[1])
                print "Save to " + self.local_save_path + self.filename + "." + self.extension[1]