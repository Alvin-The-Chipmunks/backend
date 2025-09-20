# 🗺️ 🌴 Soflo Atlas Backend

Python x FastAPI-powered backend service delivering statistics and AI insights for the Soflo Atlas application

---

## 🔑 Key Features  

- 📊 **ATTOM API Integration** – Fetches community and census data for a given ZIP code via the Attom API https://api.developer.attomdata.com/docs
- 🤖 **OpenAI API Integration** – Generates LLM insights about the user's selected category and location
- 🐳 **Docker Support** – Includes a `Dockerfile` so the app can be run in a container packaged with all necessary Python dependencies
```bash
docker build -t soflo-atlas .
docker run --name soflo-atlas -p 8000:8000 soflo-atlas
```

---