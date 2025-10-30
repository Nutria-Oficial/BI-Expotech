import requests
import pandas as pd

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
    
    # Passo 3: Transformar dados em DataFrame para uso do BI
    
    all_grades = []
    for review in data:
        for grade in review["grades"]:
            all_grades.append({
                "review_id": review["id"],
                "grade_name": grade["name"],
                "score": grade["score"],
                "weight": grade["weight"],
            })
    grades_df = pd.DataFrame(all_grades)

    grades_df
        
else:
    print("Erro ao obter token de autenticação.")