from app.service import analyze_policy


def run(policy_path):
    result = analyze_policy(policy_path)

    print(f"\n✅ Gaps found: {len(result['gaps'])}")
    print("Outputs saved in outputs/")
