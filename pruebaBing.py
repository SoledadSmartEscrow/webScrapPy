# Este codigo busca la primer coincidencia en Bing y descarga el PDF de la web encontrada

import asyncio
import os
from pyppeteer import launch
import httpx
import json
from dotenv import load_dotenv 


load_dotenv()

async def main():
    social_denomination = 'ikea'

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

        # Directorio donde se ejecuta el script y ruta completa para guardar los PDF obtenidos con el nombre de búsqueda de empresa
        current_working_directory = os.getcwd()
        pdf_filename = f'{social_denomination}.pdf'
        pdf_path = os.path.join(current_working_directory, 'public', 'pdfWebs', pdf_filename)

        # Va a la web encontrada
        await page.goto(url)

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

    except Exception as e:
        print('Error:', e)

    await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
    print("El archivo PDF fue descargado con éxito en la carpeta pdfWebs")

