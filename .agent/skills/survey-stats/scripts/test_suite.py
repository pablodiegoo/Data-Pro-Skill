
import pandas as pd
import numpy as np
import os
import sys

# Ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from turf_analysis import run_turf_analysis
from survey_pca import run_survey_pca
from visuals import plot_weighted_bars

def test_everything():
    print("--- Starting Test Suite ---")
    
    # 1. Dummy Data Creation
    print("Creating dummy data...")
    df = pd.DataFrame({
        'Resp_ID': range(100),
        'Weight': np.random.uniform(0.8, 1.2, 100),
        'Q_A': np.random.choice([0, 1], 100, p=[0.7, 0.3]),
        'Q_B': np.random.choice([0, 1], 100, p=[0.6, 0.4]),
        'Q_C': np.random.choice([0, 1], 100, p=[0.5, 0.5]),
        'Multi_Resp': np.random.choice(['A;B', 'A', 'B;C', 'C', ''], 100)
    })
    
    # 2. Test TURF
    print("\n[TEST] TURF Analysis")
    try:
        res = run_turf_analysis(df, ['Q_A', 'Q_B', 'Q_C'], n_max_size=2)
        print("Success! Result head:")
        print(res.head(2))
    except Exception as e:
        print(f"FAILED: {e}")

    # 3. Test PCA (Multi-response)
    print("\n[TEST] Survey PCA (Multi-response)")
    try:
        loadings, scores, var = run_survey_pca(df, ['Multi_Resp'], sep=';')
        print("Success! Explained Variance:")
        print(var)
    except Exception as e:
        print(f"FAILED: {e}")

    # 4. Test Visuals
    print("\n[TEST] Weighted Visuals")
    try:
        plot_weighted_bars(df, ['Q_A', 'Q_B', 'Q_C'], "Test Chart", 'test_chart.png', weight_col='Weight')
        if os.path.exists('test_chart.png'):
            print("Success! Chart generated.")
            os.remove('test_chart.png')
        else:
            print("FAILED: Chart file not found.")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    test_everything()
