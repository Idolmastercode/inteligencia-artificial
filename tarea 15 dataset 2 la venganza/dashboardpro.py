import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    df = pd.read_csv('datasetTexto.csv', on_bad_lines='skip')
except FileNotFoundError:
    print("Error: No se encuentra el archivo datasetTexto.csv")
    exit()

df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
df = df.dropna(subset=['Fecha'])

def calcular_sentimiento(texto):
    if not isinstance(texto, str): return 0
    texto = texto.lower()
    
    positivo = ['orgullo', 'maestra', 'bello', 'increible', 'emotiva', 'garantizada', 'perfecto', 'ovacion', 'amor', 'luz', 'esperanza', 'exito', 'respeto', 'genio']
    negativo = ['represion', 'miedo', 'ataque', 'heridos', 'robo', 'culpa', 'inseguridad', 'indignacion', 'fuerza', 'violencia', 'amenaza', 'desconfianza', 'muerte', 'asesinato', 'detenidos']
    
    score = 0
    for p in positivo:
        if p in texto: score += 1
    for n in negativo:
        if n in texto: score -= 1.5 
    return score

df['Sentimiento_Score'] = df['Comentario_Reaccion'].apply(calcular_sentimiento)

plt.style.use('dark_background')
fig = plt.figure(figsize=(18, 10))
fig.suptitle('DASHBOARD DE INTELIGENCIA: REALIDAD vs FICCION (NOV 2025)', fontsize=20, color='#00ff00', fontweight='bold')

grid = plt.GridSpec(2, 2, wspace=0.25, hspace=0.4)

ax1 = fig.add_subplot(grid[0, :])
nov_data = df[(df['Fecha'] >= '2025-11-01') & (df['Fecha'] <= '2025-11-19')]
timeline = nov_data.groupby(['Fecha', 'Categoria']).size().reset_index(name='Volumen')

sns.lineplot(data=timeline, x='Fecha', y='Volumen', hue='Categoria', ax=ax1, palette=['#00ff00', '#ff0044'], linewidth=3, marker='o')
ax1.set_title('ESCALADA DEL CONFLICTO VS ESTRENO', fontsize=14, color='white')
ax1.grid(color='gray', linestyle=':', alpha=0.3)

ax2 = fig.add_subplot(grid[1, 0])
sns.boxplot(x='Categoria', y='Sentimiento_Score', data=df, ax=ax2, palette=['#ff0044', '#00ff00'], hue='Categoria', legend=False)
sns.stripplot(x='Categoria', y='Sentimiento_Score', data=df, color='white', alpha=0.4, ax=ax2)
ax2.set_title('POLARIZACION: ODIO vs AMOR', fontsize=14, color='white')
ax2.axhline(0, color='yellow', linestyle='--', alpha=0.5)

ax3 = fig.add_subplot(grid[1, 1])
top_medios = df['Medio'].value_counts().head(10)
sns.barplot(y=top_medios.index, x=top_medios.values, ax=ax3, palette='viridis', hue=top_medios.index, legend=False)
ax3.set_title('QUIEN CONTROLA LA NARRATIVA', fontsize=14, color='white')
ax3.set_xlabel('Numero de Publicaciones')

output_file = 'dashboard_analisis_pro.png'
plt.savefig(output_file, dpi=150, bbox_inches='tight')
plt.show()