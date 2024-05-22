#!/bin/bash
cd app

# uvicorn sb_neural_net_ui:app --host 0.0.0.0 --port 8000 &

streamlit run sb_neural_net_ui.py --server.port=8501 --server.address=0.0.0.0
