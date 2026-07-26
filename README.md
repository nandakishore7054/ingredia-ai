# 🥗 Ingredia AI — Intelligent Recipe & Nutrition Assistant

> **Infosys Springboard Virtual Internship Project**  
> An AI-powered Computer Vision & LLM application that transforms fridge/pantry photos into personalized, nutrient-balanced recipes.

---

## 🌟 Executive Summary

**Ingredia AI** addresses the age-old problem: *"What can I cook with the ingredients I have right now?"* 

By integrating **Roboflow Object Detection (YOLO)** with **Hybrid LLM Intelligence (Groq / Llama 3.3 70B & OpenAI)**, Ingredia AI recognizes raw ingredients from images, searches a structured recipe database for optimal matches, dynamically generates missing instructions and nutritional macro breakdowns, and tailors recommendations according to user-specific dietary preferences and calorie targets.

---

## ✨ Key Features

- 📸 **Computer Vision Ingredient Detection**: Instant object detection via Roboflow Hosted Inference API (detecting confidence scores and bounding boxes).
- ⚡ **Hybrid Recipe Matching Algorithm**: Optimized single-JOIN SQL database matching with AI LLM dynamic fallback for unmatched ingredient combinations.
- 🎯 **Hyper-Personalized Recommendations**: Dynamic ranking system considering user diet (Vegetarian, Vegan, Keto), allergy exclusions, preferred cuisines, and calorie targets.
- 📊 **Nutrition Dashboard**: Interactive macro breakdowns (Calories, Protein, Carbs, Fats) with SVG progress rings and detailed dietary insight summaries.
- 💬 **Ingredia AI Culinary Assistant**: Context-aware floating AI chatbot that assists with culinary questions, sub-recipes, and ingredient substitutions.
- 🔒 **Secure Authentication & Persistence**: JWT-based session security, Favorite recipe bookmarking, user preferences, and cooking history tracking.
- 📱 **Modern & Accessible UI**: Responsive glassmorphism interface, shimmer skeleton loading states, copy-link/print capabilities, focus rings, and ARIA labels.

---

## 🏗️ System Architecture

```
[ User Image Upload ]
         │
         ▼
[ FastAPI Backend ]
         │
         ├──► [ Roboflow Hosted API (YOLO Object Detection) ]
         │           │
         │           ▼ (Detected Ingredients)
         │
         ├──► [ SQLite Recipe DB (Single-JOIN SQL Matching) ]
         │           │
         │           ├──► High Match Percentage? ──► Return DB Recipes
         │           │
         │           └──► Low Match / Fallback? ──► [ Groq / Llama-3.3 70B LLM ]
         │                                                │
         │                                                ▼ (Dynamic Recipe Generation)
         ▼
[ Next.js Frontend ] ◄── (Personalized Recommendations & Nutrition Dashboard)
```

---

## 🛠️ Technology Stack

| Layer | Technologies Used |
| :--- | :--- |
| **Frontend Framework** | Next.js 16 (App Router, React 19), Webpack |
| **Styling & Motion** | Tailwind CSS, Framer Motion, Lucide React Icons |
| **Backend API** | Python 3.11, FastAPI, Uvicorn, Pydantic |
| **Database & ORM** | SQLite, SQLAlchemy ORM |
| **Computer Vision** | Roboflow Serverless Hosted Inference API (YOLO) |
| **Generative AI** | Groq API (`llama-3.3-70b-versatile`), OpenAI API (`gpt-4o-mini`) |
| **Authentication** | Passlib (Bcrypt), PyJWT (JSON Web Tokens) |

---

## 📂 Folder Structure

```
intelligent_recipe_generator/
├── backend/
│   ├── app/
│   │   ├── db/              # SQLAlchemy models & SQLite database session
│   │   ├── routes/          # FastAPI routes (auth, recipes, favorites, preferences, recommendations, ai)
│   │   ├── services/        # Business logic (roboflow_service, matching_service, llm_service, instruction_service)
│   │   ├── utils/           # Auth helpers and JWT dependencies
│   │   └── main.py          # FastAPI application entrypoint
│   ├── database/            # SQLite recipes database (recipes.db)
│   ├── dataset/             # Roboflow Computer Vision dataset configurations & YAML
│   ├── ml/                  # ML dataset metadata & scripts
│   ├── enrich_recipes.py    # One-time LLM database enrichment script
│   └── requirements.txt     # Backend Python dependencies
├── frontend/
│   ├── app/                 # Next.js App Router pages (upload, recipes, favorites, profile, preferences)
│   ├── components/          # Reusable UI components (Navbar, RecipeCard, RecipeSkeleton, Chatbot, ProtectedRoute)
│   ├── context/             # React Context state management (AuthContext, AppContext)
│   ├── services/            # Axios API service client & interceptors
│   └── package.json         # Frontend dependencies & scripts
└── README.md
```

---

## 🚀 Quickstart Guide

### Prerequisites
- Python 3.10+
- Node.js 18+ and `npm`

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
copy .env.production.example .env
```

*Configure your `.env` with your `ROBOFLOW_API_KEY`, `GROQ_API_KEY`, and `JWT_SECRET_KEY`.*

Start the FastAPI backend server:
```bash
uvicorn app.main:app --reload --port 8000
```
*API docs available at: `http://127.0.0.1:8000/docs`*

---

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start Next.js development server (Webpack mode)
npm run dev
```

*App available at: `http://localhost:3000`*

---

## 🔐 Environment Variables

### Backend (`backend/.env`)
```env
DATABASE_URL=sqlite:///./database/recipes.db
ROBOFLOW_API_KEY=your_roboflow_key
ROBOFLOW_MODEL_URL=https://serverless.roboflow.com/object-detection-xfoqq/4
GROQ_API_KEY=your_groq_key
OPENAI_API_KEY=your_openai_key
JWT_SECRET_KEY=your_secure_secret_key
JWT_ALGORITHM=HS256
```

### Frontend (`frontend/.env.local`)
```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

---

## 🌐 Production Deployment

- **Frontend**: Deploy `frontend/` to **Vercel** (select Next.js framework preset).
- **Backend**: Deploy `backend/` to **Render** or **Railway** (Build command: `pip install -r requirements.txt`, Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`).

---

## 📜 License & Acknowledgments

Developed as part of the **Infosys Springboard Virtual Internship Program**. Special thanks to the open-source culinary datasets, Roboflow CV platform, and Groq/Llama AI communities.
