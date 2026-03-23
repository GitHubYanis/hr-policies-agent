# HR Policies Agent — Démarrage

## Prérequis

- Python 3.10+
- Node.js 18+
- Une clé API OpenAI

## 1. Variables d'environnement

Créer un fichier `.env` dans `backend/` :

```
OPENAI_API_KEY=sk-...
```

## 2. Indexer le PDF

Exécuter le notebook une fois pour peupler la base ChromaDB :

```
backend/notebooks/rag_pipeline.ipynb
```

Cela crée le dossier `chroma_db/` à la racine du projet.

## 3. Démarrer le backend

Il est recommandé d'utiliser un environnement virtuel :

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

API disponible sur `http://localhost:8000`

## 4. Démarrer le frontend

```bash
cd frontend
npm install
ng serve
```

Application disponible sur `http://localhost:4200`