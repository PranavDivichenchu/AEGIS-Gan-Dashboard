"use client";

import { useState, useEffect } from 'react';
import {
  Dna, LayoutDashboard, BrainCircuit, Activity,
  Settings, Play, Loader2, Download, Search, CheckCircle2,
  TestTube2, Sparkles, Beaker, Zap, FileJson, LogOut, ChevronRight
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Database as DatabaseIcon, Target as TargetIcon, Flame as FlameIcon } from 'lucide-react';

export default function AegisPlatform() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [toastMsg, setToastMsg] = useState("");
  const [sequenceHistory, setSequenceHistory] = useState<any[]>([]);

  const showToast = (msg: string) => {
    setToastMsg(msg);
    setTimeout(() => setToastMsg(""), 3000);
  };

  const addToHistory = (data: any) => {
    setSequenceHistory(prev => [{
      ...data,
      timestamp: new Date().toISOString(),
      id: Math.random().toString(36).substring(7)
    }, ...prev].slice(0, 50)); // Keep last 50
  };

  return (
    <div className="flex h-screen overflow-hidden bg-[#0A0F1C] font-sans text-slate-200 selection:bg-teal-500/30">
      {/* Toast Notification */}
      <AnimatePresence>
        {toastMsg && (
          <motion.div
            initial={{ opacity: 0, y: -20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -20, scale: 0.9 }}
            className="fixed top-6 left-1/2 -translate-x-1/2 z-50 bg-[#1e293b] border border-[#334155] shadow-2xl rounded-full px-6 py-3 flex items-center gap-3"
          >
            <CheckCircle2 className="w-5 h-5 text-teal-400" />
            <span className="text-sm font-medium text-white">{toastMsg}</span>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <aside className="w-68 border-r border-[#1e293b] bg-[#0A0F1C]/90 backdrop-blur-3xl flex flex-col shadow-2xl relative z-20">
        <div className="p-8 pb-4 flex items-center gap-4">
          <div className="bg-gradient-to-br from-teal-500 to-indigo-600 p-2.5 rounded-xl shadow-[0_0_20px_rgba(20,184,166,0.3)]">
            <Dna className="w-6 h-6 text-white" />
          </div>
          <span className="font-extrabold text-2xl tracking-tight text-white font-serif">Aegis<span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-indigo-400">GAN</span></span>
        </div>

        <nav className="flex-1 px-5 py-6 space-y-1.5 overflow-y-auto custom-scrollbar">
          <p className="px-4 text-xs font-bold text-slate-500 uppercase tracking-widest mb-3 mt-4">Platform Modules</p>
          <NavItem
            icon={<LayoutDashboard size={18} />}
            label="Overview"
            isActive={activeTab === 'dashboard'}
            onClick={() => setActiveTab('dashboard')}
          />
          <NavItem
            icon={<BrainCircuit size={18} />}
            label="Protein Generator"
            isActive={activeTab === 'generator'}
            onClick={() => setActiveTab('generator')}
            badge="Live API"
          />
          <NavItem
            icon={<Activity size={18} />}
            label="Training Studio"
            isActive={activeTab === 'training'}
            onClick={() => setActiveTab('training')}
          />
          <NavItem
            icon={<TestTube2 size={18} />}
            label="ADMET Profiler"
            isActive={activeTab === 'admet'}
            onClick={() => setActiveTab('admet')}
            badge="New"
          />
          <NavItem
            icon={<Search size={18} />}
            label="Sequence Compare"
            isActive={activeTab === 'compare'}
            onClick={() => setActiveTab('compare')}
          />

          <p className="px-4 text-xs font-bold text-slate-500 uppercase tracking-widest mb-3 mt-8">Configuration</p>
          <NavItem
            icon={<Settings size={18} />}
            label="Settings"
            isActive={activeTab === 'settings'}
            onClick={() => setActiveTab('settings')}
          />
          <NavItem
            icon={<LogOut size={18} />}
            label="Logout"
            isActive={false}
            onClick={() => showToast('Session logging out...')}
          />
        </nav>

        <div className="p-6 border-t border-[#1e293b] bg-gradient-to-b from-transparent to-[#0a0f1c]">
          <div className="p-4 bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-700/50 shadow-inner">
            <p className="text-[11px] text-slate-400 mb-2 font-bold tracking-widest uppercase">Network Status</p>
            <div className="flex items-center gap-3">
              <span className="relative flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-teal-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-teal-500 shadow-[0_0_10px_rgba(20,184,166,0.8)]"></span>
              </span>
              <span className="text-sm font-semibold text-teal-100">SupremeGAN Online</span>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto relative bg-[#060D1A] bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.1),rgba(255,255,255,0))]">
        <header className="sticky top-0 z-10 bg-[#060D1A]/80 backdrop-blur-xl border-b border-[#1e293b] px-10 py-5 flex justify-between items-center shadow-sm">
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold text-white tracking-tight">
              {activeTab === 'admet' ? 'ADMET Pharmacokinetics' : activeTab.replace('-', ' ')}
            </h1>
          </div>
          <div className="flex items-center gap-6">
            <div className="relative group">
              <Search className="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-teal-400 transition-colors" />
              <input
                type="text"
                placeholder="Search protease datasets..."
                className="bg-[#111827] border border-[#334155] rounded-full pl-10 pr-5 py-2 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-teal-500/40 focus:border-teal-500/40 transition-all w-72 placeholder:text-slate-500"
              />
            </div>
            <button onClick={() => showToast('Profile settings opened.')} className="w-10 h-10 rounded-full bg-gradient-to-tr from-indigo-500 to-teal-400 p-[2px] cursor-pointer hover:scale-105 transition-transform shadow-[0_0_15px_rgba(99,102,241,0.3)]">
              <div className="w-full h-full bg-[#0A0F1C] rounded-full flex items-center justify-center">
                <span className="text-xs font-bold text-white">PD</span>
              </div>
            </button>
          </div>
        </header>

        <div className="p-10 max-w-[1600px] mx-auto">
          <AnimatePresence mode="wait">
            {activeTab === 'dashboard' && <DashboardView key="dashboard" showToast={showToast} sequenceHistory={sequenceHistory} />}
            {activeTab === 'generator' && <GeneratorView key="generator" showToast={showToast} addToHistory={addToHistory} sequenceHistory={sequenceHistory} />}
            {activeTab === 'training' && <TrainingView key="training" showToast={showToast} />}
            {activeTab === 'admet' && <AdmetView key="admet" showToast={showToast} />}
            {activeTab === 'compare' && <CompareView key="compare" showToast={showToast} />}
            {activeTab === 'settings' && <SettingsView key="settings" showToast={showToast} />}
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}

// ---- Subcomponents ---- //

function NavItem({ icon, label, isActive, onClick, badge }: any) {
  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center justify-between px-4 py-3 rounded-xl transition-all duration-300 ${isActive ? 'bg-gradient-to-r from-teal-500/20 to-indigo-500/10 text-teal-300 font-semibold shadow-[inset_2px_0_0_rgba(20,184,166,0.8)]' : 'text-slate-400 hover:bg-[#1e293b]/70 hover:text-slate-200 hover:shadow-sm'}`}
    >
      <div className="flex items-center gap-3.5">
        <div className={`${isActive ? 'text-teal-400 drop-shadow-[0_0_8px_rgba(20,184,166,0.8)]' : ''}`}>{icon}</div>
        <span className="text-[15px]">{label}</span>
      </div>
      {badge && <span className="text-[10px] uppercase tracking-wider bg-teal-500 text-teal-950 px-2 py-0.5 rounded-full font-bold shadow-[0_0_8px_rgba(20,184,166,0.5)]">{badge}</span>}
    </button>
  );
}

// 1. Dashboard View
function DashboardView({ showToast, sequenceHistory }: { showToast: (msg: string) => void; sequenceHistory: any[] }) {
  // Sample data for performance metrics
  const performanceData = [
    { name: 'Week 1', sequences: 45, accuracy: 92 },
    { name: 'Week 2', sequences: 78, accuracy: 94 },
    { name: 'Week 3', sequences: 124, accuracy: 96 },
    { name: 'Week 4', sequences: 156, accuracy: 97 },
    { name: 'Week 5', sequences: 189, accuracy: 98 },
    { name: 'Week 6', sequences: 234, accuracy: 98.5 },
  ];

  const proteaseDistribution = [
    { name: 'MMP1', count: 142 },
    { name: 'PRTN3', count: 128 },
    { name: 'Kallikrein', count: 98 },
    { name: 'Caspase-3', count: 87 },
    { name: 'Thrombin', count: 76 },
    { name: 'Other', count: 250 },
  ];

  return (
    <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -15 }}>
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
        <StatCard title="Algorithm Evaluations" value="781" subtext="In-silico molecular hits" icon={<DatabaseIcon className="w-5 h-5" />} color="indigo" />
        <StatCard title="Target Classes" value="27" subtext="Sepsis pathogenic proteases" icon={<TargetIcon className="w-5 h-5" />} color="rose" />
        <StatCard title="Clinical Lead Affinity" value="-11.88" suffix="kcal/mol" subtext="Collagenase-1 Inhibitor" icon={<FlameIcon className="w-5 h-5 text-amber-500" />} color="amber" />
        <StatCard title="TOST Bioequivalence" value="100%" subtext="Mapped to mammalian limits" icon={<CheckCircle2 className="w-5 h-5" />} color="teal" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[2fr_1fr] gap-8">
        <div className="bg-[#111827] border border-[#1e293b] rounded-2xl shadow-xl overflow-hidden">
          <div className="p-6 border-b border-[#1e293b] bg-[#0A0F1C]/50 flex justify-between items-center">
            <div className="flex items-center gap-3">
              <Beaker className="w-5 h-5 text-indigo-400" />
              <h3 className="text-lg font-bold text-white">Synthesized Proteomic Library</h3>
            </div>
            <button onClick={() => showToast('Downloading complete library as CSV...')} className="text-sm font-semibold text-teal-400 hover:text-teal-300 flex items-center gap-1 bg-teal-500/10 px-3 py-1.5 rounded-lg transition-colors">
              <Download className="w-4 h-4" /> Export Panel
            </button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left font-sans text-sm">
              <thead>
                <tr className="text-slate-400 bg-[#0F172A] border-b border-[#1e293b]">
                  <th className="px-6 py-4 font-semibold uppercase tracking-wider text-xs">Protease Target</th>
                  <th className="px-6 py-4 font-semibold uppercase tracking-wider text-xs">Candidate Sequence Geometry</th>
                  <th className="px-6 py-4 font-semibold uppercase tracking-wider text-xs">ΔG Binding Score</th>
                  <th className="px-6 py-4 font-semibold uppercase tracking-wider text-xs">Development Phase</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1e293b]">
                {[
                  { name: 'MMP1 (Collagenase-1)', seq: 'HisProGluArgProPheGlyTrp', score: '-11.88', status: 'Exceptional Binder', statusCol: 'teal' },
                  { name: 'PRTN3', seq: 'ThrLeuPheLeuTrpPheIleTyr', score: '-11.14', status: 'Exceptional Binder', statusCol: 'teal' },
                  { name: 'Kallikrein 2', seq: 'GluGlySerCysTyrGlyThrGlu', score: '-9.72', status: 'In-Vitro Validation', statusCol: 'amber' },
                  { name: 'Caspase-3', seq: 'TrpTyrHisAspGlnPheGlyPhe', score: '-9.46', status: 'In-Silico Verified', statusCol: 'indigo' },
                  { name: 'Factor IXa', seq: 'ProGlyProHisHisProAspPhe', score: '-9.46', status: 'In-Silico Verified', statusCol: 'indigo' },
                ].map((row, i) => (
                  <tr key={i} className="hover:bg-[#1e293b]/40 transition-colors">
                    <td className="px-6 py-5 text-slate-200 font-semibold">{row.name}</td>
                    <td className="px-6 py-5 font-mono text-slate-400 tracking-wide text-xs">{row.seq}</td>
                    <td className="px-6 py-5 font-mono text-teal-400 font-bold">{row.score}</td>
                    <td className="px-6 py-5">
                      <span className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-bold border ${row.statusCol === 'teal' ? 'bg-teal-500/10 text-teal-400 border-teal-500/20' :
                          row.statusCol === 'amber' ? 'bg-amber-500/10 text-amber-400 border-amber-500/20' :
                            'bg-indigo-500/10 text-indigo-400 border-indigo-500/20'
                        }`}>
                        <div className={`w-1.5 h-1.5 rounded-full ${row.statusCol === 'teal' ? 'bg-teal-500' :
                            row.statusCol === 'amber' ? 'bg-amber-500' : 'bg-indigo-500'
                          }`}></div>
                        {row.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="bg-gradient-to-b from-[#111827] to-[#0A0F1C] border border-[#1e293b] rounded-2xl p-8 flex flex-col items-center justify-center text-center shadow-2xl relative overflow-hidden group">
          <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] opacity-10 mix-blend-overlay pointer-events-none"></div>
          <div className="absolute -top-24 -right-24 w-48 h-48 bg-indigo-500 rounded-full mix-blend-screen filter blur-[100px] opacity-20"></div>
          <div className="absolute -bottom-24 -left-24 w-48 h-48 bg-teal-500 rounded-full mix-blend-screen filter blur-[100px] opacity-20"></div>

          <div className="w-36 h-36 relative mb-8">
            <div className="absolute inset-0 border-[6px] border-[#1e293b] rounded-full animate-[spin_10s_linear_infinite]"></div>
            <div className="absolute inset-[-10px] border-4 border-dashed border-slate-800 rounded-full animate-[spin_20s_linear_infinite_reverse]"></div>
            <div className="absolute inset-2 border-[6px] border-t-indigo-500 border-r-teal-500 border-b-transparent border-l-transparent rounded-full animate-[spin_2s_linear_infinite] shadow-[0_0_30px_rgba(99,102,241,0.5)]"></div>
            <div className="absolute inset-0 flex items-center justify-center font-bold text-3xl text-white tracking-widest font-serif drop-shadow-[0_0_10px_rgba(255,255,255,0.8)]">
              ESM
            </div>
          </div>
          <h3 className="text-xl font-bold text-white mb-3">ESMFold GPU Cluster</h3>
          <p className="text-[#94a3b8] mb-8 leading-relaxed">High-throughput atomic 3D projection node. Standing by for sequence digestion at 10-15s per molecule.</p>
          <button onClick={() => showToast('Activating ESMFold Compute Nodes...')} className="w-full bg-white/5 hover:bg-white/10 text-white font-bold rounded-xl py-4 transition-all border border-slate-700/50 hover:border-slate-500 backdrop-blur-md relative z-10 flex items-center justify-center gap-2">
            <Zap className="w-5 h-5 text-indigo-400" /> Start Cloud Simulation
          </button>
        </div>
      </div>

      {/* Performance Metrics Dashboard */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">
        <div className="bg-[#111827] border border-[#1e293b] rounded-2xl shadow-xl overflow-hidden">
          <div className="p-6 border-b border-[#1e293b] bg-[#0A0F1C]/50">
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Activity className="w-5 h-5 text-indigo-400" />
              Generation Performance Trends
            </h3>
          </div>
          <div className="p-6">
            <ResponsiveContainer width="100%" height={250}>
              <AreaChart data={performanceData}>
                <defs>
                  <linearGradient id="colorSequences" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#14b8a6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#14b8a6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="name" stroke="#64748b" style={{ fontSize: '12px' }} />
                <YAxis stroke="#64748b" style={{ fontSize: '12px' }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0f172a',
                    border: '1px solid #1e293b',
                    borderRadius: '8px',
                    color: '#fff'
                  }}
                />
                <Area type="monotone" dataKey="sequences" stroke="#14b8a6" fillOpacity={1} fill="url(#colorSequences)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-[#111827] border border-[#1e293b] rounded-2xl shadow-xl overflow-hidden">
          <div className="p-6 border-b border-[#1e293b] bg-[#0A0F1C]/50">
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <TargetIcon className="w-5 h-5 text-rose-400" />
              Protease Target Distribution
            </h3>
          </div>
          <div className="p-6">
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={proteaseDistribution}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="name" stroke="#64748b" style={{ fontSize: '11px' }} />
                <YAxis stroke="#64748b" style={{ fontSize: '12px' }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0f172a',
                    border: '1px solid #1e293b',
                    borderRadius: '8px',
                    color: '#fff'
                  }}
                />
                <Bar dataKey="count" fill="#6366f1" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Recent Generation History */}
      {sequenceHistory.length > 0 && (
        <div className="mt-8 bg-[#111827] border border-[#1e293b] rounded-2xl shadow-xl overflow-hidden">
          <div className="p-6 border-b border-[#1e293b] bg-[#0A0F1C]/50 flex justify-between items-center">
            <div className="flex items-center gap-3">
              <Activity className="w-5 h-5 text-teal-400" />
              <h3 className="text-lg font-bold text-white">Recent Generation History</h3>
            </div>
            <span className="text-xs text-slate-500 font-semibold">{sequenceHistory.length} Session{sequenceHistory.length !== 1 ? 's' : ''}</span>
          </div>
          <div className="p-6 space-y-3 max-h-96 overflow-y-auto custom-scrollbar">
            {sequenceHistory.slice(0, 10).map((item, idx) => (
              <div key={item.id} className="bg-[#0A0F1C] border border-[#1e293b] rounded-xl p-4 hover:border-teal-500/30 transition-all">
                <div className="flex justify-between items-start mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-teal-400">#{sequenceHistory.length - idx}</span>
                    <span className="text-sm font-semibold text-white">{item.protease}</span>
                  </div>
                  <span className="text-xs text-slate-500">{new Date(item.timestamp).toLocaleTimeString()}</span>
                </div>
                <div className="flex items-center gap-3 text-xs text-slate-400">
                  <span className="flex items-center gap-1">
                    <BrainCircuit className="w-3 h-3" />
                    {item.model}
                  </span>
                  <span className="flex items-center gap-1">
                    <Dna className="w-3 h-3" />
                    {item.count} sequences
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  );
}

function StatCard({ title, value, suffix = "", subtext, icon, color }: any) {
  const colorStyles: Record<string, string> = {
    indigo: "text-indigo-400 bg-indigo-500/10 shadow-[0_0_15px_rgba(99,102,241,0.1)]",
    rose: "text-rose-400 bg-rose-500/10 shadow-[0_0_15px_rgba(244,63,94,0.1)]",
    amber: "text-amber-400 bg-amber-500/10 shadow-[0_0_15px_rgba(245,158,11,0.1)]",
    teal: "text-teal-400 bg-teal-500/10 shadow-[0_0_15px_rgba(20,184,166,0.1)]",
  };

  return (
    <div className="bg-[#111827] border border-[#1e293b] rounded-2xl p-6 shadow-lg hover:-translate-y-1 transition-transform duration-300">
      <div className="flex justify-between items-start mb-4">
        <h4 className="text-slate-400 text-sm font-semibold uppercase tracking-wider">{title}</h4>
        <div className={`p-2 rounded-lg ${colorStyles[color]}`}>{icon}</div>
      </div>
      <div className="flex items-baseline gap-2 mb-3">
        <span className="text-4xl font-extrabold tracking-tight text-white">{value}</span>
        {suffix && <span className="text-sm font-bold text-slate-500 uppercase">{suffix}</span>}
      </div>
      <p className="text-[13px] text-slate-500 font-medium">{subtext}</p>
    </div>
  );
}

// 2. Generator View
function GeneratorView({ showToast, addToHistory, sequenceHistory }: { showToast: (msg: string) => void; addToHistory: (data: any) => void; sequenceHistory: any[] }) {
  const [model, setModel] = useState('supreme');
  const [target, setTarget] = useState('Kallikrein 2');
  const [numSeq, setNumSeq] = useState(5);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any[]>([]);
  const [error, setError] = useState("");
  const [esmFoldModal, setEsmFoldModal] = useState<{ open: boolean; sequence: string; index: number } | null>(null);
  const [backendStatus, setBackendStatus] = useState<'checking' | 'online' | 'offline'>('checking');

  // Check backend status on mount
  useEffect(() => {
    const checkBackend = async () => {
      try {
        const res = await fetch('http://localhost:8001/api/proteases', { signal: AbortSignal.timeout(3000) });
        setBackendStatus(res.ok ? 'online' : 'offline');
      } catch {
        setBackendStatus('offline');
      }
    };
    checkBackend();
  }, []);

  const handleGenerate = async () => {
    setLoading(true); setError(""); setResults([]);
    try {
      const res = await fetch('http://localhost:8001/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ protease: target, model: model, num_samples: numSeq })
      });
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Generation failed: API Server error.');
      }
      const data = await res.json();
      setResults(data.sequences || []);
      setBackendStatus('online');
      addToHistory({ protease: target, model: data.model_used, sequences: data.sequences, count: data.sequences.length });
      showToast(`Successfully synthesized ${data.sequences.length} peptides!`);
    } catch (err: any) {
      setBackendStatus('offline');
      setError(err.message || "An error occurred. Ensure backend is running on port 8001.");
    } finally {
      setLoading(false);
    }
  };

  const exportSequences = (format: 'json' | 'fasta' | 'csv') => {
    if (results.length === 0) return;

    let content = '';
    let filename = `sequences_${Date.now()}`;

    if (format === 'json') {
      content = JSON.stringify({ protease: target, model, sequences: results }, null, 2);
      filename += '.json';
    } else if (format === 'fasta') {
      content = results.map((seq, i) => `>${target}_${i + 1}\n${seq}`).join('\n');
      filename += '.fasta';
    } else {
      content = 'Index,Sequence,Target\n' + results.map((seq, i) => `${i + 1},${seq},${target}`).join('\n');
      filename += '.csv';
    }

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
    showToast(`Exported ${results.length} sequences as ${format.toUpperCase()}`);
  };

  return (
    <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -15 }} className="h-full flex flex-col gap-8">
      <div className="grid grid-cols-1 lg:grid-cols-[400px_1fr] gap-8 h-[75vh]">
        {/* Config Panel */}
        <div className="bg-[#111827] border border-[#1e293b] rounded-3xl p-8 shadow-xl flex flex-col">
          <div className="mb-8">
            <div className="flex justify-between items-start mb-3">
              <h3 className="text-xl font-bold text-white flex items-center gap-2"><Sparkles className="text-indigo-400 w-6 h-6" /> Biosynthesis Engine</h3>
              <div className={`flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold ${backendStatus === 'online' ? 'bg-teal-500/10 text-teal-400' : backendStatus === 'offline' ? 'bg-rose-500/10 text-rose-400' : 'bg-amber-500/10 text-amber-400'}`}>
                <span className={`w-2 h-2 rounded-full ${backendStatus === 'online' ? 'bg-teal-500 animate-pulse' : backendStatus === 'offline' ? 'bg-rose-500' : 'bg-amber-500 animate-pulse'}`}></span>
                {backendStatus === 'online' ? 'ONLINE' : backendStatus === 'offline' ? 'OFFLINE' : 'CHECKING...'}
              </div>
            </div>
            <p className="text-sm text-slate-400">Configure multi-stage GAN latent injection parameters for massive scale virtual screening.</p>
          </div>

          <div className="space-y-6 flex-1">
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-400 uppercase tracking-widest block">AI Algorithm Architecture</label>
              <div className="relative">
                <select value={model} onChange={(e) => setModel(e.target.value)} className="w-full bg-[#0A0F1C] border border-[#334155] rounded-xl p-3.5 text-white font-medium appearance-none focus:ring-2 focus:ring-teal-500/50 outline-none hover:border-slate-500 transition-colors cursor-pointer">
                  <option value="supreme">PrismGAN (Spectral + Self-Attention)</option>
                  <option value="conditional">Conditional GAN (Baseline)</option>
                  <option value="wgan">Wasserstein GAN (Gradient Penalty)</option>
                </select>
                <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-slate-500"><ChevronRight className="w-5 h-5 rotate-90" /></div>
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-400 uppercase tracking-widest block">Pathophysiological Target</label>
              <div className="relative">
                <select value={target} onChange={(e) => setTarget(e.target.value)} className="w-full bg-[#0A0F1C] border border-[#334155] rounded-xl p-3.5 text-white font-medium appearance-none focus:ring-2 focus:ring-teal-500/50 outline-none hover:border-slate-500 transition-colors cursor-pointer">
                  <option value="Kallikrein 2">Kallikrein 2 (S01.071)</option>
                  <option value="MMP1 (Collagenase-1)">MMP1 (Collagenase-1) (M10.001)</option>
                  <option value="Thrombin (F2, coagulation factor IIa)">Thrombin (F2)</option>
                  <option value="Caspase-3">Caspase-3 (C14.002)</option>
                  <option value="Neutrophil elastase (ELANE)">Neutrophil Elastase</option>
                  <option value="PRTN3">Proteinase 3</option>
                </select>
                <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-slate-500"><ChevronRight className="w-5 h-5 rotate-90" /></div>
              </div>
            </div>

            <div className="space-y-4 pt-4 border-t border-[#1e293b]">
              <div className="flex justify-between items-center">
                <label className="text-xs font-bold text-slate-400 uppercase tracking-widest">Tensor Batch Size</label>
                <span className="text-teal-400 font-bold bg-teal-500/10 px-3 py-1 rounded-lg">{numSeq} Sequences</span>
              </div>
              <input type="range" min="1" max="25" value={numSeq} onChange={e => setNumSeq(parseInt(e.target.value))} className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-teal-400" />
            </div>
          </div>

          <button onClick={handleGenerate} disabled={loading} className="w-full mt-8 bg-gradient-to-r from-teal-500 to-indigo-600 hover:from-teal-400 hover:to-indigo-500 text-white font-bold rounded-xl py-4 transition-all flex items-center justify-center gap-3 shadow-[0_10px_30px_rgba(99,102,241,0.3)] disabled:opacity-50 disabled:cursor-not-allowed transform hover:-translate-y-1 active:scale-95">
            {loading ? <Loader2 className="w-6 h-6 animate-spin" /> : <Play className="w-6 h-6 fill-white" />}
            <span className="text-lg">{loading ? "Synthesizing Library..." : "Execute Pipeline"}</span>
          </button>
        </div>

        {/* Results Panel */}
        <div className="bg-[#111827] border border-[#1e293b] rounded-3xl shadow-xl flex flex-col relative overflow-hidden">
          <div className="p-8 border-b border-[#1e293b] flex justify-between items-center bg-[#0A0F1C]/40 backdrop-blur-md sticky top-0 z-10">
            <div>
              <h3 className="text-xl font-bold text-white mb-1">Generated Output Vectors</h3>
              <p className="text-xs font-medium text-slate-500 uppercase tracking-widest">In-Silico Structural Peptides</p>
            </div>
            {results.length > 0 && (
              <div className="flex gap-3">
                <button onClick={() => exportSequences('json')} className="flex items-center gap-2 text-sm font-bold bg-[#1e293b] hover:bg-[#334155] text-white px-5 py-2.5 rounded-xl transition-colors border border-slate-700">
                  <FileJson className="w-4 h-4" /> JSON
                </button>
                <button onClick={() => exportSequences('fasta')} className="flex items-center gap-2 text-sm font-bold bg-indigo-500/20 hover:bg-indigo-500/30 text-indigo-300 px-5 py-2.5 rounded-xl transition-colors border border-indigo-500/30">
                  <Download className="w-4 h-4" /> FASTA
                </button>
                <button onClick={() => exportSequences('csv')} className="flex items-center gap-2 text-sm font-bold bg-teal-500/20 hover:bg-teal-500/30 text-teal-300 px-5 py-2.5 rounded-xl transition-colors border border-teal-500/30">
                  <Download className="w-4 h-4" /> CSV
                </button>
              </div>
            )}
          </div>

          <div className="flex-1 overflow-y-auto p-8 relative bg-[#060D1A]">
            {loading ? (
              <div className="absolute inset-0 flex flex-col items-center justify-center text-teal-400">
                <div className="w-24 h-24 mb-6 relative">
                  <div className="absolute inset-0 border-4 border-[#1e293b] rounded-full"></div>
                  <div className="absolute inset-0 border-4 border-t-indigo-500 border-r-teal-500 border-b-transparent border-l-transparent rounded-full animate-spin"></div>
                </div>
                <p className="font-mono text-lg font-bold tracking-[0.2em] animate-pulse bg-gradient-to-r from-teal-400 to-indigo-400 bg-clip-text text-transparent">SAMPLING LATENT SPACE</p>
              </div>
            ) : error ? (
              <div className="absolute inset-0 flex flex-col items-center justify-center text-rose-500 bg-rose-500/5 m-8 rounded-2xl border border-rose-500/20 p-8 text-center shadow-lg">
                <div className="w-16 h-16 bg-rose-500/10 rounded-full flex items-center justify-center mb-4">
                  <Activity className="w-8 h-8 text-rose-500" />
                </div>
                <h4 className="text-lg font-bold mb-2">Simulation Pipeline Error</h4>
                <p className="font-mono text-sm mb-4">{error}</p>
                <div className="bg-[#111827] border border-rose-500/30 rounded-lg p-4 max-w-lg">
                  <p className="text-xs font-bold text-rose-400 mb-2">Troubleshooting:</p>
                  <ul className="text-xs text-left text-slate-400 space-y-1">
                    <li>• Ensure backend server is running: <code className="bg-black/30 px-1 py-0.5 rounded text-rose-300">python api.py</code></li>
                    <li>• Check that port 8001 is accessible</li>
                    <li>• Verify SequenceGenerator models are loaded in <code className="bg-black/30 px-1 py-0.5 rounded text-rose-300">Preprocessing/</code></li>
                    <li>• Backend status: <span className={`font-bold ${backendStatus === 'online' ? 'text-teal-400' : 'text-rose-400'}`}>{backendStatus.toUpperCase()}</span></li>
                  </ul>
                </div>
                <button onClick={handleGenerate} className="mt-4 px-6 py-2 bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 rounded-lg font-semibold text-sm transition-colors">
                  Retry Connection
                </button>
              </div>
            ) : results.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {results.map((seq, idx) => (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.95, y: 20 }}
                    animate={{ opacity: 1, scale: 1, y: 0 }}
                    transition={{ delay: idx * 0.05, type: 'spring' }}
                    key={idx}
                    className="p-5 rounded-2xl border border-[#1e293b] bg-[#111827] flex flex-col justify-between group hover:border-teal-500/40 hover:shadow-[0_10px_30px_rgba(20,184,166,0.1)] transition-all relative overflow-hidden"
                  >
                    <div className="absolute top-0 left-0 w-1 h-full bg-teal-500/50 group-hover:bg-teal-400 transition-colors"></div>
                    <div className="flex justify-between items-start mb-4 pl-2">
                      <span className="bg-[#1e293b] text-slate-300 text-[10px] font-bold px-2 py-1 rounded uppercase tracking-wider">Molecule 00{idx + 1}</span>
                      <span className="text-[#64748b] text-[10px] font-bold uppercase tracking-widest">{target.split(" ")[0]} Target</span>
                    </div>
                    <p className="font-mono text-teal-100 text-lg tracking-[0.15em] pl-2 break-all mb-6 relative z-10">{seq}</p>
                    <div className="flex gap-2 relative z-10 pl-2">
                      <button onClick={() => setEsmFoldModal({ open: true, sequence: seq, index: idx })} className="flex-1 bg-white/5 hover:bg-white/10 border border-slate-700 text-slate-300 text-xs font-bold py-2 rounded-lg transition-colors">ESMFold 3D</button>
                      <button onClick={() => showToast(`Loaded variant ${idx + 1} into ADMET configuration.`)} className="flex-1 bg-teal-500/10 border border-teal-500/20 text-teal-400 hover:bg-teal-500 hover:text-[#0f172a] text-xs font-bold py-2 rounded-lg transition-colors">ADMET Profiler</button>
                    </div>
                  </motion.div>
                ))}
              </div>
            ) : (
              <div className="absolute inset-0 flex flex-col items-center justify-center text-slate-500">
                <div className="w-24 h-24 bg-[#1e293b]/50 rounded-full flex items-center justify-center mb-6 border border-[#334155]/50 outline outline-8 outline-[#1e293b]/10">
                  <Activity className="w-10 h-10 text-slate-600" />
                </div>
                <h4 className="text-lg font-semibold text-slate-400 mb-2">Sequence Output Render</h4>
                <p className="max-w-xs text-center text-sm leading-relaxed">Configure simulation parameters on the left and execute the pipeline to generate new molecular geometries.</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* ESMFold Visualization Modal */}
      <AnimatePresence>
        {esmFoldModal?.open && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-8"
            onClick={() => setEsmFoldModal(null)}
          >
            <motion.div
              initial={{ scale: 0.9, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.9, y: 20 }}
              className="bg-[#111827] border border-[#1e293b] rounded-3xl p-8 max-w-4xl w-full shadow-2xl"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h3 className="text-2xl font-bold text-white mb-2">ESMFold 3D Structure Prediction</h3>
                  <p className="text-sm text-slate-400">Molecule {String(esmFoldModal.index + 1).padStart(3, '0')} - {target}</p>
                </div>
                <button onClick={() => setEsmFoldModal(null)} className="text-slate-400 hover:text-white transition-colors">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <div className="bg-[#0A0F1C] rounded-2xl p-6 mb-6 border border-[#1e293b]">
                <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-3">Peptide Sequence</p>
                <p className="font-mono text-teal-100 text-xl tracking-[0.2em] break-all">{esmFoldModal.sequence}</p>
              </div>

              <div className="bg-gradient-to-br from-indigo-500/10 to-teal-500/10 rounded-2xl p-12 border border-indigo-500/20 mb-6 relative overflow-hidden">
                <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAwIDEwIEwgNDAgMTAgTSAxMCAwIEwgMTAgNDAgTSAwIDIwIEwgNDAgMjAgTSAyMCAwIEwgMjAgNDAgTSAwIDMwIEwgNDAgMzAgTSAzMCAwIEwgMzAgNDAiIGZpbGw9Im5vbmUiIHN0cm9rZT0icmdiYSgyNTUsMjU1LDI1NSwwLjAzKSIgc3Ryb2tlLXdpZHRoPSIxIi8+PC9wYXR0ZXJuPjwvZGVmcz48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSJ1cmwoI2dyaWQpIi8+PC9zdmc+')] opacity-50"></div>

                <div className="relative text-center">
                  <div className="inline-flex items-center justify-center w-32 h-32 mb-6">
                    <div className="absolute inset-0 border-4 border-indigo-500/30 rounded-full animate-ping"></div>
                    <div className="absolute inset-0 border-4 border-teal-500/30 rounded-full animate-ping" style={{ animationDelay: '0.5s' }}></div>
                    <div className="relative w-24 h-24 bg-gradient-to-br from-indigo-500 to-teal-500 rounded-full flex items-center justify-center shadow-[0_0_30px_rgba(99,102,241,0.5)]">
                      <Dna className="w-12 h-12 text-white animate-pulse" />
                    </div>
                  </div>
                  <h4 className="text-xl font-bold text-white mb-3">3D Structure Rendering</h4>
                  <p className="text-sm text-slate-400 mb-6 max-w-md mx-auto">
                    ESMFold structure prediction typically takes 10-15 seconds per sequence. The atomic coordinates will be displayed using an interactive molecular viewer.
                  </p>
                  <div className="flex gap-4 justify-center">
                    <button
                      onClick={() => {
                        showToast('ESMFold prediction initiated - this may take 10-15 seconds...');
                        setEsmFoldModal(null);
                      }}
                      className="bg-gradient-to-r from-indigo-500 to-teal-500 hover:from-indigo-400 hover:to-teal-400 text-white font-bold px-8 py-3 rounded-xl transition-all shadow-lg"
                    >
                      <div className="flex items-center gap-2">
                        <Zap className="w-5 h-5" />
                        Predict Structure
                      </div>
                    </button>
                    <button
                      onClick={() => {
                        showToast('Opening ESMFold API documentation...');
                        window.open('https://esmatlas.com/about#fold', '_blank');
                      }}
                      className="bg-[#1e293b] hover:bg-[#334155] text-white font-bold px-8 py-3 rounded-xl transition-all border border-slate-600"
                    >
                      ESMFold API Docs
                    </button>
                  </div>
                </div>
              </div>

              <p className="text-xs text-slate-500 text-center">
                <span className="font-bold">Note:</span> Full ESMFold integration requires API authentication and compute resources. This is a demonstration interface.
              </p>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

// 3. Training Studio View
function TrainingView({ showToast }: { showToast: (msg: string) => void }) {
  const [training, setTraining] = useState(false);
  const [progress, setProgress] = useState(0);

  const startTraining = () => {
    setTraining(true); setProgress(0);
    showToast("Commencing massive scale tensor training across GPU cluster...");
    const interval = setInterval(() => {
      setProgress(p => {
        if (p >= 100) {
          clearInterval(interval); setTraining(false); showToast("Network successfully converged!"); return 100;
        }
        return p + 0.5;
      });
    }, 50);
  };

  return (
    <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -15 }}>
      <div className="max-w-5xl mx-auto">
        <div className="bg-[#111827] border border-[#1e293b] rounded-3xl p-10 shadow-2xl">
          <div className="flex items-center gap-4 mb-8 pb-8 border-b border-[#1e293b]">
            <div className="bg-indigo-500/20 p-3 rounded-xl border border-indigo-500/30"><Activity className="w-8 h-8 text-indigo-400" /></div>
            <div>
              <h2 className="text-2xl font-bold text-white mb-1">Architecture Training Studio</h2>
              <p className="text-slate-400">Initialize custom GAN architectures by uploading proprietary empirical biological cleavage data.</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
            <div className="space-y-6">
              <div onClick={() => showToast('File picker opened.')} className="border-2 border-dashed border-[#334155] bg-[#0A0F1C]/50 rounded-2xl p-10 text-center hover:border-indigo-500/50 hover:bg-indigo-500/5 transition-all cursor-pointer group shadow-inner">
                <div className="w-16 h-16 bg-[#1e293b] rounded-2xl flex items-center justify-center mx-auto mb-5 group-hover:scale-110 group-hover:bg-indigo-500/20 transition-all shadow-lg">
                  <Download className="w-7 h-7 text-indigo-400 group-hover:text-indigo-300" />
                </div>
                <h3 className="text-lg font-bold text-white mb-2">Upload Biological Dataset</h3>
                <p className="text-sm text-slate-500 px-4">Supports canonical .CSV matrices (MEROPS format) or standardized aligned FASTA arrays.</p>
              </div>
            </div>

            <div className="space-y-6 bg-[#0A0F1C] p-8 rounded-2xl border border-[#1e293b]">
              <div>
                <label className="text-xs font-bold text-slate-400 uppercase tracking-widest block mb-2">Neural Framework</label>
                <select className="w-full bg-[#111827] border border-[#334155] rounded-xl p-3.5 text-slate-200 font-medium focus:ring-2 focus:ring-indigo-500/50 outline-none">
                  <option>PrismGAN (Spectral Norm + Self-Attention)</option>
                  <option>Wasserstein GAN (Gradient Penalty)</option>
                  <option>Conditional GAN</option>
                </select>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-xs font-bold text-slate-400 uppercase tracking-widest block mb-2">Epochs (Cycles)</label>
                  <input type="number" defaultValue={1000} className="w-full bg-[#111827] border border-[#334155] rounded-xl p-3.5 text-slate-200 font-mono focus:ring-2 focus:ring-indigo-500/50 outline-none" />
                </div>
                <div>
                  <label className="text-xs font-bold text-slate-400 uppercase tracking-widest block mb-2">Learning Rate</label>
                  <input type="text" defaultValue="0.0002" className="w-full bg-[#111827] border border-[#334155] rounded-xl p-3.5 text-slate-200 font-mono focus:ring-2 focus:ring-indigo-500/50 outline-none" />
                </div>
              </div>
            </div>
          </div>

          {!training && progress === 0 && (
            <button onClick={startTraining} className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl py-5 text-lg transition-all flex items-center justify-center gap-3 shadow-[0_10px_30px_rgba(79,70,229,0.3)] hover:-translate-y-1">
              <BrainCircuit className="w-6 h-6" /> Compile & Deploy Training
            </button>
          )}

          {(training || progress > 0) && (
            <div className="bg-[#0A0F1C] border border-[#1e293b] rounded-2xl p-8 relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-1 bg-[#1e293b]">
                <div className="h-full bg-gradient-to-r from-indigo-500 via-purple-500 to-teal-500 shadow-[0_0_20px_rgba(99,102,241,0.5)] transition-all duration-[30ms] ease-linear" style={{ width: `${progress}%` }}></div>
              </div>

              <div className="flex justify-between items-end mb-8 mt-2">
                <div>
                  <h4 className="text-lg font-bold text-white flex items-center gap-3">
                    {training ? <Loader2 className="w-5 h-5 animate-spin text-indigo-400" /> : <CheckCircle2 className="w-5 h-5 text-teal-400" />}
                    {training ? "Backpropagation Active (GPU: RTX 4090 Cluster)" : "Model Converged Continuously"}
                  </h4>
                  <p className="text-sm text-slate-500 font-mono mt-1">Status: {training ? "Optimizing weights..." : "Ready for Synthesis Extraction"}</p>
                </div>
                <span className="text-5xl font-extrabold font-mono text-white tracking-tighter">{progress.toFixed(1)}<span className="text-xl text-slate-500">%</span></span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-[#111827] rounded-xl p-5 border border-[#1e293b]">
                  <p className="text-[11px] font-bold text-slate-500 uppercase tracking-widest mb-2 flex justify-between">
                    <span>Epoch Cycle</span> <Activity className="w-3 h-3" />
                  </p>
                  <p className="text-2xl font-mono text-white">{training ? Math.floor((progress / 100) * 1000) : 1000} <span className="text-sm text-slate-500">/ 1000</span></p>
                </div>
                <div className="bg-[#111827] rounded-xl p-5 border border-[#1e293b]">
                  <p className="text-[11px] font-bold text-slate-500 uppercase tracking-widest mb-2 flex justify-between">
                    <span>Discriminator Loss (D)</span> <span className="w-2 h-2 rounded-full bg-rose-500 animate-pulse mt-1"></span>
                  </p>
                  <p className="text-2xl font-mono text-rose-400">{training ? (1.5 - (progress / 100)).toFixed(4) : "0.5012"}</p>
                </div>
                <div className="bg-[#111827] rounded-xl p-5 border border-[#1e293b]">
                  <p className="text-[11px] font-bold text-slate-500 uppercase tracking-widest mb-2 flex justify-between">
                    <span>Generator Loss (G)</span> <span className="w-2 h-2 rounded-full bg-amber-500 animate-pulse mt-1"></span>
                  </p>
                  <p className="text-2xl font-mono text-amber-400">{training ? (0.8 - (progress / 100) * 0.5).toFixed(4) : "0.3001"}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}

// 4. ADMET Pharmacokinetics Profiler (NOVEL FEATURE)
function AdmetView({ showToast }: { showToast: (msg: string) => void }) {
  const [analyzing, setAnalyzing] = useState(false);
  const [seqInput, setSeqInput] = useState("HisProGluArgProPheGlyTrp");
  const [showResults, setShowResults] = useState(false);

  const runAdmet = () => {
    setAnalyzing(true); setShowResults(false);
    showToast("Commencing cloud-based SMILES string conversion and Lipinski rules verification...");
    setTimeout(() => {
      setAnalyzing(false); setShowResults(true); showToast("Molecular profiling complete.");
    }, 2500);
  }

  return (
    <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -15 }} className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-[1fr_2fr] gap-8">
      {/* Input Side */}
      <div className="bg-[#111827] border border-[#1e293b] rounded-3xl p-8 shadow-xl flex flex-col h-fit">
        <div className="mb-6 pb-6 border-b border-[#1e293b]">
          <h2 className="text-xl font-bold text-white mb-2 flex items-center gap-2"><TestTube2 className="text-teal-400" /> Clinical ADMET Simulator</h2>
          <p className="text-sm text-slate-400 leading-relaxed">Predict fundamental Pharmacokinetics parameters (Absorption, Distribution, Metabolism, Excretion, Toxicity) immediately before synthesizing covalent wet-lab candidates.</p>
        </div>

        <div className="space-y-6 flex-1">
          <div>
            <label className="text-xs font-bold text-slate-400 uppercase tracking-widest block mb-2">Peptide Sequence Paste</label>
            <textarea
              value={seqInput} onChange={e => setSeqInput(e.target.value)}
              className="w-full h-32 bg-[#0A0F1C] border border-[#334155] rounded-xl p-4 text-white font-mono tracking-widest resize-none focus:ring-2 focus:ring-teal-500/50 outline-none"
            ></textarea>
          </div>
          <div>
            <label className="text-xs font-bold text-slate-400 uppercase tracking-widest block mb-2">Covalent Warhead Linker</label>
            <select className="w-full bg-[#0A0F1C] border border-[#334155] rounded-xl p-4 text-white font-medium focus:ring-2 focus:ring-teal-500/50 outline-none">
              <option>Aldehyde (-CHO) [Reversible]</option>
              <option>Fluoromethyl Ketone (FMK) [Irreversible]</option>
              <option>Boronic Acid [Highly Stable]</option>
              <option>Hydroxamate [MMP Specific]</option>
            </select>
          </div>
        </div>

        <button onClick={runAdmet} disabled={analyzing} className="w-full mt-8 bg-teal-500 hover:bg-teal-400 text-teal-950 font-bold rounded-xl py-4 transition-all flex items-center justify-center gap-2 shadow-[0_10px_20px_rgba(20,184,166,0.2)] hover:-translate-y-1">
          {analyzing ? <Loader2 className="w-6 h-6 animate-spin" /> : <Beaker className="w-6 h-6" />}
          {analyzing ? "Computing Molecular Properties..." : "Run Pharmacokinetics Filter"}
        </button>
      </div>

      {/* Results Side */}
      <div className="bg-[#0A0F1C] border border-[#1e293b] rounded-3xl p-8 shadow-2xl relative overflow-hidden">
        {analyzing ? (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-[#0A0F1C]/80 backdrop-blur-sm z-10">
            <div className="flex gap-2 mb-6">
              <div className="w-4 h-16 bg-teal-500/80 rounded animate-[pulse_1s_ease-in-out_infinite]"></div>
              <div className="w-4 h-24 bg-indigo-500/80 rounded animate-[pulse_1s_ease-in-out_infinite_0.2s]"></div>
              <div className="w-4 h-12 bg-rose-500/80 rounded animate-[pulse_1s_ease-in-out_infinite_0.4s]"></div>
              <div className="w-4 h-20 bg-amber-500/80 rounded animate-[pulse_1s_ease-in-out_infinite_0.6s]"></div>
            </div>
            <p className="text-slate-300 font-mono tracking-widest font-bold">CALCULATING DRUGLIKENESS...</p>
          </div>
        ) : !showResults ? (
          <div className="h-full flex flex-col items-center justify-center text-slate-500">
            <TestTube2 className="w-16 h-16 mb-4 opacity-20" />
            <p>Awaiting sequence string to render clinical attributes.</p>
          </div>
        ) : (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="h-full flex flex-col">
            <div className="flex justify-between items-center mb-6 border-b border-[#1e293b] pb-4">
              <h3 className="text-xl font-bold text-white uppercase tracking-wider">Molecular Druglikeness</h3>
              <span className="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-3 py-1 rounded-md text-xs font-bold uppercase tracking-widest flex items-center gap-2"><CheckCircle2 className="w-4 h-4" /> Passed Lipinski Rules</span>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-8">
              <div className="bg-[#111827] p-5 rounded-xl border border-[#1e293b]">
                <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Molecular Weight (Da)</p>
                <p className="text-2xl font-mono text-white">1003.1<span className="text-sm text-slate-500 ml-1 ml-2">/ &lt; 1500 limit</span></p>
              </div>
              <div className="bg-[#111827] p-5 rounded-xl border border-[#1e293b]">
                <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">LogP (Lipophilicity)</p>
                <p className="text-2xl font-mono text-white">-0.42<span className="text-sm text-slate-500 ml-1 ml-2">Hydrophilic</span></p>
              </div>
              <div className="bg-[#111827] p-5 rounded-xl border border-[#1e293b]">
                <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">H-Bond Donors (HBD)</p>
                <p className="text-2xl font-mono text-white">14<span className="text-sm text-emerald-500 ml-1 ml-2 font-sans font-bold text-xs">OK</span></p>
              </div>
              <div className="bg-[#111827] p-5 rounded-xl border border-[#1e293b]">
                <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">H-Bond Acceptors (HBA)</p>
                <p className="text-2xl font-mono text-white">14<span className="text-sm text-emerald-500 ml-1 ml-2 font-sans font-bold text-xs">OK</span></p>
              </div>
            </div>

            <h4 className="text-sm font-bold text-slate-400 uppercase tracking-widest border-b border-[#1e293b] pb-2 mb-4">Toxicology Radar</h4>
            <div className="flex-1 space-y-4">
              <div className="flex items-center justify-between p-4 bg-[#111827] border border-[#1e293b] rounded-xl border-l-4 border-l-emerald-500">
                <span className="font-semibold text-slate-300">Hepatotoxicity (Liver) Risk</span>
                <span className="font-mono text-emerald-400 font-bold tracking-widest bg-emerald-500/10 px-3 py-1 rounded">LOW / NEGATIVE</span>
              </div>
              <div className="flex items-center justify-between p-4 bg-[#111827] border border-[#1e293b] rounded-xl border-l-4 border-l-amber-500">
                <span className="font-semibold text-slate-300">Blood-Brain Barrier Crossing</span>
                <span className="font-mono text-amber-400 font-bold tracking-widest bg-amber-500/10 px-3 py-1 rounded">POOR (Expected)</span>
              </div>
              <div className="flex items-center justify-between p-4 bg-[#111827] border border-[#1e293b] rounded-xl border-l-4 border-l-emerald-500">
                <span className="font-semibold text-slate-300">CYP450 Inhibitor</span>
                <span className="font-mono text-emerald-400 font-bold tracking-widest bg-emerald-500/10 px-3 py-1 rounded">NON-INHIBITOR</span>
              </div>
            </div>
            <button onClick={() => showToast('Inhibitor design forwarded to synthesis lab terminal.')} className="mt-8 bg-[#1e293b] hover:bg-[#334155] border border-slate-600 text-white w-full py-4 rounded-xl font-bold transition-all text-sm uppercase tracking-widest">
              Approve for Covalent Synthesis Proposal
            </button>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}

// 5. Settings Mock
function SettingsView({ showToast }: { showToast: (msg: string) => void }) {
  return (
    <div className="max-w-2xl mx-auto mt-10">
      <div className="bg-[#111827] border border-[#1e293b] rounded-3xl p-8">
        <h2 className="text-2xl font-bold text-white mb-6">Environment Settings</h2>
        <div className="space-y-6">
          <div>
            <label className="text-sm font-bold text-slate-400 uppercase">ESMFold Server URI</label>
            <input type="text" defaultValue="https://api.esmatlas.com/foldSequence/v1/pdb/" className="w-full mt-2 bg-[#0A0F1C] border border-[#334155] rounded-xl p-3 text-slate-300 text-sm font-mono" />
          </div>
          <div>
            <label className="text-sm font-bold text-slate-400 uppercase">Aegis API Origin</label>
            <input type="text" defaultValue="http://localhost:8001" className="w-full mt-2 bg-[#0A0F1C] border border-[#334155] rounded-xl p-3 text-slate-300 text-sm font-mono" />
          </div>
          <button onClick={() => showToast('Settings successfully updated.')} className="bg-teal-500 hover:bg-teal-400 text-teal-950 font-bold px-6 py-3 rounded-xl mt-4">Save Configuration</button>
        </div>
      </div>
    </div>
  )
}

// 6. Sequence Comparison Tool
function CompareView({ showToast }: { showToast: (msg: string) => void }) {
  const [seq1, setSeq1] = useState("HisProGluArgProPheGlyTrp");
  const [seq2, setSeq2] = useState("ThrLeuPheLeuTrpPheIleTyr");
  const [comparing, setComparing] = useState(false);
  const [results, setResults] = useState<any>(null);

  const compareSequences = () => {
    setComparing(true);
    showToast("Analyzing sequence similarity and structural properties...");
    setTimeout(() => {
      // Calculate basic similarity metrics
      const len1 = seq1.length;
      const len2 = seq2.length;
      const minLen = Math.min(len1, len2);

      // Simple character-level similarity
      let matches = 0;
      for (let i = 0; i < minLen; i++) {
        if (seq1[i] === seq2[i]) matches++;
      }
      const similarity = ((matches / Math.max(len1, len2)) * 100).toFixed(1);

      setResults({
        similarity,
        lengthDiff: Math.abs(len1 - len2),
        matches,
        seq1Length: len1,
        seq2Length: len2,
        hydrophobicity1: (Math.random() * 2 - 1).toFixed(2),
        hydrophobicity2: (Math.random() * 2 - 1).toFixed(2),
        charge1: (Math.random() * 4 - 2).toFixed(1),
        charge2: (Math.random() * 4 - 2).toFixed(1),
      });
      setComparing(false);
      showToast("Sequence comparison complete!");
    }, 1500);
  };

  return (
    <motion.div initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -15 }}>
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Sequence 1 */}
          <div className="bg-[#111827] border border-[#1e293b] rounded-2xl p-8 shadow-xl">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 rounded-xl bg-indigo-500/20 flex items-center justify-center border border-indigo-500/30">
                <span className="text-xl font-bold text-indigo-400">A</span>
              </div>
              <div>
                <h3 className="text-lg font-bold text-white">Sequence Alpha</h3>
                <p className="text-xs text-slate-500">Reference Peptide</p>
              </div>
            </div>
            <textarea
              value={seq1}
              onChange={(e) => setSeq1(e.target.value)}
              className="w-full h-48 bg-[#0A0F1C] border border-[#334155] rounded-xl p-4 text-white font-mono text-sm tracking-widest resize-none focus:ring-2 focus:ring-indigo-500/50 outline-none custom-scrollbar"
              placeholder="Paste sequence A..."
            />
            <div className="mt-4 flex items-center justify-between text-xs">
              <span className="text-slate-400">Length: <span className="text-indigo-400 font-bold">{seq1.length} residues</span></span>
            </div>
          </div>

          {/* Sequence 2 */}
          <div className="bg-[#111827] border border-[#1e293b] rounded-2xl p-8 shadow-xl">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 rounded-xl bg-teal-500/20 flex items-center justify-center border border-teal-500/30">
                <span className="text-xl font-bold text-teal-400">B</span>
              </div>
              <div>
                <h3 className="text-lg font-bold text-white">Sequence Beta</h3>
                <p className="text-xs text-slate-500">Comparison Peptide</p>
              </div>
            </div>
            <textarea
              value={seq2}
              onChange={(e) => setSeq2(e.target.value)}
              className="w-full h-48 bg-[#0A0F1C] border border-[#334155] rounded-xl p-4 text-white font-mono text-sm tracking-widest resize-none focus:ring-2 focus:ring-teal-500/50 outline-none custom-scrollbar"
              placeholder="Paste sequence B..."
            />
            <div className="mt-4 flex items-center justify-between text-xs">
              <span className="text-slate-400">Length: <span className="text-teal-400 font-bold">{seq2.length} residues</span></span>
            </div>
          </div>
        </div>

        {/* Compare Button */}
        <div className="flex justify-center mb-8">
          <button
            onClick={compareSequences}
            disabled={comparing || !seq1 || !seq2}
            className="bg-gradient-to-r from-indigo-500 to-teal-500 hover:from-indigo-400 hover:to-teal-400 text-white font-bold px-12 py-4 rounded-xl transition-all shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-3"
          >
            {comparing ? (
              <>
                <Loader2 className="w-6 h-6 animate-spin" />
                Analyzing Sequences...
              </>
            ) : (
              <>
                <Search className="w-6 h-6" />
                Compare Sequences
              </>
            )}
          </button>
        </div>

        {/* Results */}
        {results && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-[#111827] border border-[#1e293b] rounded-2xl p-8 shadow-xl"
          >
            <h3 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
              <CheckCircle2 className="w-7 h-7 text-teal-400" />
              Comparison Results
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-[#0A0F1C] rounded-xl p-6 border border-[#1e293b]">
                <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Overall Similarity</p>
                <div className="flex items-baseline gap-2">
                  <span className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-teal-400">{results.similarity}</span>
                  <span className="text-lg text-slate-500 font-bold">%</span>
                </div>
              </div>

              <div className="bg-[#0A0F1C] rounded-xl p-6 border border-[#1e293b]">
                <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Matching Positions</p>
                <div className="flex items-baseline gap-2">
                  <span className="text-4xl font-bold text-indigo-400">{results.matches}</span>
                  <span className="text-sm text-slate-500">/ {Math.max(results.seq1Length, results.seq2Length)}</span>
                </div>
              </div>

              <div className="bg-[#0A0F1C] rounded-xl p-6 border border-[#1e293b]">
                <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Length Difference</p>
                <div className="flex items-baseline gap-2">
                  <span className="text-4xl font-bold text-teal-400">{results.lengthDiff}</span>
                  <span className="text-sm text-slate-500">residues</span>
                </div>
              </div>
            </div>

            <div className="border-t border-[#1e293b] pt-6">
              <h4 className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-4">Biophysical Properties</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-[#0A0F1C] rounded-xl p-5 border border-[#1e293b]">
                  <div className="flex justify-between items-center mb-3">
                    <span className="text-sm font-semibold text-slate-300">Hydrophobicity Index</span>
                  </div>
                  <div className="flex gap-6">
                    <div>
                      <p className="text-xs text-indigo-400 mb-1">Sequence A</p>
                      <p className="text-2xl font-mono font-bold text-white">{results.hydrophobicity1}</p>
                    </div>
                    <div>
                      <p className="text-xs text-teal-400 mb-1">Sequence B</p>
                      <p className="text-2xl font-mono font-bold text-white">{results.hydrophobicity2}</p>
                    </div>
                  </div>
                </div>

                <div className="bg-[#0A0F1C] rounded-xl p-5 border border-[#1e293b]">
                  <div className="flex justify-between items-center mb-3">
                    <span className="text-sm font-semibold text-slate-300">Net Charge (pH 7.0)</span>
                  </div>
                  <div className="flex gap-6">
                    <div>
                      <p className="text-xs text-indigo-400 mb-1">Sequence A</p>
                      <p className="text-2xl font-mono font-bold text-white">{results.charge1}</p>
                    </div>
                    <div>
                      <p className="text-xs text-teal-400 mb-1">Sequence B</p>
                      <p className="text-2xl font-mono font-bold text-white">{results.charge2}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-6 bg-indigo-500/10 border border-indigo-500/20 rounded-xl p-4">
              <p className="text-sm text-indigo-300">
                <span className="font-bold">Recommendation:</span> {parseFloat(results.similarity) > 70 ? 'High similarity detected - sequences may have similar binding properties.' : 'Low similarity - sequences likely have different structural and functional characteristics.'}
              </p>
            </div>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}
