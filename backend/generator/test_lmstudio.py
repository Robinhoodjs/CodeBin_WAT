"""Quick diagnostic: test LM Studio connection via langchain_openai."""
import sys, time

ENDPOINT = "http://100.86.216.14:1234/v1"
API_KEY = "sk-lm-wEoH3sNG:Yn5EqrWUfOtb57o2bbGW"
MODEL = "google/gemma-3-4b"

print(f"[1] Importing langchain_openai...", flush=True)
t0 = time.time()
try:
    from langchain_openai import ChatOpenAI
    print(f"    OK ({time.time()-t0:.1f}s)", flush=True)
except Exception as e:
    print(f"    FAIL: {e}", flush=True)
    sys.exit(1)

print(f"[2] Creating ChatOpenAI(model={MODEL})...", flush=True)
t0 = time.time()
try:
    llm = ChatOpenAI(
        model=MODEL,
        base_url=ENDPOINT,
        api_key=API_KEY,
        temperature=0.0,
        max_tokens=100,
    )
    print(f"    OK ({time.time()-t0:.1f}s)", flush=True)
except Exception as e:
    print(f"    FAIL: {e}", flush=True)
    sys.exit(1)

print(f"[3] Invoking llm.invoke('Say hello')...", flush=True)
t0 = time.time()
try:
    result = llm.invoke("Count from 10 to 1")
    print(f"    OK ({time.time()-t0:.1f}s)", flush=True)
    print(f"    Response: {result.content}", flush=True)
except Exception as e:
    print(f"    FAIL: {e}", flush=True)
    sys.exit(1)

print(f"\n[4] Testing langchain.agents.create_agent...", flush=True)
t0 = time.time()
try:
    from langchain.agents import create_agent
    print(f"    OK ({time.time()-t0:.1f}s)", flush=True)
except Exception as e:
    print(f"    FAIL: {e}", flush=True)

print(f"\n[5] Creating agent and invoking...", flush=True)
t0 = time.time()
try:
    agent = create_agent(
        model=llm,
        tools=[],
        system_prompt="You are a helpful assistant. Answer in one word.",
    )
    result = agent.invoke({"messages": [{"role": "user", "content": "Say hello"}]})
    print(f"    OK ({time.time()-t0:.1f}s)", flush=True)
    print(f"    Response: {result['messages'][-1].content}", flush=True)
except Exception as e:
    print(f"    FAIL: {e}", flush=True)

print("\nDone!", flush=True)
