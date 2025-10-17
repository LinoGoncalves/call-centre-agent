@echo off
set PYTHONIOENCODING=utf-8
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1
set NUMEXPR_NUM_THREADS=1
set OPENBLAS_NUM_THREADS=1
echo Starting Streamlit demo with threading compatibility...
streamlit run src\ui\streamlit_demo.py --server.port=8502