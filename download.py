#Helper script to run the downloader with the correct CDN
#Author: Chris Cummings
#License: MIT

import settings
import downloader

if __name__ == '__main__':
    downloader.run("https://devblobs.shapevrcloud.com/infiniverse/public")