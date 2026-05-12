
import json

def calculate_comparison(iteration1_results, iteration2_results):
    """
    Simple script to compare the precision/recall metrics 
    from two Azure Custom Vision iterations.
    """
    print("--- MODEL DOMAIN COMPARISON ---")
    print(f"{'Metric':<15} | {'General':<15} | {'General [A1]':<15}")
    print("-" * 50)
    
    metrics = ['Precision', 'Recall', 'mAP']
    
    for m in metrics:
        v1 = iteration1_results.get(m, 0)
        v2 = iteration2_results.get(m, 0)
        diff = v2 - v1
        trend = "↑" if diff > 0 else "↓"
        print(f"{m:<15} | {v1:>14.1f}% | {v2:>14.1f}% ({trend} {abs(diff):.1f}%)")

if __name__ == "__main__":
    # Mock data from assignment performance dashboard
    general_domain = {"Precision": 84.2, "Recall": 81.5, "mAP": 83.8}
    a1_domain = {"Precision": 91.5, "Recall": 88.7, "mAP": 90.4}
    
    calculate_comparison(general_domain, a1_domain)
