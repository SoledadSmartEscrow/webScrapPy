
# Este codigo es solo para descargar en PDF cualquier web que le pasemos en la variable url

import asyncio
import os
from pyppeteer import launch

async def get_pdf():
    browser = await launch()
    page = await browser.newPage()

    try:
        url = "https://service.ariba.com/ProfileManagement.aw/109591067/aw?awh=r&awssk=GLQQVHaC&dard=1"

        await page.goto(url)

        # Espera unos segundos para asegurarse de que la página se cargue completamente
        await asyncio.sleep(5)

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
        
        # Directorio donde se ejecuta el script y ruta completa para guardar los PDF obtenidos con el nombre de búsqueda de empresa
        current_working_directory = os.getcwd()
        pdf_filename = f'outputWeb.pdf'
        pdf_path = os.path.join(current_working_directory, 'public', 'urlWebs', pdf_filename)

        # Guarda el PDF en la ruta indicada
        await page.pdf({'path': pdf_path})

    except Exception as e:
        print('Error:', e)

    await browser.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(get_pdf())
    


