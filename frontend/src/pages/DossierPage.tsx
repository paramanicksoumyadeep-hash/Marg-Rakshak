
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, User, Car, Calendar, ShieldCheck, FileWarning, AlertTriangle } from 'lucide-react';
import { ViolationBadge } from '../components/ViolationBadge';

const DossierPage = () => {
  const { number } = useParams();

  // Mock data representing the VAHAN synthetic registry return
  const mockDossier = {
    plate_number: number,
    owner_name: 'Synthetic Owner 42 — Demo Data',
    vehicle_class: 'two_wheeler',
    make_model: 'Honda Activa',
    registration_date: '2019-03-11',
    insurance_status: 'valid',
    puc_status: 'expired',
    total_outstanding_amount: 2500,
    challan_history: [
      { challan_id: 'CH-2026-A1B2', type: 'helmet_non_compliance', status: 'pending', amount: 1000, date: '2026-06-21' },
      { challan_id: 'CH-2025-X9Y8', type: 'stop_line_violation', status: 'pending', amount: 1500, date: '2025-11-04' },
      { challan_id: 'CH-2024-Z7W6', type: 'wrong_side_driving', status: 'paid', amount: 5000, date: '2024-02-18' },
    ]
  };

  return (
    <div className="max-w-5xl mx-auto mt-6">
      <Link to="/challans" className="text-gray-500 hover:text-gray-900 inline-flex items-center gap-2 mb-6 font-medium transition-colors">
        <ArrowLeft size={16} /> Back to Register
      </Link>

      <div className="bg-panel text-white rounded-t-3xl p-8 flex items-center justify-between">
        <div>
          <div className="text-sm text-gray-400 font-medium uppercase tracking-widest mb-2">Vehicle Dossier</div>
          <h2 className="text-4xl font-black font-mono tracking-tight text-yellow-400">{mockDossier.plate_number}</h2>
        </div>
        <div className="text-right">
          <div className="text-sm text-gray-400 font-medium mb-1">Total Outstanding</div>
          <div className="text-3xl font-bold text-primary">₹{mockDossier.total_outstanding_amount}</div>
        </div>
      </div>

      <div className="bg-white rounded-b-3xl shadow-sm border border-gray-100 p-8 grid grid-cols-2 gap-8 mb-8">
        <div className="space-y-6">
          <div className="flex items-center gap-4">
            <div className="bg-gray-100 p-3 rounded-xl"><User className="text-gray-600" /></div>
            <div>
              <div className="text-sm text-gray-500 font-medium">Registered Owner</div>
              <div className="font-semibold text-gray-900">{mockDossier.owner_name}</div>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="bg-gray-100 p-3 rounded-xl"><Car className="text-gray-600" /></div>
            <div>
              <div className="text-sm text-gray-500 font-medium">Make & Model</div>
              <div className="font-semibold text-gray-900 uppercase">{mockDossier.make_model} <span className="text-gray-400 font-normal ml-1">({mockDossier.vehicle_class})</span></div>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="bg-gray-100 p-3 rounded-xl"><Calendar className="text-gray-600" /></div>
            <div>
              <div className="text-sm text-gray-500 font-medium">Registration Date</div>
              <div className="font-semibold text-gray-900">{mockDossier.registration_date}</div>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="flex items-center justify-between p-4 rounded-2xl bg-green-50 border border-green-100">
            <div className="flex items-center gap-3">
              <ShieldCheck className="text-green-600" />
              <span className="font-semibold text-green-900">Insurance Status</span>
            </div>
            <span className="uppercase text-xs font-bold text-green-700 tracking-wider">Valid</span>
          </div>
          <div className="flex items-center justify-between p-4 rounded-2xl bg-red-50 border border-red-100">
            <div className="flex items-center gap-3">
              <AlertTriangle className="text-red-600" />
              <span className="font-semibold text-red-900">PUC Status</span>
            </div>
            <span className="uppercase text-xs font-bold text-red-700 tracking-wider">Expired</span>
          </div>
          <div className="p-4 rounded-2xl bg-gray-50 border border-gray-100 text-sm text-gray-500 flex items-start gap-3">
            <FileWarning className="shrink-0" size={18} />
            <p>Data is seeded from the synthetic MongoDB Atlas registry simulating an active VAHAN endpoint connection.</p>
          </div>
        </div>
      </div>

      <h3 className="text-xl font-bold text-gray-900 mb-4">Violation History</h3>
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-50 border-b border-gray-100 text-xs uppercase tracking-wider text-gray-500 font-semibold">
              <th className="p-4">Date</th>
              <th className="p-4">Challan ID</th>
              <th className="p-4">Violation</th>
              <th className="p-4">Amount</th>
              <th className="p-4">Status</th>
            </tr>
          </thead>
          <tbody>
            {mockDossier.challan_history.map(c => (
              <tr key={c.challan_id} className="border-b border-gray-50">
                <td className="p-4 text-gray-600">{c.date}</td>
                <td className="p-4 font-semibold text-gray-900">{c.challan_id}</td>
                <td className="p-4"><ViolationBadge type={c.type} /></td>
                <td className="p-4 font-mono font-medium">₹{c.amount}</td>
                <td className="p-4">
                  <span className={`text-xs font-bold uppercase tracking-wider ${c.status === 'paid' ? 'text-green-600' : 'text-orange-600'}`}>
                    {c.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DossierPage;
