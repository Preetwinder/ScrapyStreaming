require 'json'


def Comptroller(name, start_urls: [], allowed_domains: [])    
    settings = {"type"=>"spider_settings",
                "name"=>name,
                "start_urls"=>start_urls,
                "allowed_domains"=>allowed_domains}
    puts JSON.generate(settings)
    STDOUT.flush
    
    while true
        line = STDIN.readline()
        hash = JSON.parse(line)
        if hash['callback']
            returned = method(hash['callback']).call(hash)
        end
        puts JSON.generate(returned)
        STDOUT.flush()
    end
end
