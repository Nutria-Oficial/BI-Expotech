import requests
import pandas as pd
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

print("\nComeçando o processo de atualizar os dados do dashboard sobre a EXPOTECH!")

user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")

# Conexão com banco
engine = create_engine(
    f'postgresql://{user}:{password}@ep-polished-water-a80ydgyw-pooler.eastus2.azure.neon.tech/dbExpoTech?sslmode=require&channel_binding=require'
)
print("\nConexão com banco criada")

# Passo 1: Login
numero_mapa = 1
login_url = "https://expo-tech-backend.onrender.com/users/login"
login_data = {
    "username": f"expositor_project-uuid-{numero_mapa}@example.com",
    "password": "senha123"
}
login_headers = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"
}
response = requests.post(login_url, data=login_data, headers=login_headers)
token = response.json().get("access_token")

# Passo 2: Buscar reviews do projeto
if token:
    reviews_url = "https://expo-tech-backend.onrender.com/reviews/project/"
    reviews_headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    reviews_response = requests.get(reviews_url, headers=reviews_headers)
    data = reviews_response.json()

    print("\nDados da API puxados!")
    
    # Passo 3: Transformar dados em DataFrame para uso do BI
    
    all_grades = []
    qtd_reviews = len(data)
    i = 0
    for review in data:
        j = 0
        i+=1
        print(f"\nReview {i} de {qtd_reviews} salvando")
        for grade in review["grades"]:
            j+=1
            qtd_grades = len(review["grades"])
            all_grades.append({
                "review_id": review["id"],
                "grade_name": grade["name"],
                "score": grade["score"],
                "weight": grade["weight"],
            })
            print(f"\tGrade {j} de {qtd_grades} salva")
        print(f"Review {i} de {qtd_reviews} salva")

    grades_df = pd.DataFrame(all_grades)

    print("\nSALVANDO NO SQL")
    grades_df.to_sql(
        name="avaliacoes",
        con=engine,
        if_exists="replace",
        index=False
    )
    print("\nTodos os dados foram salvos com sucesso")
        
else:
    print("Erro ao obter token de autenticação.")