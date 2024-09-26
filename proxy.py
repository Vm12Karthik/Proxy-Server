import http.server
import socketserver
import urllib.request

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url = self.path
        
        if not url.startswith('http'):
            url = 'http://' + url
        
        try:
            # Forward the request to the actual server
            response = urllib.request.urlopen(url)
            
            # Send the response status code
            self.send_response(response.status)
            
            # Send the headers
            for header, value in response.getheaders():
                self.send_header(header, value)
            self.end_headers()
            
            # Send the content
            self.wfile.write(response.read())
        
        except Exception as e:
            self.send_error(500, f"Error: {str(e)}")

def run_proxy_server(port=8000):
    with socketserver.TCPServer(("", port), ProxyHandler) as httpd:
        print(f"Proxy server running on port {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_proxy_server()
