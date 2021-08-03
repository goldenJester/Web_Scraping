from bs4 import BeautifulSoup

# 'r' Read Permission
# 'w' Write Permission
# 'rw' Read/Write Permission
with open('example.html', 'r') as html_file:
    content = html_file.read()

    # prettify HTML using lxml
    soup = BeautifulSoup(content, 'lxml')

    # find specific HTML tags
    # 'find()' only finds the first occurence of that HTML tag 
    # tags = soup.find('h5')
    # 'find_all()' finds all occurrences of that HTML tag
    # all_tags = soup.find_all('h5')

    divs = soup.find_all('div', class_='card')
    for div in divs:
        # names are stored in <h5></h5>
        # print all the text with '.text'
        name = div.h5.text

        # prices are stored in <a></a>
        # The text of the <a></a> tag is in the format
        # "Starts at 00$" so we split and take the last token
        price = div.a.text.split()[-1]

        ## Create a dynamic f-string and print the name and price together
        print(f'{name} costs {price}')