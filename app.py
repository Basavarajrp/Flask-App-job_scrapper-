from flask import Flask,render_template,request
import requests
from bs4 import BeautifulSoup 

app = Flask(__name__)

@app.route('/',methods=['GET'])

def homePage():
    return render_template("index.html")

@app.route('/home',methods=['POST','GET']) # route to show the review comments in a web UI

def index():
    if request.method == 'POST':
        try:
            role = request.form['Rol']
            location = request.form['loc'].replace(" ","")
            URL = f"https://www.monster.com/jobs/search/?q={role}&where={location}"
            page = requests.get(URL)
            #print(page) #if responce is 200 we are good to go..

            soup = BeautifulSoup(page.content, 'html.parser') #parsing html content..

            results = soup.find(id='ResultsContainer')# contains the job results block...

            #print(results.prettify()) #prettify gives u nice html formate to view...
            job_elems = results.find_all('section', class_='card-content')

            #print(len(job_elems))
            links = []
            titles = []
            company_names = []
            location_names = []



            for job_elem in job_elems:
                title_elem = job_elem.find('h2', class_='title')
                company_elem = job_elem.find('div', class_='company')
                location_elem = job_elem.find('div', class_='location')
            
                
                
                if None in (title_elem, company_elem, location_elem):
                    continue
                title_elem = title_elem.text.strip()
                company_elem = company_elem.text.strip()
                location_elem = location_elem.text.strip()
                titles.append(title_elem)
                company_names.append(company_elem)
                location_names.append(location_elem)

                
                #for job_elems in job_elems:
                link = job_elem.find('a')["href"]
                links.append(link)
                
            return render_template('tables.html', details=zip(company_names,titles,location_names,links))    
        except Exception as e:
            print('The Exception message is: ',e)
            return "Not found"    
    else:
        return render_template('index.html')           
                

if __name__=='__main__':
    app.run(debug=True)