import React, { useState, useMemo } from 'react';
import { UploadCloud, FileImage, ShieldAlert, Loader2, CheckCircle2, Filter } from 'lucide-react';

export default function GenerateChallanPage() {
  const [files, setFiles] = useState<File[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [results, setResults] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [filterVehicle, setFilterVehicle] = useState('All');
  const [filterChallan, setFilterChallan] = useState('All');

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const droppedFiles = Array.from(e.dataTransfer.files).filter(f => f.type.startsWith('image/'));
    setFiles(prev => [...prev, ...droppedFiles]);
  };

  const handleSelectFiles = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selected = Array.from(e.target.files).filter(f => f.type.startsWith('image/'));
      setFiles(prev => [...prev, ...selected]);
    }
  };

  const handleAnalyze = async () => {
    if (files.length === 0) return;
    setIsProcessing(true);
    setError(null);

    const formData = new FormData();
    files.forEach(f => formData.append('images', f));

    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    try {
      const res = await fetch(`${apiUrl}/api/predict_images`, {
        method: 'POST',
        body: formData,
      });
      
      if (!res.ok) throw new Error("Failed to process images.");
      const data = await res.json();
      setResults(data.predictions);
    } catch (err: any) {
      setError(err.message || 'An error occurred during prediction.');
    } finally {
      setIsProcessing(false);
    }
  };

  const filteredResults = useMemo(() => {
    return results.filter(r => {
      const vMatch = filterVehicle === 'All' || r.vehicle_type === filterVehicle;
      const cMatch = filterChallan === 'All' || r.challan_type === filterChallan;
      return vMatch && cMatch;
    });
  }, [results, filterVehicle, filterChallan]);

  // Extract unique types for dropdowns
  const vehicleTypes = ['All', ...Array.from(new Set(results.map(r => r.vehicle_type)))].filter(Boolean);
  const challanTypes = ['All', ...Array.from(new Set(results.map(r => r.challan_type)))].filter(Boolean);

  return (
    <div className="flex flex-col h-full bg-white dark:bg-gray-900 transition-colors duration-300">
      <div className="mb-8">
        <h2 className="text-3xl font-black text-gray-900 dark:text-white">Generate Challans</h2>
        <p className="text-gray-500 dark:text-gray-400 mt-2">
          Upload traffic camera frames to automatically detect violations and generate e-challans.
        </p>
      </div>

      {results.length === 0 ? (
        <div className="max-w-3xl mx-auto w-full">
          {/* Upload Zone */}
          <div 
            onDragOver={e => e.preventDefault()}
            onDrop={handleDrop}
            className="border-3 border-dashed border-gray-300 dark:border-gray-700 rounded-3xl p-16 text-center hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors flex flex-col items-center justify-center cursor-pointer group"
          >
            <input 
              type="file" 
              multiple 
              accept="image/*" 
              onChange={handleSelectFiles}
              className="hidden" 
              id="file-upload" 
            />
            <label htmlFor="file-upload" className="cursor-pointer flex flex-col items-center">
              <div className="w-20 h-20 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <UploadCloud size={40} className="text-[#C8102E] dark:text-red-500" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Drag & Drop Images</h3>
              <p className="text-gray-500 dark:text-gray-400">or click to browse local files</p>
            </label>
          </div>

          {/* Selected Files List */}
          {files.length > 0 && (
            <div className="mt-8">
              <h4 className="font-bold text-gray-900 dark:text-white mb-4">Selected Files ({files.length})</h4>
              <div className="bg-gray-50 dark:bg-gray-800 rounded-2xl p-4 max-h-64 overflow-y-auto">
                {files.map((f, i) => (
                  <div key={i} className="flex items-center gap-3 py-2 border-b border-gray-200 dark:border-gray-700 last:border-0">
                    <FileImage size={16} className="text-gray-400" />
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300 truncate">{f.name}</span>
                    <span className="text-xs text-gray-400 ml-auto">{(f.size / 1024 / 1024).toFixed(2)} MB</span>
                  </div>
                ))}
              </div>
              
              <button 
                onClick={handleAnalyze}
                disabled={isProcessing}
                className="w-full mt-6 bg-[#C8102E] hover:bg-[#A00D24] text-white py-4 rounded-xl font-bold text-lg transition-all shadow-md flex items-center justify-center gap-2 disabled:opacity-70"
              >
                {isProcessing ? (
                  <><Loader2 className="animate-spin" /> Processing with YOLO...</>
                ) : (
                  <><ShieldAlert /> Analyze & Generate</>
                )}
              </button>
              {error && <p className="text-red-500 text-center mt-4 text-sm font-semibold">{error}</p>}
            </div>
          )}
        </div>
      ) : (
        /* Results Table */
        <div className="flex-1 flex flex-col">
          <div className="flex flex-col sm:flex-row items-center justify-between mb-6 bg-gray-50 dark:bg-gray-800 p-4 rounded-2xl border border-gray-200 dark:border-gray-700 gap-4">
            <div className="flex items-center gap-3 text-green-600 dark:text-green-500 font-bold">
              <CheckCircle2 />
              Processed {results.length} violations
            </div>
            
            {/* Filters */}
            <div className="flex items-center gap-4 w-full sm:w-auto">
              <div className="flex items-center gap-2">
                <Filter size={16} className="text-gray-500 dark:text-gray-400" />
                <select 
                  value={filterVehicle}
                  onChange={e => setFilterVehicle(e.target.value)}
                  className="bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white text-sm rounded-lg py-2 px-3 focus:outline-none focus:border-[#C8102E]"
                >
                  {vehicleTypes.map(vt => <option key={vt} value={vt}>{vt}</option>)}
                </select>
              </div>
              <div className="flex items-center gap-2">
                <select 
                  value={filterChallan}
                  onChange={e => setFilterChallan(e.target.value)}
                  className="bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white text-sm rounded-lg py-2 px-3 focus:outline-none focus:border-[#C8102E]"
                >
                  {challanTypes.map(ct => <option key={ct} value={ct}>{ct}</option>)}
                </select>
              </div>
              <button 
                onClick={() => { setResults([]); setFiles([]); }}
                className="ml-4 px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg text-sm font-bold hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
              >
                Reset
              </button>
            </div>
          </div>
          
          {/* Chart Section */}
          <div className="mb-6 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-3xl p-6 shadow-sm">
            <h3 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Challan Summary Overview</h3>
            <div className="flex flex-col md:flex-row gap-8">
              <div className="flex-1">
                <h4 className="text-sm font-semibold text-gray-500 mb-4 text-center">Violations Breakdown</h4>
                <div className="flex flex-wrap gap-4 justify-center">
                  {Object.entries(filteredResults.reduce((acc, curr) => {
                    acc[curr.challan_type] = (acc[curr.challan_type] || 0) + 1;
                    return acc;
                  }, {} as any)).map(([type, count]: any, i: number) => (
                    <div key={i} className="flex flex-col items-center bg-gray-50 dark:bg-gray-900 px-6 py-4 rounded-2xl border border-gray-100 dark:border-gray-700">
                      <span className="text-2xl font-black text-[#C8102E] dark:text-red-500">{count}</span>
                      <span className="text-xs font-bold text-gray-500 uppercase tracking-wider mt-1">{type.replace('_', ' ')}</span>
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="flex-1">
                <h4 className="text-sm font-semibold text-gray-500 mb-4 text-center">Vehicle Types Involved</h4>
                <div className="flex flex-wrap gap-4 justify-center">
                  {Object.entries(filteredResults.reduce((acc, curr) => {
                    acc[curr.vehicle_type] = (acc[curr.vehicle_type] || 0) + 1;
                    return acc;
                  }, {} as any)).map(([type, count]: any, i: number) => (
                    <div key={i} className="flex flex-col items-center bg-blue-50 dark:bg-blue-900/20 px-6 py-4 rounded-2xl border border-blue-100 dark:border-blue-900/30">
                      <span className="text-2xl font-black text-blue-600 dark:text-blue-400">{count}</span>
                      <span className="text-xs font-bold text-blue-600/70 dark:text-blue-400/70 uppercase tracking-wider mt-1">{type}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-3xl overflow-hidden shadow-sm flex-1">
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-gray-50 dark:bg-gray-900/50 border-b border-gray-200 dark:border-gray-700 text-sm font-bold text-gray-500 dark:text-gray-400">
                    <th className="p-4 pl-6">Image</th>
                    <th className="p-4">Image ID</th>
                    <th className="p-4">Vehicle Type</th>
                    <th className="p-4">Challan Type</th>
                    <th className="p-4 text-right pr-6">Amount (₹)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                  {filteredResults.length === 0 ? (
                    <tr>
                      <td colSpan={5} className="p-8 text-center text-gray-500 dark:text-gray-400">No results match your filters.</td>
                    </tr>
                  ) : (
                    filteredResults.map((r, i) => (
                      <tr key={i} className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors text-gray-900 dark:text-gray-100">
                        <td className="p-4 pl-6">
                          <img src={r.image_url} alt="Crop" className="w-16 h-16 object-cover rounded-lg border border-gray-200 dark:border-gray-600 bg-gray-100 dark:bg-gray-800" />
                        </td>
                        <td className="p-4 font-mono text-xs">{r.image_id.substring(0, 8)}...</td>
                        <td className="p-4 capitalize font-medium">{r.vehicle_type}</td>
                        <td className="p-4">
                          <span className="inline-flex px-3 py-1 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 text-xs font-bold rounded-full capitalize">
                            {r.challan_type.replace(/_/g, ' ')}
                          </span>
                        </td>
                        <td className="p-4 text-right pr-6 font-bold">₹{r.amount}</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
