FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yml .

RUN conda env create -f environment.yml

COPY ./src ./src

CMD ["conda", "run", "-n", "llm-agent", "streamlit", "run", "src/app.py"]