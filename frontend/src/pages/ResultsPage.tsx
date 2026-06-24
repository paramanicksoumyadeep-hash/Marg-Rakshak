
import { useParams, Link } from 'react-router-dom';
import { ArrowRight, FileCheck2 } from 'lucide-react';
import { ViolationBadge } from '../components/ViolationBadge';

import { useState, useEffect } from 'react';

const mockResults = [
  { type: 'helmet_non_compliance', count: 42 },
  { type: 'triple_riding', count: 18 },
  { type: 'wrong_side_driving', count: 5 },
  { type: 'red_light_violation', count: 12 },
  { type: 'stop_line_violation', count: 34 },
];

const ResultsPage = () => {
  const { batchId } = useParams();
  const [results, setResults] = useState<any>([]);
  const [batchStatus, setBatchStatus] = useState<any>(null);
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  useEffect(() => {
    const fetchData = async () => {
      const statusRes = await fetch(`${apiUrl}/api/batches/${batchId}/status`, { credentials: 'include' });
      if (!statusRes.ok) throw new Error("Not authorized or not found");
      const statusData = await statusRes.json();
      setBatchStatus(statusData);

      if (statusData.status === 'done') {
        const resRes = await fetch(`${apiUrl}/api/batches/${batchId}/results`, { credentials: 'include' });
        if (resRes.ok) {
          const resData = await resRes.json();
          setResults(resData);
        }
      }
    };
    fetchData();
  }, [batchId, apiUrl]);

  const displayResults = Object.keys(results).length > 0 
    ? Object.entries(results).map(([type, data]: any) => ({ type, count: data.count }))
    : mockResults;

  return (
    <div className="max-w-6xl mx-auto mt-6">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-3xl font-bold text-gray-900 tracking-tight">Batch Results</h2>
          <p className="text-gray-500 mt-1">Processed batch <span className="font-mono text-xs bg-gray-100 px-2 py-0.5 rounded">{batchId}</span> <span className="text-sm font-semibold capitalize ml-2 text-primary">{batchStatus?.status || 'Loading...'}</span></p>
        </div>
        <Link to="/challans" className="bg-panel text-white px-5 py-2.5 rounded-full font-medium hover:bg-gray-800 transition flex items-center gap-2">
          View All in Register <ArrowRight size={18} />
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {displayResults.map((res, idx) => (
          <div key={idx} className="bg-white p-6 rounded-3xl shadow-sm border border-gray-100 flex flex-col justify-between hover:border-gray-200 transition-colors">
            <div className="flex items-start justify-between mb-8">
              <ViolationBadge type={res.type} className="scale-110 origin-top-left" />
              <div className="bg-gray-50 p-2 rounded-xl text-gray-400">
                <FileCheck2 size={24} />
              </div>
            </div>
            <div>
              <div className="text-4xl font-bold text-gray-900 mb-1">{res.count}</div>
              <div className="text-sm font-medium text-gray-500">Violations Detected</div>
            </div>
          </div>
        ))}
      </div>
      
      <div className="mt-8 bg-blue-50 border border-blue-100 rounded-2xl p-6 flex items-start gap-4">
        <div className="bg-blue-100 text-blue-700 w-8 h-8 rounded-full flex items-center justify-center font-bold shrink-0">i</div>
        <div>
          <h4 className="font-semibold text-blue-900">Pipeline Status: Mock</h4>
          <p className="text-sm text-blue-800 mt-1">
            These are synthetically generated results conforming to the schema. The real YOLO adapter is stubbed out in <code>backend/pipeline/real.py</code>.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
