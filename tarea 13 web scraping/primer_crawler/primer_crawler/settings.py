BOT_NAME = 'primer_crawler'

SPIDER_MODULES = ['primer_crawler.spiders']
NEWSPIDER_MODULE = 'primer_crawler.spiders'

# --- CONFIGURACIÓN CRÍTICA PARA QUE NO TE BLOQUEEN ---
# Falsificamos un navegador real
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# Desactivamos el respeto al robots.txt (OBLIGATORIO para Reddit)
ROBOTSTXT_OBEY = False

# Un pequeño retraso para ser amables
DOWNLOAD_DELAY = 1
# -----------------------------------------------------

# Activamos el Pipeline de limpieza
ITEM_PIPELINES = {
   'primer_crawler.pipelines.LimpiezaPipeline': 300,
}

# Codificación para que salgan bien los acentos/emojis
FEED_EXPORT_ENCODING = 'utf-8'