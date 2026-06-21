import { useState, useEffect } from 'react';

import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import { Shield, Sun, Moon } from 'lucide-react';
import LandingPage from './pages/LandingPage';
import SurveillanceMapPage from './pages/SurveillanceMapPage';
import GenerateChallanPage from './pages/GenerateChallanPage';
import ResultsPage from './pages/ResultsPage';
import DossierPage from './pages/DossierPage';
import AnalyticsPage from './pages/AnalyticsPage';
import DatasetInfoPage from './pages/DatasetInfoPage';

const TopNavbar = ({ isDark, setIsDark }: { isDark: boolean, setIsDark: (val: boolean) => void }) => {
  const location = useLocation();
  const links = [
    { path: '/', label: 'Overview' },
    { path: '/map', label: 'Cameras' },
    { path: '/generate-challan', label: 'Generate Challan' },
    { path: '/analytics', label: 'Analytics' },
    { path: '/datasets', label: 'Datasets' },
  ];

  return (
    <header className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 sticky top-0 z-50 transition-colors duration-300">
      <div className="max-w-[1400px] mx-auto px-6 h-20 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center gap-4 border-r border-gray-300 dark:border-gray-700 pr-6 mr-2">
          <Shield className="text-[#C8102E] dark:text-red-500" size={28} />
          <h1 className="font-bold text-xl tracking-tight text-gray-900 dark:text-white">Marg Rakshak</h1>
        </div>

        {/* Navigation Links */}
        <nav className="flex-1 flex items-center gap-8 px-4">
          {links.map(l => {
            const isActive = location.pathname === l.path || (l.path !== '/' && location.pathname.startsWith(l.path));
            return (
              <Link
                key={l.path}
                to={l.path}
                className={`font-semibold text-[15px] transition-colors relative h-20 flex items-center ${
                  isActive 
                    ? 'text-gray-900 dark:text-white' 
                    : 'text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                }`}
              >
                {l.label}
                {isActive && (
                  <span className="absolute bottom-0 left-0 w-full h-1 bg-[#C8102E] dark:bg-red-500 rounded-t-full" />
                )}
              </Link>
            );
          })}
        </nav>

        {/* Right Actions */}
        <div className="flex items-center gap-6">
          <button 
            onClick={() => setIsDark(!isDark)}
            className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-300 transition-colors"
          >
            {isDark ? <Sun size={20} /> : <Moon size={20} />}
          </button>
        </div>
      </div>
    </header>
  );
};

function App() {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDark]);

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-white dark:bg-gray-900 transition-colors duration-300 flex flex-col">
        <TopNavbar isDark={isDark} setIsDark={setIsDark} />
        <main className="flex-1 w-full max-w-[1400px] mx-auto p-8">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/map" element={<SurveillanceMapPage />} />
            <Route path="/generate-challan" element={<GenerateChallanPage />} />
            <Route path="/results/:batchId" element={<ResultsPage />} />
            <Route path="/plates/:number" element={<DossierPage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
            <Route path="/datasets" element={<DatasetInfoPage />} />
          </Routes>
        </main>
        
        {/* Global Footer */}
        <footer className="bg-black dark:bg-white py-16 mt-auto transition-colors duration-300">
          <div className="max-w-[1400px] mx-auto px-8 flex flex-col md:flex-row items-center justify-between text-sm text-gray-400 dark:text-gray-600">
            <div className="flex items-center gap-2 mb-4 md:mb-0">
              <Shield size={18} className="text-[#C8102E] dark:text-red-600" />
              <span className="font-bold text-white dark:text-black text-base tracking-wide">Marg Rakshak</span>
              <span className="mx-2 opacity-30">|</span>
              <span>&copy; {new Date().getFullYear()}</span>
            </div>
            <div className="text-center md:text-right font-medium">
              Command Intelligence Platform
              <div className="text-xs mt-1 text-gray-500 dark:text-gray-500 uppercase tracking-widest">
                Bengaluru Traffic Police
              </div>
            </div>
          </div>
        </footer>
      </div>
    </BrowserRouter>
  );
}

export default App;
