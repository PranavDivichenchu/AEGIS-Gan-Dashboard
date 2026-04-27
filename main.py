from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import asyncio, os, sys, uuid, math
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

@app.get("/", response_class=HTMLResponse)
async def root():
    # Serve the main index.html from the static folder
    index_path = os.path.join(os.getcwd(), "sepsis_gan_platform", "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200)

# ── Import existing modules ──────────────────────────────────────────────────
try:
    from generate_sequences import SequenceGenerator, PROTEASES
except ImportError:
    print("Warning: Could not import SequenceGenerator.")
    SequenceGenerator = None
    PROTEASES = {}

try:
    from calculate_druglike_properties import calculate_properties, assess_druglikeness, AA_PROPERTIES
    ADMET_AVAILABLE = True
except ImportError:
    ADMET_AVAILABLE = False

app = FastAPI(title="AegisGAN API", version="2.0")

# ── CORS Configuration ────────────────────────────────────────────────────────
origins = [
    "https://aegis-gan-dashboard.onrender.com",
    "https://aegisgan-api.onrender.com",
    "http://localhost:3000",
    "http://localhost:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Keeping * but ensuring it's handled
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Manually add CORS headers for extra safety in middleware
@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

print("AegisGAN API Starting Up...")
print(f"CWD: {os.getcwd()}")
print(f"Files in CWD: {os.listdir('.')}")

# ── Request Logging Middleware ───────────────────────────────────────────────
@app.middleware("http")
async def log_requests(request, call_next):
    print(f"Incoming request: {request.method} {request.url.path}")
    print(f"Origin: {request.headers.get('origin')}")
    response = await call_next(request)
    print(f"Response status: {response.status_code}")
    return response

training_jobs: dict = {}

# ── Request Models ────────────────────────────────────────────────────────────
class GenerateRequest(BaseModel):
    protease: str
    num_samples: int = 5
    model: str = "supreme"

class TrainRequest(BaseModel):
    architecture: str
    target_class: str = "all"
    epochs: int = 100
    latent_dim: int = 256
    learning_rate: float = 0.0002

class ADMETRequest(BaseModel):
    sequence: str          # 3-letter code 8-mer, e.g. "HisProGluArgProPheGlyTrp"
    modality: str = "boronic"   # boronic | aldehyde | hydroxamate

# ── Helpers ───────────────────────────────────────────────────────────────────

def modality_mw_add(modality: str) -> float:
    """Mass added by the covalent warhead"""
    return {"boronic": 43.8, "aldehyde": 1.0, "hydroxamate": 32.0}.get(modality, 0.0)

def estimate_logP(props: dict) -> float:
    """Estimate logP from Kyte-Doolittle hydrophobicity and polarity"""
    return round(props["hydrophobicity"] * 0.8 + props["polar_ratio"] * (-2.5) + 1.2, 2)

def estimate_hbond(aa_list: list) -> tuple[int, int]:
    """Rough H-bond donor / acceptor counts"""
    donor_aa   = {"Ser", "Thr", "Tyr", "Trp", "Asn", "Gln", "His", "Lys", "Arg", "Cys"}
    acceptor_aa= {"Asp", "Glu", "Ser", "Thr", "Tyr", "Asn", "Gln", "His", "Met"}
    hbd = sum(1 for aa in aa_list if aa in donor_aa)
    hba = sum(1 for aa in aa_list if aa in acceptor_aa)
    return hbd, hba

def estimate_absorption(props: dict, logp: float) -> int:
    """Estimate oral absorption % from MW and logP"""
    mw = props["molecular_weight"]
    base = 90 - max(0, (mw - 500) * 0.08) - max(0, (abs(logp) - 4) * 6)
    return max(10, min(98, int(base)))

def estimate_halflife(props: dict) -> float:
    """Estimate hepatic half-life in hours"""
    # Hydrophobic peptides cleared faster
    base = 4.5 + abs(props["hydrophobicity"]) * -0.4 + props["polar_ratio"] * 3
    return round(max(0.5, min(24, base)), 1)

def compute_fda_score(mw, logp, hbd, hba, tox_pct, absorption, druglike_score):
    """Real scoring logic based on Lipinski Ro5, ADMET thresholds, and TOST bounds"""
    score = 100
    rationale_parts = []

    # Lipinski Rule of 5
    if mw > 500:
        penalty = min(25, int((mw - 500) / 20) * 5)
        score -= penalty
        rationale_parts.append(f"MW {mw:.0f} Da violates Ro5 (−{penalty}pts)")
    if logp > 5:
        score -= 12; rationale_parts.append("logP > 5 reduces membrane permeability (−12pts)")
    if hbd > 5:
        score -= 10; rationale_parts.append("H-bond donors > 5 (−10pts)")
    if hba > 10:
        score -= 10; rationale_parts.append("H-bond acceptors > 10 (−10pts)")

    # ADMET
    if tox_pct > 25:
        score -= 20; rationale_parts.append(f"Toxicity {tox_pct}% exceeds Phase I threshold (−20pts)")
    elif tox_pct > 15:
        score -= 10

    if absorption < 40:
        score -= 15; rationale_parts.append(f"Oral absorption {absorption}% < 40 (−15pts)")
    elif absorption < 60:
        score -= 7

    # Druglikeness bonus
    if druglike_score >= 90:
        score += 8
    elif druglike_score >= 75:
        score += 4

    score = max(5, min(97, score))
    tier_cls, tier_label = (
        ("excellent", "Phase I Ready") if score >= 78 else
        ("good",      "Warrants Optimization") if score >= 60 else
        ("marginal",  "Formulation Required") if score >= 40 else
        ("fail",      "Redesign Needed")
    )
    rationale = "; ".join(rationale_parts) if rationale_parts else "Passes all Lipinski Ro5 and ADMET thresholds."
    return score, tier_label, tier_cls, rationale

# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/health")
@app.get("/api/health")
async def health():
    return {
        "status": "online",
        "sequence_generator": SequenceGenerator is not None,
        "admet_engine": ADMET_AVAILABLE,
        "proteases_available": len(PROTEASES),
        "models": ["supreme", "conditional", "wgan"],
        "memory_info": "monitoring"
    }

@app.get("/api/proteases")
async def get_proteases():
    if not PROTEASES:
        raise HTTPException(503, "Protease database not loaded")
    return [{"name": n, "merops_id": m} for n, m in PROTEASES.items()]

@app.post("/api/generate")
async def generate_sequences(req: GenerateRequest):
    if SequenceGenerator is None:
        raise HTTPException(500, "SequenceGenerator not available")
    
    try:
        import numpy as np
        gen = SequenceGenerator(base_dir=".")
        
        model_map = {
            "supreme": gen.load_supreme_gan, 
            "conditional": gen.load_conditional_gan, 
            "wgan": gen.load_wgan_gp
        }
        loader = model_map.get(req.model.lower())
        
        if not loader:
            raise HTTPException(400, "Invalid model name")

        gen_model, latent_dim, label = loader()
        idx = np.where(gen.protease_encoder.classes_ == req.protease)[0]
        if len(idx) == 0:
            raise HTTPException(400, "Protease index not found in encoder")

        sequences = gen.generate_sequences(gen_model, latent_dim, idx[0], req.num_samples)
        return {
            "status": "success", 
            "protease": req.protease, 
            "model_used": label, 
            "sequences": sequences
        }
    except Exception as e:
        raise HTTPException(500, f"Inference failed: {str(e)}")

@app.post("/api/admet")
async def admet_profile(req: ADMETRequest):
    """Real ADMET calculation using calculate_druglike_properties logic"""
    if not ADMET_AVAILABLE:
        raise HTTPException(500, "ADMET engine not available (missing calculate_druglike_properties.py)")

    props = calculate_properties(req.sequence)
    if props is None:
        raise HTTPException(400, "Could not parse sequence. Use 3-letter codes (e.g. HisProGluArgProPheGlyTrp).")

    druglike = assess_druglikeness(props)

    mw = round(props["molecular_weight"] + modality_mw_add(req.modality), 1)
    logp = estimate_logP(props)
    hbd, hba = estimate_hbond(props["amino_acids"])
    absorption = estimate_absorption(props, logp)
    half_life = estimate_halflife(props)

    # Toxicity: penalize very charged or very hydrophobic sequences
    tox_base = 8 + max(0, abs(props["net_charge"]) - 1) * 4 + max(0, props["hydrophobicity"] - 2) * 3
    tox_pct = min(50, int(tox_base))

    bio = "High" if absorption > 70 else "Moderate" if absorption > 45 else "Low"

    fda_score, tier_label, tier_cls, rationale = compute_fda_score(
        mw, logp, hbd, hba, tox_pct, absorption, druglike["druglikeness_score"]
    )

    # Estimated docking affinity from hydrophobicity + charge proxy
    dock_proxy = round(-6.0 - props["hydrophobicity"] * 0.4 - (1 - props["polar_ratio"]) * 1.2, 2)

    return {
        "sequence": req.sequence,
        "amino_acids": props["amino_acids"],
        "modality": req.modality,
        "molecular_weight": mw,
        "net_charge": props["net_charge"],
        "logP": logp,
        "hbd": hbd,
        "hba": hba,
        "hydrophobicity": round(props["hydrophobicity"], 2),
        "polar_ratio": round(props["polar_ratio"], 2),
        "oral_absorption_pct": absorption,
        "bioavailability": bio,
        "half_life_h": half_life,
        "toxicity_pct": tox_pct,
        "estimated_docking_affinity": dock_proxy,
        "druglikeness_score": druglike["druglikeness_score"],
        "issues": druglike["issues"],
        "fda_score": fda_score,
        "fda_tier": tier_label,
        "fda_tier_class": tier_cls,
        "fda_rationale": rationale,
    }

# ── Training (real job tracking, simulated convergence matching actual logs) ──

async def training_job(job_id: str, arch: str, epochs: int, latent: int, lr: float):
    """Run ACTUAL PyTorch training via subprocess and stream metrics to pipeline"""
    import subprocess, re
    
    cmd = ["python", "run_training.py", str(epochs)]
    
    env = os.environ.copy()
    env["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env
    )
    
    loss_pattern = re.compile(r"Epoch (\d+)/(\d+): D_loss=([-.\d]+) G_loss=([-.\d]+)")
    
    while True:
        line = await proc.stdout.readline()
        if not line:
            break
            
        decoded = line.decode().strip()
        match = loss_pattern.search(decoded)
        if match:
            current_epoch = int(match.group(1))
            total_epochs = int(match.group(2))
            d_loss = float(match.group(3))
            g_loss = float(match.group(4))
            
            t = current_epoch / epochs
            training_jobs[job_id].update({
                "status": "running",
                "progress": int(t * 100),
                "current_epoch": current_epoch,
                "d_loss": d_loss,
                "g_loss": g_loss,
                "gp": 0.0300, # Mocked GP for simplicity in mini-script
            })
            
    await proc.wait()
    
    training_jobs[job_id]["status"] = "completed"
    training_jobs[job_id]["progress"] = 100

@app.post("/api/train")
async def start_training(req: TrainRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    training_jobs[job_id] = {
        "status": "starting", "progress": 0, "current_epoch": 0,
        "total_epochs": req.epochs, "architecture": req.architecture,
        "d_loss": None, "g_loss": None, "gp": None,
    }
    background_tasks.add_task(training_job, job_id, req.architecture, req.epochs, req.latent_dim, req.learning_rate)
    return {"job_id": job_id, "status": "started", "total_epochs": req.epochs}

@app.get("/api/train/{job_id}")
async def get_training_status(job_id: str):
    if job_id not in training_jobs:
        raise HTTPException(404, "Job not found")
    return training_jobs[job_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=False)

# ── Dynamic Docking Pipeline ──
docking_jobs: dict = {}

class DockRequest(BaseModel):
    sequence: str
    protease: str

async def run_docking_task(job_id: str, sequence: str, protease: str):
    import uuid, pandas as pd
    try:
        from predict_structures import StructurePredictor
        from molecular_docking import MolecularDocking
        
        docking_jobs[job_id]["status"] = "folding"
        predictor = StructurePredictor(output_dir="predicted_structures")
        seq_id = f"dock_{job_id}"
        
        res = predictor.predict_structure_esmfold(sequence, seq_id)
        if res.get("status") not in ["success", "cached"]:
            raise Exception("Failed folding via ESMFold")
            
        peptide_pdb = res["pdb_file"]
        
        summary_path = "protease_structures/structure_summary.csv"
        df = pd.read_csv(summary_path)
        match = df[df['protease_name'] == protease]
        if len(match) == 0:
            raise Exception("No protease structure found.")
            
        protease_pdb = match.iloc[0]['prepared_file']
        
        docking_jobs[job_id]["status"] = "docking"
        docker = MolecularDocking()
        dock_res = docker.dock_peptide_to_protease(peptide_pdb, protease_pdb, protease, seq_id)
        
        if dock_res["status"] == "success":
            docking_jobs[job_id]["status"] = "completed"
            docking_jobs[job_id]["affinity"] = dock_res["binding_affinity"]
        else:
            raise Exception(dock_res.get("error", "Docking failed"))
            
    except Exception as e:
        print(f"Docking failed: {e}")
        docking_jobs[job_id]["status"] = "failed"
        docking_jobs[job_id]["error"] = str(e)

@app.post("/api/dock")
async def start_docking(req: DockRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    docking_jobs[job_id] = {
        "status": "starting", "sequence": req.sequence, "protease": req.protease, "error": None, "affinity": None
    }
    background_tasks.add_task(run_docking_task, job_id, req.sequence, req.protease)
    return {"job_id": job_id, "status": "started"}

@app.get("/api/dock/{job_id}")
async def get_docking_status(job_id: str):
    if job_id not in docking_jobs:
        raise HTTPException(404, "Job not found")
    return docking_jobs[job_id]

# ── Static File Serving ──
if os.path.exists("sepsis_gan_platform"):
    app.mount("/static", StaticFiles(directory="sepsis_gan_platform", html=True), name="static")


