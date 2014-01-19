## Format Apache Access log into HTML based on keyword

### Abstract
I was looking for a way to log messages from a users browser via javascript with minimal effort. So I thought I could use the Apache Access Log and just produce error messages on a webserver under my control. This way I would also have the users IP address, timestamp, the the user agent and and of course the failed URL. In this URL we can encode the information we want to pass.

### Setup
The only thing you need is an apache webserver on which you are allowed to read the access log files.

### Building URL's
First of all we need an URL base path that would produce a 404 Error on the webserver. Somehing like this: http://example.com/non_existent/ now we append a tag to that base URL so we can easily identify from which context the Log entry was written. This would look something like this: http://example.com/non_existent/testcontext You can now append as many key value pairs as you like. The only limitation is that keys have to be alphanumeric for example: http://example.com/non_existent/testcontext?key1=value_1&key2=value_2...&keyN=value_N

Such an URL con now easily be called via jQuery or by simply clicking a link.

    $.get('http://example.com/non_existent/testcontext?key1=value_1');
    
This will now produce a 404 Error on the Apache webserver that will look like this:

    127.0.0.1:80 127.0.0.1 - - [19/Jan/2014:04:06:20 +0100] "GET /non_existent/testcontext?key1=value_1 HTTP/1.1" 404 435 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"

This gives us a lot of information. IP address, a timestamp, the user agent and of course the data we submitted. But since reading those log entries is pain in the ass the next step beautifies them.

### Formatting the Log files
Simply call *format.py* with the tag you are looking for and the path to the log file:

    ./format.py testcontext /var/log/apache2/access.log
    
This will now produce an HTML file which you can then view in the browser. This comes in form of a sortable HTML table.