import pandas as pd

# Lendo os arquivos CSV com encoding correto
df1 = pd.read_csv('Urb01.csv', encoding='latin1')
df2 = pd.read_csv('Urb02.csv', encoding='latin1')

# Juntando os dataframes usando concat
# Isso irá empilhar os dataframes mantendo todas as colunas
df_final = pd.concat([df1, df2], axis=0, ignore_index=True)

# Salvando o resultado em um novo arquivo CSV
df_final.to_csv('resp.csv', index=False, encoding='latin1')

print(f"Total de registros no arquivo final: {len(df_final)}")