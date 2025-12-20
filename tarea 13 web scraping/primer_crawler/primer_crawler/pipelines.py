from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class LimpiezaPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Obtenemos el título (puede venir como 'titulo' o texto del tweet)
        titulo = adapter.get("titulo")

        # Limpieza: quitar espacios al inicio/final
        if titulo:
            titulo_limpio = titulo.strip()
        else:
            titulo_limpio = ""

        # Validación: Si queda vacío después de limpiar, descartamos el item
        if titulo_limpio == "":
            raise DropItem("Título vacío o inválido encontrado")

        # Guardamos el dato limpio
        adapter["titulo"] = titulo_limpio
        return item