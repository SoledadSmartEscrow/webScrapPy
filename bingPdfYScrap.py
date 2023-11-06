# Este codigo no solo busca con Bing la que podria ser la web oficiaL, tambien descarga la web en PDF y busca las palabras clave

import asyncio
import os
from pyppeteer import launch
import httpx
import json
import re
from dotenv import load_dotenv 



load_dotenv()

async def main():
    social_denomination = 'kintai'

    # Configuración de la instancia de Chrome
    browser = await launch(headless=True)

    page = await browser.newPage()

    # Realizar una búsqueda en Bing para encontrar el sitio web oficial de la empresa
    bing_api_endpoint = 'https://api.bing.microsoft.com/v7.0/search'
    # Usa os.environ para acceder a la variable de entorno de la clave de suscripción
    bing_subscription_key = os.environ.get('BING_SUBSCRIPTION_KEY')

    # API de Bing
    bing_request_url = f'{bing_api_endpoint}?q=Sitio+web+{social_denomination}'
    bing_request_headers = {
        'Ocp-Apim-Subscription-Key': bing_subscription_key,
    }

    try:
        # Realizar la solicitud a la API de Bing
        async with httpx.AsyncClient() as session:
            response = await session.get(bing_request_url, headers=bing_request_headers)
            response.raise_for_status()
            bing_data = response.text

        bing_data = json.loads(bing_data)

        # Obtener la URL del primer resultado de búsqueda de Bing
        url = bing_data['webPages']['value'][0]['url']

        # Va a la web encontrada
        await page.goto(url)
        
        # Directorio donde se ejecuta el script y ruta completa para guardar los PDF obtenidos con el nombre de búsqueda de empresa
        current_working_directory = os.getcwd()
        pdf_filename = f'{social_denomination}.pdf'
        pdf_path = os.path.join(current_working_directory, 'public', 'pdfWebs', pdf_filename)
        
        # Si la web tiene carga infinita/dinámica, se desplaza hasta el final
        await page.evaluate("""
            () => {
                setInterval(() => {
                    window.scrollBy(0, 100);
                }, 100);
            }
        """)

        # Agregar una espera de 5 segundos antes de tomar el PDF
        await asyncio.sleep(5)

        # Guarda el PDF en la ruta indicada
        await page.pdf({'path': pdf_path})

        # Muestra el titulo de la web
        title = await page.title()
        # Búsqueda de párrafos
        element_text = await page.evaluate("() => document.querySelector('p').textContent")
        # Obtener el contenido de la web para scrapear
        page_content = await page.content()
        # Patrón y búsqueda de teléfonos
        telefono_pattern = r"\(?\+34\)?\s?\d{3}\s?\d{2}\s?\d{2}\s?\d{2}"
        telefonos = re.findall(telefono_pattern, page_content, re.IGNORECASE)
        # Patrón y búsqueda de email
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        email_match = re.search(email_pattern, page_content)
        email = email_match.group(0) if email_match else ""
        # Patrón y búsqueda de dirección
        direccion_pattern = r"(Calle|Avenida|Av\.|Blvd\.|Plaza|Carrer|Paseo|P\.|Via)\s?[A-Za-z0-9\s\-áéíóúÁÉÍÓÚñÑ]+"
        direccion_match = re.search(direccion_pattern, page_content, re.IGNORECASE)
        direccion = direccion_match.group(0) if direccion_match else ""
        # Obtener todos los elementos h1
        h1_elements = await page.querySelectorAll('h1')
        h1_texts = []
        for element in h1_elements:
         h1_text = await page.evaluate('(element) => element.textContent', element)
         h1_texts.append(h1_text)
        # Obtener todos los elementos h2
        h2_elements = await page.querySelectorAll('h2')
        h2_texts = []
        for element in h2_elements:
         h2_text = await page.evaluate('(element) => element.textContent', element)
         h2_texts.append(h2_text)

        # Obtener todos los elementos h3
        h3_elements = await page.querySelectorAll('h3')
        h3_texts = []
        for element in h3_elements:
         h3_text = await page.evaluate('(element) => element.textContent', element)
         h3_texts.append(h3_text) 
        

    except Exception as e:
        print('Error:', e)
        

    await browser.close()
    print ('WEB:', url)
    print ('TÍTULO DE LA WEB:', title)
    print('TÉLEFONO:', telefonos)
    print('EMAIL:', email)
    print('DIRECCIÓN:', direccion)    
    print('PÁRRAFOS:', element_text)
    print('h1:', h1_texts)
    print('h2:', h2_texts)
    print('h3:', h3_texts)

if __name__ == '__main__':
    asyncio.run(main())
    