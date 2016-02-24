require 'nokogiri'
require_relative 'Streaming'


def parse(response)
    body = Nokogiri::HTML(response['body'])
    base_url = '//div[@id="siteTable"]'
    list = []
    for i in (1..50).step(2) do
        url  = base_url + "/div[#{i}]/div[2]/p/a"
        p = {'type'=>'item', 'name'=>'post'}
        item = {}
        item['title'] = body.xpath(url+'/text()')[0].content
        item['url'] = 'http://www.reddit.com' + body.xpath(url+'/@href')[0].content
        p['item'] = item
        request = {"type"=>"request", "url"=>item['url'],
                   "callback"=>"get_content", 
                   "meta"=>{"item"=>p}}
        list.push(request)
    end
    return list
end


def get_content(response)
    body = Nokogiri::HTML(response['body'])
    p = response['meta']['item']
    content = body.xpath('//div[@id="siteTable"]/div/div/div/form/div/div/p/text()')
    content = content.map { |n| n.content}
    content.join()
    p['item']['content'] = content
    return p
end


Comptroller('cscareerquestions', start_urls:["http://www.reddit.com/r/cscareerquestions"],
                     allowed_domains:["reddit.com"])
