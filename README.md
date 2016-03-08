# ScrapyStreaming
A basic proof of concept for Scrapy Streaming functionality.  
  
  
  
Start spiders using `./scrapystreaming.py "executable"`.   
eg - `./scrapystreaming.py "python2 python/process.py"`, `./scrapystreaming.py "ruby ruby/process.rb"`

The communication protocol is described below.

All communication is carried out through JSON serialized lines.
The process should flush it's stdout after sending each line to make sure
that the line is sent immediately, instead of being buffered.

* The process must first send the settings for the Spider to be generated.  

`{"type":"spider_settings", "name":"TestSpider",
"allowed_domains":["example.com"], "start_urls":["http://www.example.com"]}\n`

* The process will then receive the first response.  
 
`{"type":"response", "url":"http://www.example.com" "body":"<html><body><a>test</a></body></html>",
"callback":"parse", "meta":{"item":{"title":"test"}}}\n`

* The process must call the appropriate callback function with the response.

* The process can either send requests or items back.

Requests should be serialized as -  
  
`{"type":"request", "url":"http://www.example.com", "callback":"get_content",
"meta":{"item":{"title":"test"}}}\n`

Items should be serialized as -  
  
`{"type":"item", "name":"post", "item":{"title":"test"}}\n`

