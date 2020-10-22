from bs4 import BeautifulSoup
 
html = "<h1>sayhello</h1>,<h1>saysay</h1>,<h2>say</h2>"
 
soup = BeautifulSoup(html, "html.parser")
 
print(soup.select("h1"))