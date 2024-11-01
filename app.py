from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from datetime import datetime
from urllib.parse import quote

print(100 * '#')
print()
print(25 * ' ', 'Bem Vindo ao Leads Linkedin Automation')
print()
keywords = input("Informe as Palavras Chave da busca: ")
keywords_formatted = keywords.replace(' ', '-')
keywords = quote(keywords)
pages = input('Quais paginas você deseja exportar? Ex: (1-5 ou 5)')
list_pages = None
if '-' in pages:
    list_pages = [page for page in range(int(pages[0]), int(pages[-1])+1)]
# Configurando o WebDriver automaticamente
chrome_options = Options()
#schrome_options.add_argument("--headless")
driver = webdriver.Chrome(
    options=chrome_options,
    )

# Acessa o LinkedIn
driver.get("https://www.linkedin.com/login/pt?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
time.sleep(2)

# Login no LinkedIn
username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")
username.send_keys("wilker.santos.ribeiro@gmail.com")
password.send_keys("w1lk3rbr$")
password.send_keys(Keys.RETURN)
time.sleep(3)
if '/checkpoint/' in driver.current_url:
    input("Resolva o Captcha e pressione ENTER para continuar:")
urls = []
# Navegação para uma empresa
if not list_pages:
    driver.get(f"https://www.linkedin.com/search/results/companies/?keywords={keywords}&page={pages}&companyHqGeo=%5B%22106057199%22%5D&companySize=%5B%22D%22%2C%22E%22%2C%22F%22%2C%22G%22%2C%22H%22%2C%22I%22%5D")
    time.sleep(2)
    urls_companies = driver.find_elements(By.CLASS_NAME, 'app-aware-link ')
    urls = [url.get_attribute('href') for url in urls_companies if '/company/' in url.get_attribute('href')]
else:
    for page in list_pages:
        driver.get(f"https://www.linkedin.com/search/results/companies/?keywords={keywords}&page={page}&companyHqGeo=%5B%22106057199%22%5D&companySize=%5B%22D%22%2C%22E%22%2C%22F%22%2C%22G%22%2C%22H%22%2C%22I%22%5D")
        time.sleep(2)
        urls_companies = driver.find_elements(By.CLASS_NAME, 'app-aware-link ')
        for url in urls_companies:
            if '/company/' in url.get_attribute('href'):
                urls.append(url.get_attribute('href'))

urls = list(set(urls))
# Next //*[@id="ember368"]/span
# Captura das informações da empresa
data = []
for url in urls:
    company = {}
    driver.get(f'{url}about/')
    company_name = driver.find_element(By.TAG_NAME, "h1").text
    #print(f"Nome: {company_name}")
    company.update({'Nome': company_name})
    url_linkedin = driver.current_url
    #print(f"URL: {url}about/")
    company.update({'URL': url_linkedin})
    div_informations = driver.find_element(By.CLASS_NAME, 'org-transition-scroll')
    try:
        about = div_informations.find_element(By.TAG_NAME, 'p').text
        #print(f'Sobre: {about}')
        company.update({'Sobre': about})
    except:
        print('Não encontrei')
    #phone = driver.find_element(By.CSS_SELECTOR, "CSS_SELECTOR_DO_TELEFONE").text /html/body/div[6]/div[3]/div/div[2]/div/div[2]/main/div[2]/div
    
    try:
        dts = div_informations.find_elements(By.TAG_NAME, 'dt')
        dds = div_informations.find_elements(By.TAG_NAME, 'dd')
        for i, dt in enumerate(dts):
            #print(f'{dt.find_element(By.TAG_NAME, 'h3').text}: {dds[i].text}')
            company.update({dt.find_element(By.TAG_NAME, 'h3').text: dds[i].text})
    except:
        print('Não encontrado')
    data.append(company)
# Encerrando a sessão
df = pd.DataFrame(data)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"informacoes_empresas_{keywords_formatted}_{timestamp}.xlsx"
df.to_excel(filename, index=False)
print(f"Dados salvos no arquivo '{filename}'")
driver.quit()
