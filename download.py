#Simple script to download all districts 
#Author: Chris Cummings
#License: MIT

import settings
import downloader

if __name__ == '__main__':
    downloader.run(settings.CDN_URL)